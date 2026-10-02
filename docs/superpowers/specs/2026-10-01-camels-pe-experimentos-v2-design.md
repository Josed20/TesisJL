# Diseño experimental V2 para CAMELS-PE

## Propósito

Implementar una segunda corrida reproducible para la predicción diaria de
caudal en cuencas peruanas tratadas como no aforadas. La V2 debe corregir las
limitaciones detectadas en la primera corrida, comparar las seis alternativas
adoptadas en la metodología y seleccionar una alternativa neuronal para la
cuantificación de incertidumbre. La primera corrida se conserva sin cambios.

## Alcance y criterio de éxito

La V2 producirá artefactos independientes bajo `data/experimentos_v2/`:
elegibilidad, particiones, configuraciones, modelos, predicciones, métricas,
figuras y registros de ejecución. El resultado será válido solo si ninguna
cuenca de prueba interviene en la imputación, estandarización, selección de
variables, ajuste de hiperparámetros o selección de modelo que la evalúa.

El objetivo no es reproducir ni superar de forma directa una cifra publicada
en otro país o protocolo. El éxito es obtener la mejor alternativa bajo la
misma evaluación espacial peruana, con una mejora medible frente al baseline
V1 de Random Forest (KGE mediana 0.338 y NSE mediana 0.309), o documentar de
forma transparente si no se logra.

## Datos y elegibilidad

La ventana experimental será del 1 de enero de 1981 al 31 de diciembre de
2016, definida por la disponibilidad de PET. Las variables dinámicas son
`prec`, `pet`, `tmin`, `tmean`, `tmax`, `srad` y `vprp`; el objetivo es
`flow_obs` en mm/día. `flow_sim` no se utiliza en ningún paso de desarrollo o
evaluación.

Los atributos estáticos proceden de los seis archivos de atributos permitidos:
clima, topografía, suelo, geología, cobertura y presión antrópica. Se excluye
por completo `hydrological_signatures.csv`, porque incorpora información
derivada de caudal. Para cada fold, las variables estáticas con faltantes se
imputarán con una estadística del entrenamiento y se añadirá un indicador de
ausencia cuando exista al menos un faltante. Las transformaciones y la selección
de variables se ajustarán exclusivamente con las cuencas de entrenamiento.

Las 88 cuencas que cumplen la elegibilidad V1 se podrán utilizar como cuencas
donantes durante el entrenamiento. El conjunto de reporte principal estará
formado por cuencas que, dentro de 1981--2016, tengan al menos 20 % de caudal
observado y al menos un segmento continuo de 365 días; con el inventario actual
son 46 cuencas. Las restantes cuencas no se eliminan silenciosamente: se
registran en una tabla de elegibilidad y se reportan por separado si participan
como donantes.

## Validación espacial y anti-fuga

Las cuencas se separarán por `nested_group_id`, de modo que un grupo no pueda
aparecer simultáneamente en entrenamiento, validación y prueba. La evaluación
externa será de cinco folds, preservando los grupos completos. Dado que un
grupo contiene 35 cuencas, los resultados se resumirán en tres niveles:

1. métricas por cuenca;
2. mediana de las cuencas dentro de cada grupo;
3. mediana de los grupos, que será la síntesis primaria.

Dentro de cada fold externo, la selección de hiperparámetros se hará con una
validación agrupada interna construida únicamente desde el conjunto de
entrenamiento externo. Luego de seleccionar la configuración, el modelo se
reajustará con train más validación interna y generará predicciones sobre la
prueba externa una sola vez.

La imputación, los escaladores de forzantes y atributos, los filtros de
variables y cualquier estadística aprendida se ajustarán con train interno; al
reajustar para la prueba externa podrán volver a ajustarse con train más
validación, sin consultar prueba. La misma intersección de fechas observadas
válidas será usada para comparar todos los modelos en cada cuenca.

## Modelos y mejora de configuraciones

Las seis alternativas obligatorias permanecen en el estudio:

1. GR4J regionalizado;
2. Random Forest;
3. XGBoost;
4. GRU regional;
5. LSTM regional;
6. EA-LSTM regional.

Random Forest y XGBoost recibirán búsqueda interna de hiperparámetros y una
selección de variables estáticas trazable. GR4J se calibrará en cuencas
donantes, con periodo de calentamiento y presupuesto de optimización suficiente;
la regla de regionalización se elegirá internamente entre alternativas de
atributos y vecinos/modelo de transferencia.

Las redes se entrenarán con estandarización global derivada exclusivamente de
las cuencas de entrenamiento, secuencias candidatas de 270 y 365 días, tamaños
ocultos de 128 y 256, dropout candidato 0.1--0.4 y varias semillas. No se
limitará el entrenamiento a 30 000 muestras: si existe límite de memoria se
usará muestreo balanceado por cuenca y se registrará el número de muestras. La
parada temprana y la selección se basarán en KGE por grupo de validación, no en
MSE logarítmico agregado.

Crossformer se implementará como un séptimo challenger separado, después de
que exista un baseline LSTM/EA-LSTM V2 reproducible. Su resultado no reemplaza
las seis alternativas obligatorias ni modifica el ranking principal si no
supera a la mejor red bajo los mismos folds.

## Métricas, selección y resultados

Cada predicción conservará cuenca, grupo, fold, fecha, observación y
estimación. Se calcularán NSE, KGE, RMSE, MAE y PBIAS por cuenca. La regla de
selección global será:

1. mayor mediana de KGE entre grupos;
2. si la diferencia es menor que 0.01, mayor mediana de NSE entre grupos;
3. si persiste el empate, menor mediana de `abs(PBIAS)`.

La regla se aplica con validación interna para seleccionar configuraciones y
con prueba externa únicamente para el ranking final. Se reportarán distribución,
mediana y cuartiles por cuenca, grupo, región y fold; también se incluirán
conteos de NSE positivo, diagnósticos de alto/bajo caudal y pruebas pareadas
entre modelos cuando el número de pares válidos lo permita.

## Incertidumbre y caso ilustrativo

Solo la arquitectura neuronal elegida dentro de cada fold externo recibirá
regresión cuantílica para producir Q0.05, Q0.50 y Q0.95. La evaluación externa
de incertidumbre incluirá cobertura empírica, amplitud media del intervalo y
calibración por cuenca y grupo. Un caso ilustrativo se seleccionará antes de
examinar el ranking final y mostrará observación, mediana predictiva e
intervalo; no sustituye el resumen multicuenca.

## Reproducibilidad y restricciones

- No se sobrescribe ningún archivo de `data/experimentos/`.
- Cada corrida guarda un archivo de configuración, semillas, versiones de
  paquetes, hashes o rutas de datos, tiempos y estado de ejecución.
- Los checkpoints se versionan por configuración y fold; nunca se reutilizan
  sin comprobar que coincida la configuración completa.
- Cada modelo usa los mismos splits V2 y las mismas fechas válidas de prueba.
- Una corrida fallida deja un registro explícito y no se mezcla con resultados
  completos en el resumen.
- Las conclusiones indicarán tamaño de muestra, periodo, protocolo espacial y
  limitaciones; no extrapolarán los resultados a todas las cuencas del Perú.

## Verificación de aceptación

Antes de ejecutar la corrida completa se probará el pipeline con un fold y una
muestra pequeña. Las pruebas automatizadas comprobarán: ausencia de grupos
compartidos, ajuste de transformaciones solo en entrenamiento, exclusión de
`flow_sim` y firmas, fechas comunes de evaluación, regla de ranking y
aislamiento de los artefactos V1. La corrida final solo se considerará completa
cuando existan resultados de todos los folds previstos para cada modelo y un
registro de las exclusiones o fallos.

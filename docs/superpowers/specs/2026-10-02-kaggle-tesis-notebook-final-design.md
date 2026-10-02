# Diseño del notebook final de tesis para Kaggle

**Fecha:** 2026-10-02  
**Archivo objetivo:** `kaggle_tesis_v2.ipynb`  
**Dataset:** CAMELS-PE en `/kaggle/input/datasets/cabreradev25/camels-pe/CAMELS-PE/`

## 1. Propósito

Construir un único notebook autocontenido y ejecutable con **Run All** en Kaggle para estudiar la predicción diaria de caudal en cuencas peruanas no vistas. El notebook cubrirá inspección, auditoría, selección reproducible de cuencas, partición espacial, preprocesamiento sin fuga, modelos de referencia y neuronales regionales, incertidumbre, evaluación multicuenca, visualizaciones y exportación de artefactos.

El notebook no prometerá ni fabricará un nivel de desempeño. La selección del mejor modelo se realizará exclusivamente a partir de métricas obtenidas en cuencas de test no usadas durante entrenamiento, validación, imputación, escalado ni ajuste de hiperparámetros.

## 2. Evidencia verificada en CAMELS-PE

La inspección local del mismo dataset confirmó:

- 136 archivos CSV en `03_timeseries/by_catchment/`.
- Cada archivo tiene 16,436 filas diarias entre 1981-01-01 y 2025-12-31.
- Columnas temporales reales: `date`, `prec`, `prec_var`, `flow_obs`, `flow_sim`, `pet`, `tmin`, `tmean`, `tmax`, `srad`, `vprp`.
- Objetivo: `flow_obs`.
- `flow_sim` se excluirá de toda entrada predictiva.
- `01_metadata/stations.csv` contiene `gauge_id`, `nested_group_id`, `upstream_gauge_id`, `downstream_gauge_id`, región, coordenadas y periodo observado.
- Atributos disponibles: `climatic_indices.csv`, `geologic_attributes.csv`, `human_intervention_attributes.csv`, `landcover_attributes.csv`, `soil_attributes.csv`, `topographic_attributes.csv` y `hydrological_signatures.csv`.
- `hydrological_signatures.csv` se excluirá como predictor porque se deriva del caudal observado.
- La carpeta geoespacial incluye GeoPackages generales y por cuenca.

El notebook volverá a comprobar estos hechos en Kaggle. Si el esquema no coincide, se detendrá con un mensaje diagnóstico en vez de continuar con columnas inventadas.

## 3. Lecciones de los experimentos 1 y 2

### Elementos que se conservan

- Separación por cuencas, no por días.
- Agrupamiento mediante `nested_group_id`.
- Exclusión de `flow_sim` y firmas hidrológicas.
- Evaluación por cuenca y agregación multicuenca.
- Comparación GR4J, Random Forest, XGBoost, GRU, LSTM y EA-LSTM.
- Uso de transformación `log1p` para estabilizar el objetivo no negativo.

### Limitaciones que se corrigen

- El notebook actual oculta gran parte del pipeline en un ZIP Base64 y dificulta la auditoría metodológica.
- Declara cantidades fijas de cuencas elegibles antes de calcularlas.
- No presenta una exploración completa del esquema real.
- No ofrece un interruptor único `FAST_DEV_RUN`.
- La longitud de secuencia y varios valores de entrenamiento están implícitos o dispersos.
- La incertidumbre Q0.05–Q0.95 no está implementada de extremo a extremo.
- No produce todos los archivos finales solicitados con nombres estables.
- No caracteriza los gaps antes de imputar.
- El ranking principal no documenta suficientemente la separación entre selección por validación y evaluación final de test.

## 4. Arquitectura del notebook

El notebook tendrá celdas Markdown breves y celdas de código modular, sin depender de scripts locales. Las funciones se definirán en el propio notebook y se agruparán por responsabilidad:

1. Configuración y entorno.
2. Descubrimiento e inspección del dataset.
3. Auditoría por cuenca y calidad de datos.
4. Definición explícita de variables.
5. Partición espacial y topológica.
6. Preprocesamiento sin fuga.
7. datasets tabular y secuencial.
8. Modelos.
9. Entrenamiento, validación y checkpoints.
10. Métricas e incertidumbre.
11. Smoke test y entrenamiento completo.
12. Comparación, figuras y exportación.

La configuración se centralizará en una estructura serializable con, al menos:

- `SEED`
- `FAST_DEV_RUN`
- `START_DATE`, `END_DATE`
- criterios de elegibilidad configurables
- `SEQ_LENGTH`
- `BATCH_SIZE`
- `NUM_WORKERS`
- épocas, paciencia y tasa de aprendizaje
- cuantiles `(0.05, 0.50, 0.95)`
- modelos habilitados

## 5. Descubrimiento y validación del esquema

La ruta oficial se probará primero. Solo se permitirá una búsqueda controlada bajo `/kaggle/input` como respaldo, exigiendo la presencia conjunta de `01_metadata`, `02_attributes`, `03_timeseries` y `04_geospatial`.

El notebook mostrará un árbol limitado, inventario de archivos, extensiones, tamaños y una muestra de esquemas. Validará que los 136 identificadores de `stations.csv` coincidan con los nombres de los CSV por cuenca; el número real se calculará y se mostrará, no se fijará como resultado esperado.

Las columnas candidatas se derivarán del esquema y del diccionario de datos. Las listas finales serán explícitas:

- `target_col = "flow_obs"`
- `forbidden_features = ["flow_sim"]` más cualquier variable derivada del objetivo
- `dynamic_features` seleccionadas entre las variables diarias documentadas
- `static_features` numéricas permitidas después de excluir ID, texto descriptivo, coordenadas no justificadas y firmas hidrológicas

`prec_var` se describirá y no se usará automáticamente: su inclusión será una opción de configuración respaldada por el diccionario de datos.

## 6. Auditoría, gaps y elegibilidad

Para cada cuenca se calculará:

- fechas inicial y final;
- filas y días esperados;
- duplicados y discontinuidades temporales;
- cobertura y faltantes de `flow_obs`;
- faltantes por predictor dinámico;
- longitud máxima de gaps consecutivos por variable;
- longitud máxima de tramo completamente utilizable.

Los criterios de inclusión estarán en constantes y se aplicarán después de mostrar su efecto. El notebook no tendrá asserts de cantidades históricas fijas. Generará `basin_audit.csv` y una tabla de razones de exclusión.

La imputación se limitará a gaps meteorológicos cortos, con longitud máxima configurable. Los gaps largos permanecerán inválidos y no producirán ventanas. El caudal objetivo nunca será imputado para entrenar o evaluar.

## 7. Partición espacial y anidamiento

La fuente principal será la topología explícita de `stations.csv`: `nested_group_id`, `upstream_gauge_id` y `downstream_gauge_id`. Los GeoPackages se inspeccionarán de forma ligera para comprobar disponibilidad, CRS, conteo y validez geométrica; no se inferirán nuevas relaciones si la topología oficial ya existe.

La partición será determinista por grupos topológicos. Habrá conjuntos disjuntos de `train_basins`, `validation_basins` y `test_basins`. Se verificará:

- ausencia de cuencas repetidas entre conjuntos;
- ausencia de `nested_group_id` compartidos entre conjuntos;
- conservación razonable de regiones hidrográficas cuando el número de grupos lo permita;
- registro completo de la asignación en `basin_split.csv`.

La selección de hiperparámetros utilizará train y validation. Test permanecerá sellado hasta la evaluación final.

## 8. Preprocesamiento sin fuga

Los imputadores y escaladores se ajustarán solo con datos de entrenamiento. Los objetos se guardarán en `/kaggle/working/checkpoints/` mediante `joblib` cuando corresponda.

- Dinámicas: imputación limitada por cuenca y escalado con estadísticas calculadas solo sobre train.
- Estáticas: columnas numéricas permitidas, indicadores de faltantes, imputación mediana de train y escalado de train.
- Objetivo: `log1p(max(flow_obs, 0))` durante el ajuste de modelos estadísticos y neuronales; `expm1` y recorte no negativo para reportar caudal.
- Las ventanas se crearán dentro de cada cuenca en orden cronológico y se descartarán si contienen gaps no permitidos.

## 9. Datasets y eficiencia

El dataset secuencial almacenará índices de muestras, no todas las ventanas materializadas. `__getitem__` recuperará una ventana de una única cuenca y devolverá:

- `X_dynamic [SEQ_LENGTH, n_dynamic_features]`
- `X_static [n_static_features]`
- `y`
- `basin_id`
- `date`

Se usarán `float32`, `pin_memory` solo con CUDA y un `NUM_WORKERS` prudente. El modo rápido reducirá cuencas, fechas, épocas y configuraciones, pero conservará la misma ruta lógica del entrenamiento completo.

## 10. Modelos

### Random Forest y XGBoost

Usarán predictores diarios, atributos estáticos y agregados históricos causales de precipitación/PET. Los lags y acumulados solo usarán el presente y el pasado. La búsqueda será pequeña y reproducible en validación por cuencas. XGBoost detectará compatibilidad real con GPU y tendrá fallback CPU.

### GRU y LSTM regionales

Recibirán secuencias dinámicas y atributos estáticos. Los atributos podrán concatenarse a cada paso para GRU/LSTM estándar, dejando documentada esta decisión. Tendrán `train_one_epoch`, `validate` y `train_model`, early stopping, gradient clipping, historial y checkpoint del mejor estado según validación.

### EA-LSTM

Implementará una compuerta de entrada condicionada por atributos estáticos, mientras las variables dinámicas controlan las demás transiciones. No se describirá como EA-LSTM si la implementación se reduce a concatenación tardía.

### GR4J regionalizado

Se utilizará únicamente si la implementación existente se verifica como GR4J completo de cuatro parámetros, incluyendo stores y hidrogramas unitarios, y supera pruebas deterministas. Si no puede verificarse, la sección quedará visible como `TODO METODOLÓGICO` y el notebook continuará con los demás modelos sin sustituirlo silenciosamente.

## 11. Incertidumbre

La estrategia principal será regresión cuantílica para el EA-LSTM regional, con cuantiles 0.05, 0.50 y 0.95 y pérdida pinball. La salida respetará el orden de cuantiles mediante parametrización monótona o corrección explícitamente documentada. La predicción puntual será Q0.50.

Se calcularán por cuenca:

- cobertura del intervalo del 90 % (`PICP90`);
- amplitud media (`MPIW90`);
- error absoluto de cobertura respecto al nominal 0.90;
- porcentaje de cruces de cuantiles antes de cualquier corrección.

Los modelos puntuales no recibirán intervalos artificiales. La tabla mostrará métricas de incertidumbre solo para modelos probabilísticos.

## 12. Métricas y selección

Las predicciones se conservarán en formato largo con `basin_id`, `date`, `observed`, `predicted`, `model` y, cuando existan, `q05`, `q50`, `q95`.

Por cuenca se calcularán:

- NSE;
- KGE;
- MAE;
- RMSE;
- PBIAS;
- R² de Pearson como métrica complementaria;
- RSR;
- NSE-log y KGE-log para caudales bajos.

La fórmula de PBIAS será:

`100 * sum(predicted - observed) / sum(observed)`

Con esta convención, PBIAS positivo indica sobreestimación y negativo indica subestimación. Se documentará explícitamente para evitar ambigüedad con convenciones de signo opuestas.

El resumen por modelo incluirá media, mediana, Q25, Q75 y porcentaje de cuencas con NSE > 0. KGE mediano será el criterio principal de ranking; NSE mediano y `abs(PBIAS)` actuarán como desempates. No se usará el conjunto de test para elegir configuraciones.

## 13. Visualizaciones y artefactos

Se generarán figuras con títulos, ejes, unidades y resolución apta para tesis:

- boxplots de NSE y KGE por modelo;
- observado frente a predicho;
- serie temporal de una cuenca elegida reproduciblemente;
- intervalo Q0.05–Q0.95 del modelo probabilístico;
- comparación multicuenca;
- historial de entrenamiento.

Directorios:

- `/kaggle/working/results/`
- `/kaggle/working/checkpoints/`
- `/kaggle/working/figures/`

Archivos mínimos:

- `basin_audit.csv`
- `basin_split.csv`
- `metrics_by_basin.csv`
- `metrics_summary.csv`
- `predictions_test.csv`
- `training_history.csv`
- checkpoints y preprocesadores disponibles
- `run_config.json`

## 14. Smoke test y ejecución completa

`FAST_DEV_RUN = True` será el valor seguro inicial para validar Run All con pocas cuencas, un periodo reducido, lotes pequeños y una o dos épocas. El notebook imprimirá de forma destacada que esos resultados no son válidos como resultado final de tesis.

Para la corrida definitiva, el usuario cambiará únicamente `FAST_DEV_RUN = False` y ejecutará Run All. El pipeline completo reutilizará las mismas funciones y producirá artefactos separados para no mezclar resultados de desarrollo y finales.

## 15. Verificación antes de entrega

La entrega se considerará lista cuando:

- el notebook sea JSON válido y todas sus celdas Python compilen, salvo comandos mágicos explícitos evitables;
- no contenga rutas locales de Windows;
- no dependa de archivos del proyecto fuera del notebook y CAMELS-PE;
- las pruebas unitarias embebidas cubran métricas, partición, ventanas, fuga del preprocesamiento y orden de cuantiles;
- un smoke test local con CAMELS-PE complete exploración, split, preprocessing y al menos una pasada mínima por cada modelo habilitado que pueda ejecutarse en el entorno;
- los errores opcionales —por ejemplo una dependencia GR4J no verificable— queden documentados y no se presenten como resultados válidos.


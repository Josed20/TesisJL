# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Qué es este repositorio

Espacio de trabajo de una tesis de pregrado (TESIS I, ESAN) sobre **predicción diaria de caudal en cuencas peruanas no vistas (sin aforo) usando el dataset CAMELS-PE**. Toda la redacción de la tesis, los nombres de archivos, los mensajes de commit y las guías están en **español**; redacta el contenido de la tesis en español salvo que se indique lo contrario.

El árbol actual contiene **solo material de referencia**: no hay código, build, lint ni tests.

- `Plan_Tesis_FDTOOH/`, `Paper_FDTOOH/`: carpetas de trabajo para el plan de tesis y el paper (actualmente vacías).
- `guias para avanzar plan tesis/`: plantilla oficial del plan de tesis (`PLAN DE TESIS (2).docx`).
- `guias para avanzar paper/`: plantilla Springer/ESAN del paper (`.docm`), guías para redactar la Introducción y los Trabajos Relacionados, e imágenes que muestran cómo citar y cómo redactar el estado del arte. Síguelas al redactar las secciones del paper.
- `metodologias para plan y paper guias/`: metodología de la matriz de investigación y lista de temas de tesis predictivos.
- `Tesis anteriores/`, `Paper anteriores/`: tesis y papers previos para usar como ejemplos de estructura.

Para leer estos binarios se necesitan los skills `pdf`, `docx` y `pptx`; `.docm` es un archivo de Word con macros.

## Historial relevante

Commits anteriores contenían un pipeline de experimentos en Python bajo `data/experimentos_v2/` (configuración, dataset/elegibilidad, particiones espaciales, preprocesamiento sin fuga de información, métricas y tests con pytest) y documentos de diseño en `docs/superpowers/`. El commit `33a0b6e` eliminó el código y los datos; las eliminaciones de `docs/superpowers/` aún no están confirmadas (sin commit). Recupera cualquiera de esos archivos con `git show <commit>:<ruta>` (por ejemplo, `git show 4e053e4:data/experimentos_v2/src/preprocessing.py`) en lugar de reescribirlos desde cero. El entregable final previsto era un único notebook de Kaggle autocontenido (`kaggle_tesis_v2.ipynb`, especificación en `git show 585ded1`) que lee CAMELS-PE desde `/kaggle/input/datasets/cabreradev25/camels-pe/CAMELS-PE/`.

## Reglas metodológicas de trabajos previos

Si se reconstruye el código de experimentos, se deben mantener estas decisiones ya establecidas:

- La variable objetivo es `flow_obs`. Nunca uses `flow_sim` ni `hydrological_signatures.csv` como predictores (ambos derivan del caudal observado o simulado).
- Particiona **por cuenca, no por día**, agrupando con `nested_group_id` de `01_metadata/stations.csv` para que las cuencas anidadas nunca queden repartidas entre entrenamiento, validación y test.
- Ajusta la imputación, el escalado y los hiperparámetros solo con las cuencas de entrenamiento y validación; selecciona el modelo final con validación y reporta las métricas de test una sola vez (sin fuga de información).
- Evalúa por cuenca y luego agrega entre cuencas. Modelos comparados: GR4J, Random Forest, XGBoost, GRU, LSTM y EA-LSTM; la variable objetivo se transforma con `log1p`.
- No fijes en el código la cantidad de cuencas elegibles ni afirmes niveles de desempeño: calcúlalos a partir de los datos.

# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Qué es este repositorio

Tesis de pregrado (TESIS I, Universidad ESAN, Ingeniería de Tecnologías de Información y Sistemas; asesor: Wilfredo Mamani Ticona) sobre la **clasificación por diente de fenestración (F), dehiscencia (D) o normal (N) del hueso alveolar a partir de fotografía intraoral frontal y CBCT, usando el dataset FDTooth**. Todo se redacta en **español**; el paper también se redacta en español y el usuario lo traducirá al inglés al final, por su cuenta. No traduzcas nada al inglés salvo que se pida.

Hay dos entregables en LaTeX. Cada uno tiene `main.tex`, `referencias.bib` e `img/`:

- `Paper_FDTOOH/`: paper con formato Springer LNCS (`llncs` + `splncs04`, citas numéricas `[1]`). La guía de redacción extraída de los materiales del curso está en `Paper_FDTOOH/GUIA_REDACCION_PAPER.md`; **léela antes de redactar cualquier sección** (embudo de la Introducción, fórmula de Related Work, cómo presentar citas, patrón del título).
- `Plan_Tesis_FDTOOH/`: plan de tesis que replica `guias para avanzar plan tesis/PLAN DE TESIS (2).docx`. Formato: A4, márgenes de 2.54 cm, Times New Roman 12, interlineado doble, texto justificado, sangría de 1.25 cm y referencias APA 7 (`biblatex` `style=apa` + `biber`; `\textcite` / `\parencite`). Capítulos: "CAPÍTULO I/II/III" centrados; subtítulos numerados `1.1.`, `1.2.1.`, `2.2.1.1.` (en `\paragraph`). Se respeta el orden de la plantilla: carátula → dedicatoria → índices → Resumen/Abstract → Introducción → Cap. I Planteamiento → Cap. II Marco Teórico → Cap. III Metodología → Referencias → Anexo 1 Matriz de Consistencia.

## Código de colores de redacción (obligatorio en ambos `.tex`)

Al redactar, marca siempre los términos con estas macros, definidas en el preámbulo de cada `main.tex`:

| Macro | Uso | Color |
| --- | --- | --- |
| `\prob{}` | problema / variable dependiente (fenestración, dehiscencia, hueso alveolar) | azul |
| `\sol{}` | solución / técnica / variable independiente (Deep Learning, ensamble híbrido, ConvNeXt V2, SVM, RF…) | rojo |
| `\dat{}` | dataset y modalidades de datos (FDTooth, CBCT, fotografía intraoral) | verde |
| `\con{}` | conectores de adición (Del mismo modo, Asimismo, Por otra parte, De igual manera, Finalmente) | resaltado amarillo |
| `\res{}` | solo paper, Trabajos Relacionados: resultados y métricas de cada antecedente | morado |
| `\hal{}` | solo paper, Trabajos Relacionados: hallazgo de cada antecedente (texto plano, usa `soul`) | resaltado verde |

Los Trabajos Relacionados del paper siguen `guias para avanzar paper/Related Works_v5.pdf`, que es la guía definitiva: preámbulo → autores encadenados con conectores → «Finalmente, [autor]», sin oración de síntesis. El vacío de investigación va al final de la Introducción. Detalle en `Paper_FDTOOH/GUIA_REDACCION_PAPER.md` §4. **Extensión del paper:** límite habitual de LNCS para un *full paper*, 12–15 páginas con referencias; hoy tiene 16 (pendiente de recortar). El límite exacto lo fija la convocatoria del congreso.

Para la versión final se cambia `\colorestrue` por `\coloresfalse` en el preámbulo. Así se quitan los colores sin tocar el texto. El recuadro de leyenda «Borrador» ya se eliminó de ambos documentos a pedido del usuario; no lo vuelvas a añadir. **Título definitivo** (patrón de `PREDICTIVO_TEMAS_v1.pdf`): «Diseño de un Sistema de \sol{Visión Computacional} para el Pre-diagnóstico de \prob{Fenestración y Dehiscencia Ósea Alveolar} a partir de \dat{Fotografías Intraorales y Tomografías CBCT}». El paper usa el mismo título. Problemas, objetivos e hipótesis deben usar estos mismos términos.

## Compilar

```bash
cd Paper_FDTOOH && latexmk -pdf main.tex        # pdflatex + bibtex
cd Plan_Tesis_FDTOOH && latexmk -pdf main.tex   # pdflatex + biber
```

MiKTeX está instalado y tiene `llncs`, `biblatex-apa`, `newtx` y `titlesec`. Los archivos auxiliares están en `.gitignore`.

- BibTeX lee `@` incluso dentro de líneas que empiezan con `%`. No escribas `@tipo{` en los comentarios de `referencias.bib`.
- El paper usa `Paper_FDTOOH/splncs04unsrt.bst`, una copia local de `splncs04` sin ordenar, para que las referencias se numeren por orden de aparición, como en la guía. En las citas múltiples, escribe las claves en orden ascendente de número.
- **Criterio de fuentes (obligatorio):** solo artículos publicados en los últimos 5 años (2021 en adelante) y en revistas **Q1** (SJR). No se aceptan conferencias, tesis, revistas no Q1, noticias ni preprints. Excepciones: la OMS, como fuente oficial de estadísticas, y las fuentes originales de los modelos y herramientas usados en la Metodología (TotalSegmentator, ConvNeXt V2 en CVPR 2023, DINOv2 como preprint de arXiv, porque no se pudo confirmar su versión en TMLR, y los clasificadores de la 3.3: Cortes y Vapnik 1995, Breiman 2001, Friedman 2001 y Cover y Hart 1967, verificados en Crossref). Para buscar y verificar metadatos usa la API de Europe PMC (`https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=...&format=json&resultType=core`), que también da el texto completo de los artículos con PMCID.
- Las referencias de la Introducción ya se verificaron así (DOI, volumen, páginas). Al agregar una nueva, verifícala igual: no completes datos de memoria.
- Autores del paper: José Cabrera-Ticlla y Lucero Ayala-Mauricio (Universidad ESAN; correos `22200150@ue.edu.pe` y `22200171@ue.edu.pe`) y el asesor Wilfredo Ticona (afiliación 1: Universidad ESAN, `wmamani@esan.edu.pe`; afiliación 2: Universidad Tecnológica del Perú, `C19404@utp.edu.pe`).
- El plan de tesis ya está redactado. Su `referencias.bib` copia las entradas del paper y agrega Guo 2026, Yuan 2026, Moor 2023, Domic 2026 y el libro de Hernández-Sampieri y Mendoza (2018), que es la excepción metodológica usada por las tesis anteriores de ESAN. Si cambia una referencia compartida, actualízala en ambos `.bib`.
- Verifica cada referencia contra su DOI o fuente original. No inventes entradas ni cifras.

## Metodología de la tesis (`img/metodologia.png`)

**Decisión del usuario (16/10/2026): la tesis tiene una sola metodología, los ensambles híbridos.** Ya no se comparan tres metodologías. No escribas M1, M2 ni M3 en los documentos, y no presentes DINOv2 (M3) como parte del trabajo: solo puede aparecer como antecedente en los Trabajos Relacionados. Los componentes se nombran así: «ConvNeXt V2 (Foto+CBCT)», «ConvNeXt V2 (CBCT)», «Ambas» (las dos redes juntas) y «RF (CBCT)». **El ensamble promedia con el mismo peso todas las probabilidades que lo forman** (código: `np.mean` sobre la lista de modelos en `auditoria/rejilla_dl_ml.py`): en «Ambas + RF» cada modelo pesa 1/3, no es un promedio anidado. Comprobado el 23/10/2026: el anidado daría 0.804/0.828, no 0.810/0.842.

**Figura vigente (16/10/2026)**, 4 bloques. Cada bloque es una subsección de Metodología en el paper (3.1 a 3.4) y una fase en el plan (Fase 1 a 4), y da origen a un PE, un OE y una HE. Desde el 06/11/2026, el paper usa la versión en inglés que entregó el usuario (`Paper_FDTOOH/img/metodologia_en.png`); el plan sigue con `metodologia.png` en español:

1. **Obtención del dataset:** FDTooth, 241 pacientes. En el texto también se incluye el control de calidad: integridad SHA256 de 487 archivos y exclusión de 24 pacientes (23 por discordancia CSV–JSON y 1 por coordenadas incompatibles). Resultado: 217 pacientes y 2604 dientes.
2. **Preprocesamiento:**
   - Foto: recorte por caja ampliada hacia la encía, orientación canónica y redimensionamiento a 768 px en el lado largo.
   - CBCT: DICOM a valores tipo HU, TotalSegmentator (2600 de 2604 dientes) y ROI 3D de 14 × 10 × 32 mm a 0.2 mm.
   - Partición por paciente: desarrollo 174 / 2088 y prueba 43 / 516.
   - **Sin normalización de color:** ConvNeXt V2 usó `fotos/original`. Gray-world y CLAHE solo alimentaban los rasgos de foto de la antigua M1, que ya no se usan.
3. **Ensambles híbridos:** combinación a nivel de decisión mediante el promedio de las probabilidades de N, F y D.
   - Deep Learning: ConvNeXt V2 Tiny (ImageNet-22k) ajustada con CBCT 2.5D y con fusión Foto+CBCT (dos ramas y cabeza común). Una tercera configuración, «Ambas», incluye las dos redes en el ensamble. Se entrena con pérdida ponderada, aumento de datos, TTA y 3 semillas en la prueba.
   - Machine Learning: SVM (RBF), RF, HGB y KNN con rasgos diseñados de la CBCT: perfil de grosor vestibular con 400/700/1000 HU, cresta, zonas sin hueso, hueco más largo, grosor lingual, longitud, volumen y posición en la arcada.
   - Rejilla: 3 configuraciones de DL × 4 de ML = 12 ensambles. El seleccionado en desarrollo es Ambas + RF.
4. **Evaluación:**
   - Métricas: Macro-F1 (principal), F1 ponderado, exactitud, precisión y sensibilidad macro, AUC-ROC OvR, F1 por clase, matriz de confusión, y sensibilidad F/D y especificidad al agrupar F y D frente a N.
   - Protocolo: validación cruzada anidada de 5 folds agrupada por paciente (OOF) y prueba retenida de 43 pacientes evaluada **una sola vez**. La rejilla en la prueba es solo descriptiva.
   - IC: bootstrap pareado de pacientes con 2000 remuestreos.

Referencias que sirven para comparar, pero no forman parte del sistema: ConvNeXt V2 solo con foto (0.534 en desarrollo / 0.551 en prueba) y la réplica del antecedente solo con foto (MobileNetV3-Small, 0.548, medida solo en desarrollo).

Las versiones anteriores de la figura (14/10, con tres metodologías, y 16/10 v1) están en el scratchpad de la sesión.

## Resultados y figuras

- Las cifras finales están en `resultados_tesis.md`. Hay una copia en la raíz del repositorio con el mismo contenido que la original, que se genera en el proyecto de código (`C:\Cursos\Ciclo IX\Computación Grafica\ProyectoComputaciónGrafica\resultados\`, script `auditoria/figuras_tesis.py`). No completes las cifras de memoria.
  - Para la metodología única usa la **sección 4**: Tablas 4.1 (desarrollo) y 4.2 (prueba) de los 12 ensambles.
  - De la sección 5 usa solo las filas del ensamble y de sus componentes: ConvNeXt V2 Fusión, CBCT y Foto, y RF CBCT. Ignora las de DINOv2 y M1 foto/fusión.
  - Comparaciones válidas: ensamble − ConvNeXt fusión (+0.014 en desarrollo, significativa; +0.006 en prueba, no significativa); ConvNeXt fusión − RF CBCT (+0.049, significativa); fusión − CBCT (−0.001, no significativa); CBCT − foto (+0.285, significativa).
- Figuras generadas sin entrenar nada (con el Python del `.venv` del proyecto de código):
  - `figuras_tesis/figuras_extra.py`: ejemplos N/F/D y flujo de cohorte (plan).
  - `figuras_tesis/figuras_hibrido.py`: `figC_macro_f1_componentes` (ensamble y componentes, desarrollo y prueba) `figD_matrices_confusion_hibrido` (ensamble y sus 3 componentes; ya no va en el paper) y `figE_matriz_confusion_ensamble` (solo el ensamble elegido; es la Fig. 4 del paper desde el 23/10/2026, a pedido del usuario).
  - La Fig. 1 v3 y las matrices con M1/M2/M3 quedaron obsoletas.
- Maquetación del paper, revisada con Codex el 21/10/2026:
  - La 3.2 sigue el formato de `Paper anteriores/113240 _VALERIO Paul_vFINAL.pdf` (23/10/2026): Tabla 1 de actividades (Actividad | Descripción | Tareas), con las mismas actividades que el bloque 2 de la Fig. 1; un párrafo con título en negrita por actividad, con sus citas; Ec. (1) de conversión a HU; y Fig. 2 = `ejemplos_clases.pdf` (resultado del preprocesamiento por clase). La Fig. 2 tiene imágenes de pacientes: no la abras ni renderices su página (hoy pág. 8; antes de renderizar, ubícala con `pdftotext`).
  - La 3.3 sigue el mismo formato: Tabla 2 de actividades (bloque 3 de la Fig. 1), un párrafo con cita por actividad y las Ec. (2) kernel RBF, (3) probabilidad del RF y (4) promedio del ensamble. En desarrollo también se probaron *stacking*, contexto del paciente y umbrales (`metodologias/ensamble.py`); ninguno superó al promedio.
  - Las Tablas 3 y 4 (ensambles e hiperparámetros) van en un solo entorno `table` con `[!t]` y quedan juntas arriba de la página 11.
  - La Tabla 2 usa `[H]` (paquete `float`) para quedar justo después del párrafo introductorio de la 3.3, antes de las explicaciones (06/11/2026).
  - La Metodología empieza en página nueva (`\clearpage`) y la Fig. 1 va con `[!h]` justo después de la frase introductoria, antes de 3.1, como en la plantilla. El costo es un hueco de unas dos quintas partes de página al final de los Trabajos Relacionados (pág. 4).
  - Las Fig. 3 y 4 usan `[!t]`, sin `p`, para que ninguna figura quede sola en media página.
  - Tras cada cambio, revisa las páginas renderizadas (`pdftoppm`) para detectar huecos y floats lejos de su mención.
- Paper: 16 páginas (una más que el límite habitual); el límite es el de un *full paper* LNCS (12–15). No condenses los Trabajos Relacionados: conservan todos los antecedentes con el formato de la guía v5.
  - Contenido: metodología, Tabla 1 con las actividades del preprocesamiento, Tabla 2 con las actividades de los ensambles, Tabla 3 con los 12 ensambles (Macro-F1 en desarrollo y métricas de prueba), Tabla 4 con los hiperparámetros de cada uno de los 12 ensambles, en el mismo orden de la Tabla 3 (lr y épocas de ConvNeXt V2, hiperparámetros del ML y peso de cada modelo; el espacio de búsqueda y los ajustes comunes de las redes van en la nota; a pedido del usuario, 06/11/2026), `macro_f1_componentes.pdf` y `matriz_confusion_ensamble.pdf` (solo la matriz del ensamble; las cifras de los componentes quedan en el texto de 4.3).
  - Hiperparámetros elegidos, según `predicciones_test/*_params.json` y `kaggle/k04_m2_final_test.py`:
    - ConvNeXt V2: lr de la cabeza 1e-3 y del backbone 1e-4; 7 épocas (Foto+CBCT) y 16 (CBCT); AdamW con decaimiento de pesos 0.05, OneCycle, lote de 32, suavizado de etiquetas de 0.1 y 3 semillas.
    - SVM: C = 3, γ = 0.003.
    - RF: 500 árboles, max_features = 0.2, min_samples_leaf = 1.
    - HGB: learning_rate = 0.1, max_leaf_nodes = 7, L2 = 1.0.
    - KNN: k = 31.
- En el plan, debajo de cada figura y tabla va «Fuente: …» (macro `\fuente{}`), como en la mayoría de las tesis de ESAN, no «Nota.» de APA. La fuente indica solo el origen; las explicaciones van en el texto.
- Plan: logo, `ejemplos_clases.pdf` (2.2.2.1), `flujo_cohorte.pdf` (3.2) y la metodología. No lleva figuras de resultados.
- El plan se alineó con la metodología única el 21/10/2026:
  - PE3, OE3 y HE3 tratan del ensamble híbrido frente a sus componentes.
  - Bases Teóricas, Clasificación: rasgos + ML, ajuste fino y ensambles híbridos.
  - Marco Conceptual: «Ensamble híbrido» y «Rasgos diseñados» reemplazan a «Modelo fundacional».
  - La VI de la operacionalización tiene tres dimensiones: componente DL, componente ML y modalidad.
  - Las fases 1–4 llevan los nombres de la figura.
  - La Figura 3 va con `[!t]`.
- Decisión del usuario: no se entrena nada más. El antecedente (0.548) solo existe en desarrollo y no se dibuja en el panel de prueba.

## Material de referencia

- `guias para avanzar paper/`: plantilla `Plantilla_SPRINGER_ESAN (2).docm` y guías de Introducción, Related Works y citas (resumidas en la guía de redacción).
- `metodologias para plan y paper guias/`: lógica Solución (VI) / Problema (VD) / métricas / aportes, y el formato de la figura de metodología.
- `Tesis anteriores/`, `Paper anteriores/`: ejemplos de estructura.

Para leer estos binarios se necesitan los skills `pdf` y `docx`. El `.docm` no abre con `python-docx`; se lee descomprimiendo `word/document.xml`.

## Historial

Antes, el tema era la predicción de caudal con CAMELS-PE. Ese código (`data/experimentos_v2/`) se eliminó en el commit `33a0b6e` y ya no es el tema de la tesis. Solo se puede recuperar con `git show` si se pide explícitamente.

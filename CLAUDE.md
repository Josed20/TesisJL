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
| `\sol{}` | solución / técnica / variable independiente (Deep Learning, SVM, ConvNeXt V2, DINOv2…) | rojo |
| `\dat{}` | dataset y modalidades de datos (FDTooth, CBCT, fotografía intraoral) | verde |
| `\con{}` | conectores de adición (Del mismo modo, Asimismo, Por otra parte, De igual manera) | resaltado amarillo |

Para la versión final se cambia `\colorestrue` por `\coloresfalse` en el preámbulo. Así se quitan los colores y el recuadro de leyenda «Borrador» sin tocar el texto. **Título definitivo** (patrón de `PREDICTIVO_TEMAS_v1.pdf`): «Diseño de un Sistema de \sol{Visión Computacional} para el Pre-diagnóstico de \prob{Fenestración y Dehiscencia Ósea Alveolar} a partir de \dat{Fotografías Intraorales y Tomografías CBCT}». El paper usa el mismo título. Problemas, objetivos e hipótesis deben usar estos mismos términos.

## Compilar

```bash
cd Paper_FDTOOH && latexmk -pdf main.tex        # pdflatex + bibtex
cd Plan_Tesis_FDTOOH && latexmk -pdf main.tex   # pdflatex + biber
```

MiKTeX está instalado y tiene `llncs`, `biblatex-apa`, `newtx` y `titlesec`. Los archivos auxiliares están en `.gitignore`.

- BibTeX lee `@` incluso dentro de líneas que empiezan con `%`. No escribas `@tipo{` en los comentarios de `referencias.bib`.
- El paper usa `Paper_FDTOOH/splncs04unsrt.bst`, una copia local de `splncs04` sin ordenar, para que las referencias se numeren por orden de aparición, como en la guía. En las citas múltiples, escribe las claves en orden ascendente de número.
- **Criterio de fuentes (obligatorio):** solo artículos publicados en los últimos 5 años (2021 en adelante) y en revistas **Q1** (SJR). No se aceptan conferencias, tesis, revistas no Q1, noticias ni preprints. Excepciones: la OMS, como fuente oficial de estadísticas, y las fuentes originales de los modelos y herramientas usados en la Metodología (TotalSegmentator, ConvNeXt V2 en CVPR 2023 y DINOv2 como preprint de arXiv, porque no se pudo confirmar su versión en TMLR). Para buscar y verificar metadatos usa la API de Europe PMC (`https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=...&format=json&resultType=core`), que también da el texto completo de los artículos con PMCID.
- Las referencias de la Introducción ya se verificaron así (DOI, volumen, páginas). Al agregar una nueva, verifícala igual: no completes datos de memoria.
- Autores del paper: José Cabrera-Ticlla y Lucero Ayala-Mauricio (Universidad ESAN; correos `22200150@ue.edu.pe` y `22200171@ue.edu.pe`) y el asesor Wilfredo Ticona (afiliación 1: Universidad ESAN, `wmamani@esan.edu.pe`; afiliación 2: Universidad Tecnológica del Perú, `C19404@utp.edu.pe`).
- El `main.tex` del plan tiene un `\nocite{*}` temporal. Quítalo cuando el texto ya tenga citas reales.
- Verifica cada referencia contra su DOI o fuente original. No inventes entradas ni cifras.

## Metodología de la tesis (`img/metodologia.png`)

Es la figura central (versión del 14/10/2026) y se usa en ambos documentos. Compara tres metodologías: **M1** (gris) rasgos diseñados a mano + ML, **M2** (azul) ajuste fino de ConvNeXt V2 Tiny y **M3** (verde) DINOv2 ViT-B/14 + ML. Sus bloques son la base de los problemas, objetivos e hipótesis específicos (PE/OE/HE) y de las subsecciones de Metodología:

1. **Datos y control de calidad:** FDTooth, con 241 pacientes, fotografías intraorales y CBCT.
2. **Preprocesamiento:** selección de cohorte. En la foto: recorte por cajas, orientación canónica y normalización de color (Gray-world + CLAHE). En el CBCT: DICOM a valores tipo HU, segmentación dental con TotalSegmentator, ROI 3D alineada al diente de 14 × 10 × 32 mm y remuestreo a 0.2 mm. Partición por paciente: 217 pacientes y 2604 dientes.
3. **Extracción de características (M1):** en la foto, HOG, LBP y color LAB; en el CBCT, grosor óseo vestibular.
4. **Modelado:** M1 con SVM, RF, Gradient Boosting y KNN; M2 con ConvNeXt V2 Tiny; M3 con DINOv2 ViT-B/14 + regresión logística y SVM. Salida por diente: N (normal), F (fenestración) o D (dehiscencia).
5. **Evaluación (bloque 4 de la figura):** Macro-F1, F1 ponderado, Accuracy, Precisión, Recall, AUC-ROC y matriz de confusión. Prueba retenida de 43 pacientes, evaluada **una sola vez**.

En el paper son cinco subsecciones (3.1 a 3.5). En el plan son cuatro fases: la Fase 3 agrupa la extracción de características y el modelado.

Detalles que vienen de la versión anterior de la figura y que el usuario confirmó que siguen vigentes (ya están en la Metodología del paper): integridad SHA256 de 487 archivos; exclusión de 24 pacientes (23 por discordancia CSV–JSON y 1 por coordenadas incompatibles); 2600 de 2604 dientes segmentados; desarrollo 174 pacientes / 2088 dientes y prueba 43 / 516; foto redimensionada a 768 px en el lado largo; HOG con PCA; entradas de M2 y M3: foto, CBCT 2.5D y fusión de dos ramas; protocolo de 5 folds externos agrupados por paciente con selección interna y predicciones OOF.

## Material de referencia

- `guias para avanzar paper/`: plantilla `Plantilla_SPRINGER_ESAN (2).docm` y guías de Introducción, Related Works y citas (resumidas en la guía de redacción).
- `metodologias para plan y paper guias/`: lógica Solución (VI) / Problema (VD) / métricas / aportes, y el formato de la figura de metodología.
- `Tesis anteriores/`, `Paper anteriores/`: ejemplos de estructura.

Para leer estos binarios se necesitan los skills `pdf` y `docx`. El `.docm` no abre con `python-docx`; se lee descomprimiendo `word/document.xml`.

## Historial

Antes, el tema era la predicción de caudal con CAMELS-PE. Ese código (`data/experimentos_v2/`) se eliminó en el commit `33a0b6e` y ya no es el tema de la tesis. Solo se puede recuperar con `git show` si se pide explícitamente.

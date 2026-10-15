# Guía de redacción del paper (extraída de las guías del curso)

Fuentes: `guias para avanzar paper/` (Introducción_v3.pdf, Related Works_v3 (1).pdf,
comopresentarcitas.png, formacorrectaderedactarelestadodelarte.png,
Plantilla_SPRINGER_ESAN (2).docm) y `metodologias para plan y paper guias/`
(PREDICTIVO_TEMAS_v1.pdf, Metodología_Matriz de Investigación_VIRGINIA.pdf).

## 1. Formato (plantilla Springer ESAN = LNCS)

| Elemento | Formato en la plantilla | En LaTeX (`llncs`) |
| --- | --- | --- |
| Título | 14 pt, negrita, centrado | `\title{}` |
| Autores | centrado; superíndices de afiliación | `\author{... \inst{1}}` |
| Afiliaciones y correos | 9 pt, centrado | `\institute{}` + `\email{}` |
| Abstract | 9 pt, sangría 1 cm a ambos lados | `abstract` |
| Keywords | 9 pt, alineado a la izquierda | `\keywords{}` |
| Secciones | numeradas, 12 pt negrita | `\section{}` |
| Subsecciones | numeradas, 10 pt negrita | `\subsection{}` |
| Cuerpo | justificado; primer párrafo tras un título sin sangría; los siguientes con sangría | automático |
| Figuras | leyenda **debajo**, 9 pt, centrada: "Fig. 1. ..." | `\caption` después de `\includegraphics` |
| Tablas | leyenda **encima**, 9 pt, centrada: "Table 1. ..." | `\caption` antes de `tabular` |
| Referencias | lista numerada, 9 pt; citas en el texto `[1]`, `[7], [8], [9]` | `splncs04` + `\cite{}` |

Secciones de la plantilla, en este orden: **Introduction → Related Work →
Methodology (subsecciones A, B, C, D: una por fase de la figura de
metodología) → Results → Conclusions → References**. La figura de la metodología va
en la sección Methodology ("Fig. 1. Methodology").

La plantilla ESAN está en inglés, pero el borrador (`main.tex`) se redacta en
español: Introducción, Trabajos Relacionados, Metodología, Resultados,
Conclusiones. La traducción al inglés se hará al final, por separado.

## 2. Título

Patrón usado en todos los ejemplos del curso:

> [Modelo / Sistema] + [adjetivo: Robusto, Híbrido, Multimodal] + de
> [tarea: Clasificación / Pre-diagnóstico] de **[PROBLEMA]** basado en
> **[TÉCNICA: Deep Learning / Machine Learning]**

En las guías, los términos del **problema** (variable dependiente) se marcan en
**azul** y los de la **solución o técnica** (variable independiente) en **rojo**.
Estos mismos términos deben repetirse a lo largo de la Introducción y de Related
Work. Así el texto queda anclado al título.

En `PREDICTIVO_TEMAS_v1.pdf` los **datos** aparecen en **verde** (por ejemplo,
"a partir de la Escritura de una Persona"). En los `.tex` esta convención se aplica
con las macros `\prob{}` (azul), `\sol{}` (rojo), `\dat{}` (verde) y `\con{}`
(conector resaltado en amarillo).

Aplicado a FDTooth: problema = *fenestración y dehiscencia ósea alveolar*;
solución = *Deep Learning (ConvNeXt V2, DINOv2) y Machine Learning (SVM, RF, GB,
KNN, LR)*; datos = *fotografía intraoral + CBCT*.

## 3. Introducción: estructura en embudo (Introducción_v3.pdf)

Cada párrafo baja un nivel. Cada afirmación lleva su cita `[n]`.

1. **Problema y relevancia mundial.** Se define el problema y por qué es crítico
   para la salud, con citas académicas [1], [2].
2. **Cifras globales de una organización oficial** (OMS u otra), con año,
   cantidades y porcentajes. Se cierra con por qué es imperativo detectarlo a
   tiempo [3].
3. **Región: América Latina y el Caribe** (OPS u otro organismo regional), con
   cifras y factores de riesgo. Luego, ejemplos por país (Argentina, México,
   Colombia/Chile) [4], [5].
4. **Perú**: posición del problema a nivel nacional, porcentajes y declaraciones
   de instituciones peruanas (MINSA, EsSalud, El Peruano, gob.pe) [5], [6].
5. **La IA como respuesta.** El auge de la IA, el ML y el DL en el área, qué
   aportan a los especialistas y la evidencia reciente de su eficacia. Se cierra
   con una cita múltiple [7], [8], [9].

Las fuentes pueden ser artículos (con DOI) y páginas institucionales. Las
páginas web se citan con `Accessed: <fecha>. [Online]. Available: <URL>`.
Extensión de referencia: alrededor de 1 página y 9 referencias.

## 4. Related Work / estado del arte (Related Works_v3 (1).pdf)

- Se organiza en **subsecciones temáticas**, cada una con el patrón
  "[Técnica] para [problema / dominio]". Ejemplos: "2.1 Métodos de Ensemble
  (Machine Learning) para la clasificación en salud mental" y "2.2 Arquitecturas
  híbridas de Deep Learning para la evaluación psiquiátrica".
- Cada subsección es **un párrafo**. Empieza con una oración de contexto sobre la
  línea de investigación. Luego vienen de 4 a 5 trabajos encadenados.
- Cada trabajo se escribe con la fórmula:
  **Autor et al. [n] + verbo (compararon / aplicaron / propusieron /
  emplearon / desarrollaron) + técnicas + datos (nombre del dataset y N) + mejor
  resultado con métrica y valor + hallazgo clave.**
  Ejemplo: "Liu et al. [8] compararon RF, XGBoost y LightGBM en una cohorte de
  15,173 personas…, y LightGBM alcanzó el AUC más alto (0,85)…".
- Los trabajos se enlazan con **conectores** (resaltados en amarillo en la guía):
  *Del mismo modo, Asimismo, Por otra parte, De igual manera*. En el ejemplo, la
  segunda subsección abre con un puente desde la anterior: "Conscientes de las
  limitaciones de los modelos de modalidad única…".

### Forma correcta de redactar el estado del arte (diapositiva)

- Narración lógica y ordenada de todo lo revisado.
- Citar antecedentes que estén en contexto con la realidad a estudiar y que
  ayuden a definir el problema de estudio.
- Las citas de distintos autores deben relacionarse dentro de un contexto. Para
  eso se usan conectores.

## 5. Cómo presentar las citas dentro de un párrafo (diapositiva)

Secuencia de un párrafo bien citado:

1. **Preámbulo**: idea general del tema.
2. **Introducción a la cita**: frase que prepara la cita.
3. **Cita** textual o referencia directa.
4. **Conector** (*Sin embargo, Ciertamente…*), que expresa divergencia,
   convergencia, síntesis o inflexión.
5. **Parafraseo** de un autor.
6. **Parafraseo múltiple**: varios autores que coinciden, citados juntos.
7. **Conclusión, análisis, síntesis o conciliación** de las citas e ideas, con
   voz propia.

Se cita para aportar evidencia que sostenga los argumentos.

## 6. Lógica de la investigación (PREDICTIVO_TEMAS_v1.pdf)

- "Divide y vencerás": el problema se divide en fases (Fase 1…N), y cada fase se
  convierte en una subsección de Methodology y en un objetivo específico.
- **Solución = variable independiente** (técnicas) y **Problema = variable
  dependiente**. Cada una se sustenta con papers y libros.
- Las **métricas** miden el desempeño y conectan solución y problema. Resultados
  típicos: Accuracy, Precision, Recall, F1-Score, matriz de confusión. Para
  FDTooth, la métrica principal es Macro-F1, junto con métricas por clase.
- Hay que explicitar el **aporte tecnológico** y el **aporte científico**.

## 7. Figura de la metodología (Matriz de Investigación de referencia)

Se usa un diagrama con 4 bloques numerados: **1. Adquisición → 2.
Preprocesamiento → 3. Extracción de características → 4. Modelado y
clasificación**. Tiene ramas de color, una por metodología comparada
(Metodología 1 gris, 2 azul, 3 verde), que llegan a la salida de clases. La
figura de FDTooth (`img/metodologia.png`) ya sigue este formato:
M1 = rasgos manuales + ML, M2 = ajuste fino, M3 = DINOv2 + ML.

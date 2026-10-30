# Informe de pulido: Diseño de un Sistema de Visión Computacional para el Pre-diagnóstico de Fenestración y Dehiscencia Ósea Alveolar a partir de Fotografías Intraorales y Tomografías CBCT

Para: los autores, José Cabrera-Ticlla y Lucero Ayala-Mauricio, y su asesor, Wilfredo Ticona.
Revisión hecha con la skill `paper-polishing` (plugin academic-research v1.0.0) sobre `Paper_FDTOOH/main.pdf` (12 páginas, LNCS) el 21/10/2026.

## Evaluación general
**Recomendación:** Revisión menor.
**Justificación:** El protocolo es sólido y la sección de resultados es honesta:
- Partición por paciente.
- Validación cruzada anidada.
- Prueba retenida evaluada una vez.
- *Bootstrap* pareado con 2000 remuestreos.
- Ventaja no significativa reportada como tal.

Hay dos problemas de fondo:
- Hay una tensión sin resolver entre la motivación («la CBCT es poco práctica») y el resultado («la CBCT es indispensable»).
- La contribución principal, el ensamble, mejora poco a su mejor componente.

Ambos se arreglan con redacción, sin experimentos nuevos.

## Tres fortalezas principales
1. **Rigor del protocolo de evaluación (3.4, Tabla 1):**
   - Partición por paciente y validación cruzada anidada.
   - Rejilla de 12 ensambles elegida en desarrollo; la prueba es «solo descriptiva».
   - El texto lo declara de forma explícita, algo poco común y que blinda el trabajo contra la acusación de sobreajuste en la selección.
2. **Honestidad estadística (4.4, 4.5):**
   - Se informa que la ventaja del ensamble sobre ConvNeXt V2 con fusión es significativa en desarrollo (+0.014) y no en la prueba (+0.006; IC −0.014 a +0.026).
   - Se reconoce que la fusión no mejora a la CBCT sola.
3. **Análisis de componentes y de errores claro (Fig. 2, Fig. 3, 4.3):**
   - Se ve qué aporta cada componente; por ejemplo, RF comete 15 errores D→N y el ensamble conserva las 148 fenestraciones de la red con CBCT.
   - La lectura clínica de la sensibilidad F/D (0.979) está bien argumentada.

## Problemas críticos (corregir antes de enviar)
1. **Falta la declaración «Disclosure of Interests» (después de Conclusiones):**
   - Springer exige hoy en LNCS declarar los conflictos de interés o afirmar que no los hay. La clase `llncs` instalada ya trae el entorno `credits` con `\discintname`.
   - **Corrección:** antes de la bibliografía, añadir:
     ```latex
     \begin{credits}
     \subsubsection{\discintname}
     Los autores declaran no tener conflictos de interés.
     \end{credits}
     ```
     Se puede añadir un agradecimiento opcional a PhysioNet o a los autores de FDTooth.
2. **Tensión entre la motivación y el resultado (Introducción, párr. 3, frente a 4.5 y Conclusiones):**
   - La Introducción presenta como problema que «su uso rutinario [de la CBCT] es poco práctico por la radiación».
   - El resultado central es que el sistema **necesita** la CBCT y que la fotografía no aporta.
   - Un revisor preguntará para qué sirve un pre-diagnóstico que exige el examen que se quería evitar.
   - **Corrección:** decir en 4.5, en una o dos oraciones, el escenario de uso realista. El sistema apoya la lectura de una CBCT **ya indicada**, por ejemplo antes de la ortodoncia, que es cuando se evalúan estos defectos [3]: marca qué dientes revisar y reduce omisiones (sensibilidad de 0.979). También conviene matizar en la Introducción que la fotografía se evalúa como posible filtro y que el estudio mide si basta.

## Problemas mayores (debilitan el trabajo)
1. **El resumen sobrevende la ventaja del ensamble (Resumen, última oración):**
   - «superó [...] por un margen menor, a los de Deep Learning» omite que la diferencia no es significativa.
   - **Corrección:** «…y obtuvo un *Macro-F1* similar al de la mejor red (diferencia no significativa en la prueba)».
2. **Falta reproducibilidad en 3.2 y 3.3:**
   - Faltan detalles que ya están en el código: tamaño de entrada (foto 384×224, CBCT 320×144), ventana HU (−300 a 2200) y cómo se forman los cortes 2.5D (número de cortes y separación).
   - También faltan los aumentos usados, el hardware y una declaración de disponibilidad de código y datos (FDTooth: acceso acreditado en PhysioNet).
   - **Corrección:** dos o tres líneas en 3.3 y una frase de disponibilidad de datos.
3. **Los Trabajos Relacionados no cubren la técnica propuesta (sección 2):**
   - El método es un ensamble híbrido de DL y ML, pero el único antecedente de ensamble es la votación suave de Sha et al. [9], y dentro de ML clásico.
   - La subsección 2.3 trata de DINOv2, que el trabajo ya no usa.
   - **Corrección:** añadir uno o dos antecedentes de ensambles en odontología o de DL sobre hueso alveolar anterior (ver «Citas faltantes»). Se puede hacer manteniendo la estructura de la guía v5.
4. **Origen de las etiquetas (4.5, Limitaciones):**
   - Las etiquetas vienen de la lectura de la CBCT por dos odontólogos (κ > 0.9), no de una referencia independiente como la cirugía.
   - El modelo aprende a reproducir esa lectura.
   - **Corrección:** añadirlo a las limitaciones en media oración.

## Comentarios por sección

### Resumen
- Corregir el matiz de significancia (problema mayor 1).
- «AUC» y «CBCT» aparecen sin definir. Se aceptan en un resumen, pero en el cuerpo deben definirse la primera vez.

### 1. Introducción
- El embudo (OMS → América Latina → Perú → IA → propósito) cumple la guía.
- Añadir en el párrafo 4 una frase sobre el escenario clínico de uso (problema crítico 2).
- «AUC» se usa en el párrafo 3 sin definirse; escribir «área bajo la curva ROC (AUC)».

### 2. Trabajos Relacionados
- El formato v5 está bien aplicado: conectores, \res{} y \hal{}.
- La 2.3 justifica la fusión multimodal, que sí se discute, pero no el ensamble. Ver el problema mayor 3.

### 3. Metodología
- La figura antecede a las subsecciones, como en la plantilla. Bien.
- 3.3: indicar que la elección del ensamble usó solo predicciones fuera de partición, como ya dice 3.4. Solo hay que remitir a ella.
- 3.4: la lista de métricas coincide con los resultados reportados. Bien.

### 4. Resultados
- 4.1: correcto. La frase «combinar las dos redes superó a usar una sola con cualquiera de los cuatro clasificadores» es un buen hallazgo; conviene que la Discusión diga por qué (redes con errores distintos: la de CBCT confunde N→F y la de fusión, menos).
- 4.3: la Fig. 3 respalda bien el texto.
- 4.5: añadir el escenario de uso y la limitación de las etiquetas. Comparar con el antecedente solo en lo comparable, advirtiendo que su AUC de 0.76 es binario y solo con foto.

### 5. Conclusiones
- Coherentes con los resultados. La palabra «indispensable» está justificada por la diferencia de +0.285 (IC +0.231 a +0.345).

## Revisión de ecuaciones
El paper no tiene ecuaciones numeradas. Opcional: definir *Macro-F1* en 3.4 con una fórmula, $\text{Macro-F1}=\frac{1}{3}\sum_{c\in\{N,F,D\}}F1_c$. Ayuda a un lector de odontología.

## Revisión de figuras y tablas
| Elemento | Estado actual | Mejora sugerida |
|---|---|---|
| Fig. 1 | Diagrama de 4 bloques. Las etiquetas mezclan español e inglés («Accuracy», «Recall macro») | Unificar el idioma con el del texto; al traducir, todo en inglés. El texto de los bloques es pequeño: comprobar que se lea impreso a 12.2 cm |
| Fig. 2 | Barras de desarrollo y prueba por componente; valores rotados a unos 6 pt; la línea del antecedente cruza también las barras de prueba | Subir las etiquetas a 7 u 8 pt. Dibujar la línea del antecedente solo a la altura de las barras de desarrollo, o dejar como está y conservar la aclaración de la leyenda |
| Fig. 3 | Cuatro matrices con conteo y porcentaje; texto de celda a unos 6 pt | Subir el texto de celda a 7 pt; los títulos de panel ya caben |
| Tabla 1 | 12 ensambles con rejilla; métricas de desarrollo y prueba | Clara. Opcional: marcar con un asterisco que la rejilla de prueba es descriptiva |
| Tabla 2 | Hiperparámetros por componente, por bloques DL / ML / Ensamble | Clara. Opcional: añadir el espacio de búsqueda, por ejemplo C ∈ {0.3, 1, 3, 10}, para mayor reproducibilidad |

## Citas faltantes
Candidatas halladas con `paper_search.py` (Semantic Scholar) y Europe PMC, filtradas a 2021 en adelante. **Ninguna está verificada como Q1 (SJR) ni revisada en texto completo.** Hay que confirmarlas según la regla de CLAUDE.md antes de citarlas.

| Ubicación | Afirmación | Cita sugerida | Por qué |
|---|---|---|---|
| 2.2 o 2.3 (técnica: ensambles) | Ensambles de modelos en diagnóstico dental | Multi-label dental disorder diagnosis based on MobileNetV2 and swin transformer using bagging ensemble classifier. *Scientific Reports* (2024). doi:10.1038/s41598-024-73297-9 | Único ensamble con DL en odontología en Europe PMC (2021+); da contexto al método propuesto |
| 2.2 (DL sobre hueso alveolar anterior) | DL sobre hueso alveolar anterior en CBCT | Deep learning-assisted cone-beam computed tomography volumetric assessment of mandibular anterior alveolar... *Am J Orthod Dentofacial Orthop* (2026). doi:10.1016/j.ajodo.2026.06.012 | Misma región anatómica y contexto ortodóntico que FDTooth |
| 2.2 (segmentación del hueso alveolar) | CNN para segmentar el hueso alveolar en CBCT | Convolutional neural network-based automated maxillary alveolar bone segmentation on cone-beam computed tomography. *Clin Oral Implants Res* (2023). doi:10.1111/clr.14063 | Antecedente muy citado (57 citas en Europe PMC) sobre hueso alveolar |
| 4.5 (defectos óseos) | DL para clasificar deficiencias del reborde | Deep learning for the identification of ridge deficiency around dental implants. *Clin Implant Dent Relat Res* (2024). doi:10.1111/cid.13301 | Clasificación de defectos óseos alveolares con DL |

## Lista de revisión
- [ ] **Prioridad 1 (crítico):** añadir el entorno `credits` con «Disclosure of Interests» antes de la bibliografía.
- [ ] **Prioridad 2 (crítico):** en 4.5, y con una frase en la Introducción, el escenario de uso: apoyo a la lectura de una CBCT ya indicada, no su sustitución.
- [ ] **Prioridad 3 (mayor):** en el Resumen, decir que la diferencia con la mejor red no es significativa.
- [ ] **Prioridad 4 (mayor):** en 3.3, añadir tamaños de entrada, ventana HU, construcción 2.5D y aumentos; añadir la disponibilidad de datos y código.
- [ ] **Prioridad 5 (mayor):** uno o dos antecedentes de ensambles o de DL sobre hueso alveolar, verificados como Q1.
- [ ] **Prioridad 6 (mayor):** en las limitaciones, que las etiquetas vienen de la lectura de la CBCT.
- [ ] **Prioridad 7 (menor):** definir «AUC» en el cuerpo; unificar el idioma de la Fig. 1; subir a 7 u 8 pt el texto de las Fig. 2 y 3.
- [ ] **Prioridad 8 (menor):** opcional, la fórmula de Macro-F1 y el espacio de búsqueda en la Tabla 2.

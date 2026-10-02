# CAMELS-PE Experimentos V2 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Construir y ejecutar una segunda corrida espacial reproducible que seleccione el mejor modelo de caudal diario sin fuga de información.

**Architecture:** Se añadirá un pipeline independiente bajo `data/experimentos_v2/`, dejando intacta la V1. Los módulos comunes centralizarán elegibilidad, particiones, preprocesamiento por fold, métricas y trazabilidad; cada modelo consumirá esas interfaces y emitirá predicciones con un esquema común. Un agregador calcula métricas por cuenca, grupo, región y fold, y aplica la regla de selección aprobada.

**Tech Stack:** Python 3, pandas, NumPy, scikit-learn, XGBoost, SciPy, PyTorch, pytest y CSV/JSON.

**Spec:** `docs/superpowers/specs/2026-10-01-camels-pe-experimentos-v2-design.md`

## Global Constraints

- Conservar sin cambios `data/experimentos/` y guardar solo bajo `data/experimentos_v2/`.
- Usar exclusivamente 1981-01-01 a 2016-12-31, `flow_obs` como objetivo y nunca `flow_sim` ni `hydrological_signatures.csv`.
- Separar siempre por `nested_group_id`; test no interviene en transformaciones, ajuste ni selección.
- Ajustar imputación, escalado y filtrado solo con train interno; al refit se permite train más validación, nunca test.
- La selección principal es KGE mediana entre grupos; si la diferencia es menor de 0.01, NSE; después `abs(PBIAS)`.
- Mantener configuraciones, semillas, versión de dependencias, estado de cada fold y resultados de errores.

## Review Focus

- Cuencas con baja disponibilidad: no pueden entrar al reporte principal si no cumplen 20 % y 365 días continuos dentro de la ventana efectiva.
- Grupo anidado mayoritario: no puede compartir un split y no debe pesar más que un grupo pequeño en el ranking global.
- Datos de prueba: ningún estadístico de test puede cambiar imputadores, escaladores, filtros o hiperparámetros.
- Fechas de evaluación: las seis predicciones comparadas para una cuenca deben reducirse a una intersección común de fechas observadas.
- Corridas incompletas: un fold fallido debe aparecer como fallido y quedar fuera del ranking, sin reutilizar checkpoints incompatibles.

---

### Task 1: Estructura V2, configuración y registro reproducible

**Files:**
- Create: `data/experimentos_v2/README.md`
- Create: `data/experimentos_v2/config/base.json`
- Create: `data/experimentos_v2/src/config.py`
- Create: `data/experimentos_v2/src/run_registry.py`
- Create: `data/experimentos_v2/tests/test_config.py`

**Interfaces:**
- Produces: `ExperimentConfig.load(path: Path) -> ExperimentConfig` and `RunRegistry.start_run(config: ExperimentConfig) -> Path`.
- Produces: a run directory containing immutable `config.json`, `environment.json` and `status.json`.

- [ ] **Step 1: Write failing configuration and registry tests**

Assert that V2 paths never resolve inside `data/experimentos/`, the temporal range is 1981-01-01 through 2016-12-31, and a started run persists configuration and environment metadata.

- [ ] **Step 2: Run configuration tests to verify they fail**

Run: `pytest data/experimentos_v2/tests/test_config.py -v`
Expected: FAIL because V2 modules do not exist.

- [ ] **Step 3: Implement configuration and run registry modules**

Implement typed configuration loading and a registry that creates unique run IDs, records package versions and prevents checkpoint reuse unless the complete configuration fingerprint matches.

- [ ] **Step 4: Run configuration tests to verify they pass**

Run: `pytest data/experimentos_v2/tests/test_config.py -v`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add data/experimentos_v2
git commit -m "feat: add V2 experiment configuration and registry"
```

### Task 2: Elegibilidad V2 y particiones espaciales

**Files:**
- Create: `data/experimentos_v2/src/eligibility.py`
- Create: `data/experimentos_v2/src/splits.py`
- Create: `data/experimentos_v2/scripts/01_build_eligibility.py`
- Create: `data/experimentos_v2/scripts/02_build_splits.py`
- Create: `data/experimentos_v2/tests/test_eligibility.py`
- Create: `data/experimentos_v2/tests/test_splits.py`

**Interfaces:**
- Produces: `build_eligibility(config: ExperimentConfig) -> pd.DataFrame` with `eligible_donor` and `eligible_report`.
- Produces: `build_spatial_splits(eligibility: pd.DataFrame, config: ExperimentConfig) -> pd.DataFrame` with outer and inner assignments.

- [ ] **Step 1: Write failing eligibility and group-isolation tests**

Use miniature daily data to verify eligibility uses only the configured dates and enforces 20 % availability plus longest run of 365 days for reporting. Verify that `flow_sim` and target-derived signatures are excluded from every model feature source, and test every outer and inner split for disjoint group sets.

- [ ] **Step 2: Run these tests to verify they fail**

Run: `pytest data/experimentos_v2/tests/test_eligibility.py data/experimentos_v2/tests/test_splits.py -v`
Expected: FAIL because the pipeline does not exist.

- [ ] **Step 3: Implement V2 eligibility and nested grouped split builders**

Build donor/report flags in the exact window. Persist tables of exclusions, group sizes, outer assignments and inner assignments. Preserve all `nested_group_id` members in one partition and mark the 35-member group explicitly in diagnostics.

- [ ] **Step 4: Run eligibility and split tests to verify they pass**

Run: `pytest data/experimentos_v2/tests/test_eligibility.py data/experimentos_v2/tests/test_splits.py -v`
Expected: PASS.

- [ ] **Step 5: Execute artifact generation and inspect counts**

Run: `python data/experimentos_v2/scripts/01_build_eligibility.py && python data/experimentos_v2/scripts/02_build_splits.py`
Expected: donor count, report count and complete split CSVs saved in the V2 run directory.

- [ ] **Step 6: Commit**

```bash
git add data/experimentos_v2
git commit -m "feat: add V2 eligibility and spatial splits"
```

### Task 3: Preprocesamiento por fold y conjuntos de datos comunes

**Files:**
- Create: `data/experimentos_v2/src/data_loading.py`
- Create: `data/experimentos_v2/src/preprocessing.py`
- Create: `data/experimentos_v2/src/datasets.py`
- Create: `data/experimentos_v2/tests/test_preprocessing.py`

**Interfaces:**
- Produces: `FoldPreprocessor.fit(train_ids: Sequence[str]) -> FoldPreprocessor` and `transform(ids: Sequence[str]) -> PreparedCatchments`.
- Produces: `make_tabular_samples(...)` and `make_sequence_samples(...)` without using observed flow as an input.

- [ ] **Step 1: Write failing anti-fuga and missing-data tests**

Assert that changing test values does not alter train-fitted scaler/imputer parameters; that missing static values generate indicators; that signatures and `flow_sim` never appear among features; and that sequences never cross catchment boundaries.

- [ ] **Step 2: Run preprocessing tests to verify they fail**

Run: `pytest data/experimentos_v2/tests/test_preprocessing.py -v`
Expected: FAIL because preprocessing classes do not exist.

- [ ] **Step 3: Implement fold-only preprocessing and datasets**

Use training-only medians and scaling statistics, global forcing scaling across training catchments, feature metadata, 30-day tabular lags, and 270/365-day sequence candidates. Implement balanced-by-catchment sampling as an optional memory control and record its effective sample counts.

- [ ] **Step 4: Run preprocessing tests to verify they pass**

Run: `pytest data/experimentos_v2/tests/test_preprocessing.py -v`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add data/experimentos_v2
git commit -m "feat: add leakage-safe V2 preprocessing"
```

### Task 4: Métricas comunes, fechas compartidas y agregación por grupo

**Files:**
- Create: `data/experimentos_v2/src/metrics.py`
- Create: `data/experimentos_v2/src/evaluation.py`
- Create: `data/experimentos_v2/tests/test_evaluation.py`

**Interfaces:**
- Produces: `evaluate_predictions(predictions: pd.DataFrame) -> pd.DataFrame`.
- Produces: `aggregate_results(catchment_metrics: pd.DataFrame) -> ModelSummary` and `select_winner(summary: pd.DataFrame) -> str`.

- [ ] **Step 1: Write failing evaluation tests**

Test common-date intersections, KGE/NSE/RMSE/MAE/PBIAS calculations, group medians that give equal group weight, the 0.01 KGE tie-break and exclusion of failed folds from the ranking.

- [ ] **Step 2: Run evaluation tests to verify they fail**

Run: `pytest data/experimentos_v2/tests/test_evaluation.py -v`
Expected: FAIL because evaluation functions do not exist.

- [ ] **Step 3: Implement common-schema evaluation and selection**

Require every prediction record to contain run, model, fold, split, group, gauge, date, observation and simulation. Build group-, region- and fold-level summaries and a deterministic selection table with all tie-break fields.

- [ ] **Step 4: Run evaluation tests to verify they pass**

Run: `pytest data/experimentos_v2/tests/test_evaluation.py -v`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add data/experimentos_v2
git commit -m "feat: add V2 grouped evaluation and ranking"
```

### Task 5: Modelos V2 deterministas

**Files:**
- Create: `data/experimentos_v2/src/models/gr4j.py`
- Create: `data/experimentos_v2/src/models/trees.py`
- Create: `data/experimentos_v2/src/models/recurrent.py`
- Create: `data/experimentos_v2/src/training.py`
- Create: `data/experimentos_v2/scripts/03_run_deterministic.py`
- Create: `data/experimentos_v2/tests/test_models_smoke.py`

**Interfaces:**
- Produces: `fit_predict_outer_fold(model_name: str, outer_fold: int, config: ExperimentConfig) -> pd.DataFrame`.
- Consumes: prepared fold datasets, inner assignments and shared evaluation schema.

- [ ] **Step 1: Write failing model smoke tests**

For synthetic data, assert each of GR4J, RF, XGBoost, GRU, LSTM and EA-LSTM produces finite nonnegative flows with the standard prediction schema; assert hyperparameters are selected from inner validation only.

- [ ] **Step 2: Run model smoke tests to verify they fail**

Run: `pytest data/experimentos_v2/tests/test_models_smoke.py -v`
Expected: FAIL because V2 model adapters do not exist.

- [ ] **Step 3: Implement tree and GR4J model adapters**

Implement inner search grids for Random Forest and XGBoost. Implement GR4J calibration with warm-up, a recorded optimization budget and inner selection among documented regionalization strategies.

- [ ] **Step 4: Implement recurrent model adapters**

Implement GRU, LSTM and EA-LSTM candidates for sequence lengths 270/365, hidden sizes 128/256 and dropout 0.1/0.2/0.4. Use early stopping on validation grouped KGE and run configured random seeds; retain the selected configuration and seed metrics.

- [ ] **Step 5: Run model smoke tests to verify they pass**

Run: `pytest data/experimentos_v2/tests/test_models_smoke.py -v`
Expected: PASS.

- [ ] **Step 6: Execute a one-fold pilot for all six models**

Run: `python data/experimentos_v2/scripts/03_run_deterministic.py --fold 0 --models E1_GR4J E2_RF E3_XGB E4_GRU E5_LSTM E6_EALSTM --pilot`
Expected: six completed or explicitly failed model records, prediction CSVs, metrics and a pilot ranking under one V2 run ID.

- [ ] **Step 7: Commit**

```bash
git add data/experimentos_v2
git commit -m "feat: add V2 deterministic model runners"
```

### Task 6: Corrida completa, diagnóstico y challenger Crossformer

**Files:**
- Create: `data/experimentos_v2/src/models/crossformer.py`
- Create: `data/experimentos_v2/scripts/04_run_full.py`
- Create: `data/experimentos_v2/scripts/05_build_report.py`
- Create: `data/experimentos_v2/tests/test_report.py`

**Interfaces:**
- Consumes: V2 run artifacts for all completed outer folds.
- Produces: full selection CSV, figures, report Markdown and optional Crossformer challenger results.

- [ ] **Step 1: Write failing reporting tests**

Test that a report rejects missing expected folds, labels an incomplete model clearly and produces winner, baseline delta, group summary and regional summary from complete results.

- [ ] **Step 2: Run reporting tests to verify they fail**

Run: `pytest data/experimentos_v2/tests/test_report.py -v`
Expected: FAIL because reporting code does not exist.

- [ ] **Step 3: Implement full runner and report builder**

Implement resume-safe full execution across five outer folds, status tracking, diagnostic plots, selection tables and a report that compares V2 against the frozen V1 baseline without conflating protocols.

- [ ] **Step 4: Run report tests to verify they pass**

Run: `pytest data/experimentos_v2/tests/test_report.py -v`
Expected: PASS.

- [ ] **Step 5: Execute the six-model full run and inspect completion**

Run: `python data/experimentos_v2/scripts/04_run_full.py --models E1_GR4J E2_RF E3_XGB E4_GRU E5_LSTM E6_EALSTM`
Expected: five completed external folds for each eligible deterministic model, V2 ranking and comparison report.

- [ ] **Step 6: Implement and run Crossformer only after the recurrent baseline passes the pilot**

Run: `python data/experimentos_v2/scripts/04_run_full.py --models E7_CROSSFORMER`
Expected: separate challenger artifacts under the same schema; it appears in an extension comparison, not the six-model thesis ranking unless formally adopted.

- [ ] **Step 7: Commit**

```bash
git add data/experimentos_v2
git commit -m "feat: run V2 experiments and report selection"
```

### Task 7: Cuantificación de incertidumbre de la red seleccionada

**Files:**
- Create: `data/experimentos_v2/src/uncertainty.py`
- Create: `data/experimentos_v2/scripts/06_run_quantiles.py`
- Create: `data/experimentos_v2/tests/test_uncertainty.py`

**Interfaces:**
- Consumes: selected neural model per external fold and fold-safe preprocessing.
- Produces: Q0.05, Q0.50 and Q0.95 prediction records plus coverage, width and calibration summaries.

- [ ] **Step 1: Write failing quantile tests**

Assert quantiles are ordered, interval metrics are calculated per catchment and group, and the runner refuses a non-neural or externally selected architecture.

- [ ] **Step 2: Run uncertainty tests to verify they fail**

Run: `pytest data/experimentos_v2/tests/test_uncertainty.py -v`
Expected: FAIL because the uncertainty module does not exist.

- [ ] **Step 3: Implement quantile training and evaluation**

Implement pinball-loss outputs for 0.05, 0.50 and 0.95 on the internally selected neural architecture only. Preserve test isolation and generate the predesignated illustrative hydrograph.

- [ ] **Step 4: Run uncertainty tests to verify they pass**

Run: `pytest data/experimentos_v2/tests/test_uncertainty.py -v`
Expected: PASS.

- [ ] **Step 5: Execute uncertainty experiment and final verification**

Run: `python data/experimentos_v2/scripts/06_run_quantiles.py`
Expected: complete interval predictions, coverage/width/calibration tables and final report augmentation.

- [ ] **Step 6: Commit**

```bash
git add data/experimentos_v2
git commit -m "feat: add V2 predictive uncertainty evaluation"
```

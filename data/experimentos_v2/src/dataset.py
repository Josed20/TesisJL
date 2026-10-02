"""Auditoría de datos y particiones espaciales sin fuga para CAMELS-PE V2."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.model_selection import GroupKFold


DEFAULT_FEATURES = ("prec", "pet", "tmin", "tmean", "tmax", "srad", "vprp")


def _longest_true_run(mask: pd.Series) -> int:
    """Devuelve la longitud de la mayor racha consecutiva verdadera."""
    values = mask.to_numpy(dtype=bool)
    longest = current = 0
    for value in values:
        current = current + 1 if value else 0
        longest = max(longest, current)
    return longest


def audit_camels_pe(
    camels_root: Path,
    start_date: str,
    end_date: str,
    features: tuple[str, ...] = DEFAULT_FEATURES,
    target: str = "flow_obs",
) -> pd.DataFrame:
    """Audita sólo la ventana efectiva; nunca utiliza ``flow_sim`` como predictor."""
    camels_root = Path(camels_root)
    stations = pd.read_csv(camels_root / "01_metadata" / "stations.csv")
    series_root = camels_root / "03_timeseries" / "by_catchment"
    start, end = pd.Timestamp(start_date), pd.Timestamp(end_date)
    records: list[dict[str, object]] = []

    for station in stations.itertuples(index=False):
        gauge_id = station.gauge_id
        path = series_root / f"{gauge_id}.csv"
        if not path.exists():
            records.append({"gauge_id": gauge_id, "file_found": False})
            continue
        full_frame = pd.read_csv(path, parse_dates=["date"])
        full_target_valid = full_frame[target].notna() if target in full_frame else pd.Series(False, index=full_frame.index)
        frame = full_frame.loc[(full_frame.date >= start) & (full_frame.date <= end)].sort_values("date")
        target_valid = frame[target].notna() if target in frame else pd.Series(False, index=frame.index)
        available_features = [feature for feature in features if feature in frame]
        complete = target_valid & frame[available_features].notna().all(axis=1)
        total_days = len(frame)
        records.append(
            {
                "gauge_id": gauge_id,
                "nested_group_id": station.nested_group_id,
                "gauge_region": station.gauge_region,
                "file_found": True,
                "window_days": total_days,
                "flow_obs_valid_days": int(target_valid.sum()),
                "pct_flow_obs": 100.0 * float(target_valid.mean()) if total_days else 0.0,
                "pct_flow_obs_full_record": 100.0 * float(full_target_valid.mean()) if len(full_frame) else 0.0,
                "complete_days": int(complete.sum()),
                "longest_complete_run_days": _longest_true_run(complete),
            }
        )
    return pd.DataFrame.from_records(records)


def select_samples(
    audit: pd.DataFrame,
    min_coverage_pct: float,
    min_continuous_days: int,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Separa donantes de entrenamiento y muestra robusta para el reporte."""
    # El marco donante replica el universo V1 de 88 cuencas (cobertura del
    # registro completo). La muestra de reporte exige, adicionalmente, calidad
    # dentro de la ventana efectiva de entrenamiento/evaluación.
    donors = audit.loc[
        audit.file_found & (audit.pct_flow_obs_full_record >= min_coverage_pct)
    ].copy()
    reporting = donors.loc[
        (donors.pct_flow_obs >= min_coverage_pct)
        & (donors.longest_complete_run_days >= min_continuous_days)
    ].copy()
    return donors.reset_index(drop=True), reporting.reset_index(drop=True)


def build_nested_splits(donors: pd.DataFrame, outer_folds: int = 5) -> pd.DataFrame:
    """Crea folds externos e internos agrupados por topología de cuenca."""
    if donors.nested_group_id.nunique() < outer_folds:
        raise ValueError("No hay suficientes grupos topológicos para los folds externos")
    result = donors.copy().reset_index(drop=True)
    group_values = result.nested_group_id.to_numpy()
    dummy = np.zeros(len(result))
    outer = GroupKFold(n_splits=outer_folds)
    fold_test = np.full(len(result), -1, dtype=int)
    for fold, (_, test_index) in enumerate(outer.split(dummy, groups=group_values)):
        fold_test[test_index] = fold
    result["fold_test"] = fold_test

    for fold in range(outer_folds):
        column = f"split_fold_{fold}"
        result[column] = "train"
        result.loc[result.fold_test == fold, column] = "test"
        train_val_index = result.index[result.fold_test != fold].to_numpy()
        train_val_groups = result.loc[train_val_index, "nested_group_id"].to_numpy()
        n_inner = min(4, len(np.unique(train_val_groups)))
        inner = GroupKFold(n_splits=n_inner)
        inner_splits = list(inner.split(np.zeros(len(train_val_index)), groups=train_val_groups))
        _, validation_local = inner_splits[fold % n_inner]
        result.loc[train_val_index[validation_local], column] = "val"
    return result


def write_protocol_artifacts(
    camels_root: Path,
    output_root: Path,
    start_date: str,
    end_date: str,
    min_coverage_pct: float,
    min_continuous_days: int,
    outer_folds: int,
) -> dict[str, object]:
    """Genera las tablas de elegibilidad y particiones que consume la corrida."""
    output_root = Path(output_root)
    audit = audit_camels_pe(camels_root, start_date, end_date)
    donors, reporting = select_samples(audit, min_coverage_pct, min_continuous_days)
    audit["donor_eligible"] = audit.gauge_id.isin(donors.gauge_id)
    audit["reporting_eligible"] = audit.gauge_id.isin(reporting.gauge_id)
    assignments = build_nested_splits(donors, outer_folds=outer_folds)

    eligibility_dir = output_root / "01_elegibilidad"
    splits_dir = output_root / "02_splits"
    eligibility_dir.mkdir(parents=True, exist_ok=True)
    splits_dir.mkdir(parents=True, exist_ok=True)
    eligibility_path = eligibility_dir / "tabla_elegibilidad_v2.csv"
    splits_path = splits_dir / "splits_asignaciones.csv"
    groups_path = splits_dir / "grupos_por_fold.csv"
    audit.to_csv(eligibility_path, index=False)
    assignments.to_csv(splits_path, index=False)

    group_rows: list[dict[str, object]] = []
    for fold in range(outer_folds):
        split_column = f"split_fold_{fold}"
        for (group, split), subset in assignments.groupby(["nested_group_id", split_column]):
            group_rows.append(
                {
                    "fold": fold,
                    "nested_group_id": group,
                    "split": split,
                    "n_basins": len(subset),
                    "n_reporting_basins": int(subset.gauge_id.isin(reporting.gauge_id).sum()),
                }
            )
    pd.DataFrame(group_rows).to_csv(groups_path, index=False)
    return {
        "eligibility": audit,
        "assignments": assignments,
        "eligibility_path": eligibility_path,
        "splits_path": splits_path,
        "groups_path": groups_path,
    }

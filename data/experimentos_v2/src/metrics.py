"""Métricas hidrológicas y agregación espacial equitativa."""

from __future__ import annotations

import numpy as np
import pandas as pd


def _metrics(observed: np.ndarray, predicted: np.ndarray) -> dict[str, float]:
    valid = np.isfinite(observed) & np.isfinite(predicted)
    observed, predicted = observed[valid], predicted[valid]
    if len(observed) < 2 or np.isclose(np.var(observed), 0.0):
        return {"nse": np.nan, "kge": np.nan, "pbias": np.nan, "n_obs": int(len(observed))}
    nse = 1.0 - np.sum((predicted - observed) ** 2) / np.sum((observed - observed.mean()) ** 2)
    correlation = np.corrcoef(observed, predicted)[0, 1]
    alpha = np.std(predicted) / np.std(observed)
    beta = np.mean(predicted) / np.mean(observed) if not np.isclose(np.mean(observed), 0.0) else np.nan
    kge = 1.0 - np.sqrt((correlation - 1) ** 2 + (alpha - 1) ** 2 + (beta - 1) ** 2)
    pbias = 100.0 * np.sum(predicted - observed) / np.sum(observed) if not np.isclose(np.sum(observed), 0.0) else np.nan
    return {"nse": float(nse), "kge": float(kge), "pbias": float(pbias), "n_obs": int(len(observed))}


def evaluate_by_basin(predictions: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for gauge_id, frame in predictions.groupby("gauge_id"):
        row = {"gauge_id": gauge_id}
        row.update(_metrics(frame.flow_obs.to_numpy(float), frame.flow_pred.to_numpy(float)))
        if "nested_group_id" in frame:
            row["nested_group_id"] = frame.nested_group_id.iloc[0]
        rows.append(row)
    return pd.DataFrame(rows)


def group_equal_weight_summary(basin_metrics: pd.DataFrame) -> dict[str, float]:
    grouped = basin_metrics.groupby("nested_group_id")[["kge", "nse", "pbias"]].median()
    return {
        "median_group_kge": float(grouped.kge.median()),
        "median_group_nse": float(grouped.nse.median()),
        "median_group_abs_pbias": float(grouped.pbias.abs().median()),
        "n_groups": int(len(grouped)),
    }

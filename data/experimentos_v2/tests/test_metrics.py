from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

V2_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(V2_ROOT))

from src.metrics import evaluate_by_basin, group_equal_weight_summary


def test_perfect_predictions_have_perfect_nse_kge_and_zero_pbias() -> None:
    predictions = pd.DataFrame({"gauge_id": ["a"] * 4, "flow_obs": [1., 2., 3., 4.], "flow_pred": [1., 2., 3., 4.]})
    metrics = evaluate_by_basin(predictions)
    assert metrics.loc[0, "nse"] == 1.0
    assert metrics.loc[0, "kge"] == 1.0
    assert metrics.loc[0, "pbias"] == 0.0


def test_summary_gives_each_nested_group_equal_weight() -> None:
    basin_metrics = pd.DataFrame({"nested_group_id": ["large"] * 10 + ["small"], "kge": [0.0] * 10 + [1.0], "nse": [0.0] * 10 + [1.0], "pbias": [0.0] * 11})
    summary = group_equal_weight_summary(basin_metrics)
    assert summary["median_group_kge"] == 0.5

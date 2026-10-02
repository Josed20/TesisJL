from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

V2_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(V2_ROOT))

from src.preprocessing import FoldPreprocessor, load_allowed_static_attributes


def test_dynamic_statistics_are_fit_only_on_training_rows() -> None:
    train = pd.DataFrame({"prec": [1.0, 3.0, np.nan], "pet": [2.0, 4.0, 6.0]})
    held_out = pd.DataFrame({"prec": [1000.0], "pet": [2000.0]})
    processor = FoldPreprocessor(dynamic_features=("prec", "pet"), static_features=())
    processor.fit_dynamic(train)
    transformed = processor.transform_dynamic(held_out)
    assert processor.dynamic_medians_["prec"] == 2.0
    assert transformed.loc[0, "prec"] > 100.0
    assert transformed.loc[0, "pet"] > 100.0


def test_static_missingness_is_train_fitted_and_exposed_as_indicator() -> None:
    train = pd.DataFrame({"gauge_id": ["a", "b"], "elev": [100.0, np.nan]})
    held_out = pd.DataFrame({"gauge_id": ["c"], "elev": [np.nan]})
    processor = FoldPreprocessor(dynamic_features=(), static_features=("elev",))
    processor.fit_static(train)
    transformed = processor.transform_static(held_out)
    assert processor.static_medians_["elev"] == 100.0
    assert transformed.loc[0, "elev_missing"] == 1
    assert transformed.loc[0, "elev"] == 0.0


def test_static_loader_excludes_hydrological_signatures_and_keeps_numeric_attributes() -> None:
    project_root = V2_ROOT.parents[1]
    attributes, feature_names = load_allowed_static_attributes(project_root / "data" / "CAMELS-PE")
    assert "gauge_id" in attributes
    assert "q_mean" not in feature_names
    assert "area" in feature_names
    assert len(attributes) == 136

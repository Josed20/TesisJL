"""Transformaciones ajustadas sólo con el conjunto train de cada fold."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


def load_allowed_static_attributes(camels_root: Path) -> tuple[pd.DataFrame, tuple[str, ...]]:
    """Carga atributos estáticos numéricos y excluye firmas hidrológicas prohibidas."""
    attributes_root = Path(camels_root) / "02_attributes"
    tables: list[pd.DataFrame] = []
    for path in sorted(attributes_root.glob("*_attributes.csv")):
        if path.name == "hydrological_signatures.csv":
            continue
        table = pd.read_csv(path)
        numeric = [column for column in table.columns if column == "gauge_id" or pd.api.types.is_numeric_dtype(table[column])]
        tables.append(table[numeric])
    if not tables:
        raise FileNotFoundError(f"No se encontraron atributos permitidos en {attributes_root}")
    attributes = tables[0]
    for table in tables[1:]:
        attributes = attributes.merge(table, on="gauge_id", how="outer", validate="one_to_one")
    features = tuple(column for column in attributes.columns if column != "gauge_id")
    return attributes, features


class FoldPreprocessor:
    """Imputa y estandariza sin observar validación ni test al ajustar parámetros."""

    def __init__(self, dynamic_features: tuple[str, ...], static_features: tuple[str, ...]):
        self.dynamic_features = dynamic_features
        self.static_features = static_features
        self.dynamic_medians_: dict[str, float] = {}
        self.dynamic_means_: dict[str, float] = {}
        self.dynamic_stds_: dict[str, float] = {}
        self.static_medians_: dict[str, float] = {}
        self.static_means_: dict[str, float] = {}
        self.static_stds_: dict[str, float] = {}

    @staticmethod
    def _safe_std(values: pd.Series) -> float:
        std = float(values.std(ddof=0))
        return std if np.isfinite(std) and std > 0 else 1.0

    def fit_dynamic(self, train: pd.DataFrame) -> "FoldPreprocessor":
        for feature in self.dynamic_features:
            values = pd.to_numeric(train[feature], errors="coerce")
            median = float(values.median())
            if not np.isfinite(median):
                median = 0.0
            filled = values.fillna(median)
            self.dynamic_medians_[feature] = median
            self.dynamic_means_[feature] = float(filled.mean())
            self.dynamic_stds_[feature] = self._safe_std(filled)
        return self

    def transform_dynamic(self, frame: pd.DataFrame) -> pd.DataFrame:
        if set(self.dynamic_features) - self.dynamic_medians_.keys():
            raise RuntimeError("fit_dynamic debe ejecutarse antes de transformar")
        result = frame.copy()
        for feature in self.dynamic_features:
            values = pd.to_numeric(result[feature], errors="coerce").fillna(self.dynamic_medians_[feature])
            result[feature] = (values - self.dynamic_means_[feature]) / self.dynamic_stds_[feature]
        return result

    def fit_static(self, train: pd.DataFrame) -> "FoldPreprocessor":
        for feature in self.static_features:
            values = pd.to_numeric(train[feature], errors="coerce")
            median = float(values.median())
            if not np.isfinite(median):
                median = 0.0
            filled = values.fillna(median)
            self.static_medians_[feature] = median
            self.static_means_[feature] = float(filled.mean())
            self.static_stds_[feature] = self._safe_std(filled)
        return self

    def transform_static(self, frame: pd.DataFrame) -> pd.DataFrame:
        if set(self.static_features) - self.static_medians_.keys():
            raise RuntimeError("fit_static debe ejecutarse antes de transformar")
        result = frame.copy()
        for feature in self.static_features:
            values = pd.to_numeric(result[feature], errors="coerce")
            result[f"{feature}_missing"] = values.isna().astype("int8")
            filled = values.fillna(self.static_medians_[feature])
            result[feature] = (filled - self.static_means_[feature]) / self.static_stds_[feature]
        return result

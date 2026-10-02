"""Carga y validación de la configuración de Experimentos V2."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
import hashlib
import json
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class ExperimentConfig:
    """Configuración inmutable de una corrida V2."""

    start_date: str
    end_date: str
    output_root: Path
    seed: int
    outer_folds: int = 5
    report_min_coverage_pct: float = 20.0
    report_min_continuous_days: int = 365
    dynamic_features: tuple[str, ...] = field(default_factory=tuple)
    target: str = "flow_obs"
    excluded_features: tuple[str, ...] = field(default_factory=tuple)

    @classmethod
    def load(cls, path: Path) -> "ExperimentConfig":
        """Lee un JSON y resuelve rutas relativas contra dicho archivo."""
        path = Path(path).resolve()
        payload = json.loads(path.read_text(encoding="utf-8"))
        output_root = Path(payload["output_root"])
        if not output_root.is_absolute():
            output_root = (path.parent / output_root).resolve()
        output_root = output_root.resolve()

        if output_root.name != "experimentos_v2":
            raise ValueError("output_root debe ser exactamente el directorio experimentos_v2")
        if "experimentos" in output_root.parts and "experimentos_v2" not in output_root.parts:
            raise ValueError("V2 no puede escribir en el directorio de experimentos V1")

        return cls(
            start_date=str(payload["start_date"]),
            end_date=str(payload["end_date"]),
            output_root=output_root,
            seed=int(payload["seed"]),
            outer_folds=int(payload.get("outer_folds", 5)),
            report_min_coverage_pct=float(payload.get("report_min_coverage_pct", 20.0)),
            report_min_continuous_days=int(payload.get("report_min_continuous_days", 365)),
            dynamic_features=tuple(payload.get("dynamic_features", [])),
            target=str(payload.get("target", "flow_obs")),
            excluded_features=tuple(payload.get("excluded_features", [])),
        )

    def to_dict(self) -> dict[str, Any]:
        """Devuelve una representación JSON estable de la configuración."""
        payload = asdict(self)
        payload["output_root"] = str(self.output_root)
        payload["dynamic_features"] = list(self.dynamic_features)
        payload["excluded_features"] = list(self.excluded_features)
        return payload

    @property
    def fingerprint(self) -> str:
        """Huella para identificar exactamente la configuración aplicada."""
        encoded = json.dumps(self.to_dict(), ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


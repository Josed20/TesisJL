"""Registro auditable e inmutable de corridas V2."""

from __future__ import annotations

from datetime import datetime, timezone
import importlib.metadata
import json
from pathlib import Path
import platform
import sys
from typing import Any

from .config import ExperimentConfig


class RunRegistry:
    """Crea directorios de corrida sin sobrescribir resultados existentes."""

    @staticmethod
    def _write_json(path: Path, payload: dict[str, Any]) -> None:
        path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )

    @staticmethod
    def _environment() -> dict[str, Any]:
        packages = {}
        for package in ("numpy", "pandas", "scikit-learn", "xgboost", "torch", "optuna"):
            try:
                packages[package] = importlib.metadata.version(package)
            except importlib.metadata.PackageNotFoundError:
                packages[package] = None
        return {
            "created_at_utc": datetime.now(timezone.utc).isoformat(),
            "python": sys.version,
            "platform": platform.platform(),
            "packages": packages,
        }

    @classmethod
    def start_run(cls, config: ExperimentConfig, run_id: str | None = None) -> Path:
        """Inicia una corrida y conserva su configuración y entorno exactos."""
        if not run_id:
            run_id = datetime.now(timezone.utc).strftime("run-%Y%m%dT%H%M%SZ")
        if not run_id or Path(run_id).name != run_id:
            raise ValueError("run_id debe ser un único nombre de directorio")

        run_dir = config.output_root / "runs" / run_id
        if run_dir.exists():
            raise FileExistsError(f"La corrida ya existe y no se sobrescribirá: {run_dir}")
        run_dir.mkdir(parents=True, exist_ok=False)
        cls._write_json(run_dir / "config.json", config.to_dict())
        cls._write_json(run_dir / "environment.json", cls._environment())
        cls._write_json(
            run_dir / "status.json",
            {"state": "created", "config_fingerprint": config.fingerprint},
        )
        return run_dir


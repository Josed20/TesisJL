from __future__ import annotations

import json
import importlib
import sys
from pathlib import Path

import pytest


V2_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(V2_ROOT))

def _v2_modules():
    try:
        config_module = importlib.import_module("src.config")
        registry_module = importlib.import_module("src.run_registry")
    except ModuleNotFoundError as exc:
        pytest.fail(f"V2 configuration modules are not implemented: {exc}")
    return config_module, registry_module


def test_base_config_uses_v2_paths_and_fixed_effective_window() -> None:
    config_module, _ = _v2_modules()
    ExperimentConfig = config_module.ExperimentConfig
    config = ExperimentConfig.load(V2_ROOT / "config" / "base.json")

    assert config.start_date == "1981-01-01"
    assert config.end_date == "2016-12-31"
    assert config.output_root == V2_ROOT
    assert "experimentos_v2" in str(config.output_root)
    assert "data/experimentos/" not in config.output_root.as_posix()


def test_registry_persists_immutable_config_environment_and_status(
    tmp_path: Path,
) -> None:
    config_module, registry_module = _v2_modules()
    ExperimentConfig = config_module.ExperimentConfig
    RunRegistry = registry_module.RunRegistry
    config_path = tmp_path / "base.json"
    config_path.write_text(
        json.dumps(
            {
                "start_date": "1981-01-01",
                "end_date": "2016-12-31",
                "output_root": str(tmp_path / "experimentos_v2"),
                "seed": 42,
            }
        ),
        encoding="utf-8",
    )
    config = ExperimentConfig.load(config_path)

    run_dir = RunRegistry.start_run(config, run_id="test-run")

    assert (run_dir / "config.json").exists()
    assert (run_dir / "environment.json").exists()
    assert json.loads((run_dir / "status.json").read_text(encoding="utf-8"))[
        "state"
    ] == "created"
    with pytest.raises(FileExistsError):
        RunRegistry.start_run(config, run_id="test-run")

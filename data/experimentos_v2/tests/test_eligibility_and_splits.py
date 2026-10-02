from __future__ import annotations

import sys
from pathlib import Path

V2_ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = V2_ROOT.parents[1]
sys.path.insert(0, str(V2_ROOT))

from src.dataset import audit_camels_pe, build_nested_splits, select_samples, write_protocol_artifacts


def test_effective_window_reproduces_defined_donor_and_reporting_samples() -> None:
    table = audit_camels_pe(
        PROJECT_ROOT / "data" / "CAMELS-PE",
        start_date="1981-01-01",
        end_date="2016-12-31",
    )
    donors, reporting = select_samples(table, min_coverage_pct=20.0, min_continuous_days=365)
    assert len(table) == 136
    assert len(donors) == 88
    assert len(reporting) == 46
    assert set(reporting.gauge_id).issubset(set(donors.gauge_id))
    assert (reporting.longest_complete_run_days >= 365).all()


def test_grouped_outer_and_inner_splits_never_divide_nested_groups() -> None:
    table = audit_camels_pe(
        PROJECT_ROOT / "data" / "CAMELS-PE",
        start_date="1981-01-01",
        end_date="2016-12-31",
    )
    donors, _ = select_samples(table, min_coverage_pct=20.0, min_continuous_days=365)
    assignments = build_nested_splits(donors, outer_folds=5)
    assert len(assignments) == len(donors)
    assert assignments.fold_test.nunique() == 5
    assert (assignments.groupby("nested_group_id").fold_test.nunique() == 1).all()
    for fold in range(5):
        by_group = assignments.groupby("nested_group_id")[f"split_fold_{fold}"].nunique()
        assert (by_group == 1).all()
        assert set(assignments[f"split_fold_{fold}"]) == {"train", "val", "test"}


def test_protocol_artifacts_preserve_donor_and_reporting_flags(tmp_path: Path) -> None:
    artifacts = write_protocol_artifacts(
        camels_root=PROJECT_ROOT / "data" / "CAMELS-PE",
        output_root=tmp_path,
        start_date="1981-01-01",
        end_date="2016-12-31",
        min_coverage_pct=20.0,
        min_continuous_days=365,
        outer_folds=5,
    )
    audit = artifacts["eligibility"]
    assert artifacts["eligibility_path"].exists()
    assert artifacts["splits_path"].exists()
    assert audit.donor_eligible.sum() == 88
    assert audit.reporting_eligible.sum() == 46

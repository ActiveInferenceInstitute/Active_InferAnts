"""Inventory refresh does not rewrite historical gate measurements."""

import importlib.util
import json
import re
from pathlib import Path


def test_refresh_counts_preserves_measurements_and_frozen_baseline(
    tmp_path, monkeypatch
):
    root = Path(__file__).resolve().parents[1]
    spec = importlib.util.spec_from_file_location(
        "gate_metrics", root / "scripts/docgen/gate_metrics.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    original = json.loads(
        re.search(
            r"<!-- gate-metrics-receipt\n(.*?)\n-->",
            (root / "docs/_generated/gate_metrics.md").read_text(),
            re.DOTALL,
        ).group(1)
    )
    metrics = tmp_path / "gate_metrics.md"
    metrics.write_text(module.render(original))
    monkeypatch.setattr(module, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(module, "METRICS", metrics)
    current = {**original["counts"], "tests_fast": original["counts"]["tests_fast"] + 1}
    monkeypatch.setattr(module, "counts", lambda: current)

    def forbidden_measurement():
        raise AssertionError("inventory refresh must not execute measurement arms")

    monkeypatch.setattr(module, "measure_arms", forbidden_measurement)
    monkeypatch.setattr(module, "measure_out_of_scope", forbidden_measurement)
    assert module.main(["--refresh-counts"]) == 0
    refreshed = json.loads(
        re.search(
            r"<!-- gate-metrics-receipt\n(.*?)\n-->", metrics.read_text(), re.DOTALL
        ).group(1)
    )
    assert refreshed["counts"] == current
    assert refreshed["inventory_recorded"] == module.date.today().isoformat()
    for key, value in original.items():
        if key not in {"counts", "inventory_recorded"}:
            assert refreshed[key] == value

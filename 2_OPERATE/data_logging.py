"""Data logging for the 2_OPERATE simulation pipeline.

``DataLogger`` records per-step simulation state and writes results as JSON.
The class name and method surface match the pipeline contract used by
``plan_Simulation.py`` and ``execute_Simulation.py``.
"""

from __future__ import annotations

import json
import logging
import os
from typing import Any

logger = logging.getLogger(__name__)


class DataLogger:
    """Collects and persists simulation data.

    Parameters
    ----------
    output_dir:
        Directory where result files are written. Created if missing.
    """

    def __init__(self, output_dir: str = "simulation_output") -> None:
        self.output_dir = output_dir
        self.records: list[dict[str, Any]] = []
        self.simulation: Any = None
        os.makedirs(self.output_dir, exist_ok=True)

    def initialize(self, simulation: Any) -> None:
        """Attach the simulation and reset any previous records."""
        self.simulation = simulation
        self.records = []
        logger.debug("DataLogger initialized for simulation %s", type(simulation).__name__)

    def log_step(self, step: int, simulation: Any) -> None:
        """Record a per-step snapshot."""
        record: dict[str, Any] = {"step": int(step)}
        if simulation is not None:
            results = getattr(simulation, "aggregate_results", None)
            if callable(results):
                record.update({"step_metrics": results()})
        self.records.append(record)

    def save_results(self, results: dict[str, Any]) -> str:
        """Persist a results dictionary to JSON and return the file path."""
        path = os.path.join(self.output_dir, "results.json")
        with open(path, "w") as fh:
            json.dump(_json_safe(results), fh, indent=2)
        logger.info("Results saved to %s", path)
        return path

    def save_multiple_results(self, all_results: list[dict[str, Any]]) -> str:
        """Persist a list of results (multiple simulations) to JSON."""
        path = os.path.join(self.output_dir, "results_all.json")
        with open(path, "w") as fh:
            json.dump([_json_safe(r) for r in all_results], fh, indent=2)
        logger.info("Aggregated results saved to %s", path)
        return path

    def generate_report(self) -> dict[str, Any]:
        """Return a report dictionary of everything recorded."""
        return {"records": self.records, "result_count": len(self.records)}

    def finalize(self) -> None:
        """Flush any remaining state (no-op for the file-backed logger)."""
        logger.debug("DataLogger finalized with %d records", len(self.records))


def _json_safe(value: Any) -> Any:
    """Convert numpy values / nested structures to JSON-safe Python objects."""
    if isinstance(value, dict):
        return {str(k): _json_safe(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_json_safe(v) for v in value]
    if hasattr(value, "item"):  # numpy scalars / arrays
        try:
            return value.item()
        except ValueError:
            return [_json_safe(v) for v in value.tolist()]
    return value

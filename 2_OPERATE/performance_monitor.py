"""Runtime performance monitoring for the 2_OPERATE simulation pipeline.

``PerformanceMonitor`` tracks wall-clock timing and offers a parameter
adjustment hook used by ``execute_Simulation.py``. The class name and method
surface match the pipeline contract.
"""

from __future__ import annotations

import logging
import time
from typing import Any

logger = logging.getLogger(__name__)


class PerformanceMonitor:
    """Tracks execution timing and decides when parameters should adapt.

    Parameters
    ----------
    adjustment_interval:
        How often (in steps) to offer a parameter adjustment. ``None``
        disables adjustments.
    """

    def __init__(self, adjustment_interval: int = 100) -> None:
        self.adjustment_interval = adjustment_interval
        self._start_time: float | None = None
        self._end_time: float | None = None
        self.steps_monitored = 0

    def start(self) -> None:
        """Start the monitoring window."""
        self._start_time = time.monotonic()
        self._end_time = None
        logger.debug("PerformanceMonitor started")

    def stop(self) -> None:
        """Stop the monitoring window."""
        self._end_time = time.monotonic()
        logger.debug("PerformanceMonitor stopped")

    def should_adjust_parameters(self, step: int) -> bool:
        """Return True when a parameter-adjustment checkpoint is due."""
        self.steps_monitored = max(self.steps_monitored, int(step) + 1)
        if self.adjustment_interval is None or self.adjustment_interval <= 0:
            return False
        return int(step) > 0 and int(step) % self.adjustment_interval == 0

    def suggest_parameter_adjustments(self) -> dict[str, Any]:
        """Return a suggested parameter update (empty by default).

        Subclasses / integrations may override this to implement adaptive
        behaviour; the pipeline treats the result as an optional update.
        """
        return {}

    def get_metrics(self) -> dict[str, Any]:
        """Return the accumulated performance metrics."""
        elapsed = None
        if self._start_time is not None:
            end = self._end_time if self._end_time is not None else time.monotonic()
            elapsed = end - self._start_time
        return {
            "elapsed_seconds": elapsed,
            "steps_monitored": self.steps_monitored,
        }

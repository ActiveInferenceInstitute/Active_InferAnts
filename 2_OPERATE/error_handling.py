"""Error handling for the 2_OPERATE simulation pipeline.

``SimulationError`` is the pipeline's domain exception, and
``handle_simulation_error`` is the centralized handler used by
``execute_Simulation.py``.
"""

from __future__ import annotations

import logging
from typing import Any

logger = logging.getLogger(__name__)


class SimulationError(Exception):
    """Raised when a simulation step or component fails."""


def handle_simulation_error(error: Exception, context: str = "Simulation") -> Any:
    """Log and re-raise a simulation error with pipeline context.

    Parameters
    ----------
    error:
        The underlying exception.
    context:
        A human-readable description of where the failure occurred.

    Raises
    ------
    SimulationError
        Always re-raised (the original exception is chained).
    """
    logger.error("%s failed: %s", context, error, exc_info=True)
    raise SimulationError(f"{context} failed: {error}") from error

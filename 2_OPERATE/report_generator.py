"""Report generation for the 2_OPERATE simulation pipeline.

``ReportGenerator`` renders a plain-text report from a results dictionary.
The class name and method surface match the contract used by
``execute_Simulation.py``.
"""

from __future__ import annotations

import logging
from typing import Any

logger = logging.getLogger(__name__)


class ReportGenerator:
    """Generates human-readable text reports from simulation data."""

    def generate_report(self, data: dict[str, Any]) -> str:
        """Render ``data`` as a formatted text report."""
        lines: list[str] = ["Active InferAnts — Simulation Report", "=" * 40]
        for section, payload in data.items():
            lines.append("")
            lines.append(f"[{section}]")
            if isinstance(payload, dict):
                for key, value in payload.items():
                    lines.append(f"  {key}: {value}")
            else:
                lines.append(f"  {payload}")
        report = "\n".join(lines)
        logger.debug("Report generated (%d chars)", len(report))
        return report

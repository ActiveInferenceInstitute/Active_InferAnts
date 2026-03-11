# AGENTS.md — Reporting & Communication

> Agent guidance for the `4_REPORT` directory within the Active InferAnts framework.

## Purpose

Report generation, specification, and communication of results. This phase transforms measured outcomes into structured reports.

## Directory Contents

- 📄 `specify_report.py` — `DataSourceType` enum + report specification dataclasses: defines report structure, data sources, and JSON serialization with UUID tracking
- 📄 `execute_report.py` — `ReportExecutor` class: async report generation with `asyncio`, logging, and multi-format output

## Agent Instructions

- Maintain report specification schema consistency with `3_MEASURE` output types (`MeasurementMethod`, `QRFParameters`).
- Ensure `specify_report.py` `DataSourceType` enum matches actual available data sources.
- Preserve async execution patterns in `ReportExecutor`.
- Track report output formats and their consumers in `5_FOLLOWUP`.
- Follow the repository's CC BY-NC-ND 4.0 license.
- Keep all documentation synchronized with actual contents.

## Quality Checklist

- [ ] All files documented and up-to-date
- [ ] Report schema matches 3_MEASURE outputs
- [ ] README.md and SPEC.md synchronized with this AGENTS.md

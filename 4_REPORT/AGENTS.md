# AGENTS.md — Reporting & Communication

> Agent guidance for the `4_REPORT` directory within the Active InferAnts framework.

## Purpose

Report specifications and asynchronous orchestration. End-to-end execution
requires real collection, analysis, generation, delivery and error providers;
those implementations are not included here. The contract requires
`DataCollector`, `DataAnalyzer`, `ReportGenerator`, `ReportDeliverer`,
reporting-specific errors and qualified dependencies/configuration.

## Directory Contents

- 📄 `specify_report.py` — `DataSourceType` enum + report specification dataclasses: defines report structure, data sources, and JSON serialization with UUID tracking
- `execute_report.py` — `ReportExecutor`: provider-dependent asynchronous orchestration, not a standalone reporting CLI.

## Agent Instructions

- Maintain report specification schema consistency with `3_MEASURE` output types (`MeasurementMethod`, `QRFParameters`).
- Treat `DataSourceType` as specification vocabulary, not provider availability.
- Preserve asynchronous provider orchestration while consuming synchronous
  `ReportSpecification.validate()`. Require real provider ownership and explicit
  integration acceptance; no success substitutes or unrelated phase modules.
- Track report output formats and their consumers in `5_FOLLOWUP`.
- Follow the repository's CC BY-NC-ND 4.0 license.
- Keep all documentation synchronized with actual contents.

## Quality Checklist

- [ ] All files documented and up-to-date
- [ ] Report schema matches 3_MEASURE outputs
- [ ] README.md and SPEC.md synchronized with this AGENTS.md
- [ ] Provider-dependent execution and missing provider/dependency requirements are explicit.

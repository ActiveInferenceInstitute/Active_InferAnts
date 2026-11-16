# Reporting & Communication

Report specifications and asynchronous reporting orchestration. End-to-end
execution requires real collection, analysis, generation, delivery and error
providers; those implementations are not included here.

## Modules

| Module | Description |
|---|---|
| `specify_report.py` | `DataSourceType` enum + report specification dataclasses — defines report structure, sources, and JSON serialization with UUID tracking |
| `execute_report.py` | `ReportExecutor`: provider-dependent asynchronous orchestration, not a standalone reporting CLI |

The reporting contract requires `DataCollector`, `DataAnalyzer`,
`ReportGenerator`, `ReportDeliverer`, reporting-specific error types, and
qualified dependencies/configuration. Specification enums and synchronous
validation do not establish provider availability. Do not add success stubs
or substitute unrelated phase modules.

## Pipeline Position

```
3_MEASURE → [4_REPORT] → 5_FOLLOWUP
```

- **Intended input**: Measured summaries and metrics.
- **Intended provider-dependent output**: Formatted stakeholder reports and subsequent follow-up.

## Related

- Parent: [Active InferAnts](../README.md)
- Previous phase: [3_MEASURE](../3_MEASURE/README.md)
- Next phase: [5_FOLLOWUP](../5_FOLLOWUP/README.md)

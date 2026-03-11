# Reporting & Communication

Report generation, specification, and communication of results. This phase transforms measured outcomes into structured reports.

## Modules

| Module | Description |
|---|---|
| `specify_report.py` | `DataSourceType` enum + report specification dataclasses — defines report structure, sources, and JSON serialization with UUID tracking |
| `execute_report.py` | `ReportExecutor` class — async report generation with `asyncio`, logging, and multi-format output |

## Pipeline Position

```
3_MEASURE → [4_REPORT] → 5_FOLLOWUP
```

- **Input**: Statistical summaries, categorized results, and metrics from `3_MEASURE`
- **Output**: Formatted reports for stakeholder communication, consumed by `5_FOLLOWUP`

## Related

- Parent: [Active InferAnts](../README.md)
- Previous phase: [3_MEASURE](../3_MEASURE/README.md)
- Next phase: [5_FOLLOWUP](../5_FOLLOWUP/README.md)

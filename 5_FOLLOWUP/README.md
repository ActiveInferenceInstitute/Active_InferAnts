# Continuous Improvement

Follow-up actions, continuous improvement planning, and iterative refinement. This phase closes the loop between reporting and future operations.

## Modules

| Module | Description |
|---|---|
| `specify_followup.py` | `FollowUpType`, `SessionType`, `UpdateArea` enums; `Session`, `Stakeholder`, `Resource` dataclasses; `TextReportGenerator` and `HTMLReportGenerator` classes |
| `execute_followup.py` | `FollowUpExecutor` class — orchestrates full follow-up workflow integrating 7 services: `EmailService`, `ProjectManager`, `MetricsAnalyzer`, `ResourceAllocator`, `NotificationService`, `DatabaseService`, `TaskScheduler` |

## Pipeline Position

```
4_REPORT → [5_FOLLOWUP] → 6_API
```

- **Input**: Generated reports from `4_REPORT`
- **Output**: Action items, session plans, and stakeholder communications; feeds back into `1_PREPARE`

## Related

- Parent: [Active InferAnts](../README.md)
- Previous phase: [4_REPORT](../4_REPORT/README.md)
- Next phase: [6_API](../6_API/README.md)

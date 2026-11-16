# Continuous Improvement

Follow-up specifications, local text/HTML formatting and provider-dependent
orchestration. Service-backed execution requires real providers not included here.

## Modules

| Module | Description |
|---|---|
| `specify_followup.py` | `FollowUpType`, `SessionType`, `SessionModality`; `UpdateArea`, `Session`, `Stakeholder`, `Resource`; `FollowUpSpecification` and local text/HTML formatters |
| `execute_followup.py` | `FollowUpExecutor` requires seven service providers plus `ErrorHandler`; these are not bundled integrations |

Execution requires `EmailService`, `ProjectManager`, `MetricsAnalyzer`,
`ResourceAllocator`, `NotificationService`, `DatabaseService`, `TaskScheduler`
and `ErrorHandler`. Provider ownership, dependencies, configuration, effects
and acceptance must be supplied explicitly.

`SessionType` describes purpose; required `SessionModality` describes `VIRTUAL`
or `IN_PERSON` delivery. Updates use `UpdateArea.notes`. Canonical JSON stores
enum names, duration seconds, ISO timestamps and nullable dates; import restores
declared typed fields. Historical `default=str` artifacts are not automatically
rewritten or heuristically migrated.

Handled component failures prevent successful finalization. Local finalization
records actual specification state and a local UTC timestamp; it does not invent
external persistence or notification effects.

## Pipeline Position

```
4_REPORT → [5_FOLLOWUP] → 6_API
```

- **Intended input**: Report outcomes/follow-up specifications.
- **Intended provider-dependent output**: Action items, sessions, stakeholder communications and feedback.

## Related

- Parent: [Active InferAnts](../README.md)
- Previous phase: [4_REPORT](../4_REPORT/README.md)
- Next phase: [6_API](../6_API/README.md)

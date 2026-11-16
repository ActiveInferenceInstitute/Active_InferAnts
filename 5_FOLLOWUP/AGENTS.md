# AGENTS.md — Continuous Improvement

> Agent guidance for the `5_FOLLOWUP` directory within the Active InferAnts framework.

## Purpose

Follow-up specifications, local text/HTML formatting and provider-dependent
orchestration. Service-backed execution requires real providers not included here.

## Directory Contents

- `specify_followup.py` — `FollowUpType`, `SessionType`, `SessionModality` enums;
  `UpdateArea`, `Session`, `Stakeholder`, `Resource` dataclasses;
  `FollowUpSpecification` and local text/HTML formatters.
- `execute_followup.py` — `FollowUpExecutor`: provider-dependent orchestration
  requiring `EmailService`, `ProjectManager`, `MetricsAnalyzer`,
  `ResourceAllocator`, `NotificationService`, `DatabaseService`,
  `TaskScheduler` and `ErrorHandler`.

## Agent Instructions

- Maintain declared specification and typed serialization contracts.
- Verify service-backed orchestration only with real configured providers and
  explicit acceptance; service names alone do not establish availability.
  Distinguish local formatting/finalization from external effects.
- Preserve the session lifecycle: prepare → run → post-session tasks → status update.
- Track the feedback loop: follow-up outputs should inform future `1_PREPARE` configurations.
- Follow the repository's CC BY-NC-ND 4.0 license.
- Keep all documentation synchronized with actual contents.

## Quality Checklist

- [ ] All files documented and up-to-date
- [ ] Provider-dependent execution is explicitly distinguished from local specification/report formatting.
- [ ] README.md and SPEC.md synchronized with this AGENTS.md

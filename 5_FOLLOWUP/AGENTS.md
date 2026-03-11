# AGENTS.md — Continuous Improvement

> Agent guidance for the `5_FOLLOWUP` directory within the Active InferAnts framework.

## Purpose

Follow-up actions, continuous improvement planning, and iterative refinement. This phase closes the loop between reporting and future operations.

## Directory Contents

- 📄 `specify_followup.py` — Follow-up specification types: `FollowUpType`, `SessionType`, `UpdateArea` enums; `Session`, `Stakeholder`, `Resource` dataclasses; `TextReportGenerator` and `HTMLReportGenerator` classes
- 📄 `execute_followup.py` — `FollowUpExecutor` class: orchestrates full follow-up workflow integrating 7 services — `EmailService`, `ProjectManager`, `MetricsAnalyzer`, `ResourceAllocator`, `NotificationService`, `DatabaseService`, `TaskScheduler`

## Agent Instructions

- Maintain the `FollowUpSpecification` dataclass hierarchy in `specify_followup.py`.
- Ensure `FollowUpExecutor` correctly consumes all specification types and orchestrates all 7 services.
- Preserve the session lifecycle: prepare → run → post-session tasks → status update.
- Track the feedback loop: follow-up outputs should inform future `1_PREPARE` configurations.
- Follow the repository's CC BY-NC-ND 4.0 license.
- Keep all documentation synchronized with actual contents.

## Quality Checklist

- [ ] All files documented and up-to-date
- [ ] All 7 service integrations verified
- [ ] README.md and SPEC.md synchronized with this AGENTS.md

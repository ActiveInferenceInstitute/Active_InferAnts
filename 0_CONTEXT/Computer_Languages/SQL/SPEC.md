# SPEC.md — Active Inference in SQL

> Technical specification for `0_CONTEXT/Computer_Languages/SQL` within the Active InferAnts framework.

## Overview

SQL — declarative database query implementation

## Structure

- 📄 `AGENTS.md`
- 📄 `README.md`
- 📄 `SKILL.md`
- 📄 `SQL.sql`
- 📄 `run.sh`

## Interfaces

- **Input**: Active Inference parameters (state space, observation model, transition model)
- **Output**: Inference results (beliefs, policies, free energy values)
- **API**: Language-specific API consistent with the cross-language Active Inference interface
- **Testing**: Validated via `master_controller.py test sql`

## Dependencies

- SQL compiler/interpreter (see language-specific README)
- Active Inference mathematical libraries for SQL
- Visualization libraries (where applicable)

## Version

- **Framework**: Active InferAnts
- **License**: CC BY-NC-ND 4.0

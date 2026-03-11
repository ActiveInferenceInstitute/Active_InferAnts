# SPEC.md — Active Inference in TypeScript

> Technical specification for `0_CONTEXT/Computer_Languages/TypeScript` within the Active InferAnts framework.

## Overview

TypeScript — type-safe JavaScript implementation

## Structure

- 📁 `src/`
- 📄 `AGENTS.md`
- 📄 `README.md`
- 📄 `SKILL.md`
- 📄 `package.json`
- 📄 `run.sh`
- 📄 `tsconfig.json`

## Interfaces

- **Input**: Active Inference parameters (state space, observation model, transition model)
- **Output**: Inference results (beliefs, policies, free energy values)
- **API**: Language-specific API consistent with the cross-language Active Inference interface
- **Testing**: Validated via `master_controller.py test typescript`

## Dependencies

- TypeScript compiler/interpreter (see language-specific README)
- Active Inference mathematical libraries for TypeScript
- Visualization libraries (where applicable)

## Version

- **Framework**: Active InferAnts
- **License**: CC BY-NC-ND 4.0

# SPEC.md — Active Inference in Kotlin

> Technical specification for `0_CONTEXT/Computer_Languages/Kotlin` within the Active InferAnts framework.

## Overview

Kotlin — modern JVM language implementation

## Structure

- 📁 `src/`
- 📄 `AGENTS.md`
- 📄 `README.md`
- 📄 `build.gradle.kts`
- 📄 `run.sh`

## Interfaces

- **Input**: Active Inference parameters (state space, observation model, transition model)
- **Output**: Inference results (beliefs, policies, free energy values)
- **API**: Language-specific API consistent with the cross-language Active Inference interface
- **Testing**: Validated via `master_controller.py test kotlin`

## Dependencies

- Kotlin compiler/interpreter (see language-specific README)
- Active Inference mathematical libraries for Kotlin
- Visualization libraries (where applicable)

## Version

- **Framework**: Active InferAnts
- **License**: CC BY-NC-ND 4.0

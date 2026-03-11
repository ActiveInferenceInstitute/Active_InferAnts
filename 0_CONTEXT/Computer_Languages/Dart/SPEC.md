# SPEC.md — Active Inference in Dart

> Technical specification for `0_CONTEXT/Computer_Languages/Dart` within the Active InferAnts framework.

## Overview

Dart — scripting implementation

## Structure

- 📄 `AGENTS.md`
- 📄 `README.md`
- 📄 `SKILL.md`
- 📄 `active_inference.dart`
- 📄 `run.sh`

## Interfaces

- **Input**: Active Inference parameters (state space, observation model, transition model)
- **Output**: Inference results (beliefs, policies, free energy values)
- **API**: Language-specific API consistent with the cross-language Active Inference interface
- **Testing**: Validated via `master_controller.py test dart`

## Dependencies

- Dart interpreter (see language-specific README)
- Active Inference mathematical libraries for Dart
- Visualization libraries (where applicable)

## Version

- **Framework**: Active InferAnts
- **License**: CC BY-NC-ND 4.0

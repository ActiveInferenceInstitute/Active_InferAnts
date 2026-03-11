# SPEC.md — Active Inference in Objective-C

> Technical specification for `0_CONTEXT/Computer_Languages/ObjectiveC` within the Active InferAnts framework.

## Overview

Objective-C — systems compiled implementation

## Structure

- 📄 `AGENTS.md`
- 📄 `README.md`
- 📄 `SKILL.md`
- 📄 `active_inference.m`
- 📄 `run.sh`

## Interfaces

- **Input**: Active Inference parameters (state space, observation model, transition model)
- **Output**: Inference results (beliefs, policies, free energy values)
- **API**: Language-specific API consistent with the cross-language Active Inference interface
- **Testing**: Validated via `master_controller.py test objectivec`

## Dependencies

- Objective-C compiler (see language-specific README)
- Active Inference mathematical libraries for Objective-C
- Visualization libraries (where applicable)

## Version

- **Framework**: Active InferAnts
- **License**: CC BY-NC-ND 4.0

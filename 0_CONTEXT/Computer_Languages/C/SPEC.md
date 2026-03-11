# SPEC.md — Active Inference in C

> Technical specification for `0_CONTEXT/Computer_Languages/C` within the Active InferAnts framework.

## Overview

C — systems-level implementation for maximum performance

## Structure

- 📄 `AGENTS.md`
- 📄 `Active_Inference.c`
- 📄 `README.md`
- 📄 `active_inference`
- 📄 `run.sh`
- 📄 `teacher_model.c`

## Interfaces

- **Input**: Active Inference parameters (state space, observation model, transition model)
- **Output**: Inference results (beliefs, policies, free energy values)
- **API**: Language-specific API consistent with the cross-language Active Inference interface
- **Testing**: Validated via `master_controller.py test c`

## Dependencies

- C compiler/interpreter (see language-specific README)
- Active Inference mathematical libraries for C
- Visualization libraries (where applicable)

## Version

- **Framework**: Active InferAnts
- **License**: CC BY-NC-ND 4.0

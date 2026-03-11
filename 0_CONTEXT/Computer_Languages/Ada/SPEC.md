# SPEC.md — Active Inference in Ada

> Technical specification for `0_CONTEXT/Computer_Languages/Ada` within the Active InferAnts framework.

## Overview

Ada — safety-critical systems language with strong typing

## Structure

- 📄 `AGENTS.md`
- 📄 `README.md`
- 📄 `active_inference.adb`
- 📄 `active_inference.ads`
- 📄 `demo.adb`
- 📄 `run.sh`

## Interfaces

- **Input**: Active Inference parameters (state space, observation model, transition model)
- **Output**: Inference results (beliefs, policies, free energy values)
- **API**: Language-specific API consistent with the cross-language Active Inference interface
- **Testing**: Validated via `master_controller.py test ada`

## Dependencies

- Ada compiler/interpreter (see language-specific README)
- Active Inference mathematical libraries for Ada
- Visualization libraries (where applicable)

## Version

- **Framework**: Active InferAnts
- **License**: CC BY-NC-ND 4.0

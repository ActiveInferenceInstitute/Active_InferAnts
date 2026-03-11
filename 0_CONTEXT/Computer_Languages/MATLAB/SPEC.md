# SPEC.md — Active Inference in MATLAB

> Technical specification for `0_CONTEXT/Computer_Languages/MATLAB` within the Active InferAnts framework.

## Overview

MATLAB — numerical computing and matrix operations

## Structure

- 📄 `AGENTS.md`
- 📄 `ActiveInferenceAgent.m`
- 📄 `README.md`
- 📄 `SKILL.md`
- 📄 `demo.m`
- 📄 `run.sh`

## Interfaces

- **Input**: Active Inference parameters (state space, observation model, transition model)
- **Output**: Inference results (beliefs, policies, free energy values)
- **API**: Language-specific API consistent with the cross-language Active Inference interface
- **Testing**: Validated via `master_controller.py test matlab`

## Dependencies

- MATLAB compiler/interpreter (see language-specific README)
- Active Inference mathematical libraries for MATLAB
- Visualization libraries (where applicable)

## Version

- **Framework**: Active InferAnts
- **License**: CC BY-NC-ND 4.0

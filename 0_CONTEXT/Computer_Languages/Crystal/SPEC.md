# SPEC.md — Active Inference in Crystal

> Technical specification for `0_CONTEXT/Computer_Languages/Crystal` within the Active InferAnts framework.

## Overview

Crystal — Ruby-like syntax with compiled performance

## Structure

- 📄 `AGENTS.md`
- 📄 `README.md`
- 📄 `SKILL.md`
- 📄 `active_inference.cr`
- 📄 `run.sh`

## Interfaces

- **Input**: Active Inference parameters (state space, observation model, transition model)
- **Output**: Inference results (beliefs, policies, free energy values)
- **API**: Language-specific API consistent with the cross-language Active Inference interface
- **Testing**: Validated via `master_controller.py test crystal`

## Dependencies

- Crystal compiler/interpreter (see language-specific README)
- Active Inference mathematical libraries for Crystal
- Visualization libraries (where applicable)

## Version

- **Framework**: Active InferAnts
- **License**: CC BY-NC-ND 4.0

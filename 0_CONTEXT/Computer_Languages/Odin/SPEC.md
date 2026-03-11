# SPEC.md — Active Inference in Odin

> Technical specification for `0_CONTEXT/Computer_Languages/Odin` within the Active InferAnts framework.

## Overview

Odin — systems programming language implementation

## Structure

- 📄 `AGENTS.md`
- 📄 `README.md`
- 📄 `SKILL.md`
- 📄 `active_inference.odin`
- 📄 `run.sh`

## Interfaces

- **Input**: Active Inference parameters (state space, observation model, transition model)
- **Output**: Inference results (beliefs, policies, free energy values)
- **API**: Language-specific API consistent with the cross-language Active Inference interface
- **Testing**: Validated via `master_controller.py test odin`

## Dependencies

- Odin compiler/interpreter (see language-specific README)
- Active Inference mathematical libraries for Odin
- Visualization libraries (where applicable)

## Version

- **Framework**: Active InferAnts
- **License**: CC BY-NC-ND 4.0

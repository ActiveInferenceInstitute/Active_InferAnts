# SPEC.md — Active Inference in V

> Technical specification for `0_CONTEXT/Computer_Languages/V` within the Active InferAnts framework.

## Overview

V — simple, fast compiled language implementation

## Structure

- 📄 `AGENTS.md`
- 📄 `README.md`
- 📄 `SKILL.md`
- 📄 `active_inference.v`
- 📄 `run.sh`

## Interfaces

- **Input**: Active Inference parameters (state space, observation model, transition model)
- **Output**: Inference results (beliefs, policies, free energy values)
- **API**: Language-specific API consistent with the cross-language Active Inference interface
- **Testing**: Validated via `master_controller.py test v`

## Dependencies

- V compiler/interpreter (see language-specific README)
- Active Inference mathematical libraries for V
- Visualization libraries (where applicable)

## Version

- **Framework**: Active InferAnts
- **License**: CC BY-NC-ND 4.0

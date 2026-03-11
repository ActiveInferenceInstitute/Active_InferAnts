# SPEC.md — Active Inference in Jock

> Technical specification for `0_CONTEXT/Computer_Languages/Jock` within the Active InferAnts framework.

## Overview

Jock — experimental language implementation

## Structure

- 📄 `AGENTS.md`
- 📄 `Active_Jockference.md`
- 📄 `Jock_Documentation.md`
- 📄 `README.md`
- 📄 `SKILL.md`
- 📄 `Urbit_Active_Jockference.md`
- 📄 `active_inference.jock`
- 📄 `run.sh`

## Interfaces

- **Input**: Active Inference parameters (state space, observation model, transition model)
- **Output**: Inference results (beliefs, policies, free energy values)
- **API**: Language-specific API consistent with the cross-language Active Inference interface
- **Testing**: Validated via `master_controller.py test jock`

## Dependencies

- Jock compiler/interpreter (see language-specific README)
- Active Inference mathematical libraries for Jock
- Visualization libraries (where applicable)

## Version

- **Framework**: Active InferAnts
- **License**: CC BY-NC-ND 4.0

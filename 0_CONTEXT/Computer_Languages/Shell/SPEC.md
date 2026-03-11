# SPEC.md — Active Inference in Shell

> Technical specification for `0_CONTEXT/Computer_Languages/Shell` within the Active InferAnts framework.

## Overview

Shell — Unix scripting implementation

## Structure

- 📄 `AGENTS.md`
- 📄 `Active_Shellference.sh`
- 📄 `README.md`
- 📄 `SKILL.md`
- 📄 `config.sh`
- 📄 `run.sh`

## Interfaces

- **Input**: Active Inference parameters (state space, observation model, transition model)
- **Output**: Inference results (beliefs, policies, free energy values)
- **API**: Language-specific API consistent with the cross-language Active Inference interface
- **Testing**: Validated via `master_controller.py test shell`

## Dependencies

- Shell compiler/interpreter (see language-specific README)
- Active Inference mathematical libraries for Shell
- Visualization libraries (where applicable)

## Version

- **Framework**: Active InferAnts
- **License**: CC BY-NC-ND 4.0

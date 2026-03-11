# SPEC.md — Active Inference in COBOL

> Technical specification for `0_CONTEXT/Computer_Languages/COBOL` within the Active InferAnts framework.

## Overview

COBOL — legacy compiled implementation

## Structure

- 📄 `AGENTS.md`
- 📄 `README.md`
- 📄 `SKILL.md`
- 📄 `active_inference.cob`
- 📄 `run.sh`

## Interfaces

- **Input**: Active Inference parameters (state space, observation model, transition model)
- **Output**: Inference results (beliefs, policies, free energy values)
- **API**: Language-specific API consistent with the cross-language Active Inference interface
- **Testing**: Validated via `master_controller.py test cobol`

## Dependencies

- COBOL compiler (see language-specific README)
- Active Inference mathematical libraries for COBOL
- Visualization libraries (where applicable)

## Version

- **Framework**: Active InferAnts
- **License**: CC BY-NC-ND 4.0

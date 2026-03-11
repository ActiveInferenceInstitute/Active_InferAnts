# SPEC.md — Active Inference in Tcl

> Technical specification for `0_CONTEXT/Computer_Languages/Tcl` within the Active InferAnts framework.

## Overview

Tcl — scripting implementation

## Structure

- 📄 `AGENTS.md`
- 📄 `README.md`
- 📄 `SKILL.md`
- 📄 `active_inference.tcl`
- 📄 `run.sh`

## Interfaces

- **Input**: Active Inference parameters (state space, observation model, transition model)
- **Output**: Inference results (beliefs, policies, free energy values)
- **API**: Language-specific API consistent with the cross-language Active Inference interface
- **Testing**: Validated via `master_controller.py test tcl`

## Dependencies

- Tcl interpreter (see language-specific README)
- Active Inference mathematical libraries for Tcl
- Visualization libraries (where applicable)

## Version

- **Framework**: Active InferAnts
- **License**: CC BY-NC-ND 4.0

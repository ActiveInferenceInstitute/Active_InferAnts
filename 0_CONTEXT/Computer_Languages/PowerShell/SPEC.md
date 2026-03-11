# SPEC.md — Active Inference in PowerShell

> Technical specification for `0_CONTEXT/Computer_Languages/PowerShell` within the Active InferAnts framework.

## Overview

PowerShell — scripting implementation

## Structure

- 📄 `AGENTS.md`
- 📄 `README.md`
- 📄 `SKILL.md`
- 📄 `active_inference.ps1`
- 📄 `run.sh`

## Interfaces

- **Input**: Active Inference parameters (state space, observation model, transition model)
- **Output**: Inference results (beliefs, policies, free energy values)
- **API**: Language-specific API consistent with the cross-language Active Inference interface
- **Testing**: Validated via `master_controller.py test powershell`

## Dependencies

- PowerShell interpreter (see language-specific README)
- Active Inference mathematical libraries for PowerShell
- Visualization libraries (where applicable)

## Version

- **Framework**: Active InferAnts
- **License**: CC BY-NC-ND 4.0

# SPEC.md — Active Inference in FSharp

> Technical specification for `0_CONTEXT/Computer_Languages/FSharp` within the Active InferAnts framework.

## Overview

F# — functional-first .NET implementation

## Structure

- 📄 `AGENTS.md`
- 📄 `ActiveInference.fs`
- 📄 `README.md`
- 📄 `SKILL.md`
- 📄 `run.sh`

## Interfaces

- **Input**: Active Inference parameters (state space, observation model, transition model)
- **Output**: Inference results (beliefs, policies, free energy values)
- **API**: Language-specific API consistent with the cross-language Active Inference interface
- **Testing**: Validated via `master_controller.py test fsharp`

## Dependencies

- FSharp compiler/interpreter (see language-specific README)
- Active Inference mathematical libraries for FSharp
- Visualization libraries (where applicable)

## Version

- **Framework**: Active InferAnts
- **License**: CC BY-NC-ND 4.0

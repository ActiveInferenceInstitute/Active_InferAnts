# SPEC.md — Active Inference in Haskell

> Technical specification for `0_CONTEXT/Computer_Languages/Haskell` within the Active InferAnts framework.

## Overview

Haskell — purely functional implementation with strong type system

## Structure

- 📁 `app/`
- 📁 `src/`
- 📄 `AGENTS.md`
- 📄 `README.md`
- 📄 `package.yaml`
- 📄 `run.sh`

## Interfaces

- **Input**: Active Inference parameters (state space, observation model, transition model)
- **Output**: Inference results (beliefs, policies, free energy values)
- **API**: Language-specific API consistent with the cross-language Active Inference interface
- **Testing**: Validated via `master_controller.py test haskell`

## Dependencies

- Haskell compiler/interpreter (see language-specific README)
- Active Inference mathematical libraries for Haskell
- Visualization libraries (where applicable)

## Version

- **Framework**: Active InferAnts
- **License**: CC BY-NC-ND 4.0

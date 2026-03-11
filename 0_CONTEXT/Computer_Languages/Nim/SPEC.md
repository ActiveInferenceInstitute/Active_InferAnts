# SPEC.md — Active Inference in Nim

> Technical specification for `0_CONTEXT/Computer_Languages/Nim` within the Active InferAnts framework.

## Overview

Nim — efficient compiled language with Python-like syntax

## Structure

- 📄 `AGENTS.md`
- 📄 `README.md`
- 📄 `SKILL.md`
- 📄 `active_inference.nim`
- 📄 `run.sh`

## Interfaces

- **Input**: Active Inference parameters (state space, observation model, transition model)
- **Output**: Inference results (beliefs, policies, free energy values)
- **API**: Language-specific API consistent with the cross-language Active Inference interface
- **Testing**: Validated via `master_controller.py test nim`

## Dependencies

- Nim compiler/interpreter (see language-specific README)
- Active Inference mathematical libraries for Nim
- Visualization libraries (where applicable)

## Version

- **Framework**: Active InferAnts
- **License**: CC BY-NC-ND 4.0

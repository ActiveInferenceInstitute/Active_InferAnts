# SPEC.md — Active Inference in Lua

> Technical specification for `0_CONTEXT/Computer_Languages/Lua` within the Active InferAnts framework.

## Overview

Lua — lightweight embeddable scripting implementation

## Structure

- 📄 `AGENTS.md`
- 📄 `README.md`
- 📄 `SKILL.md`
- 📄 `active_inference.lua`
- 📄 `run.sh`

## Interfaces

- **Input**: Active Inference parameters (state space, observation model, transition model)
- **Output**: Inference results (beliefs, policies, free energy values)
- **API**: Language-specific API consistent with the cross-language Active Inference interface
- **Testing**: Validated via `master_controller.py test lua`

## Dependencies

- Lua compiler/interpreter (see language-specific README)
- Active Inference mathematical libraries for Lua
- Visualization libraries (where applicable)

## Version

- **Framework**: Active InferAnts
- **License**: CC BY-NC-ND 4.0

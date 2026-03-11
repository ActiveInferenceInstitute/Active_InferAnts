# SPEC.md — Active Inference in Assembly

> Technical specification for `0_CONTEXT/Computer_Languages/Assembly` within the Active InferAnts framework.

## Overview

Assembly — low-level machine-code implementations

## Structure

- 📄 `AGENTS.md`
- 📄 `README.md`
- 📄 `SKILL.md`
- 📄 `active_inference.asm`
- 📄 `run.sh`

## Interfaces

- **Input**: Active Inference parameters (state space, observation model, transition model)
- **Output**: Inference results (beliefs, policies, free energy values)
- **API**: Language-specific API consistent with the cross-language Active Inference interface
- **Testing**: Validated via `master_controller.py test assembly`

## Dependencies

- Assembly compiler/interpreter (see language-specific README)
- Active Inference mathematical libraries for Assembly
- Visualization libraries (where applicable)

## Version

- **Framework**: Active InferAnts
- **License**: CC BY-NC-ND 4.0

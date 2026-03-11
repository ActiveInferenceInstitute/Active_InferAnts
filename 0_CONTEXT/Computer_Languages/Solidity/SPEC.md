# SPEC.md — Active Inference in Solidity

> Technical specification for `0_CONTEXT/Computer_Languages/Solidity` within the Active InferAnts framework.

## Overview

Solidity — blockchain compiled implementation

## Structure

- 📄 `AGENTS.md`
- 📄 `ActiveInference.sol`
- 📄 `README.md`
- 📄 `SKILL.md`
- 📄 `run.sh`

## Interfaces

- **Input**: Active Inference parameters (state space, observation model, transition model)
- **Output**: Inference results (beliefs, policies, free energy values)
- **API**: Language-specific API consistent with the cross-language Active Inference interface
- **Testing**: Validated via `master_controller.py test solidity`

## Dependencies

- Solidity compiler (see language-specific README)
- Active Inference mathematical libraries for Solidity
- Visualization libraries (where applicable)

## Version

- **Framework**: Active InferAnts
- **License**: CC BY-NC-ND 4.0

# SPEC.md — Active Inference in Ruby

> Technical specification for `0_CONTEXT/Computer_Languages/Ruby` within the Active InferAnts framework.

## Overview

Ruby — dynamic, expressive implementation

## Structure

- 📄 `AGENTS.md`
- 📄 `README.md`
- 📄 `SKILL.md`
- 📄 `active_inference_agent.rb`
- 📄 `run.sh`

## Interfaces

- **Input**: Active Inference parameters (state space, observation model, transition model)
- **Output**: Inference results (beliefs, policies, free energy values)
- **API**: Language-specific API consistent with the cross-language Active Inference interface
- **Testing**: Validated via `master_controller.py test ruby`

## Dependencies

- Ruby compiler/interpreter (see language-specific README)
- Active Inference mathematical libraries for Ruby
- Visualization libraries (where applicable)

## Version

- **Framework**: Active InferAnts
- **License**: CC BY-NC-ND 4.0

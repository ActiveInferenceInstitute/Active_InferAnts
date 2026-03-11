# SPEC.md — Active Inference in Erlang

> Technical specification for `0_CONTEXT/Computer_Languages/Erlang` within the Active InferAnts framework.

## Overview

Erlang — distributed systems implementation on BEAM VM

## Structure

- 📄 `AGENTS.md`
- 📄 `README.md`
- 📄 `SKILL.md`
- 📄 `active_inference.erl`
- 📄 `run.sh`

## Interfaces

- **Input**: Active Inference parameters (state space, observation model, transition model)
- **Output**: Inference results (beliefs, policies, free energy values)
- **API**: Language-specific API consistent with the cross-language Active Inference interface
- **Testing**: Validated via `master_controller.py test erlang`

## Dependencies

- Erlang compiler/interpreter (see language-specific README)
- Active Inference mathematical libraries for Erlang
- Visualization libraries (where applicable)

## Version

- **Framework**: Active InferAnts
- **License**: CC BY-NC-ND 4.0

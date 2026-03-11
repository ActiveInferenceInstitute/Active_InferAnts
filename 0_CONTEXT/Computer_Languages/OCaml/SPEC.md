# SPEC.md — Active Inference in OCaml

> Technical specification for `0_CONTEXT/Computer_Languages/OCaml` within the Active InferAnts framework.

## Overview

OCaml — strongly-typed functional programming implementation

## Structure

- 📄 `AGENTS.md`
- 📄 `README.md`
- 📄 `SKILL.md`
- 📄 `active_inference.ml`
- 📄 `run.sh`

## Interfaces

- **Input**: Active Inference parameters (state space, observation model, transition model)
- **Output**: Inference results (beliefs, policies, free energy values)
- **API**: Language-specific API consistent with the cross-language Active Inference interface
- **Testing**: Validated via `master_controller.py test ocaml`

## Dependencies

- OCaml compiler/interpreter (see language-specific README)
- Active Inference mathematical libraries for OCaml
- Visualization libraries (where applicable)

## Version

- **Framework**: Active InferAnts
- **License**: CC BY-NC-ND 4.0

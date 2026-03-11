# SPEC.md — Active Inference in Golang

> Technical specification for `0_CONTEXT/Computer_Languages/Golang` within the Active InferAnts framework.

## Overview

Go — concurrent, statically-typed implementation

## Structure

- 📄 `AGENTS.md`
- 📄 `GoLang_Agent.go`
- 📄 `GoLang_Description.md`
- 📄 `GoLang_Thing.go`
- 📄 `README.md`
- 📄 `run.sh`

## Interfaces

- **Input**: Active Inference parameters (state space, observation model, transition model)
- **Output**: Inference results (beliefs, policies, free energy values)
- **API**: Language-specific API consistent with the cross-language Active Inference interface
- **Testing**: Validated via `master_controller.py test golang`

## Dependencies

- Golang compiler/interpreter (see language-specific README)
- Active Inference mathematical libraries for Golang
- Visualization libraries (where applicable)

## Version

- **Framework**: Active InferAnts
- **License**: CC BY-NC-ND 4.0

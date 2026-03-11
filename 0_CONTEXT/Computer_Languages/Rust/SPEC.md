# SPEC.md — Active Inference in Rust

> Technical specification for `0_CONTEXT/Computer_Languages/Rust` within the Active InferAnts framework.

## Overview

Rust — memory-safe systems implementation

## Structure

- 📁 `RustConfig/`
- 📁 `RustThings/`
- 📁 `src/`
- 📄 `AGENTS.md`
- 📄 `Cargo.lock`
- 📄 `Cargo.toml`
- 📄 `README.md`
- 📄 `Rust.README.md`
- 📄 `config.json`
- 📄 `run.sh`
- 📄 `system_spec_RUST.txt`

## Interfaces

- **Input**: Active Inference parameters (state space, observation model, transition model)
- **Output**: Inference results (beliefs, policies, free energy values)
- **API**: Language-specific API consistent with the cross-language Active Inference interface
- **Testing**: Validated via `master_controller.py test rust`

## Dependencies

- Rust compiler/interpreter (see language-specific README)
- Active Inference mathematical libraries for Rust
- Visualization libraries (where applicable)

## Version

- **Framework**: Active InferAnts
- **License**: CC BY-NC-ND 4.0

# SPEC.md — Active Inference in CSharp

> Technical specification for `0_CONTEXT/Computer_Languages/CSharp` within the Active InferAnts framework.

## Overview

C# — .NET ecosystem implementation

## Structure

- 📄 `AGENTS.md`
- 📄 `ActiveInference.csproj`
- 📄 `Demo.cs`
- 📄 `Program.cs`
- 📄 `README.md`
- 📄 `SKILL.md`

## Interfaces

- **Input**: Active Inference parameters (state space, observation model, transition model)
- **Output**: Inference results (beliefs, policies, free energy values)
- **API**: Language-specific API consistent with the cross-language Active Inference interface
- **Testing**: Validated via `master_controller.py test csharp`

## Dependencies

- CSharp compiler/interpreter (see language-specific README)
- Active Inference mathematical libraries for CSharp
- Visualization libraries (where applicable)

## Version

- **Framework**: Active InferAnts
- **License**: CC BY-NC-ND 4.0

# SPEC.md — Third-Party Integrations

> Technical specification for `9_OTHER` within the Active InferAnts framework.

## Overview

Third-party integrations, specialized modules, and experimental features. This phase extends the core framework with external platform connections.

## Structure

- 📁 `ActivityPub/`
- 📁 `BPMN/`
- 📁 `Coda/`
- 📁 `FOIA/`
- 📁 `Github/`
- 📁 `HoloChain/`
- 📁 `Kafka/`
- 📁 `Languages/`
- 📁 `Matterbridge/`
- 📁 `Nostr/`
- 📁 `TheBrain/`
- 📁 `eBPF/`
- 📄 `AGENTS.md`
- 📄 `README.md`

## Interfaces

- **Input**: Receives output from the preceding pipeline phase
- **Output**: Produces structured data/artifacts for the subsequent phase
- **Configuration**: Managed via `config.json` at the repository root

## Dependencies

- Python 3.8+
- NumPy, SciPy (core mathematical operations)
- See `requirements.txt` at repository root for full dependency list

## Version

- **Framework**: Active InferAnts
- **License**: CC BY-NC-ND 4.0

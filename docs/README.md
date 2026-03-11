# Active InferAnts Documentation

Comprehensive documentation for the Active InferAnts multi-language Active Inference framework.

## Quick Navigation

| Section | Description |
|---------|-------------|
| [Architecture](architecture/) | System design, pipeline flow, and component relationships |
| [API Reference](api/) | REST API endpoints, data models, and integration contracts |
| [Guides](guides/) | Getting started, development workflows, and tutorials |
| [Reference](reference/) | Configuration, languages, and technical specifications |
| [Security](security/) | Security architecture, cryptographic primitives, and threat model |

## Project Overview

Active InferAnts implements Active Inference algorithms across **40 programming languages** with a **6-phase operational pipeline** (0_CONTEXT → 1_PREPARE → 2_OPERATE → 3_MEASURE → 4_REPORT → 5_FOLLOWUP) and external API layer (6_API). Third-party integrations live in 9_OTHER.

- **254 Python modules** across core pipeline and systems
- **40 language implementations** with shared generative model architecture
- **12 third-party integrations** (Kafka, Nostr, HoloChain, ActivityPub, etc.)
- **17 research entity profiles** and **8 funding agency** documentation sets

## License

CC BY-NC-ND 4.0 — See [LICENSE](../LICENSE)

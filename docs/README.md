# Active InferAnts Documentation

Comprehensive documentation for the Active InferAnts multi-language Active Inference framework.

## Quick Navigation

| Section | Docs | Description |
|---------|------|-------------|
| [Architecture](architecture/) | 5 | System design, pipeline flow, generative model |
| [API Reference](api/) | 3 | REST endpoints, data models, authentication |
| [Concepts](concepts/) | 8 | Active Inference primer, agent types, category theory |
| [Guides](guides/) | 5 | Getting started, adding languages, contributing |
| [Operations](operations/) | 5 | Deployment, monitoring, logging, governance |
| [Reference](reference/) | 5 | Configuration, 50-language matrix, glossary |
| [Security](security/) | 2 | Security architecture, cryptographic primitives |
| [Systems](systems/) | 6 | P3IF, Cognitive Sovereignty, IC2S2, William Blake |
| [Testing](testing/) | 3 | Testing strategy, cross-language tests, verification |
| [Tutorials](tutorials/) | 6 | First agent, pipeline, results analysis, benchmarking |

## Project Overview

Active InferAnts implements Active Inference across **50 programming languages** registered in [`0_CONTEXT/Computer_Languages/languages.json`](../0_CONTEXT/Computer_Languages/languages.json), with a **6-phase operational pipeline**:

```
0_CONTEXT → 1_PREPARE → 2_OPERATE → 3_MEASURE → 4_REPORT → 5_FOLLOWUP → 6_API
```

| Metric | Value |
|--------|-------|
| Tracked Python files | 266 |
| Language implementations | 50 |
| Specialized systems | 10 |
| Third-party integrations | 12 |
| Research entity profiles | 17 |
| Funding agency docs | 8 |
| Tracked Markdown files | 7,262 |

## Getting Started

1. **New to Active Inference?** → [Active Inference Primer](concepts/active_inference_primer.md)
2. **Want to run code?** → [Getting Started](guides/getting_started.md)
3. **Building an agent?** → [Your First Agent](tutorials/first_agent.md)
4. **Understanding the pipeline?** → [Pipeline Overview](architecture/pipeline_overview.md)
5. **Adding a language?** → [Adding a Language](guides/adding_a_language.md)

## License

CC BY-NC-ND 4.0 — See [LICENSE](../LICENSE)

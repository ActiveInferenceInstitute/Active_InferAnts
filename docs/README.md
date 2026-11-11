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

## Full document index

Every content document in this tree, grouped by section. Each section also has its
own `README.md` index, `AGENTS.md` agent guide, and `SPEC.md`.

### Architecture
- [Pipeline Overview](architecture/pipeline_overview.md)
- [Component Map](architecture/component_map.md)
- [Data Flow](architecture/data_flow.md)
- [Generative Model](architecture/generative_model.md)
- [Integration Architecture](architecture/integration_architecture.md)

### API Reference
- [Knowledge API](api/knowledge_api.md)
- [MetaInformAnt API](api/metainformant_api.md)
- [Data Models](api/data_models.md)

### Concepts
- [Active Inference Primer](concepts/active_inference_primer.md)
- [Agent Types](concepts/agent_types.md)
- [BOLTS Framework](concepts/bolts_framework.md)
- [Category Theory](concepts/category_theory.md)
- [Cognitive Security](concepts/cognitive_security.md)
- [Digital Twins](concepts/digital_twins.md)
- [Multi-Language Design](concepts/multi_language_design.md)
- [Pheromone Signaling](concepts/pheromone_signaling.md)

### Guides
- [Getting Started](guides/getting_started.md)
- [Adding a Language](guides/adding_a_language.md)
- [Running Simulations](guides/running_simulations.md)
- [Research Workflow](guides/research_workflow.md)
- [Contributing](guides/contributing.md)

### Operations
- [Simulation Operations](operations/simulation_operations.md)
- [API Deployment](operations/api_deployment.md)
- [Monitoring](operations/monitoring.md)
- [Logging](operations/logging.md)
- [Governance](operations/governance.md)

### Reference
- [Configuration](reference/configuration.md)
- [Language Matrix](reference/language_matrix.md)
- [Systems Reference](reference/systems_reference.md)
- [Glossary](reference/glossary.md)
- [Dependencies](reference/dependencies.md)

### Security
- [Security Architecture](security/security_architecture.md)
- [Cryptographic Primitives](security/cryptographic_primitives.md)

### Systems
- [P3IF](systems/p3if.md)
- [Cognitive Sovereignty](systems/cognitive_sovereignty.md)
- [IC2S2](systems/ic2s2.md)
- [William Blake](systems/william_blake.md)
- [Active Data Sampling](systems/active_data_sampling.md)
- [Meta Systems](systems/meta_systems.md)

### Testing
- [Testing Strategy](testing/testing_strategy.md)
- [Cross-Language Tests](testing/cross_language_tests.md)
- [Verification Methods](testing/verification_methods.md)

### Tutorials
- [Your First Agent](tutorials/first_agent.md)
- [Running the Pipeline](tutorials/running_pipeline.md)
- [Analyzing Results](tutorials/analyzing_results.md)
- [Adding a System](tutorials/adding_a_system.md)
- [Grant Generation](tutorials/grant_generation.md)
- [Benchmarking](tutorials/benchmarking.md)

## Project Overview

Active InferAnts implements Active Inference across **50 programming languages** registered in [`0_CONTEXT/Computer_Languages/languages.json`](../0_CONTEXT/Computer_Languages/languages.json), with a **6-phase operational pipeline**:

```
0_CONTEXT → 1_PREPARE → 2_OPERATE → 3_MEASURE → 4_REPORT → 5_FOLLOWUP → 6_API
```

| Metric | Value |
|--------|-------|
| Tracked Python files | 280 |
| Language implementations | 50 |
| Specialized systems | 10 |
| Third-party integrations | 12 |
| Research entity profiles | 17 |
| Funding agency docs | 8 |
| Tracked Markdown files | 7,269 |

## Getting Started

1. **New to Active Inference?** → [Active Inference Primer](concepts/active_inference_primer.md)
2. **Want to run code?** → [Getting Started](guides/getting_started.md)
3. **Building an agent?** → [Your First Agent](tutorials/first_agent.md)
4. **Understanding the pipeline?** → [Pipeline Overview](architecture/pipeline_overview.md)
5. **Adding a language?** → [Adding a Language](guides/adding_a_language.md)

## License

CC BY-NC-ND 4.0 — See [LICENSE](../LICENSE)

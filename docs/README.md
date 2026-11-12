# Active InferAnts Documentation

Comprehensive documentation for the Active InferAnts multi-language Active Inference framework.

**Quick Reference:** [Documentation index](documentation-index.md) |
[Run guide](RUN_GUIDE.md) | [Gate metrics](_generated/gate_metrics.md)

`docs/README.md` is the hub you are reading; [`index.md`](index.md) is the
MkDocs home page (`mkdocs.yml` excludes this hub from the built site so the two
do not collide). [`documentation-index.md`](documentation-index.md) is the flat
index of every long-lived document, generated from the tree by
`scripts/docgen/doc_index.py`.

## Quick Navigation

| Section | Description |
|---------|-------------|
| [Architecture](architecture/README.md) | System design, pipeline flow, generative model |
| [API Reference](api/README.md) | REST endpoints, data models, authentication |
| [Concepts](concepts/README.md) | Active Inference primer, agent types, category theory |
| [Guides](guides/README.md) | Getting started, adding languages, contributing |
| [Operations](operations/README.md) | Deployment, monitoring, logging, governance |
| [Reference](reference/README.md) | Configuration, language matrix, glossary |
| [Security](security/README.md) | Security architecture, cryptographic primitives |
| [Systems](systems/README.md) | P3IF, Cognitive Sovereignty, IC2S2, William Blake |
| [Testing](testing/README.md) | Testing strategy, cross-language tests, verification |
| [Tutorials](tutorials/README.md) | First agent, pipeline, results analysis, benchmarking |

Each section has its own `README.md` index, `AGENTS.md` agent guide, and
`SPEC.md`. Per-section document counts are in the
[documentation index](documentation-index.md), which is generated — do not copy
the numbers here.

## Gate and measured facts

The repository's single check entry point is [`../run.sh`](../run.sh); its arms
(`lint`, `test-fast`, `test-full`, `docs`, `gnn`) and the commands CI runs are
documented in the [run guide](RUN_GUIDE.md).

Every measured number the documentation quotes — arm wall times, test counts,
tracked-file inventory, and the out-of-scope lint counts — lives in
[`_generated/gate_metrics.md`](_generated/gate_metrics.md), written by
`scripts/docgen/gate_metrics.py`. Link it instead of restating a number.

## Project Overview

Active InferAnts implements Active Inference across the languages registered in
[`0_CONTEXT/Computer_Languages/languages.json`](../0_CONTEXT/Computer_Languages/languages.json),
with a **6-phase operational pipeline**:

```
0_CONTEXT → 1_PREPARE → 2_OPERATE → 3_MEASURE → 4_REPORT → 5_FOLLOWUP → 6_API
```

The framework's core Python package is `active_infer_ants/`; the continuous
Gaussian agent is specified in
[`gnn/gaussian_agent.gnn.md`](../gnn/gaussian_agent.gnn.md) and validated
against the revision pinned in [`gnn/upstream.json`](../gnn/upstream.json)
(see the [run guide](RUN_GUIDE.md#the-gnn-arm)).

## Getting Started

1. **New to Active Inference?** → [Active Inference Primer](concepts/active_inference_primer.md)
2. **Want to run code?** → [Getting Started](guides/getting_started.md)
3. **Building an agent?** → [Your First Agent](tutorials/first_agent.md)
4. **Understanding the pipeline?** → [Pipeline Overview](architecture/pipeline_overview.md)
5. **Adding a language?** → [Adding a Language](guides/adding_a_language.md)

## License

CC BY-NC-ND 4.0 — See [LICENSE](../LICENSE)

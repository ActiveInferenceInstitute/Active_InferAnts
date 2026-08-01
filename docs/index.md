# Active InferAnts

Welcome to the Active InferAnts documentation hub.

Active InferAnts is a multi-language Active Inference framework for advanced AI
research and applications. The repository implements the core Active Inference
algorithms in **50 programming languages**, with a 6-phase operational pipeline
(Prepare → Operate → Measure → Report → Follow-up → API).

## Quick links

- [Repository README](../README.md) — overview, quick start, architecture, APIs.
- [Architecture](architecture/index.md) — pipeline flow and system design.
- [API reference](api/index.md) — the Knowledge and MetaInformAnt REST APIs.
- [Concepts](concepts/index.md) — Active Inference primer and agent types.
- [Guides](guides/index.md) — getting started and tutorials.
- [Operations](operations/index.md) — deployment, monitoring, governance.
- [Reference](reference/index.md) — configuration, language matrix, glossary.
- [Security](security/index.md) — security architecture and crypto primitives.
- [Systems](systems/index.md) — P3IF, Cognitive Sovereignty, IC2S2, and more.
- [Testing](testing/index.md) — testing strategy and cross-language verification.
- [Tutorials](tutorials/index.md) — first agent, pipeline, analysis, grants.

## The `active_infer_ants` package

The core, Python-oriented package lives at the repository root and is
installable with `pip install -e .`:

```python
from active_infer_ants import InferenceModel, ActiveInferenceAgent, Environment

model = InferenceModel()
results = model.run(max_iterations=1000)
model.visualize(results)
```

See the [repository README](../README.md) for the full quick start.

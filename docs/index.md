# Active InferAnts

Welcome to the Active InferAnts documentation hub.

Active InferAnts is a multi-language Active Inference framework for advanced AI
research and applications. The repository implements the core Active Inference
algorithms in **50 programming languages**, with a 6-phase operational pipeline
(Prepare → Operate → Measure → Report → Follow-up → API).

## Quick links

- [Repository README](https://github.com/ActiveInferenceInstitute/Active_InferAnts/blob/main/README.md) — overview, quick start, architecture, APIs.
- [Run guide](RUN_GUIDE.md) — the `./run.sh` arms, the lint surface, and where CI runs each one.
- [Documentation index](documentation-index.md) — every document, generated from the tree.
- [Gate metrics](_generated/gate_metrics.md) — measured arm wall times and test counts.
- [Architecture](architecture/README.md) — pipeline flow and system design.
- [API reference](api/README.md) — the Knowledge and MetaInformAnt REST APIs.
- [Concepts](concepts/README.md) — Active Inference primer and agent types.
- [Guides](guides/README.md) — getting started and tutorials.
- [Operations](operations/README.md) — deployment, monitoring, governance.
- [Reference](reference/README.md) — configuration, language matrix, glossary.
- [Security](security/README.md) — security architecture and crypto primitives.
- [Systems](systems/README.md) — P3IF, Cognitive Sovereignty, IC2S2, and more.
- [Testing](testing/README.md) — testing strategy and cross-language verification.
- [Tutorials](tutorials/README.md) — first agent, pipeline, analysis, grants.

## The `active_infer_ants` package

The core, Python-oriented package lives at the repository root and is
installable with `pip install -e .`:

```python
from active_infer_ants import InferenceModel, ActiveInferenceAgent, Environment

model = InferenceModel()
results = model.run(max_iterations=1000)
model.visualize(results)
```

See the [repository README](https://github.com/ActiveInferenceInstitute/Active_InferAnts/blob/main/README.md) for the full quick start.

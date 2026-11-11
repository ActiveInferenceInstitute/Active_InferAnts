# `active_infer_ants` — core package

The installable Python package that implements the public API referenced by the
repository [`README.md`](../README.md). It is deliberately small and NumPy-based so
it runs anywhere, and it is the target of the GNN specification in
[`../gnn/gaussian_agent.gnn.md`](../gnn/gaussian_agent.gnn.md).

## Contents

| Module | Provides |
|--------|----------|
| `agent.py` | `ActiveInferenceAgent` — `infer(observation)`, `learn(reward)`, `from_config(config)`, `visualize_beliefs()`; the Gaussian agent specified in the GNN file |
| `environment.py` | `Environment` — `observe()` and `step(action)` for the toy environment |
| `colony.py` | `AntColony` and `PheromoneNetwork` — multi-agent parallel inference and stigmergic pheromone trails |
| `model.py` | `InferenceModel` — `run(max_iterations)` orchestrator and `visualize(results)` |

`__init__.py` re-exports `InferenceModel`, `ActiveInferenceAgent`, `Environment`,
`AntColony`, and `PheromoneNetwork` and defines `__version__`.

## Install and use

```bash
pip install -e .          # from the repository root
```

```python
from active_infer_ants import InferenceModel

model = InferenceModel()
results = model.run(max_iterations=1000)
model.visualize(results)
```

The package is exercised by [`../tests/test_active_infer_ants.py`](../tests/test_active_infer_ants.py)
and by the GNN conformance test. When you change `agent.py`, keep
`../gnn/gaussian_agent.gnn.md` in step and re-run
`python scripts/validate_gnn_spec.py`.

## Related

- Parent: [Active InferAnts](../README.md)
- Tests: [tests/](../tests/README.md)
- GNN specification: [gnn/gaussian_agent.gnn.md](../gnn/gaussian_agent.gnn.md)

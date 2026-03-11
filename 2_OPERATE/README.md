# Runtime Execution

Runtime execution, simulation management, and cognitive utilities. This phase orchestrates the execution of Active Inference simulations and agent behaviors.

## Modules

| Module | Description |
|---|---|
| `plan_Simulation.py` | Simulation planning — configures state spaces, observation models, and transition matrices from `config` and `metaconfig` |
| `execute_Simulation.py` | `SimulationExecutor` class — time-stepped simulation loop with visualization frequency and sleep duration controls |
| `render_Simulation.py` | `SimulationRenderer` class — matplotlib animations, custom `Entity` rendering, and real-time display |
| `cognitive_utilities.py` | `CognitiveUtilities` class — agent behavioral analysis, cognitive load assessment, decision support, and multi-format export (JSON/CSV/Excel via pandas) |
| `situational_Antwareness.py` | `AgentVisualizer` ABC — A/B/C/D/G/F matrix visualization, eigenvalue analysis, seaborn heatmaps, and agent state evolution tracking |

## Pipeline Position

```
1_PREPARE → [2_OPERATE] → 3_MEASURE
```

- **Input**: Prepared agents, configurations, and environment models from `1_PREPARE`
- **Output**: Simulation traces, behavioral metrics, cognitive load data for `3_MEASURE`

## Related

- Parent: [Active InferAnts](../README.md)
- Previous phase: [1_PREPARE](../1_PREPARE/README.md)
- Next phase: [3_MEASURE](../3_MEASURE/README.md)

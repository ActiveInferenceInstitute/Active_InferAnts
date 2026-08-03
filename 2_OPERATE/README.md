# Runtime Execution

Runtime execution, simulation management, and cognitive utilities. This phase orchestrates the execution of Active Inference simulations and agent behaviors.

## Modules

| Module | Description |
|---|---|
| `plan_Simulation.py` | `SimulationPlanner` (alias `SimulationSetup`) — simulation planning: environment setup, agent initialization, and parameter configuration (reads `1_PREPARE/configs`) |
| `execute_Simulation.py` | `SimulationExecutor` class — time-stepped simulation loop with visualization frequency and sleep duration controls |
| `render_Simulation.py` | `SimulationRenderer` class — matplotlib animations, custom `Entity` rendering, and real-time display |
| `environment.py` | `Environment` class — 2D grid world with pheromone field, food sources, and nests |
| `MetaInformAnt_Simulation.py` | `MetaInformAntSimulation` class — drives `active_infer_ants` agents through the grid environment |
| `data_logging.py` | `DataLogger` class — per-step records and JSON result persistence |
| `performance_monitor.py` | `PerformanceMonitor` class — runtime timing and parameter-adjustment checkpoints |
| `performance_metrics.py` | `PerformanceTracker` class — scalar metrics and cross-run aggregates |
| `error_handling.py` | `SimulationError` exception + `handle_simulation_error` helper |
| `exception_handling.py` | `SimulationExceptionHandler` class — fail-closed error payloads |
| `report_generator.py` | `ReportGenerator` class — plain-text simulation reports |
| `computational_resources.py` | `estimate_computational_resources` — advisory cost estimate |
| `visualization.py` | `SimulationVisualizer` class — summary and comparative plots |
| `cognitive_utilities.py` | `CognitiveUtilities` class — agent behavioral analysis, cognitive load assessment, decision support, and multi-format export (JSON/CSV/Excel via pandas) |
| `situational_Antwareness.py` | `AgentVisualizer` ABC + `ConcreteAgentVisualizer` — A/B/C/D/G/F matrix visualization, eigenvalue analysis, seaborn heatmaps, and agent state evolution tracking |

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

# AGENTS.md — Runtime Execution

> Agent guidance for the `2_OPERATE` directory within the Active InferAnts framework.

## Purpose

Runtime execution, simulation management, and cognitive utilities. This phase orchestrates the execution of Active Inference simulations and agent behaviors.

## Directory Contents

### Pipeline Modules

- 📄 `plan_Simulation.py` — `SimulationPlanner` class (alias `SimulationSetup`): simulation planning — environment setup, agent initialization, and parameter configuration (reads `1_PREPARE/configs`)
- 📄 `execute_Simulation.py` — `SimulationExecutor` class: time-stepped simulation loop with visualization frequency and sleep duration controls
- 📄 `render_Simulation.py` — `SimulationRenderer` class: matplotlib-based animation, `Entity` rendering, and real-time visualization
- 📄 `environment.py` — `Environment` class: 2D grid world with pheromone field, food sources, and nests; `build_environment_from_config` helper
- 📄 `MetaInformAnt_Simulation.py` — `MetaInformAntSimulation` class: drives `active_infer_ants` agents through the grid environment (progress, aggregate results, visualization parameters)

### Observability & Support

- 📄 `data_logging.py` — `DataLogger` class: per-step records and JSON result persistence
- 📄 `performance_monitor.py` — `PerformanceMonitor` class: runtime timing and parameter-adjustment checkpoints
- 📄 `performance_metrics.py` — `PerformanceTracker` class: scalar metrics and cross-run aggregates
- 📄 `error_handling.py` — `SimulationError` exception + `handle_simulation_error` re-raise helper
- 📄 `exception_handling.py` — `SimulationExceptionHandler` class: fail-closed error payloads
- 📄 `report_generator.py` — `ReportGenerator` class: plain-text simulation reports
- 📄 `computational_resources.py` — `estimate_computational_resources` advisory cost estimate
- 📄 `visualization.py` — `SimulationVisualizer` class: summary and comparative plots

### Analysis

- 📄 `cognitive_utilities.py` — `CognitiveUtilities` class: agent behavioral analysis, cognitive load assessment, decision support, and multi-format export (JSON/CSV/Excel via pandas)
- 📄 `situational_Antwareness.py` — `AgentVisualizer` abstract base class + `ConcreteAgentVisualizer`: A/B/C/D/G/F matrix visualization, eigenvalue analysis, seaborn heatmaps, and agent state evolution tracking

## Agent Instructions

- Maintain simulation execution pipeline: `plan_Simulation.py` → `execute_Simulation.py` → `render_Simulation.py`.
- The pipeline is wired to the `active_infer_ants` package for the agent-side API; keep the wiring and the integration suite (`tests/test_simulation_pipeline.py`) in sync.
- Ensure `CognitiveUtilities` export methods (JSON/CSV/Excel) produce valid output.
- Preserve the `AgentVisualizer` ABC hierarchy and `ConcreteAgentVisualizer` integration with the simulation context.
- The optional per-agent visualizer requires matrix attributes (`A_matrix`, `B_matrix`, …) that `active_infer_ants` agents do not carry; keep that call path guarded and non-fatal.
- Track pipeline inputs from `1_PREPARE` agent definitions and outputs consumed by `3_MEASURE`.
- Follow the repository's CC BY-NC-ND 4.0 license.
- Keep all documentation synchronized with actual contents.

## Quality Checklist

- [ ] All files documented and up-to-date
- [ ] Pipeline flow (plan → execute → render) verified
- [ ] Integration suite covers the pipeline end-to-end
- [ ] README.md and SPEC.md synchronized with this AGENTS.md

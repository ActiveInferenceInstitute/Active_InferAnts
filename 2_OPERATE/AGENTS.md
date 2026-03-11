# AGENTS.md — Runtime Execution

> Agent guidance for the `2_OPERATE` directory within the Active InferAnts framework.

## Purpose

Runtime execution, simulation management, and cognitive utilities. This phase orchestrates the execution of Active Inference simulations and agent behaviors.

## Directory Contents

- 📄 `plan_Simulation.py` — Simulation planning: environment setup, agent initialization, and parameter configuration (`numpy`, `config`, `metaconfig`)
- 📄 `execute_Simulation.py` — `SimulationExecutor` class: time-stepped simulation loop with visualization frequency and sleep duration controls
- 📄 `render_Simulation.py` — `SimulationRenderer` class: matplotlib-based animation, `Entity` rendering, and real-time visualization
- 📄 `cognitive_utilities.py` — `CognitiveUtilities` class: agent behavioral analysis, cognitive load assessment, decision support, and multi-format export (JSON/CSV/Excel via pandas)
- 📄 `situational_Antwareness.py` — `AgentVisualizer` abstract base class: A/B/C/D/G/F matrix visualization, eigenvalue analysis, seaborn heatmaps, and agent state evolution tracking

## Agent Instructions

- Maintain simulation execution pipeline: `plan_Simulation.py` → `execute_Simulation.py` → `render_Simulation.py`.
- Ensure `CognitiveUtilities` export methods (JSON/CSV/Excel) produce valid output.
- Preserve the `AgentVisualizer` ABC hierarchy and `ConcreteAgentVisualizer` integration with the simulation context.
- Track pipeline inputs from `1_PREPARE` agent definitions and outputs consumed by `3_MEASURE`.
- Follow the repository's CC BY-NC-ND 4.0 license.
- Keep all documentation synchronized with actual contents.

## Quality Checklist

- [ ] All files documented and up-to-date
- [ ] Pipeline flow (plan → execute → render) verified
- [ ] README.md and SPEC.md synchronized with this AGENTS.md

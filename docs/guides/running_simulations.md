# Running Simulations

Configuring and running Active Inference simulations in the pipeline.

## Simulation Pipeline

> **Status**: the `2_OPERATE` pipeline is under repair (repository `TODO.md`,
> item M-4) — the scripts reference modules that do not exist in the tree yet.
> The descriptions below document the intended contracts. For a working
> simulation today, use the `active_infer_ants` package (see
> [Getting Started](getting_started.md)).

```
plan_Simulation.py → execute_Simulation.py → render_Simulation.py
```

### Step 1: Plan

`plan_Simulation.py` configures:
- Environment state space and observation model
- Agent populations and initialization
- Transition matrices from `config` and `metaconfig`

### Step 2: Execute

`execute_Simulation.py` runs:
- `SimulationExecutor` manages the time-stepped loop
- Configurable visualization frequency and sleep duration
- Outputs simulation traces for measurement

### Step 3: Render

`render_Simulation.py` provides:
- `SimulationRenderer` with matplotlib animation
- Custom `Entity` rendering for agents
- Real-time display or saved output

## Post-Simulation Analysis

### Measurement (`3_MEASURE/`)

```bash
python3 3_MEASURE/categorization.py    # Graph-based categorization
python3 3_MEASURE/statistics.py        # Statistical analysis
python3 3_MEASURE/summarize.py         # Entropy-based summarization
```

### Reporting (`4_REPORT/`)

```bash
python3 4_REPORT/execute_report.py     # Async report generation
```

## Cognitive Analysis

Use `CognitiveUtilities` for post-hoc analysis:

```python
from cognitive_utilities import CognitiveUtilities

cu = CognitiveUtilities(simulation_data)
behavior = cu.analyze_agent_behavior()
load = cu.evaluate_cognitive_load()
summary = cu.summarize_cognitive_insights(behavior, load)
cu.export_summary(summary, json_path="output.json", csv_path="output.csv")
```

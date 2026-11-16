# Running Simulations

Configuring and running Active Inference simulations in the pipeline.

## Simulation Pipeline

```
plan_Simulation.py → execute_Simulation.py → render_Simulation.py
```

### Step 1: Plan

`plan_Simulation.py` configures:
- Environment state space and observation model
- Agent populations and initialization
- Transition matrices from `config` and `metaconfig`

### Step 2: Execute

`SimulationExecutor` manages the time-stepped loop. Its constructor accepts
`visualization_interval`, `pause_duration`, `log_level`, `output_dir`, and
`max_steps`; see [executor parameters](../operations/simulation_operations.md#simulationexecutor-parameters).
It records steps and produces local `simulation_report.txt` under `output_dir`.
Required failures are not successful runs.

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

`4_REPORT/` defines report specifications and asynchronous orchestration,
not a standalone report-generation CLI. Real collection, analysis, generation,
delivery and error providers are not bundled. Service-backed `5_FOLLOWUP/`
execution likewise requires owner-selected providers and qualified
configuration/dependencies.

The local `2_OPERATE` simulation report is separate. Do not substitute
unrelated simulation support modules for missing report/follow-up providers.

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

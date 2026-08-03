# Getting Started

## Prerequisites

- Python 3.9+ (matching `pyproject.toml`)
- NumPy, matplotlib, pandas, seaborn
- PyMDP (`pip install pymdp`) only for the `pymdp_Ant_*` agents in `1_PREPARE/Things`

## Quick Start (Python package)

The installable `active_infer_ants` package is the supported entry point:

```bash
# Clone the repository
git clone https://github.com/ActiveInferenceInstitute/ActiveInferAnts.git
cd ActiveInferAnts

# Install Python dependencies
pip install -r requirements.txt

# Optional: install in development mode (adds pytest + ruff)
pip install -e ".[dev]"
```

```python
from active_infer_ants import InferenceModel

model = InferenceModel()
results = model.run(max_iterations=1000)
model.visualize(results)
```

A CLI demo is also available after installing the package:

```bash
active-inferants --iterations 100
```

## Quick Start (multi-language orchestration)

```bash
# Show status of all language implementations
python3 0_CONTEXT/Computer_Languages/master_controller.py status

# Run a specific language implementation (e.g. Python)
python3 0_CONTEXT/Computer_Languages/master_controller.py run python
```

## Configuration

Edit `config.json` to customize simulation parameters:

```json
{
    "initial_values": {
        "sensory_input": 10,
        "prediction": 10,
        "learning_rate": 3,
        "precision": 5,
        "exploration_factor": 2
    },
    "max_iterations": 1000,
    "visualization_enabled": true
}
```

## A Note on the 2_OPERATE Pipeline

The `2_OPERATE/plan_Simulation.py → execute_Simulation.py →
render_Simulation.py` pipeline is currently **under repair** (see the
repository `TODO.md`, item M-4): the scripts reference modules that do not yet
exist in the tree and cannot be run end-to-end. For a working simulation
experience today, use the `active_infer_ants` package above or the
multi-language orchestration scripts.

## Running a Language Implementation

Each language directory contains its own implementation and run script:

```bash
cd 0_CONTEXT/Computer_Languages/Python
./run.sh

# Or run the implementation directly
python3 Student_Teacher.py
```

## Next Steps

- [Running Simulations](running_simulations.md) — Advanced simulation configuration
- [Pipeline Overview](../architecture/pipeline_overview.md) — Understanding the 6-phase pipeline
- [Generative Model](../architecture/generative_model.md) — Mathematical foundations

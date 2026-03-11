# Getting Started

## Prerequisites

- Python 3.8+
- NumPy, matplotlib, pandas, seaborn
- PyMDP (`pip install pymdp`)

## Quick Start

```bash
# Clone the repository
git clone https://github.com/ActiveInferenceInstitute/ActiveInferAnts.git
cd ActiveInferAnts

# Install Python dependencies
pip install numpy matplotlib pandas seaborn pymdp

# Run a simulation
cd 2_OPERATE
python3 plan_Simulation.py
python3 execute_Simulation.py
python3 render_Simulation.py
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

## Running a Language Implementation

Each language has a `run.sh` script:

```bash
cd 0_CONTEXT/Computer_Languages/Python
./run.sh

# Or run directly
python3 Student_Teacher.py
```

## Next Steps

- [Running Simulations](running_simulations.md) — Advanced simulation configuration
- [Pipeline Overview](../architecture/pipeline_overview.md) — Understanding the 6-phase pipeline
- [Generative Model](../architecture/generative_model.md) — Mathematical foundations

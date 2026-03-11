# Configuration Reference

All configuration parameters for the Active InferAnts framework.

## Root Configuration (`config.json`)

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `sensory_input` | int | 10 | Dimensionality of sensory input |
| `prediction` | int | 10 | Prediction horizon steps |
| `learning_rate` | float | 3.0 | Learning rate for belief updating |
| `precision` | float | 5.0 | Precision (inverse variance) of beliefs |
| `temporal_integration` | int | 1 | Temporal integration window |
| `exploration_factor` | float | 2.0 | Exploration-exploitation balance |
| `model_complexity` | int | 3 | Generative model complexity level |
| `goal_directed_behavior` | int | 4 | Goal-directedness parameter |
| `uncertainty` | float | 2.0 | Initial uncertainty level |
| `max_iterations` | int | 1000 | Maximum simulation iterations |
| `visualization_enabled` | bool | true | Enable matplotlib output |
| `output_directory` | string | "./simulation_output" | Output directory path |
| `logging_level` | string | "INFO" | Python logging level |

## Generative Model Defaults

| Parameter | Value | Description |
|-----------|-------|-------------|
| `num_states` | 4 | Number of hidden states |
| `num_observations` | 3 | Number of observation channels |
| `num_actions` | 2 | Number of available actions |
| Prior distribution | Uniform | D = [0.25, 0.25, 0.25, 0.25] |

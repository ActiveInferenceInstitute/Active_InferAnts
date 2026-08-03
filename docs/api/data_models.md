# Data Models

Shared data models and schemas used across the Active InferAnts pipeline.

## Pipeline Data Models

### 3_MEASURE Models

| Model | Module | Description |
|-------|--------|-------------|
| `MeasurementMethod` | `specify_measure.py` | Enum of supported measurement methods |
| `QRFParameters` | `specify_measure.py` | Quantum Reference Frame parameters dataclass |

### 4_REPORT Models

| Model | Module | Description |
|-------|--------|-------------|
| `DataSourceType` | `specify_report.py` | Enum of data source types |
| `ReportSpecification` | `specify_report.py` | Report specification with UUID, JSON serialization |
| `ReportSection` | `specify_report.py` | Pydantic report-section model |

### 5_FOLLOWUP Models

| Model | Module | Description |
|-------|--------|-------------|
| `FollowUpType` | `specify_followup.py` | Enum of follow-up action types |
| `SessionType` | `specify_followup.py` | Enum of session types |
| `UpdateArea` | `specify_followup.py` | Dataclass describing an update area |
| `Session` | `specify_followup.py` | Session dataclass |
| `Stakeholder` | `specify_followup.py` | Stakeholder dataclass |
| `Resource` | `specify_followup.py` | Resource dataclass |

### 1_PREPARE Agent Models

| Model | Module | Description |
|-------|--------|-------------|
| `ActiveNestmate` | `InferAnts.py` | Nestmate agent with A/B/C/D matrices |
| `ActiveColony` | `InferAnts.py` | Colony-level agent aggregation |
| `Thing` | `Thing.py` | Base Active Inference entity (PyMDP) |

## Configuration Schema

See `config.json` at repository root. Simulation parameters are grouped under
`initial_values`; runtime/output settings are top-level:

```json
{
    "initial_values": {
        "sensory_input": 10,
        "prediction": 10,
        "learning_rate": 3,
        "precision": 5,
        "temporal_integration": 1,
        "exploration_factor": 2,
        "model_complexity": 3,
        "goal_directed_behavior": 4,
        "uncertainty": 2
    },
    "max_iterations": 1000,
    "visualization_enabled": true,
    "output_directory": "./simulation_output",
    "logging_level": "INFO"
}
```

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `initial_values.sensory_input` | int | 10 | Sensory input dimension |
| `initial_values.prediction` | int | 10 | Prediction horizon |
| `initial_values.learning_rate` | float | 3 | Learning rate |
| `initial_values.precision` | float | 5 | Precision (inverse variance) |
| `initial_values.temporal_integration` | int | 1 | Temporal integration window |
| `initial_values.exploration_factor` | float | 2 | Exploration-exploitation balance |
| `initial_values.model_complexity` | int | 3 | Generative model complexity level |
| `initial_values.goal_directed_behavior` | int | 4 | Goal-directedness parameter |
| `initial_values.uncertainty` | float | 2 | Initial uncertainty level |
| `max_iterations` | int | 1000 | Maximum simulation iterations |
| `visualization_enabled` | bool | true | Enable matplotlib output |
| `output_directory` | string | "./simulation_output" | Output directory path |
| `logging_level` | string | "INFO" | Python logging level |

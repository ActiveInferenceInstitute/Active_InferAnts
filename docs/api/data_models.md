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
| Report Specification | `specify_report.py` | Dataclass with UUID, JSON serialization |

### 5_FOLLOWUP Models

| Model | Module | Description |
|-------|--------|-------------|
| `FollowUpType` | `specify_followup.py` | Enum of follow-up action types |
| `SessionType` | `specify_followup.py` | Enum of session types |
| `UpdateArea` | `specify_followup.py` | Enum of update areas |
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

See `config.json` at repository root:

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `sensory_input` | int | 10 | Sensory input dimension |
| `prediction` | int | 10 | Prediction horizon |
| `learning_rate` | float | 3 | Learning rate |
| `precision` | float | 5 | Precision (inverse variance) |
| `max_iterations` | int | 1000 | Maximum simulation iterations |
| `visualization_enabled` | bool | true | Enable matplotlib output |
| `logging_level` | string | "INFO" | Python logging level |

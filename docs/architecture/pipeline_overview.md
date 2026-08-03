# Pipeline Overview

Active InferAnts uses a 6-phase operational pipeline inspired by Active Inference's perception-action loop.

## Pipeline Flow

```
0_CONTEXT → 1_PREPARE → 2_OPERATE → 3_MEASURE → 4_REPORT → 5_FOLLOWUP
                                                                  ↓
                                                              6_API (external)
                                                              9_OTHER (integrations)
```

## Phase Descriptions

### Phase 0: Context (`0_CONTEXT/`)

Foundation layer providing language implementations, system definitions, and specifications.

| Component | Purpose |
|-----------|---------|
|| `Computer_Languages/` | 50 registered language implementations of Active Inference agents |
| `Systems/` | Specialized systems (P3IF, IC2S2, Cognitive Sovereignty, William Blake, BOLTS) |
| `specs_and_prompts/` | System specification documents (v1, v2, v3) |

### Phase 1: Prepare (`1_PREPARE/`)

Agent definitions, utilities, configuration, and research methods.

| Component | Purpose |
|-----------|---------|
| `Things/` | `ActiveNestmate`, `ActiveColony`, `Thing` base class, PyMDP agents |
| `General/` | CogSec, Cryptography, DigitalTwin, Pheromones, Networking |
| `Utils/` | Security mesh, vault adapter, quantum security, encryption |
| `Methods/` | Research methods, grant generation, FieldSHIFT-2, theory translation |
| `configs/` | Simulation configuration files |

### Phase 2: Operate (`2_OPERATE/`)

Runtime simulation execution.

| Module | Class | Purpose |
|--------|-------|---------|
| `plan_Simulation.py` | `SimulationPlanner` (alias `SimulationSetup`) | Configure environment and agents; build the simulation |
| `execute_Simulation.py` | `SimulationExecutor` | Time-stepped simulation loop |
| `render_Simulation.py` | `SimulationRenderer` | Matplotlib animation and display |
| `cognitive_utilities.py` | `CognitiveUtilities` | Behavioral analysis, cognitive load, export |
| `situational_Antwareness.py` | `AgentVisualizer` / `ConcreteAgentVisualizer` | Matrix visualization, eigenvalue analysis |

### Phase 3: Measure (`3_MEASURE/`)

Analysis and quantification of simulation outputs.

| Module | Class | Purpose |
|--------|-------|---------|
| `categorization.py` | `CategoryTheoryAnalyzer` | Graph-based categorization (NetworkX) |
| `poly_functor.py` | `PolyFunctor` | 6 polynomial functor types (Tuple2/3, List, Maybe, Either, Tree) |
| `specify_measure.py` | `MeasurementMethod`, `QRFParameters` | Quantum Reference Frame specs |
| `statistics.py` | `SimulationSummary` | Statistical analysis (pandas/seaborn) |
| `summarize.py` | `SimulationEntity` | Entropy-based summarization |

### Phase 4: Report (`4_REPORT/`)

| Module | Class | Purpose |
|--------|-------|---------|
| `specify_report.py` | `DataSourceType` | Report specification with UUID tracking |
| `execute_report.py` | `ReportExecutor` | Async report generation (asyncio) |

### Phase 5: Follow-Up (`5_FOLLOWUP/`)

| Module | Class | Purpose |
|--------|-------|---------|
| `specify_followup.py` | `FollowUpType`, `SessionType` | Follow-up specifications |
| `execute_followup.py` | `FollowUpExecutor` | 7-service orchestration |

### Phase 6: API (`6_API/`)

| Module | Stack | Purpose |
|--------|-------|---------|
| `Knowledge_API.py` | FastAPI + SQLAlchemy + MongoDB + Redis + Neo4j + Elasticsearch | Knowledge management |
| `MetaInformAnt_API.py` | FastAPI + asyncio | Meta-information and agent management |

## Configuration

Root `config.json` defines simulation parameters (simulation values are nested
under `initial_values`; runtime/output settings are top-level):

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
    "visualization_enabled": true,
    "logging_level": "INFO"
}
```

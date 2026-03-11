# Agent Types

Taxonomy of Active Inference agents in the framework.

## Core Agent Hierarchy

```
Thing (base class — PyMDP)
├── ActiveNestmate (InferAnts.py)
│   ├── ActiveForager
│   └── ActiveDefender
├── ActiveColony (InferAnts.py)
└── pymdp_Ant variants
    ├── pymdp_Ant_1 (full PyMDP)
    └── pseudo-pymdp_Ant_1/2 (simplified)
```

## Agent Definitions

### `Thing` (`1_PREPARE/Things/Thing.py`)

Base Active Inference entity using PyMDP's `inference`, `control`, and `utils` modules.

| Attribute | Type | Description |
|-----------|------|-------------|
| A matrix | np.ndarray | Observation likelihood |
| B matrix | np.ndarray | Transition dynamics |
| C vector | np.ndarray | Preferences |
| D vector | np.ndarray | State prior |
| beliefs | np.ndarray | Current posterior beliefs |

### `ActiveNestmate` (`1_PREPARE/Things/InferAnts.py`)

Ant colony nestmate agent with NumPy-based generative models and extended parameters.

| Feature | Description |
|---------|-------------|
| Position tracking | (x, y) coordinates in environment |
| Influence factor | Measure of environmental influence |
| Agent parameters | Typed configuration dictionary |
| Movement history | Tracked for `CognitiveUtilities` analysis |
| Interaction log | Used for cognitive load computation |

### `ActiveColony` (`1_PREPARE/Things/InferAnts.py`)

Colony-level agent aggregating `ActiveNestmate` populations.

### Visualization (`2_OPERATE/situational_Antwareness.py`)

`AgentVisualizer` inspects agent internals:

| Inspected | Analysis |
|-----------|----------|
| A, B, C, D, G, F matrices | Shape, size, eigenvalues, entropy, condition number |
| Position | Environmental location |
| Influence factor | Environmental coupling |
| Agent-specific info | Nestmate config, colony config, foraging strategy, defense capabilities |

## Agent Subtypes (Visualization Support)

| Agent Type | Extracted Info |
|------------|---------------|
| `ActiveNestmate` | `nestmate_config` |
| `ActiveColony` | `colony_config` |
| `ActiveForager` | `foraging_strategy` |
| `ActiveDefender` | `defense_capabilities` |

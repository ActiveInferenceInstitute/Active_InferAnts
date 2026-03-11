# Cognitive Security

Adversarial simulation and belief robustness using Active Inference agents.

## Overview

`1_PREPARE/General/CogSec.py` implements cognitive security — the protection of belief formation processes against adversarial manipulation. It uses `ActiveNestmate` and `ActiveColony` agents from `InferAnts.py` to simulate and test belief robustness.

## Architecture

```
CogSec.py
├── imports ActiveNestmate, ActiveColony from InferAnts
├── uses config, metaconfig for parameters
└── simulates adversarial scenarios
```

## Threat Model

| Threat | Active Inference Framing | Defense |
|--------|--------------------------|---------|
| Disinformation | Manipulated A matrix (false likelihood) | Precision weighting of observations |
| Echo chambers | Biased B matrix (restricted transitions) | Epistemic exploration policies |
| Confirmation bias | Overly peaked D vector | Uniform prior regularization |
| Preference manipulation | Altered C vector | Goal robustness checks |

## Integration Points

- **CogSec.py** → `InferAnts.py` (agent types)
- **CogSec.py** → `config.py`, `metaconfig.py` (parameters)
- Outputs feed into `2_OPERATE` simulation pipeline

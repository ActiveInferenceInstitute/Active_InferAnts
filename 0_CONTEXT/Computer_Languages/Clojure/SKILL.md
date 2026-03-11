---
name: Active Inference in Clojure
description: Clojure implementation of Active Inference with belief updating, free energy minimization, and policy selection
---

# Active Inference in Clojure

## Overview

This skill provides a complete Active Inference implementation in Clojure,
demonstrating Bayesian belief updating, variational free energy calculation,
and expected free energy-based policy selection.

## Core Algorithms

1. **Belief Updating**: Bayesian inference using observation likelihoods to update posterior beliefs
2. **Free Energy Calculation**: KL divergence between posterior beliefs and prior distribution
3. **Policy Selection**: Softmax action selection over expected free energy per action
4. **Perception-Action Loop**: Iterative sense → infer → act cycle with generative model

## Key Files

- `project.clj` — Source implementation
- `run.sh` — Execution script (handles compilation if needed)
- `README.md` — Usage documentation and requirements

## Usage

```bash
cd 0_CONTEXT/Computer_Languages/Clojure/
./run.sh
```

## Language-Specific Features

- Immutable data structures
- Pure function composition
- Strong type inference

## Integration

- Tested via `master_controller.py test clojure`
- Benchmarked via `benchmark_suite.py`
- Listed in `languages.json` under category "Functional"

## Prerequisites

See `README.md` for Clojure-specific installation requirements.

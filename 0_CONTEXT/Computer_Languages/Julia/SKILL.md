---
name: Active Inference in Julia
description: Julia implementation of Active Inference with belief updating, free energy minimization, and policy selection
---

# Active Inference in Julia

## Overview

This skill provides a complete Active Inference implementation in Julia,
demonstrating Bayesian belief updating, variational free energy calculation,
and expected free energy-based policy selection.

## Core Algorithms

1. **Belief Updating**: Bayesian inference using observation likelihoods to update posterior beliefs
2. **Free Energy Calculation**: KL divergence between posterior beliefs and prior distribution
3. **Policy Selection**: Softmax action selection over expected free energy per action
4. **Perception-Action Loop**: Iterative sense → infer → act cycle with generative model

## Key Files

- `Clone_Julia_Repo.jl` — Source implementation
- `Julia_InferAnts.jl` — Source implementation
- `RxInfer.jl` — Source implementation
- `RxInfer_Agent_Model.jl` — Source implementation
- `run.sh` — Execution script (handles compilation if needed)
- `README.md` — Usage documentation and requirements

## Usage

```bash
cd 0_CONTEXT/Computer_Languages/Julia/
./run.sh
```

## Language-Specific Features

- Native matrix/array operations
- Scientific computing ecosystem
- Built-in visualization support

## Integration

- Tested via `master_controller.py test julia`
- Benchmarked via `benchmark_suite.py`
- Listed in `languages.json` under category "Scientific"

## Prerequisites

See `README.md` for Julia-specific installation requirements.

---
name: Active Inference in Scala
description: Scala implementation of Active Inference with belief updating, free energy minimization, and policy selection
---

# Active Inference in Scala

## Overview

This skill provides a complete Active Inference implementation in Scala,
demonstrating Bayesian belief updating, variational free energy calculation,
and expected free energy-based policy selection.

## Core Algorithms

1. **Belief Updating**: Bayesian inference using observation likelihoods to update posterior beliefs
2. **Free Energy Calculation**: KL divergence between posterior beliefs and prior distribution
3. **Policy Selection**: Softmax action selection over expected free energy per action
4. **Perception-Action Loop**: Iterative sense → infer → act cycle with generative model

## Key Files

- `src/main/scala/ActiveInferenceAgent.scala` — Source implementation
- `run.sh` — Execution script (handles compilation if needed)
- `README.md` — Usage documentation and requirements

## Usage

```bash
cd 0_CONTEXT/Computer_Languages/Scala/
./run.sh
```

## Language-Specific Features

- Cross-platform runtime environment
- Extensive ecosystem and libraries
- Garbage collected memory management

## Integration

- Tested via `master_controller.py test scala`
- Benchmarked via `benchmark_suite.py`
- Listed in `languages.json` under category "JVM/.NET"

## Prerequisites

See `README.md` for Scala-specific installation requirements.

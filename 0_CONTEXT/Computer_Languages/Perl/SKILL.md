---
name: Active Inference in Perl
description: Perl implementation of Active Inference with belief updating, free energy minimization, and policy selection
---

# Active Inference in Perl

## Overview

This skill provides a complete Active Inference implementation in Perl,
demonstrating Bayesian belief updating, variational free energy calculation,
and expected free energy-based policy selection.

## Core Algorithms

1. **Belief Updating**: Bayesian inference using observation likelihoods to update posterior beliefs
2. **Free Energy Calculation**: KL divergence between posterior beliefs and prior distribution
3. **Policy Selection**: Softmax action selection over expected free energy per action
4. **Perception-Action Loop**: Iterative sense → infer → act cycle with generative model

## Key Files

- `Perl_Agent.pl` — Source implementation
- `run.sh` — Execution script (handles compilation if needed)
- `README.md` — Usage documentation and requirements

## Usage

```bash
cd 0_CONTEXT/Computer_Languages/Perl/
./run.sh
```

## Language-Specific Features

- Rapid prototyping and iteration
- Dynamic typing flexibility
- Rich standard library

## Integration

- Tested via `master_controller.py test perl`
- Benchmarked via `benchmark_suite.py`
- Listed in `languages.json` under category "Scripting"

## Prerequisites

See `README.md` for Perl-specific installation requirements.

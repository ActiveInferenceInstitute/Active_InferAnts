---
name: Active Inference in Elixir
description: Elixir implementation of Active Inference with OTP GenServer, belief updating, free energy minimization, and policy selection
---

# Active Inference in Elixir

## Overview

This skill provides a complete Active Inference implementation in Elixir,
demonstrating Bayesian belief updating, variational free energy calculation,
and expected free energy-based policy selection using OTP patterns.

## Core Algorithms

1. **Belief Updating**: Bayesian inference using observation likelihoods to update posterior beliefs
2. **Free Energy Calculation**: KL divergence between posterior beliefs and prior distribution
3. **Policy Selection**: Softmax action selection over expected free energy per action
4. **Perception-Action Loop**: Iterative sense → infer → act cycle with generative model

## Key Files

- `lib/active_inference.ex` — Core module (normalize, KL divergence, softmax)
- `lib/active_inference/agent.ex` — GenServer Agent (belief updating, EFE, policy)
- `lib/active_inference/application.ex` — OTP Application supervisor
- `demo.exs` — Interactive demo script
- `mix.exs` — Mix project configuration
- `run.sh` — Execution script (handles compilation if needed)
- `README.md` — Usage documentation and requirements

## Usage

```bash
cd 0_CONTEXT/Computer_Languages/Elixir/
./run.sh
```

## Language-Specific Features

- OTP GenServer for stateful agent
- Supervision tree for fault tolerance
- Functional pipeline composition
- Pattern matching for observation dispatch

## Integration

- Tested via `master_controller.py test elixir`
- Benchmarked via `benchmark_suite.py`
- Listed in `languages.json` under category "Functional"

## Prerequisites

See `README.md` for Elixir-specific installation requirements.

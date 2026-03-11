# Active Inference Implementation in Prolog

This directory contains a Prolog implementation expressing Active Inference as logical predicates and facts, enabling declarative belief updating and policy selection.

## Overview

The Prolog implementation provides:
- Core Active Inference generative model (A, B, C, D matrices)
- Bayesian belief updating via observation likelihood
- Free energy calculation and policy selection
- Simulation loop with configurable parameters

## Core Components

- **`active_inference.pl`**: Main Active Inference agent implementation
- **`run.sh`**: Build and execution script

## Key Features

- **Declarative fact-based generative models**
- **Unification-based belief updating**
- **Backtracking for policy search**

## Architecture

### Generative Model

The implementation defines the standard Active Inference generative model:

- **A matrix** (Likelihood): Maps hidden states to observations — P(o|s)
- **B matrix** (Transition): State transition probabilities given actions — P(s'|s,a)
- **C vector** (Preferences): Observation preferences driving goal-directed behavior
- **D vector** (Prior): Prior beliefs over initial hidden states

### Inference Loop

1. **Observe**: Receive observation from environment
2. **Update beliefs**: Bayesian posterior = likelihood × prior, normalized
3. **Evaluate policies**: Calculate expected free energy for each action
4. **Select action**: Choose policy minimizing expected free energy
5. **Transition**: Environment updates state based on action

## Dependencies

- SWI-Prolog 8.0+

## Building and Running

```bash
# Via run script
./run.sh

# Manual build
swipl -s active_inference.pl -g start -t halt
```

## Configuration

The implementation uses a standard 4-state, 3-observation, 2-action generative model:
- **States**: 4 hidden states with uniform prior
- **Observations**: 3 observation channels
- **Actions**: 2 available actions

## References

1. **Friston, K. (2010)**: The free-energy principle: a unified brain theory?
2. **Da Costa, L., et al. (2020)**: Active inference on discrete state-spaces
3. **Parr, T., & Friston, K. (2019)**: Generalised free energy and active inference

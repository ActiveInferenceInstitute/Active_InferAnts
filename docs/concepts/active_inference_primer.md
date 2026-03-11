# Active Inference Primer

## What is Active Inference?

Active Inference is a unified theory of brain function (and, more broadly, adaptive systems) proposing that all living systems minimize a quantity called **variational free energy**. This framework, developed primarily by Karl Friston, unifies perception, action, learning, and decision-making under a single mathematical objective.

## Core Principles

### 1. The Free Energy Principle (FEP)

Any self-organizing system that persists in a changing environment must act to minimize surprise (technically, the long-run average of surprisal). Since surprise is intractable to compute directly, organisms minimize an upper bound called **variational free energy**.

### 2. Generative Models

Every agent maintains an internal **generative model** — a probabilistic model of how the environment generates observations:

```
P(observations, states) = P(observations | states) × P(states)
                          ─────────────────────    ─────────
                          Likelihood (A matrix)    Prior (D vector)
```

### 3. Belief Updating (Perception)

When an agent receives an observation, it updates its beliefs about hidden states using Bayes' rule:

```
P(state | observation) ∝ P(observation | state) × P(state)
     posterior           ───────────────────────   ──────
                              A matrix              prior
```

### 4. Action Selection

Actions are selected to minimize **expected free energy** (EFE), which balances:
- **Pragmatic value** — achieving preferred outcomes (exploitation)
- **Epistemic value** — reducing uncertainty about the world (exploration)

```
G(π) = E_π[log Q(s) - log P(o|s) - log P(o)]
       ─────────────   ───────────   ─────────
       information     accuracy      pragmatic
       gain                          value
```

### 5. Learning

Over longer timescales, agents update the parameters of their generative model (the A, B, C, D matrices themselves) based on accumulated experience.

## Implementation in Active InferAnts

### The Generative Model (A/B/C/D Matrices)

| Matrix | Shape | Role | Active InferAnts Default |
|--------|-------|------|--------------------------|
| **A** | (obs × states) | Likelihood mapping | 3×3 identity-like |
| **B** | (states × states × actions) | Transition dynamics | 2×2 per action |
| **C** | (observations,) | Preferences | [0.0, 0.5, 0.0] |
| **D** | (states,) | Initial state prior | Uniform [0.25, 0.25, 0.25, 0.25] |

### The Perception-Action Loop

```
                    ┌──────────────┐
                    │  Environment │
                    └──────┬───────┘
                           │ observation
                           ▼
                    ┌──────────────┐
                    │  Perceive    │  Bayesian belief updating
                    │  (A matrix)  │  posterior = A × prior
                    └──────┬───────┘
                           │ beliefs
                           ▼
                    ┌──────────────┐
                    │  Evaluate    │  Expected free energy
                    │  Policies    │  for each action sequence
                    └──────┬───────┘
                           │ policy
                           ▼
                    ┌──────────────┐
                    │  Act         │  Execute selected action
                    │  (B matrix)  │  Environment transitions
                    └──────┬───────┘
                           │ action
                           ▼
                    ┌──────────────┐
                    │  Environment │  State transition
                    │  transitions │  s' ~ B(·|s, a)
                    └──────────────┘
```

### PyMDP Integration

Active InferAnts uses [PyMDP](https://github.com/infer-actively/pymdp) for the Python reference implementation:

```python
from pymdp import inference, control, utils

# Create generative model
A = utils.random_A_matrix(num_obs, num_states)
B = utils.random_B_matrix(num_states, num_actions)

# Perception: update beliefs given observation
qs = inference.update_posterior_states(A, observation, prior=D)

# Action selection: minimize expected free energy
policies = control.construct_policies(num_states, num_actions)
G = control.get_expected_states(qs, B, policies)
action = control.sample_action(G, policies)
```

## Key References

1. Friston, K. (2010). *The free-energy principle: a unified brain theory?* Nature Reviews Neuroscience, 11(2), 127-138.
2. Da Costa, L., et al. (2020). *Active inference on discrete state-spaces: A synthesis.* Journal of Mathematical Psychology, 99.
3. Parr, T., Pezzulo, G., & Friston, K. (2022). *Active Inference: The Free Energy Principle in Mind, Brain, and Behavior.* MIT Press.
4. Smith, R., et al. (2022). *A step-by-step tutorial on active inference.* Journal of Mathematical Psychology, 107.

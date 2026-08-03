# Generative Model Architecture

The mathematical foundation used by the language implementations where the discrete-state model is implemented.

## Active Inference Generative Model

Active InferAnts implements the discrete-state Active Inference framework with the standard generative model:

### State Space

- **Hidden States**: 4 states (default), representing internal environmental conditions
- **Observations**: 3 observation channels
- **Actions**: 2 available actions

### Matrices

The canonical dimensions follow the registry contract: A is observation×state
(3×4), B is state×action×state (4×2×4), C is over observations (3), and D is
over states (4).

#### A Matrix — Likelihood Model

Maps hidden states to observations. P(o|s).

```
A = [[0.8, 0.1, 0.05, 0.05],
     [0.1, 0.8, 0.05, 0.05],
     [0.1, 0.1, 0.9, 0.9]]
```

Each column sums to 1 (for each hidden state, observations sum to 1).

#### B Matrix — Transition Model

State transition probabilities given actions. P(s'|s,a). With 4 states and 2
actions this is a 4×2×4 tensor; the action-0 slice is the identity (stay) and
the action-1 slice is a cyclic shift (move):

```
B[:, :, 0] = [[1, 0, 0, 0],
              [0, 1, 0, 0],
              [0, 0, 1, 0],
              [0, 0, 0, 1]]

B[:, :, 1] = [[0, 0, 0, 1],
              [1, 0, 0, 0],
              [0, 1, 0, 0],
              [0, 0, 1, 0]]
```

Each column of each action slice sums to 1.

#### C Vector — Preferences

Observation preferences driving goal-directed behavior.

```
C = [0.0, 0.5, 0.0]
```

#### D Vector — Prior

Prior beliefs over initial hidden states.

```
D = [0.25, 0.25, 0.25, 0.25]  # Uniform prior
```

## Inference Loop

1. **Observe**: Receive observation from environment
2. **Infer**: Bayesian posterior = likelihood × prior (normalized)
3. **Evaluate**: Calculate expected free energy for each policy
4. **Select**: Choose action minimizing expected free energy
5. **Act**: Execute action; environment transitions state

## PyMDP Integration

The Python reference implementation uses `pymdp`:

```python
from pymdp import inference, control, utils

# Belief updating
posterior = inference.update_posterior_states(A, observation, prior)

# Policy selection
policy = control.construct_policies(num_states, num_actions)
G = control.get_expected_states(posterior, B, policy)
action = control.sample_action(G, policy)
```

## References

1. Friston, K. (2010). The free-energy principle: a unified brain theory?
2. Da Costa, L., et al. (2020). Active inference on discrete state-spaces
3. Parr, T., Pezzulo, G., & Friston, K. (2022). Active Inference

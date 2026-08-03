# Tutorial: Your First Agent

Build a minimal Active Inference agent from scratch.

## Prerequisites

```bash
pip install numpy pymdp
```

## Step 1: Define the Generative Model

```python
import numpy as np

# Observation likelihood: 3 observations, 4 hidden states (columns sum to 1)
A = np.array([
    [0.8, 0.1, 0.05, 0.05],
    [0.1, 0.8, 0.05, 0.05],
    [0.1, 0.1, 0.9, 0.9]
])

# Transition model: 4 states × 4 states × 2 actions
B = np.zeros((4, 4, 2))
B[:,:,0] = np.eye(4)                    # Action 0: stay
B[:,:,1] = np.roll(np.eye(4), 1, axis=0) # Action 1: move

# Preferences: prefer observation 0
C = np.array([1.0, 0.0, -1.0])

# Prior: uniform over states
D = np.array([0.25, 0.25, 0.25, 0.25])
```

## Step 2: Implement Belief Updating

```python
def update_beliefs(A, observation, prior):
    """Bayesian belief update: posterior ∝ likelihood × prior"""
    likelihood = A[observation, :]
    posterior = likelihood * prior
    posterior /= posterior.sum()  # Normalize
    return posterior
```

## Step 3: Implement Action Selection

```python
def expected_free_energy(A, B, C, beliefs, action):
    """Compute expected free energy for a given action."""
    # Predicted next state
    predicted_state = B[:, :, action] @ beliefs
    # Predicted observation
    predicted_obs = A @ predicted_state
    # Pragmatic value (preference alignment)
    pragmatic = np.sum(predicted_obs * C)
    # Epistemic value (information gain)
    epistemic = -np.sum(predicted_obs * np.log(predicted_obs + 1e-16))
    return -(pragmatic + epistemic)

def select_action(A, B, C, beliefs, num_actions=2):
    """Select action minimizing expected free energy."""
    G = [expected_free_energy(A, B, C, beliefs, a) for a in range(num_actions)]
    return np.argmin(G)
```

## Step 4: Run the Loop

```python
beliefs = D.copy()
for t in range(100):
    observation = np.random.choice(3, p=A[:, np.argmax(beliefs)])
    beliefs = update_beliefs(A, observation, beliefs)
    action = select_action(A, B, C, beliefs)
    beliefs = B[:, :, action] @ beliefs
    print(f"t={t}: obs={observation}, action={action}, beliefs={beliefs.round(3)}")
```

## Next Steps

- See [Agent Types](../concepts/agent_types.md) for the full agent hierarchy
- See [Running Simulations](../guides/running_simulations.md) for pipeline execution

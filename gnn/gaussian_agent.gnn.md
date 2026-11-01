# Active InferAnts Gaussian Agent - GNN specification
# Generalized Notation Notation (GNN) specification of the framework agent in
# the active_infer_ants package (active_infer_ants/agent.py): a static-latent
# linear-Gaussian model whose posterior is the agent's precision-weighted
# belief update.
# Validated against the pinned GNN revision in gnn/upstream.json.

## GNNSection
ActInfContinuous

## GNNVersionAndFlags
GNN v1

## ModelName
Active InferAnts Gaussian Agent

## ModelAnnotation
The Active InferAnts framework agent (active_infer_ants.ActiveInferenceAgent)
as a native linear-Gaussian state-space model. The latent state is static:
the agent fuses a Gaussian prior over its preferred state with a Gaussian
observation, and returns the posterior mean as its action.

- x: the latent state (the agent's belief mean), dimension n_dims.
- y: the observation vector; an identity readout of x (H = I).
- F = I: the latent state does not drift between steps.
- Q = (1 / prior_precision) I: prior covariance of the static latent
  (default prior_precision = 2.0, so Q = 0.5 I).
- R = (1 / sensory_precision) I: observation-noise covariance
  (default sensory_precision = 5.0, so R = 0.2 I).
- prior_mean: the agent's preferred state (starts at zeros).
- prior_cov: (1 / prior_precision) I, matching Q.

The declared parameterization is the package default (n_dims = 3, the default
``complexity`` of InferenceModel / ActiveInferenceAgent.from_config). The
agent's infer() performs the exact Gaussian posterior update implied by these
matrices; learn(reward) moves prior_mean toward the posterior mean at
``learning_rate``. The returned action is the posterior mean: the generative
model itself has no control input, and the environment consumes the action.

## StateSpaceBlock
# Continuous latent state (belief mean)
x[3,1,type=float]         # Latent state
# Continuous observation (sensory input)
y[3,1,type=float]         # Observation
# State transition matrix (static latent)
F[3,3,type=float]         # Dynamics: identity
# Observation matrix
H[3,3,type=float]         # Readout: identity
# Process-noise covariance
Q[3,3,type=float]         # Prior covariance of the static latent
# Observation-noise covariance
R[3,3,type=float]         # Sensory-noise covariance
# Gaussian prior over the latent state
prior_mean[3,type=float]  # Preferred state
prior_cov[3,3,type=float] # Prior covariance
# Time index
t[1,type=int]             # Discrete time step

## Connections
prior_mean>x
F>x
x>y
H>y
Q>x
R>y

## InitialParameterization
# F: static latent state (no drift between steps).
F={
  (1.0, 0.0, 0.0),
  (0.0, 1.0, 0.0),
  (0.0, 0.0, 1.0)
}

# H: identity readout of the latent state.
H={
  (1.0, 0.0, 0.0),
  (0.0, 1.0, 0.0),
  (0.0, 0.0, 1.0)
}

# Q: prior covariance of the static latent; Q = (1 / prior_precision) I with
# the package default prior_precision = 2.0.
Q={
  (0.5, 0.0, 0.0),
  (0.0, 0.5, 0.0),
  (0.0, 0.0, 0.5)
}

# R: observation-noise covariance; R = (1 / sensory_precision) I with the
# package default sensory_precision = 5.0.
R={
  (0.2, 0.0, 0.0),
  (0.0, 0.2, 0.0),
  (0.0, 0.0, 0.2)
}

# Gaussian prior over the initial belief: the agent's preferred state starts
# at zeros with the same covariance as Q.
prior_mean={(0.0, 0.0, 0.0)}
prior_cov={
  (0.5, 0.0, 0.0),
  (0.0, 0.5, 0.0),
  (0.0, 0.0, 0.5)
}

## Equations
# Generative model (linear-Gaussian state-space, static latent):
#   x ~ N(prior_mean, prior_cov)
#   y = H x + N(0, R)
#   x_t+1 = F x_t + N(0, Q)          # F = I: no drift
# Exact posterior (the agent's infer()):
#   Pi_post = H^T R^-1 H + Q^-1 = (1/sensory_precision + 1/prior_precision) I
#   mu_post = Pi_post^-1 (H^T R^-1 y + Q^-1 prior_mean)
# The returned action is mu_post; learn(reward) updates
#   prior_mean <- prior_mean + learning_rate * (mu_post - prior_mean)

## Time
Dynamic
DiscreteTime=t
ModelTimeHorizon=1

## ActInfOntologyAnnotation
F=StateTransitionMatrix
H=ObservationMatrix
Q=ProcessNoiseCovariance
R=ObservationNoiseCovariance
prior_mean=PriorMean
prior_cov=PriorCovariance
x=ContinuousHiddenState
y=ContinuousObservation
t=Time

## ModelParameters
num_states: 3
num_observations: 3
num_timesteps: 1
prior_precision: 2.0
sensory_precision: 5.0
learning_rate: 0.1

## Footer
Active InferAnts Gaussian Agent v1 - GNN representation of the
active_infer_ants framework agent (static-latent linear-Gaussian model).

## Signature
pending

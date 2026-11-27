# Methods

The continuous Python agent combines a preferred prior mean with a vector observation. If prior and sensory precisions are $p_0$ and $p_s$, the posterior precision is $p_0 + p_s$ and the posterior mean is $(p_0 m_0 + p_s o)/(p_0+p_s)$. The agent turns the posterior-to-target mismatch into an action with a configurable step size [@agent]. This update is applied to the vector elements in the implemented model. The GNN document records the Gaussian structure checked against this implementation [@specification].

The discrete-state examples in the framework should be evaluated against their own language registry entries and matrix contracts. This distinction matters when comparing continuous Gaussian belief updates to the observation and action indices used by a categorical model.

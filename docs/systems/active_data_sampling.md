# Active Data Sampling

Optimal experimental design using Active Inference.

## Location

`0_CONTEXT/Systems/Active_Data_Sampling/`

## Pipeline

| Stage | Module | Description |
|-------|--------|-------------|
| Methods | `Methods_ActiveDataSampling.py` | NumPy-based sampling methods |
| Run | `Run_ActiveDataSampling.py` | NumPy execution of sampling experiment |
| Analysis | `Analysis_ActiveDataSampling.py` | Statistical analysis of results |
| Visualization | `Visualization_ActiveDataSampling.py` | Matplotlib plot generation |

## Concept

Active Data Sampling applies Active Inference to experimental design: the agent selects which data points to sample next, minimizing expected free energy to maximize information gain (epistemic value) while achieving experimental goals (pragmatic value).

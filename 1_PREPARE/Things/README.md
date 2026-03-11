# Things — Active Inference Agents

Agent implementations, digital twins, and PyMDP-based Active Inference entities.

## Modules

| Module | Description |
|---|---|
| `InferAnts.py` | Core `ActiveNestmate` and `ActiveColony` classes with NumPy-based generative models |
| `Thing.py` | Base `Thing` using PyMDP (`inference`, `control`, `utils`) for generic Active Inference entities |
| `initialize_Nestmate_Colony.py` | Colony initialization: creates `ActiveNestmate` populations with configuration |
| `pseudo-pymdp_Ant_1.py` | Pseudo-PyMDP ant agent variant 1 with tabulated state display |
| `pseudo-pymdp_Ant_2.py` | Pseudo-PyMDP ant agent variant 2 with tabulated state display |
| `pymdp_Ant_1.py` | Full PyMDP ant agent using `pymdp.inference` and `pymdp.control` |

## Related

- Parent: [1_PREPARE](../README.md)

# Pheromone Signaling

Chemical communication for stigmergic coordination in Active InferAnts.

## Module: `1_PREPARE/General/Pheromones.py`

Implements pheromone-based indirect communication between agents.

## Architecture

| Component | Description |
|-----------|-------------|
| `Enum` chemical types | Distinct pheromone species (trail, alarm, recruitment) |
| Diffusion model | Spatial pheromone spreading using NumPy |
| Decay functions | Time-dependent evaporation |
| Concentration fields | 2D arrays of pheromone concentrations |

## Stigmergic Coordination

Agents don't communicate directly. Instead:

1. **Deposit** — Agent deposits pheromone at current location
2. **Diffuse** — Pheromone spreads spatially (diffusion equation)
3. **Decay** — Pheromone evaporates over time (exponential decay)
4. **Sense** — Other agents observe local pheromone concentrations
5. **Act** — Agents bias actions toward high-concentration areas

## Active Inference Connection

In the Active Inference framework, pheromone concentrations are **observations** that inform the agent's posterior beliefs. Pheromone deposition is an **action** that modifies the environment, influencing future observations for other agents.

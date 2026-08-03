# Data Flow

How data transforms as it moves through the Active InferAnts pipeline.

## Pipeline Data Flow

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  0_CONTEXT   │    │  1_PREPARE   │    │  2_OPERATE   │
│  Languages,  │───▶│  Agents,     │───▶│  Simulation  │
│  Systems,    │    │  Configs,    │    │  Execution   │
│  Specs       │    │  Methods     │    │              │
└─────────────┘    └─────────────┘    └──────┬──────┘
                                              │
                                              ▼
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  5_FOLLOWUP  │    │  4_REPORT    │    │  3_MEASURE   │
│  Sessions,   │◀───│  Async       │◀───│  Statistics, │
│  Stakeholder │    │  Reports     │    │  Functors,   │
│  Engagement  │    │              │    │  Categories  │
└──────┬──────┘    └─────────────┘    └─────────────┘
       │
       ▼
┌─────────────┐    ┌─────────────┐
│   6_API      │    │   9_OTHER    │
│  REST APIs   │    │  Kafka,      │
│  Knowledge   │    │  Nostr, etc. │
└─────────────┘    └─────────────┘
```

## Key Data Structures

### Generative Model (A/B/C/D Matrices)

The language implementations use a shared A/B/C/D generative-model vocabulary where applicable; the canonical registry is `0_CONTEXT/Computer_Languages/languages.json`.

| Matrix | Name | Shape | Description |
|--------|------|-------|-------------|
| **A** | Likelihood | (obs × states) | P(observation \| hidden state) |
| **B** | Transition | (states × actions × states) | P(next_state \| state, action) |
| **C** | Preferences | (observations,) | Log-preferences over observations |
| **D** | Prior | (states,) | Prior beliefs over initial states |

### Simulation Trace

Output from `2_OPERATE`, consumed by `3_MEASURE`:
- Agent positions, belief trajectories, action histories
- Cognitive load scores and behavioral metrics
- Environmental state evolution

### Measurement Output

Output from `3_MEASURE`, consumed by `4_REPORT`:
- `CategoryTheoryAnalyzer` graph structures
- `SimulationSummary` statistical tables
- `QRFParameters` measurement specifications

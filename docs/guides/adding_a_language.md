# Adding a Language Implementation

How to add a new programming language to the Active InferAnts framework.

## Directory Structure

Create `0_CONTEXT/Computer_Languages/<LanguageName>/`:

```
<LanguageName>/
├── AGENTS.md           # Agent guidance (use template below)
├── README.md           # Language-specific documentation
├── SPEC.md             # Technical specification
├── active_inference.*  # Main implementation file
└── run.sh              # Build and run script
```

## Implementation Requirements

Every language implementation must include:

### 1. Generative Model (A/B/C/D Matrices)

```
A matrix: 3×3 observation likelihood
B matrix: 2×2 transition probabilities
C vector: 3-element observation preferences
D vector: 4-element state prior (uniform)
```

### 2. Core Functions

| Function | Description |
|----------|-------------|
| Initialize agent | Set up A, B, C, D matrices and belief state |
| Update beliefs | Bayesian posterior = likelihood × prior |
| Calculate free energy | Expected free energy for policy evaluation |
| Select action | Choose action minimizing expected free energy |
| Step | Execute one inference-action cycle |

### 3. Run Script (`run.sh`)

```bash
#!/bin/bash
# Build and run the Active Inference implementation
<compile_command>
<run_command>
```

## AGENTS.md Template

```markdown
# AGENTS.md — <Language Name>

> Agent guidance for the `0_CONTEXT/Computer_Languages/<Language>` directory.

## Purpose

<Language> implementation of Active Inference for the Active InferAnts framework.

## Directory Contents

- 📄 `active_inference.*` — Main implementation
- 📄 `run.sh` — Build and execution script

## Agent Instructions

- Maintain generative model consistency (A/B/C/D matrices).
- Ensure run.sh works with standard toolchain.
- Follow the repository's CC BY-NC-ND 4.0 license.
```

## Testing

Use the benchmark suite:

```bash
cd 0_CONTEXT/Computer_Languages
python3 benchmark_suite.py
```

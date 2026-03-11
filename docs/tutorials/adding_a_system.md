# Tutorial: Adding a System

Create a new specialized system in `0_CONTEXT/Systems/`.

## Step 1: Create Directory Structure

```bash
mkdir -p 0_CONTEXT/Systems/MySystem
```

## Step 2: Create Documentation Triad

Create `AGENTS.md`, `README.md`, and `SPEC.md` following the established patterns.

## Step 3: Implement Core Modules

Typical system structure:

```
MySystem/
├── AGENTS.md
├── README.md
├── SPEC.md
├── main.py              # Entry point
├── MySystem.py           # Core implementation
├── Run_MySystem.py       # Execution wrapper
├── Analysis_MySystem.py  # Analysis module
└── Visualization_MySystem.py  # Visualization
```

## Step 4: Follow Naming Conventions

- Use `PascalCase` for system names
- Use `snake_case` for module files
- Use descriptive module prefixes (`Analysis_`, `Run_`, `Visualization_`)

## Existing Systems to Reference

| System | Modules | Pattern |
|--------|---------|---------|
| Active Data Sampling | 4 | Methods → Run → Analysis → Visualization |
| Cognitive Sovereignty | 5 | Generate → Simulate → Analyze (3-stage) |
| P3IF | 6 | Core → Run → Synthesize → Analyze → Visualize |
| William Blake | 5 | Analysis → Entity Extraction → NLP |
| IC2S2 | 8 | Main + 7 utility modules |

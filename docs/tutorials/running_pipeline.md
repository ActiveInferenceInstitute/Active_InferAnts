# Tutorial: Running the Pipeline

Execute the full 6-phase pipeline end-to-end.

> The `2_OPERATE` scripts (`plan_Simulation.py`, `execute_Simulation.py`,
> `render_Simulation.py`) are wired to the `active_infer_ants` package and run
> end-to-end; see `tests/test_simulation_pipeline.py` for the integration
> suite.

## Phase 1: Prepare

```bash
cd 1_PREPARE

# Review configuration
cat ../config.json

# Agent definitions are in Things/
ls Things/*.py
```

## Phase 2: Operate

```bash
cd ../2_OPERATE

# Step 1: Plan the simulation
python3 plan_Simulation.py

# Step 2: Execute the simulation
python3 execute_Simulation.py

# Step 3: Render visualization
python3 render_Simulation.py
```

## Phase 3: Measure

```bash
cd ../3_MEASURE

# Statistical analysis
python3 statistics.py

# Graph-based categorization
python3 categorization.py

# Entropy-based summarization
python3 summarize.py
```

## Phase 4: Report

```bash
cd ../4_REPORT
python3 execute_report.py
```

## Phase 5: Follow-Up

```bash
cd ../5_FOLLOWUP
python3 execute_followup.py
```

## Phase 6: API (Optional)

```bash
cd ../6_API
uvicorn Knowledge_API:app --reload
# Visit http://localhost:8000/api/docs for the Swagger UI
```

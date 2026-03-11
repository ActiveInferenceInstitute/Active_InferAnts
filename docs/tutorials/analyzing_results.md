# Tutorial: Analyzing Results

Using 3_MEASURE tools for statistical analysis of simulation outputs.

## Using SimulationSummary

```python
from statistics import SimulationSummary

# Load simulation data
summary = SimulationSummary(data)
summary.compute_statistics()
summary.generate_plots()
```

## Using CognitiveUtilities

```python
from cognitive_utilities import CognitiveUtilities

cu = CognitiveUtilities(simulation_data)

# Behavioral analysis
behavior = cu.analyze_agent_behavior()
# Returns: {agent_id: {total_distance, activity_levels}}

# Cognitive load assessment
load = cu.evaluate_cognitive_load()
# Returns: {agent_id: load_score}

# Decision support
support = cu.generate_decision_support(agent_id="agent_1")
# Returns: {behavior_analysis, cognitive_load, recommendations}

# Visualization
cu.visualize_behavior_metrics(behavior, save_path="metrics.png")
cu.visualize_cognitive_load_distribution(load, save_path="load_dist.png")

# Export
summary = cu.summarize_cognitive_insights(behavior, load)
cu.export_summary(summary,
    json_path="results.json",
    csv_path="results.csv",
    excel_path="results.xlsx")
```

## Using CategoryTheoryAnalyzer

```python
from categorization import CategoryTheoryAnalyzer

analyzer = CategoryTheoryAnalyzer()
# Build category graph from results
# Compose morphisms
# Extract functorial patterns
```

## Using PolyFunctor

```python
from poly_functor import ListFunctor, MaybeFunctor, TreeFunctor

# Apply transformations across different data structures
list_f = ListFunctor()
result = list_f.hmap(lambda x: x * 2, [1, 2, 3])  # [2, 4, 6]

maybe_f = MaybeFunctor()
result = maybe_f.hmap(lambda x: x + 1, None)  # None
result = maybe_f.hmap(lambda x: x + 1, 5)     # 6
```

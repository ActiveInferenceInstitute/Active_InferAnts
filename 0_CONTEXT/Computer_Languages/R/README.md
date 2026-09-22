# Active Inference in R

A statistical computing implementation of the Active Inference framework using R's powerful data analysis and visualization capabilities.

## Overview

This R implementation provides:

- 📊 **Statistical Analysis**: Comprehensive statistical analysis and visualization
- 🔬 **Data-Driven**: Matrix operations and probability distributions
- 📈 **Time Series**: Belief evolution and performance tracking
- 🎯 **Interactive**: Command-line interface with detailed output

## Features

### Core Components

- **`ActiveInferenceAgent`**: R6 class-based agent implementation
- **Statistical Analysis**: Belief updating with proper normalization
- **CSV/TSV Output**: Structured data export for analysis
- **Performance Metrics**: Comprehensive statistics tracking
- **Multi-Agent Environment**: Ant colony simulation

### Mathematical Foundations

The implementation uses a complete generative model:

- **A Matrix**: Likelihood mapping `p(o|s)` - probability of observations given states
- **B Matrix**: Transition model `p(s'|s,a)` - state transitions given actions
- **C Vector**: Preferences `p(o)` - preferred observations
- **D Vector**: Prior beliefs `p(s)` - initial state beliefs

## Installation

### Prerequisites

- **R**: Version 4.0+ (download from [CRAN](https://cran.r-project.org/))
- **R6**: Object-oriented programming for R

### Installing Dependencies

```R
# Install required packages
install.packages("R6")
install.packages("MASS")
install.packages("Matrix")
```

### Running the Implementation

```bash
# Navigate to the R directory
cd Active_InferAnts/0_CONTEXT/Computer_Languages/R

# Run single agent demo
Rscript active_inference.R single-agent

# Run ant colony demo
Rscript active_inference.R ant-colony

# Run both demos
Rscript active_inference.R demo
```

## Core Concepts

### Object-Oriented Design with R6

```R
# Create agent with custom configuration
agent <- ActiveInferenceAgent$new(
    n_states = 3,
    n_observations = 3,
    n_actions = 3,
    learning_rate = 0.1,
    uncertainty_weight = 0.1,
    output_dir = "output/single_agent"
)
```

### Belief Updating

```R
# Bayesian belief updating
update_beliefs <- function(observation) {
    likelihood <- A_matrix[observation, ]
    posterior <- current_beliefs * likelihood
    current_beliefs <<- posterior / sum(posterior)
    return(current_beliefs)
}
```

### Free Energy Minimization

```R
# Calculate variational free energy
calculate_vfe <- function() {
    expected_likelihood <- calculate_expected_likelihood()
    entropy <- calculate_entropy(current_beliefs)
    return(-expected_likelihood - entropy)
}
```

### Expected Free Energy

```R
# Calculate expected free energy for action selection
calculate_efe <- function(action) {
    predicted_beliefs <- predict_beliefs(action)
    pragmatic_value <- calculate_pragmatic_value(predicted_beliefs)
    epistemic_value <- calculate_epistemic_value(predicted_beliefs)
    return(list(
        expected = pragmatic_value - uncertainty_weight * epistemic_value,
        pragmatic = pragmatic_value,
        epistemic = epistemic_value
    ))
}
```

## Examples

### Single Agent Demo

```bash
Rscript active_inference.R single-agent
```

Demonstrates:
- Agent initialization with statistical parameter validation
- Belief updating through Bayesian inference
- Action selection via expected free energy minimization
- Comprehensive performance statistics
- CSV export of belief evolution and actions

### Multi-Agent Simulation

```bash
Rscript active_inference.R ant-colony
```

Features:
- Statistical modeling of pheromone communication
- Multi-agent coordination through environment interaction
- Emergent collective behavior analysis
- Spatial distribution analysis of pheromones and food

## Output Files

### Single Agent Results

- **`statistics.txt`**: Complete agent statistics and configuration
- **`belief_history.csv`**: Time series of belief states over time
- **`action_history.csv`**: Sequence of selected actions with observations
- **`free_energy_history.csv`**: Free energy values over time

### Multi-Agent Results

- **`pheromone_grid.csv`**: Spatial distribution of home and food pheromones
- **`food_grid.csv`**: Food source locations and remaining amounts
- **Individual ant results**: Each ant saves its own belief and action history

## Architecture

### Project Structure

```
R/
├── active_inference.R     # Main implementation and demos
└── output/                # Generated results (created automatically)
    ├── single_agent/
    │   ├── statistics.txt
    │   ├── belief_history.csv
    │   └── action_history.csv
    └── ant_colony/
        ├── pheromone_grid.csv
        └── food_grid.csv
```

### Key Classes

#### `ActiveInferenceAgent`

Main agent class implementing active inference:

- **Statistical Methods**: Proper probability normalization and entropy calculation
- **Matrix Operations**: Efficient linear algebra for belief propagation
- **Data Persistence**: CSV export for analysis and visualization
- **Performance Tracking**: Comprehensive statistics and timing
- **Validation**: Input parameter checking and error handling

#### `AntColonyEnvironment`

Multi-agent environment:

- **Spatial Modeling**: 2D grid-based environment representation
- **Pheromone Dynamics**: Statistical modeling of pheromone diffusion
- **Agent Interaction**: Coordinated multi-agent behavior
- **Resource Management**: Food source allocation and consumption

## Performance

### Statistical Efficiency

- **Vectorized Operations**: R's vectorized operations for efficient computation
- **Matrix Algebra**: BLAS-optimized linear algebra operations
- **Memory Management**: Efficient data structures for large simulations
- **Statistical Functions**: Optimized statistical distributions and calculations

### Benchmarking

```R
# Performance measurement
start_time <- Sys.time()
# ... simulation code ...
end_time <- Sys.time()
execution_time <- difftime(end_time, start_time, units = "secs")
```

## Advanced Features

### Statistical Analysis

```R
# Belief evolution analysis
belief_df <- read.csv("output/single_agent/belief_history.csv")
plot(belief_df$Step, belief_df$State0, type = "l",
     xlab = "Time Step", ylab = "Belief Probability",
     main = "Belief Evolution Over Time")
```

### Data Export and Analysis

```R
# Comprehensive statistics export
stats <- agent$get_statistics()
write.table(as.data.frame(stats), "statistics.txt", sep = "\t")

# Time series analysis
belief_matrix <- do.call(rbind, belief_history)
belief_evolution <- apply(belief_matrix, 2, function(x) c(mean(x), sd(x), min(x), max(x)))
```

### Multi-Agent Coordination

```R
# Statistical analysis of collective behavior
pheromone_stats <- sapply(pheromone_grid, function(row) {
    c(mean = mean(unlist(row)), sd = sd(unlist(row)))
})

# Agent performance comparison
agent_stats <- lapply(ants, function(ant) ant$agent$get_statistics())
performance_df <- do.call(rbind, agent_stats)
```

## Future Extensions

- [ ] Statistical visualization with ggplot2
- [ ] Advanced statistical modeling with MCMC
- [ ] Time series analysis of belief evolution
- [ ] Machine learning integration with caret
- [ ] Web dashboard with Shiny
- [ ] Parallel processing with foreach
- [ ] Advanced statistical testing and validation

## Contributing

### Development Guidelines

1. **Statistical Rigor**: All implementations must use proper statistical methods
2. **Data Validation**: Input parameter checking and error handling
3. **Documentation**: Comprehensive inline documentation and examples
4. **Performance**: Efficient vectorized operations where possible
5. **Reproducibility**: Set random seeds for reproducible results

### Code Style

- Follow R coding best practices and style guides
- Use meaningful variable names and comprehensive comments
- Implement proper error handling with tryCatch
- Create reproducible examples with set.seed()
- Document all functions with proper Roxygen2 comments

## References

### Key Papers

1. **Friston, K. (2010)**: The free-energy principle: a unified brain theory?
2. **Da Costa, L., et al. (2020)**: Active inference on discrete state-spaces
3. **Parr, T., & Friston, K. (2019)**: Generalised free energy and active inference

### R Resources

1. **R Language Definition**: Official R documentation
2. **Advanced R**: Comprehensive R programming guide
3. **R Packages**: CRAN package documentation

## License

MIT License - see LICENSE file for details.

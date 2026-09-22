# Active Inference in Haskell

A functional programming implementation of the Active Inference framework using Haskell's strong type system, purity, and mathematical elegance.

## Overview

This Haskell implementation provides:

- 🧠 **Strong Type Safety**: Compile-time guarantees with Haskell's type system
- 🔧 **Functional Purity**: Pure functions with referential transparency
- 📊 **Mathematical Elegance**: Direct translation of mathematical concepts
- 🎯 **Type-Driven Development**: Types guide implementation and catch errors
- 📈 **Performance**: Efficient lazy evaluation and optimization

## Features

### Core Components

- **`ActiveInference.Core`**: Core types and fundamental functions
- **`ActiveInference.Agent`**: Agent implementation with belief updating
- **`ActiveInference.Environment`**: Multi-agent environments
- **Standalone Demos**: Complete executable demonstrations
- **CSV/JSON Output**: Results saved to structured files

### Mathematical Foundations

The implementation uses a complete generative model:

- **A Matrix**: Likelihood mapping `p(o|s)` - probability of observations given states
- **B Matrix**: Transition model `p(s'|s,a)` - state transitions given actions
- **C Vector**: Preferences `p(o)` - preferred observations
- **D Vector**: Prior beliefs `p(s)` - initial state beliefs

## Installation

### Prerequisites

- **GHC**: Glasgow Haskell Compiler (9.0+)
- **Cabal**: Haskell build system
- **Stack**: Optional, alternative build system

### Building with Stack

```bash
# Navigate to the Haskell directory
cd Active_InferAnts/0_CONTEXT/Computer_Languages/Haskell

# Install dependencies and build
stack build

# Run single agent demo
stack exec active-inference-demo single-agent

# Run ant colony demo
stack exec active-inference-demo ant-colony

# Run both demos
stack exec active-inference-demo both
```

### Building with Cabal

```bash
# Install dependencies
cabal update
cabal install --dependencies-only

# Build the project
cabal build

# Run demos
cabal run active-inference-demo -- single-agent
cabal run active-inference-demo -- ant-colony
```

### Standalone Script Execution

```bash
# If you have stack installed globally
stack Main.hs

# Or compile and run
ghc Main.hs
./Main single-agent
```

## Core Concepts

### Type-Safe Configuration

```haskell
data AgentConfig = AgentConfig
    { nStates :: Int
    , nObservations :: Int
    , nActions :: Int
    , learningRate :: Probability
    , uncertaintyWeight :: Probability
    , precision :: Probability
    , enableLogging :: Bool
    , outputDirectory :: FilePath
    , randomSeed :: Int
    } deriving (Show, Eq)
```

### Pure Functions for Belief Updating

```haskell
-- Pure belief updating
updateBeliefs :: GenerativeModel -> Vector Probability -> Observation -> Vector Probability
updateBeliefs model beliefs observation =
    let likelihood = getObservationLikelihood model observation
        posterior = V.zipWith (*) beliefs likelihood
    in normalizeVector posterior
```

### Free Energy Minimization

```haskell
-- Variational free energy calculation
calculateFreeEnergy :: GenerativeModel -> Vector Probability -> VFE
calculateFreeEnergy model beliefs =
    let expectedLikelihood = calculateExpectedLikelihood model beliefs
        entropy = calculateEntropy beliefs
    in VFE (-expectedLikelihood - entropy)
```

### Expected Free Energy

```haskell
-- Expected free energy for action selection
calculateExpectedFreeEnergy :: ActiveInferenceAgent -> Action -> FreeEnergy
calculateExpectedFreeEnergy agent action =
    let predictedBeliefs = predictBeliefs (generativeModel agent) (currentBeliefs agent) action
        pragmaticValue = calculatePragmaticValue agent predictedBeliefs
        epistemicValue = calculateEpistemicValue agent predictedBeliefs
    in pragmaticValue - uncertaintyWeight (config agent) * epistemicValue
```

## Examples

### Single Agent Demo

```bash
stack exec active-inference-demo single-agent
```

Demonstrates:
- Agent initialization with type-safe configuration
- Belief updating through perception-action cycles
- Free energy minimization
- Comprehensive statistics and results saving

### Multi-Agent Simulation

```bash
stack exec active-inference-demo ant-colony
```

Features:
- Concurrent ant agents with individual active inference
- Pheromone-based communication
- Food foraging behavior
- Emergent collective intelligence

## Architecture

### Project Structure

```
Haskell/
├── package.yaml          # Project configuration
├── src/
│   ├── ActiveInference/
│   │   ├── Core.hs       # Core types and functions
│   │   ├── Agent.hs      # Agent implementation
│   │   └── Environment.hs # Multi-agent environments
│   └── Main.hs           # Standalone demo script
├── app/
│   └── Main.hs           # Executable entry point
└── output/               # Generated results (created automatically)
    ├── single_agent/
    │   ├── statistics.txt
    │   ├── belief_history.csv
    │   └── action_history.csv
    └── ant_colony/
        ├── simulation_results.json
        └── simulation_steps.csv
```

### Key Features

#### Strong Type System

```haskell
-- Compile-time guarantees
validateConfig :: AgentConfig -> Either String AgentConfig
validateConfig config
    | nStates config <= 0 = Left "Number of states must be positive"
    | otherwise = Right config
```

#### Pure Functions

```haskell
-- Pure belief updating with no side effects
stepAgent :: ActiveInferenceAgent -> Observation -> IO ActiveInferenceAgent
stepAgent agent observation = do
    let updatedBeliefs = updateBeliefs (generativeModel agent) (currentBeliefs agent) observation
        action = selectAction agent
        -- ... pure transformations
    pure updatedAgent
```

#### Efficient Data Structures

```haskell
-- Type-safe matrices and vectors
type Matrix = M.Matrix Probability
type Vector = V.Vector Probability
type LikelihoodMatrix = Matrix
type TransitionMatrices = V.Vector Matrix
```

## Output Files

### Single Agent Results

- **`statistics.txt`**: Complete agent statistics and configuration
- **`belief_history.csv`**: Time series of belief states over time
- **`action_history.csv`**: Sequence of selected actions
- **`free_energy_history.csv`**: Free energy values over time

### Multi-Agent Results

- **`simulation_results.json`**: Complete simulation data with all steps
- **`simulation_steps.csv`**: Step-by-step simulation statistics
- **Individual agent results**: Each ant saves its own results

## Mathematical Foundations

### Generative Model

The implementation faithfully represents the mathematical structure:

```
p(o,s) = p(o|s) * p(s)           -- Likelihood and prior
p(s'|s,a) = B[s',s,a]            -- State transitions
F(s) = -E_q[ln p(o,s)] + H[q(s)] -- Variational free energy
G(a) = E_{q(s'|a)}[F(s')]        -- Expected free energy
```

### Belief Updating

Bayesian belief updating is implemented purely:

```haskell
updateBeliefs :: GenerativeModel -> Vector Probability -> Observation -> Vector Probability
updateBeliefs model beliefs obs =
    let likelihood = A ! obs  -- Row of likelihood matrix
        posterior = beliefs * likelihood  -- Element-wise multiplication
    in normalize posterior    -- Normalize to probability distribution
```

### Action Selection

Expected free energy minimization:

```haskell
selectAction :: ActiveInferenceAgent -> Action
selectAction agent =
    let efes = [calculateExpectedFreeEnergy agent action | action <- [0..nActions-1]]
        (bestAction, _) = minimumBy (comparing snd) (zip [0..] efes)
    in bestAction
```

## Performance

### Optimization Features

- **Lazy Evaluation**: Computations only when needed
- **Immutable Data**: Pure functions with persistent data structures
- **Vector Operations**: Efficient bulk operations with Data.Vector
- **Matrix Operations**: Optimized linear algebra with Data.Matrix

### Benchmarking

```haskell
-- Example performance measurement
timeAction :: IO a -> IO (a, Double)
timeAction action = do
    start <- getCurrentTime
    result <- action
    end <- getCurrentTime
    let duration = realToFrac $ diffUTCTime end start
    pure (result, duration)
```

## Advanced Features

### Type-Driven Development

```haskell
-- Types guide implementation
data EFE = EFE
    { expectedFE :: FreeEnergy
    , pragmaticValue :: FreeEnergy
    , epistemicValue :: FreeEnergy
    } deriving (Show, Eq, Ord)

-- Type-safe configuration validation
validateConfig :: AgentConfig -> Either String AgentConfig
```

### Functional Composition

```haskell
-- Compose perception and action
perceptionActionCycle :: ActiveInferenceAgent -> Observation -> IO ActiveInferenceAgent
perceptionActionCycle = updateBeliefs >=> selectAction >=> executeAction
```

### Monadic Agent State

```haskell
-- Agent state in State monad
type AgentState a = StateT ActiveInferenceAgent IO a

-- Pure state transformations
updateBeliefsPure :: Observation -> AgentState ()
updateBeliefsPure observation = do
    agent <- get
    let updatedBeliefs = ActiveInference.Core.updateBeliefs
                        (generativeModel agent)
                        (currentBeliefs agent)
                        observation
    put agent { currentBeliefs = updatedBeliefs }
```

## Future Extensions

- [ ] Parallel multi-agent simulation with Control.Parallel
- [ ] GPU acceleration with accelerate
- [ ] Advanced learning mechanisms (meta-learning)
- [ ] Integration with machine learning frameworks
- [ ] Real-time performance monitoring
- [ ] Web interface with Scotty/Yesod

## Contributing

### Development Guidelines

1. **Type Safety**: All code must pass strict type checking
2. **Pure Functions**: Minimize side effects, maximize purity
3. **Documentation**: Comprehensive Haddock documentation
4. **Testing**: Property-based tests with QuickCheck
5. **Performance**: Profile-guided optimization

### Code Style

- Follow Haskell style guidelines
- Use meaningful type names and documentation
- Leverage type system for correctness
- Write property-based tests
- Maintain functional purity where possible

## References

### Key Papers

1. **Friston, K. (2010)**: The free-energy principle: a unified brain theory?
2. **Da Costa, L., et al. (2020)**: Active inference on discrete state-spaces
3. **Parr, T., & Friston, K. (2019)**: Generalised free energy and active inference

### Haskell Resources

1. **Haskell Programming Language**: Official Haskell documentation
2. **Learn You a Haskell**: Comprehensive beginner tutorial
3. **Real World Haskell**: Practical Haskell programming

## License

MIT License - see LICENSE file for details.

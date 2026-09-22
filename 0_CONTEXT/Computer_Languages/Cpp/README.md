# Active Inference in C++

A high-performance, type-safe implementation of the Active Inference framework using modern C++ with Eigen for efficient matrix operations.

## Overview

This C++ implementation provides:

- 🚀 **High Performance**: Optimized matrix operations with Eigen
- 🛡️ **Type Safety**: Strong compile-time type checking
- 📊 **Comprehensive Error Handling**: Custom exception types with detailed messages
- 🧪 **Template Metaprogramming**: Generic algorithms for mathematical operations
- 📈 **Performance Monitoring**: Detailed timing and statistics

## Features

### Core Components

- **`ActiveInferenceAgent`**: Main agent implementation with RAII resource management
- **Custom Exception Types**: `ActiveInferenceError`, `BeliefUpdateError`, `PolicySelectionError`
- **Template Utilities**: Generic functions for probability distributions and matrix operations
- **Performance Monitoring**: Comprehensive statistics and timing
- **Multi-Agent Environment**: Ant colony simulation with concurrent agents

### Mathematical Foundations

The implementation uses a complete generative model:

- **A Matrix**: Likelihood mapping `p(o|s)` - probability of observations given states
- **B Matrix**: Transition model `p(s'|s,a)` - state transitions given actions
- **C Vector**: Preferences `p(o)` - preferred observations
- **D Vector**: Prior beliefs `p(s)` - initial state beliefs

## Installation

### Prerequisites

- **CMake**: Version 3.16 or higher
- **C++ Compiler**: GCC 8.0+, Clang 7.0+, or MSVC 2019+
- **Eigen Library**: Version 3.4 or higher

### Building

```bash
# Clone and navigate to the directory
cd Active_InferAnts/0_CONTEXT/Computer_Languages/Cpp

# Create build directory
mkdir build && cd build

# Configure with CMake
cmake ..

# Build the project
make

# Run the demo
./active_inference_demo
```

### Dependencies

```bash
# Ubuntu/Debian
sudo apt-get install libeigen3-dev

# macOS with Homebrew
brew install eigen

# Or install Eigen manually from http://eigen.tuxfamily.org/
```

## Core Concepts

### Type-Safe Agent Configuration

```cpp
struct AgentConfig {
    int nStates = 3;           // Number of hidden states
    int nObservations = 3;     // Number of observation types
    int nActions = 3;          // Number of possible actions
    double learningRate = 0.1; // Learning rate for belief updates
    double uncertaintyWeight = 0.1; // Weight for epistemic value
    double precision = 1.0;    // Precision parameter
    bool verbose = false;      // Enable verbose logging
};
```

### Perception-Action Cycle

```cpp
ActiveInferenceAgent agent(config);

// Perception-action loop
int observation = 1;
int action = agent.step(observation);

std::cout << "Selected action: " << action << std::endl;
std::cout << "Free energy: " << agent.calculateVariationalFreeEnergy() << std::endl;
```

### Error Handling

```cpp
try {
    int action = agent.step(observation);
    std::cout << "Action selected: " << action << std::endl;
} catch (const BeliefUpdateError& e) {
    std::cerr << "Belief update failed: " << e.what() << std::endl;
} catch (const PolicySelectionError& e) {
    std::cerr << "Policy selection failed: " << e.what() << std::endl;
}
```

## Mathematical Foundations

### Free Energy Minimization

Active inference minimizes variational free energy:

```
F = E_q[ln q(s) - ln p(o,s)]
```

Where:
- `q(s)`: Current beliefs about hidden states
- `p(o,s)`: Generative model likelihood

### Expected Free Energy

Actions are selected by minimizing expected free energy:

```
G(π) = E_{q(s'|π)}[ln q(s'|π) - ln p(o'|s')] + γ H[q(s'|π)]
```

## Examples

### Single Agent Demo

```bash
cd build
./active_inference_demo
```

Shows a single active inference agent learning through interaction.

### Multi-Agent Simulation

```cpp
AntColonyEnvironment::EnvironmentConfig config;
config.gridSize = 10;
config.nAnts = 8;
config.foodSources = 3;
config.pheromoneDecay = 0.95;

AntColonyEnvironment environment(config);
environment.runSimulation(100);
```

## Architecture

### Project Structure

```
Cpp/
├── CMakeLists.txt          # Build configuration
├── include/
│   └── ActiveInferenceAgent.h  # Main header file
├── src/
│   ├── main.cpp           # Demo program
│   ├── ActiveInferenceAgent.cpp # Agent implementation
│   └── ...                # Additional source files
└── tests/                 # Unit tests (future)
```

### Key Classes

#### `ActiveInferenceAgent`

Main agent class implementing active inference:

- **RAII Design**: Automatic resource management
- **Template Methods**: Generic mathematical operations
- **Error Handling**: Comprehensive exception safety
- **Performance Monitoring**: Detailed statistics tracking
- **Thread Safety**: Designed for concurrent environments

#### Custom Exception Hierarchy

```cpp
class ActiveInferenceError : public std::runtime_error {
public:
    explicit ActiveInferenceError(const std::string& message)
        : std::runtime_error(message) {}
};

class BeliefUpdateError : public ActiveInferenceError {
    // Specialized for belief updating failures
};

class PolicySelectionError : public ActiveInferenceError {
    // Specialized for policy selection failures
};
```

## Performance

### Benchmarks

- **Matrix Operations**: Eigen-optimized linear algebra
- **Memory Usage**: Efficient data structures with minimal overhead
- **Compilation**: Fast compile times with header-only Eigen
- **Runtime**: Optimized for real-time applications

### Optimization Features

- **SIMD Operations**: Vectorized mathematical operations
- **Cache-Friendly**: Optimized data layouts
- **Template Specialization**: Compile-time optimization
- **Move Semantics**: Efficient object transfer

## Advanced Features

### Template Metaprogramming

```cpp
template<typename Derived>
bool isProbabilityVector(const Eigen::DenseBase<Derived>& vec, double tolerance = 1e-6) {
    // Compile-time probability distribution validation
    return vec.minCoeff() >= -tolerance && std::abs(vec.sum() - 1.0) < tolerance;
}
```

### RAII Resource Management

```cpp
class ActiveInferenceAgent {
private:
    Eigen::MatrixXd A, B, C, D;  // Automatically managed matrices
    std::mt19937 rng;             // RAII random number generator
    AgentHistory history;         // Automatically managed history
};
```

### Comprehensive Statistics

```cpp
auto statistics = agent.getStatistics();
std::cout << "Total steps: " << statistics["totalSteps"] << std::endl;
std::cout << "Average free energy: " << statistics["averageFreeEnergy"] << std::endl;
std::cout << "Action distribution: " << std::endl;
for (int i = 0; i < config.nActions; ++i) {
    std::cout << "  Action " << i << ": " << statistics["action" + std::to_string(i) + "Count"] << std::endl;
}
```

## Building and Testing

### Debug Build

```bash
cd build
cmake -DCMAKE_BUILD_TYPE=Debug ..
make
```

### Release Build

```bash
cd build
cmake -DCMAKE_BUILD_TYPE=Release ..
make
```

### Running Tests (Future)

```bash
cd build
ctest --verbose
```

## Future Extensions

- [ ] Unit test suite with Google Test
- [ ] Performance benchmarking suite
- [ ] Parallel multi-agent simulation
- [ ] GPU acceleration with CUDA
- [ ] Real-time visualization interface
- [ ] Integration with ROS for robotics
- [ ] Advanced learning mechanisms (meta-learning)

## Contributing

### Development Guidelines

1. **RAII Principle**: All resources managed through RAII
2. **Exception Safety**: Strong exception guarantee where possible
3. **Performance**: Profile-guided optimization
4. **Documentation**: Comprehensive Doxygen comments
5. **Testing**: Unit tests for all new functionality

### Code Style

- Follow C++ Core Guidelines
- Use modern C++17 features
- Template metaprogramming for generic algorithms
- Comprehensive error handling
- Performance-conscious design

## References

### Key Papers

1. **Friston, K. (2010)**: The free-energy principle: a unified brain theory?
2. **Da Costa, L., et al. (2020)**: Active inference on discrete state-spaces
3. **Parr, T., & Friston, K. (2019)**: Generalised free energy and active inference

### C++ Resources

1. **C++ Core Guidelines**: Modern C++ best practices
2. **Eigen Documentation**: Matrix library reference
3. **Modern C++ Design**: Advanced C++ techniques

## License

MIT License - see LICENSE file for details.

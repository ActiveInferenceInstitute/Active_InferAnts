# Active Inference in TypeScript

A type-safe, production-ready implementation of the Active Inference framework with comprehensive error handling, detailed logging, and educational examples.

## Overview

This TypeScript implementation provides:

- 🛡️ **Type Safety**: Strong static typing prevents runtime errors
- 📊 **Comprehensive Monitoring**: Detailed logging and performance metrics
- 🧪 **Error Handling**: Custom error types with context information
- 🎓 **Educational**: Well-documented code with extensive examples
- 🏗️ **Modular Architecture**: Clean separation of concerns

## Features

### Core Components

- **`ActiveInferenceAgent`**: Main agent implementation with type-safe operations
- **Custom Error Types**: `ActiveInferenceError`, `BeliefUpdateError`, `PolicySelectionError`
- **Comprehensive Logging**: Detailed tracking of agent behavior and performance
- **Mathematical Utilities**: Type-safe matrix and vector operations

### Type System

```typescript
interface AgentConfig {
    readonly nStates: number;
    readonly nObservations: number;
    readonly nActions: number;
    readonly learningRate: number;
    readonly uncertaintyWeight: number;
    readonly precision: number;
}

interface FreeEnergy {
    readonly variational: number;
    readonly expected: number;
    readonly pragmatic: number;
    readonly epistemic: number;
}
```

## Installation

```bash
# Install dependencies
npm install

# Build the project
npm run build

# Run the ant colony demo
npm run demo

# Run tests
npm test

# Type checking
npm run type-check
```

## Core Concepts

### Type-Safe Agent

```typescript
const config: AgentConfig = {
    nStates: 3,
    nObservations: 3,
    nActions: 3,
    learningRate: 0.1,
    uncertaintyWeight: 0.1,
    precision: 1.0
};

const agent = new ActiveInferenceAgent(config);
```

### Perception-Action Cycle

```typescript
// Type-safe perception-action loop
const observation: Observation = 1;
const action: Action = agent.step(observation);

console.log(`Action: ${action}`);
console.log(`Free Energy: ${agent.calculateVariationalFreeEnergy()}`);
```

### Error Handling

```typescript
try {
    const action = agent.step(observation);
    console.log(`Selected action: ${action}`);
} catch (error) {
    if (error instanceof PolicySelectionError) {
        console.error(`Policy selection failed: ${error.message}`);
        console.error(`Context:`, error.context);
    }
}
```

## Mathematical Foundations

### Generative Model

The implementation uses a complete generative model:

- **A Matrix**: Likelihood mapping `p(o|s)` - probability of observations given states
- **B Matrix**: Transition model `p(s'|s,a)` - state transitions given actions
- **C Vector**: Preferences `p(o)` - preferred observations
- **D Vector**: Prior beliefs `p(s)` - initial state beliefs

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
npm run demo
```

Shows a single active inference agent learning through interaction.

### Multi-Agent Simulation

```typescript
import { AntColonyEnvironment } from './src/demos/ant-colony-demo.js';

const config: EnvironmentConfig = {
    gridSize: 10,
    nAnts: 8,
    foodSources: 3,
    pheromoneDecay: 0.95,
    maxSteps: 100
};

const environment = new AntColonyEnvironment(config);
const results = environment.runSimulation(50);
```

## Architecture

### Project Structure

```
src/
├── types.ts              # Type definitions and interfaces
├── ActiveInferenceAgent.ts # Main agent implementation
├── demos/
│   └── ant-colony-demo.ts   # Multi-agent simulation demo
└── utils/                # Utility functions (future)
```

### Key Classes

#### `ActiveInferenceAgent`

Main agent class implementing active inference:

- **Type-safe operations**: All methods have strong typing
- **Error handling**: Comprehensive error catching and reporting
- **Performance monitoring**: Detailed statistics and logging
- **Modular design**: Clean separation of concerns

#### Custom Error Types

```typescript
class ActiveInferenceError extends Error {
    constructor(
        message: string,
        public readonly code: string,
        public readonly context?: Record<string, any>
    ) {
        super(message);
    }
}
```

## Performance

### Benchmarks

- **Type Checking**: Compile-time safety with minimal runtime overhead
- **Memory Usage**: Efficient matrix operations with mathjs
- **Error Handling**: Fast error detection and recovery
- **Scalability**: Type-safe multi-agent coordination

### Optimization Features

- **Immutable Data Structures**: Where appropriate for safety
- **Efficient Matrix Operations**: Optimized linear algebra
- **Lazy Evaluation**: On-demand computation of complex metrics
- **Memory Pooling**: Reused data structures to minimize GC pressure

## Educational Value

### Learning Objectives

1. **Type Safety**: Understanding benefits of strong typing
2. **Error Handling**: Comprehensive error management strategies
3. **Active Inference**: Core concepts and mathematical foundations
4. **Software Architecture**: Modular, maintainable code design
5. **Testing**: Type-driven development and testing strategies

### Code Examples

The implementation includes:

- **Detailed Comments**: Extensive inline documentation
- **Working Examples**: Complete runnable demonstrations
- **Error Scenarios**: Examples of proper error handling
- **Performance Analysis**: Statistics and monitoring tools

## Development

### Building

```bash
# Development build with source maps
npm run build

# Watch mode for development
npm run dev
```

### Testing

```bash
# Run all tests
npm test

# Coverage needs a jest flag: this package.json has no test:coverage script
npm test -- --coverage

# Type checking only
npm run type-check
```

### Linting

```bash
# Check code style
npm run lint

# Auto-fix needs an eslint flag: this package.json has no lint:fix script
npm run lint -- --fix
```

## Advanced Features

### Custom Error Types

- `BeliefUpdateError`: Belief updating failures
- `PolicySelectionError`: Action selection failures
- `ActiveInferenceError`: General framework errors

### Comprehensive Logging

```typescript
const history = agent.getHistory();
const statistics = agent.getStatistics();

console.log(`Total steps: ${statistics.totalSteps}`);
console.log(`Average free energy: ${statistics.averageFreeEnergy}`);
console.log(`Action distribution:`, statistics.actionDistribution);
```

### Type-Safe Configuration

```typescript
const config: AgentConfig = {
    nStates: 4,
    nObservations: 3,
    nActions: 4,
    learningRate: 0.1,
    uncertaintyWeight: 0.2,
    precision: 1.0
};
```

## Future Extensions

- [ ] Web dashboard for real-time visualization
- [ ] Performance profiling and optimization
- [ ] Advanced learning mechanisms (meta-learning)
- [ ] Distributed multi-agent systems
- [ ] Integration with machine learning frameworks
- [ ] Real-time performance monitoring

## Contributing

### Development Guidelines

1. **Type Safety**: All code must pass strict TypeScript checks
2. **Error Handling**: Comprehensive error catching and reporting
3. **Documentation**: Detailed JSDoc comments for all public APIs
4. **Testing**: Unit tests for all new functionality
5. **Performance**: Consider performance implications of changes

### Code Style

- Use interfaces for all data structures
- Implement proper error handling
- Include comprehensive JSDoc documentation
- Follow TypeScript best practices
- Maintain type safety throughout

## References

### Key Papers

1. **Friston, K. (2010)**: The free-energy principle: a unified brain theory?
2. **Da Costa, L., et al. (2020)**: Active inference on discrete state-spaces
3. **Parr, T., & Friston, K. (2019)**: Generalised free energy and active inference

### TypeScript Resources

1. **TypeScript Handbook**: Official language documentation
2. **TypeScript Deep Dive**: Comprehensive online book
3. **Effective TypeScript**: Best practices guide

## License

MIT License - see package.json for details.

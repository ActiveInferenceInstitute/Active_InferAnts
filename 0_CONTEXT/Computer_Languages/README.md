# Active Inference / Free Energy Principle Implementations

This directory contains implementations of the Active Inference / Free Energy Principle across multiple programming languages. Each implementation demonstrates core concepts of active inference including belief updating, policy selection, and free energy minimization.

## Overview

Active Inference is a framework for understanding perception, action, and learning in biological and artificial agents. It formalizes the idea that agents act to minimize surprise or prediction error by maintaining internal models of the world.

### Core Concepts Implemented

- **Generative Models**: Internal models of how observations are generated from hidden states
- **Belief Updating**: Bayesian inference to update beliefs about hidden states
- **Expected Free Energy**: Calculation of expected surprise under different policies
- **Policy Selection**: Choosing actions that minimize expected free energy
- **Perception-Action Loop**: Continuous cycle of sensing, inference, and action

## Language Implementations

| Language | Status | Description | Key Features | Dependencies |
|----------|--------|-------------|--------------|--------------|
| **Brainfuck** | ✅ Complete | Esoteric language implementation with sophisticated cognitive processes | Memory-efficient, minimalistic | None |
| **C** | ✅ Complete | Low-level systems implementation | High performance, teacher-student model | Standard library only |
| **C++** | ✅ Complete | Object-oriented implementation with templates | Generic programming, RAII, high performance | Standard library, Eigen (recommended) |
| **C#** | ✅ Complete | .NET implementation with LINQ | Modern syntax, async support | .NET Standard |
| **COBOL** | ✅ Complete | Enterprise legacy structured implementation | Fixed-point arithmetic, data division | GnuCOBOL |
| **Common Lisp** | ✅ Complete | Symbolic computation implementation | S-expressions, CLOS, macros | SBCL/CLISP/ECL |
| **D** | ✅ Complete | Systems metaprogramming implementation | Compile-time features, templates | DMD/LDC2/GDC |
| **Dart** | ✅ Complete | Flutter ecosystem implementation | Null safety, class system | Dart SDK 2.12+ |
| **Golang** | ✅ Complete | Concurrent agent-based simulation | Goroutines, channels, ant colony simulation | Standard library only |
| **Groovy** | ✅ Complete | JVM scripting implementation | GDK enhancements, closures | Groovy 3.0+ |
| **Haskell** | ✅ Complete | Functional programming approach | Pure functions, monads, type safety, lazy evaluation | Haskell Platform |
| **Java** | ✅ Complete | Object-oriented ant colony simulation | JVM ecosystem, Bayesian inference | Standard library only |
| **JavaScript** | ✅ Complete | Node.js implementation | Event-driven, npm ecosystem, ant colony simulation | Node.js, mathjs, plotly.js |
| **Jock** | ✅ Complete | Functional language for distributed systems | Category theory, Urbit integration | Urbit runtime |
| **Julia** | ✅ Complete | Scientific computing implementation | High-performance, RxInfer integration | Julia ecosystem |
| **Kotlin** | ✅ Complete | Modern JVM language implementation | Concise syntax, coroutines, type safety | Kotlin/JVM, Gradle |
| **MATLAB/Octave** | ✅ Complete | Matrix-based implementation | Signal processing, visualization, control systems | MATLAB/Octave |
| **Objective-C** | ✅ Complete | Apple legacy Foundation implementation | NSMutableArray, message passing | Xcode CLT |
| **Perl** | ✅ Complete | Dynamic language implementation | Text processing, CPAN modules | Standard library |
| **PHP** | ✅ Complete | Web-oriented implementation | Web integration, Composer, modern PHP features | PHP 8.0+ |
| **PowerShell** | ✅ Complete | Cross-platform automation implementation | .NET integration, pipeline | PowerShell 5.1+/pwsh |
| **Python** | ✅ Complete | Scientific implementation with numpy | Rich ecosystem, Student-Teacher POMDP | numpy, scipy, matplotlib |
| **R** | ✅ Complete | Statistical programming implementation | Statistical analysis, visualization, data export | R ecosystem |
| **Ruby** | ✅ Complete | Dynamic object-oriented implementation | Elegant syntax, gems, metaprogramming | Ruby 2.5+ |
| **Rust** | ✅ Complete | Systems programming implementation | Memory safety, performance | ndarray, thiserror |
| **Scala** | ✅ Complete | Functional JVM language | Type system, functional programming | Scala ecosystem |
| **Scheme** | ✅ Complete | SICP heritage functional implementation | R7RS, vectors, closures | Chibi-Scheme/Guile |
| **Shell** | ✅ Complete | Command-line implementation | System integration, pipes | POSIX shell |
| **Solidity** | ✅ Complete | Blockchain smart contract implementation | WAD fixed-point, events, EVM | solc 0.8+ |
| **SQL** | ✅ Complete | Database-driven implementation | Declarative programming, queries | SQLite/PostgreSQL |
| **Swift** | ✅ Complete | Modern systems programming | Type safety, performance, Apple ecosystem | Swift ecosystem |
| **Tcl** | ✅ Complete | Extensible scripting implementation | Dicts, dynamic typing, Tk toolkit | Tcl 8.5+ |
| **TypeScript** | ✅ Complete | Typed JavaScript implementation | Static typing, comprehensive error handling | Node.js, TypeScript, mathjs |
| **Ada** | ✅ Complete | Safety-critical systems implementation | Strong typing, concurrency, reliability | GNAT, Ada standard library |
| **Assembly** | ✅ Complete | Low-level hardware implementation | Direct hardware control, optimization | NASM/GAS assembler |
| **Clojure** | ✅ Complete | Functional Lisp implementation | Immutable data, JVM ecosystem | Leiningen, Clojure standard library |
| **Crystal** | ✅ Complete | Ruby-like compiled implementation | Performance, type safety, macros | Crystal standard library |
| **Elixir** | ✅ Complete | Distributed functional implementation | Erlang VM, fault-tolerance, OTP | Mix, Erlang ecosystem |
| **Erlang** | ✅ Complete | Concurrent distributed implementation | Actor model, fault-tolerance | Erlang/OTP standard library |
| **F#** | ✅ Complete | Functional .NET implementation | Type providers, async workflows | .NET Core, F# ecosystem |
| **Fortran** | ✅ Complete | Scientific computing implementation | Numerical computing, performance | Fortran standard library |
| **Lua** | ✅ Complete | Lightweight embeddable implementation | Fast, simple, extensible | Lua standard library |
| **Nim** | ✅ Complete | Python-like systems implementation | Performance, expressiveness, macros | Nim standard library |
| **OCaml** | ✅ Complete | Functional systems implementation | Type inference, performance | OCaml standard library |
| **Odin** | ✅ Complete | Modern systems alternative to C | Manual memory management, SIMD | Odin compiler |
| **Pascal** | ✅ Complete | Educational structured implementation | Clear syntax, teaching focused | Free Pascal, Lazarus |
| **Prolog** | ✅ Complete | Logic programming implementation | Declarative, constraint solving | SWI-Prolog, constraint libraries |
| **Racket** | ✅ Complete | Lisp dialect educational implementation | Language-oriented programming | Racket standard library |
| **V** | ✅ Complete | Simple fast compiled implementation | C interop, data-oriented | V compiler |
| **Zig** | ✅ Complete | Modern systems implementation | Safety, performance, C replacement | Zig standard library |

## Implementation Patterns

### Core Components

Each implementation typically includes:

1. **Agent Structure**: Defines the agent's internal state and parameters
2. **Generative Model**: A, B, C, D matrices or equivalent structures
3. **Inference Engine**: Belief updating and policy selection algorithms
4. **Environment Interface**: Interaction with external world
5. **Visualization/Analysis**: Results display and analysis tools

### Common Approaches

- **Student-Teacher Models**: Learning through interaction (Python, C)
- **Ant Colony Optimization**: Swarm intelligence (Java, Golang)
- **POMDP Frameworks**: Partially observable decision processes
- **Bayesian Networks**: Probabilistic graphical models
- **Category Theory**: Mathematical structure preservation (Jock, Haskell)

## Getting Started

### Prerequisites

Most implementations require only standard libraries. For advanced features:

```bash
# Python
pip install numpy scipy matplotlib

# Julia
using Pkg; Pkg.add("RxInfer")

# Rust
cargo add ndarray thiserror

# JavaScript/TypeScript
npm install @types/node
```

### Running Examples

Each language directory contains:

- Main implementation file(s)
- `run.sh` — automated execution script
- `README.md` — language-specific documentation

### CLI Usage

```bash
# Run all implementations sequentially
./run_all.sh

# Run a specific language
./run_all.sh python
./run_all.sh rust

# List all available languages
./run_all.sh --list

# Run in parallel
./run_all.sh --parallel

# Python master controller (richer features)
python3 master_controller.py status
python3 master_controller.py run python
python3 master_controller.py benchmark
python3 master_controller.py deps
```

See `run_all.sh --help` or `python3 master_controller.py --help` for full options.

## Architecture Patterns

### Modular Design

```
Language/
├── Core/           # Core active inference algorithms
├── Models/         # Specific model implementations
├── Environments/   # Environment interfaces
├── Utils/          # Helper functions and utilities
├── Examples/       # Usage examples
└── Tests/          # Test suites
```

### Common Interfaces

Most implementations follow similar interfaces:

```python
# Python example
class ActiveInferenceAgent:
    def __init__(self, config):
        # Initialize generative model
        pass

    def update_beliefs(self, observation):
        # Bayesian belief updating
        pass

    def select_action(self):
        # Policy selection via EFE minimization
        pass

    def step(self, observation):
        # Perception-action cycle
        pass
```

## Advanced Features

### Multi-Agent Systems

Several implementations support multiple agents:

- **Golang**: Concurrent goroutines with channels
- **Java**: Thread-safe agent colonies
- **Rust**: Async/await with tokio

### Distributed Computing

- **Jock**: Built for distributed Urbit networks
- **Rust**: Async agents with message passing
- **Golang**: Channel-based communication

### Visualization

- **Python**: matplotlib/seaborn plots
- **Julia**: Plots.jl ecosystem
- **Java**: JavaFX/Swing interfaces

## Performance Characteristics

| Language | Performance | Memory Usage | Concurrency | Ecosystem |
|----------|-------------|--------------|-------------|-----------|
| **C** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐ |
| **Rust** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Julia** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Golang** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Python** | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Java** | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Ada** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
| **Assembly** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐ | ⭐ |
| **Clojure** | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Crystal** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
| **Elixir** | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Erlang** | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **F#** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Fortran** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ |
| **Lua** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ |
| **Nim** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
| **OCaml** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Pascal** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ |
| **Prolog** | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
| **Racket** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Zig** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |

## Contributing

### Adding New Languages

1. Create language directory: `LanguageName/`
2. Implement core active inference algorithms
3. Create `run.sh` (executable) and `README.md`
4. Add the language to `languages.json` (canonical registry)
5. Run `./run_all.sh <language>` to verify
6. Update this README's language table

### Implementation Guidelines

- Follow language-specific conventions
- Include comprehensive documentation
- Provide working examples
- Implement core active inference concepts
- Handle errors gracefully

### Testing

Each implementation should include:

- Unit tests for core functions
- Integration tests for agent behavior
- Performance benchmarks
- Documentation examples

## Research Applications

### Neuroscience

- Perception and sensory processing
- Decision-making under uncertainty
- Motor control and action selection
- Learning and memory formation

### Artificial Intelligence

- Autonomous agents and robots
- Reinforcement learning
- Cognitive architectures
- Multi-agent systems

### Complex Systems

- Swarm intelligence
- Collective behavior
- Self-organization
- Adaptive systems

## References

### Key Papers

1. **Friston, K. (2010)**: The free-energy principle: a unified brain theory?
2. **Friston, K. et al. (2017)**: Active inference and learning
3. **Da Costa, L. et al. (2020)**: Active inference on discrete state-spaces
4. **Parr, T. & Friston, K. (2019)**: Generalised free energy and active inference

### Books

- Friston, K. (2019): *A free energy principle for a particular physics*
- Buckley, C. et al. (2017): *The free energy principle*

## License

This collection of implementations is provided under the CC BY-NC-ND 4.0 License consistent with the parent Active InferAnts framework.

## Acknowledgments

Implementations inspired by:

- Karl Friston's work on Active Inference
- The PyMDP library (Python)
- Various research papers and tutorials
- Open-source active inference community

---

*For questions or contributions, please see individual language directories or create an issue in the main repository.*

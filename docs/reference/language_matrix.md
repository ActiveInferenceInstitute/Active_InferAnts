# Language Implementation Matrix

All 50 programming languages registered in `0_CONTEXT/Computer_Languages/languages.json`.

| # | Language | Paradigm | Main File | Build Tool |
|---|----------|----------|-----------|------------|
| 1 | Ada | Compiled, strong typing | `active_inference.adb` | GNAT |
| 2 | Assembly | x86-64 machine code | `active_inference.asm` | NASM |
| 3 | Brainfuck | Esoteric | `Brainfuck_ActiveInference.py` | Python |
| 4 | C | Systems programming | `Active_Inference.c` | GCC |
| 5 | C# | .NET managed | `Program.cs` | dotnet |
| 6 | C++ | Systems, OOP | `src/` | CMake |
| 7 | Clojure | JVM, Lisp | `src/` | Leiningen |
| 8 | COBOL | Enterprise legacy | `active_inference.cob` | GnuCOBOL |
| 9 | Common Lisp | Functional, Lisp | `active_inference.lisp` | SBCL |
| 10 | Crystal | Ruby-like, compiled | `active_inference.cr` | Crystal |
| 11 | D | Systems metaprogramming | `active_inference.d` | DMD |
| 12 | Dart | Flutter/Google ecosystem | `active_inference.dart` | Dart |
| 13 | Elixir | BEAM VM, functional | `demo.exs` | Mix |
| 14 | Erlang | BEAM VM, concurrent | `active_inference.erl` | erlc |
| 15 | F# | .NET, functional | `ActiveInference.fs` | dotnet |
| 16 | Fortran | Scientific computing | `active_inference.f90` | gfortran |
| 17 | Go | Compiled, concurrent | `GoLang_Agent.go` | go |
| 18 | Groovy | JVM scripting | `active_inference.groovy` | Groovy |
| 19 | Haskell | Pure functional | `src/` | Stack |
| 20 | Java | JVM, OOP | `AntColony.java` | javac |
| 21 | JavaScript | Dynamic, web | `active_inference.js` | Node.js |
| 22 | Jock | Urbit, functional | `active_inference.jock` | Urbit |
| 23 | Julia | Scientific computing | `Julia_InferAnts.jl` | Julia |
| 24 | Kotlin | JVM, modern | `src/` | Gradle |
| 25 | Lua | Lightweight, embeddable | `active_inference.lua` | Lua |
| 26 | MATLAB | Numerical computing | `ActiveInferenceAgent.m` | MATLAB |
| 27 | Nim | Python-like, compiled | `active_inference.nim` | Nim |
| 28 | OCaml | Functional, typed | `active_inference.ml` | ocamlfind |
| 29 | Objective-C | Apple legacy | `active_inference.m` | clang |
| 30 | Odin | Systems programming | `active_inference.odin` | Odin |
| 31 | PHP | Web scripting | `ActiveInferenceAgent.php` | PHP |
| 32 | Pascal | Structured programming | `active_inference.pas` | FPC |
| 33 | Perl | Text processing | `Perl_Agent.pl` | Perl |
| 34 | PowerShell | Windows/cross-platform automation | `active_inference.ps1` | pwsh |
| 35 | Prolog | Logic programming | `active_inference.pl` | SWI-Prolog |
| 36 | Python | Reference implementation | `Student_Teacher.py` | Python 3 |
| 37 | R | Statistical computing | `active_inference.R` | R |
| 38 | Racket | Lisp, language-oriented | `active_inference.rkt` | Racket |
| 39 | Ruby | Dynamic, OOP | `active_inference_agent.rb` | Ruby |
| 40 | Rust | Systems, safe | `src/` | Cargo |
| 41 | SQL | Declarative, relational | `SQL.sql` | SQL client |
| 42 | Scala | JVM, functional+OOP | `src/` | sbt |
| 43 | Scheme | SICP heritage functional | `active_inference.scm` | chibi-scheme |
| 44 | Shell | Scripting | `Active_Shellference.sh` | Bash |
| 45 | Solidity | Blockchain smart contracts | `ActiveInference.sol` | solc |
| 46 | Swift | Apple ecosystem | `ActiveInferenceAgent.swift` | Swift |
| 47 | Tcl | Extensible scripting | `active_inference.tcl` | tclsh |
| 48 | TypeScript | Typed JavaScript | `src/` | tsc |
| 49 | V | Simple systems lang | `active_inference.v` | V |
| 50 | Zig | Low-level, safe | `active_inference.zig` | Zig |

The registry is authoritative for the language list and metadata. The table above is a concise reference for the implementations represented in this repository; consult `languages.json` before adding or renaming an entry.

## Orchestration Scripts

| Script | Description |
|--------|-------------|
| `run_all.sh` | Run all language implementations sequentially |
| `master_controller.py` | Orchestrate multi-language execution |
| `benchmark_suite.py` | Performance benchmarking across languages |
| `test_suite.py` | Cross-language test runner |
| `config_manager.py` | Shared configuration management |
| `reporting_system.py` | Cross-language reporting |
| `status_dashboard.sh` | Real-time status dashboard |

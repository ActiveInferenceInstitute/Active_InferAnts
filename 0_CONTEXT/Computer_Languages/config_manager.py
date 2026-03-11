#!/usr/bin/env python3
"""
Configuration Manager for Active Inference Multi-Language System

This module provides centralized configuration management for all language
implementations, including dependency checking, environment setup, and
parameter management.
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any
import platform
import importlib.util

class DependencyChecker:
    """Check and manage dependencies for all language implementations."""

    def __init__(self):
        self.system = platform.system().lower()
        self.dependencies = self._load_dependency_definitions()

    def _load_dependency_definitions(self) -> Dict[str, Dict[str, Any]]:
        """Load dependency definitions for all languages."""
        return {
            "python": {
                "checker": self._check_python_deps,
                "installer": self._install_python_deps,
                "required": ["numpy", "scipy", "matplotlib", "seaborn", "pandas"]
            },
            "java": {
                "checker": self._check_java_deps,
                "installer": self._install_java_deps,
                "required": ["java", "javac"]
            },
            "javascript": {
                "checker": self._check_nodejs_deps,
                "installer": self._install_nodejs_deps,
                "required": ["node", "npm"]
            },
            "cpp": {
                "checker": self._check_cpp_deps,
                "installer": self._install_cpp_deps,
                "required": ["gcc", "cmake"]
            },
            "rust": {
                "checker": self._check_rust_deps,
                "installer": self._install_rust_deps,
                "required": ["cargo", "rustc"]
            },
            "go": {
                "checker": self._check_go_deps,
                "installer": self._install_go_deps,
                "required": ["go"]
            },
            "haskell": {
                "checker": self._check_haskell_deps,
                "installer": self._install_haskell_deps,
                "required": ["stack", "ghc"]
            },
            "clojure": {
                "checker": self._check_clojure_deps,
                "installer": self._install_clojure_deps,
                "required": ["java", "lein"]
            },
            "elixir": {
                "checker": self._check_elixir_deps,
                "installer": self._install_elixir_deps,
                "required": ["elixir", "mix", "erl"]
            },
            "erlang": {
                "checker": self._check_erlang_deps,
                "installer": self._install_erlang_deps,
                "required": ["erl", "erlc"]
            },
            "lua": {
                "checker": self._check_lua_deps,
                "installer": self._install_lua_deps,
                "required": ["lua"]
            },
            "perl": {
                "checker": self._check_perl_deps,
                "installer": self._install_perl_deps,
                "required": ["perl"]
            },
            "r": {
                "checker": self._check_r_deps,
                "installer": self._install_r_deps,
                "required": ["R"]
            },
            "racket": {
                "checker": self._check_racket_deps,
                "installer": self._install_racket_deps,
                "required": ["racket"]
            },
            "fortran": {
                "checker": self._check_fortran_deps,
                "installer": self._install_fortran_deps,
                "required": ["gfortran"]
            },
            "ada": {
                "checker": self._check_ada_deps,
                "installer": self._install_ada_deps,
                "required": ["gnat"]
            },
            "assembly": {
                "checker": self._check_assembly_deps,
                "installer": self._install_assembly_deps,
                "required": ["nasm", "ld"]
            },
            "brainfuck": {
                "checker": self._check_brainfuck_deps,
                "installer": self._install_brainfuck_deps,
                "required": ["python3"]
            },
            "crystal": {
                "checker": self._check_crystal_deps,
                "installer": self._install_crystal_deps,
                "required": ["crystal"]
            },
            "nim": {
                "checker": self._check_nim_deps,
                "installer": self._install_nim_deps,
                "required": ["nim"]
            },
            "ocaml": {
                "checker": self._check_ocaml_deps,
                "installer": self._install_ocaml_deps,
                "required": ["ocaml"]
            },
            "pascal": {
                "checker": self._check_pascal_deps,
                "installer": self._install_pascal_deps,
                "required": ["fpc"]
            },
            "prolog": {
                "checker": self._check_prolog_deps,
                "installer": self._install_prolog_deps,
                "required": ["swipl"]
            },
            "shell": {
                "checker": self._check_shell_deps,
                "installer": self._install_shell_deps,
                "required": ["bash", "bc", "awk"]
            },
            "sql": {
                "checker": self._check_sql_deps,
                "installer": self._install_sql_deps,
                "required": ["sqlite3"]  # Can be extended for PostgreSQL, MySQL
            },
            "typescript": {
                "checker": self._check_typescript_deps,
                "installer": self._install_typescript_deps,
                "required": ["node", "npm", "tsc"]
            },
            "zig": {
                "checker": self._check_zig_deps,
                "installer": self._install_zig_deps,
                "required": ["zig"]
            },
            "v": {
                "checker": self._check_v_deps,
                "installer": self._install_v_deps,
                "required": ["v"]
            },
            "odin": {
                "checker": self._check_odin_deps,
                "installer": self._install_odin_deps,
                "required": ["odin"]
            },
            "kotlin": {
                "checker": lambda: self._check_single_command("kotlin"),
                "installer": lambda: self._print_install_url("Kotlin", "https://kotlinlang.org/docs/command-line.html"),
                "required": ["kotlin"]
            },
            "scala": {
                "checker": lambda: self._check_single_command("scala"),
                "installer": lambda: self._print_install_url("Scala", "https://www.scala-lang.org/download/"),
                "required": ["scala"]
            },
            "swift": {
                "checker": lambda: self._check_single_command("swift"),
                "installer": lambda: self._print_install_url("Swift", "https://www.swift.org/install/"),
                "required": ["swift"]
            },
            "csharp": {
                "checker": lambda: self._check_single_command("dotnet"),
                "installer": lambda: self._print_install_url("C#/.NET", "https://dotnet.microsoft.com/download"),
                "required": ["dotnet"]
            },
            "fsharp": {
                "checker": lambda: self._check_single_command("dotnet"),
                "installer": lambda: self._print_install_url("F#/.NET", "https://dotnet.microsoft.com/download"),
                "required": ["dotnet"]
            },
            "matlab": {
                "checker": lambda: self._check_single_command("matlab"),
                "installer": lambda: self._print_install_url("MATLAB", "https://www.mathworks.com/products/matlab.html"),
                "required": ["matlab"]
            },
            "ruby": {
                "checker": lambda: self._check_single_command("ruby"),
                "installer": lambda: self._print_install_url("Ruby", "https://www.ruby-lang.org/en/downloads/"),
                "required": ["ruby"]
            },
            "php": {
                "checker": lambda: self._check_single_command("php"),
                "installer": lambda: self._print_install_url("PHP", "https://www.php.net/downloads.php"),
                "required": ["php"]
            },
            "jock": {
                "checker": lambda: self._check_single_command("urbit"),
                "installer": lambda: self._print_install_url("Jock/Urbit", "https://urbit.org/getting-started"),
                "required": ["urbit"]
            },
            "d": {
                "checker": lambda: self._check_single_command("dmd"),
                "installer": lambda: self._print_install_url("D", "https://dlang.org/download.html"),
                "required": ["dmd"]
            },
            "dart": {
                "checker": lambda: self._check_single_command("dart"),
                "installer": lambda: self._print_install_url("Dart", "https://dart.dev/get-dart"),
                "required": ["dart"]
            },
            "groovy": {
                "checker": lambda: self._check_single_command("groovy"),
                "installer": lambda: self._print_install_url("Groovy", "https://groovy-lang.org/install.html"),
                "required": ["groovy"]
            },
            "commonlisp": {
                "checker": lambda: self._check_single_command("sbcl"),
                "installer": lambda: self._print_install_url("Common Lisp (SBCL)", "https://www.sbcl.org/"),
                "required": ["sbcl"]
            },
            "objectivec": {
                "checker": lambda: self._check_single_command("clang"),
                "installer": lambda: self._print_install_url("Objective-C", "https://developer.apple.com/xcode/"),
                "required": ["clang"]
            },
            "powershell": {
                "checker": lambda: self._check_single_command("pwsh"),
                "installer": lambda: self._print_install_url("PowerShell", "https://github.com/PowerShell/PowerShell"),
                "required": ["pwsh"]
            },
            "scheme": {
                "checker": lambda: self._check_single_command("chibi-scheme"),
                "installer": lambda: self._print_install_url("Scheme", "https://github.com/ashinn/chibi-scheme"),
                "required": ["chibi-scheme"]
            },
            "cobol": {
                "checker": lambda: self._check_single_command("cobc"),
                "installer": lambda: self._print_install_url("COBOL (GnuCOBOL)", "https://gnucobol.sourceforge.io/"),
                "required": ["cobc"]
            },
            "solidity": {
                "checker": lambda: self._check_single_command("solc"),
                "installer": lambda: self._print_install_url("Solidity", "https://docs.soliditylang.org/"),
                "required": ["solc"]
            },
            "tcl": {
                "checker": lambda: self._check_single_command("tclsh"),
                "installer": lambda: self._print_install_url("Tcl", "https://www.tcl-lang.org/"),
                "required": ["tclsh"]
            }
        }

    def check_language_dependencies(self, language: str) -> Tuple[bool, List[str], List[str]]:
        """Check dependencies for a specific language."""
        if language not in self.dependencies:
            return False, [], [f"Unknown language: {language}"]

        dep_info = self.dependencies[language]
        checker = dep_info["checker"]
        return checker()

    def install_language_dependencies(self, language: str) -> bool:
        """Install dependencies for a specific language."""
        if language not in self.dependencies:
            print(f"❌ Unknown language: {language}")
            return False

        dep_info = self.dependencies[language]
        installer = dep_info["installer"]
        return installer()

    # Language-specific dependency checkers and installers
    def _check_python_deps(self) -> Tuple[bool, List[str], List[str]]:
        """Check Python dependencies."""
        available = []
        missing = []
        required = ["numpy", "scipy", "matplotlib", "seaborn", "pandas"]

        for pkg in required:
            try:
                importlib.import_module(pkg.replace("-", "_"))
                available.append(pkg)
            except ImportError:
                missing.append(pkg)

        return len(missing) == 0, available, missing

    def _install_python_deps(self) -> bool:
        """Install Python dependencies."""
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "numpy", "scipy", "matplotlib", "seaborn", "pandas"],
                         check=True, capture_output=True)
            return True
        except subprocess.CalledProcessError:
            return False

    def _check_java_deps(self) -> Tuple[bool, List[str], List[str]]:
        """Check Java dependencies."""
        available = []
        missing = []

        if self._command_exists("java"):
            available.append("java")
        else:
            missing.append("java")

        if self._command_exists("javac"):
            available.append("javac")
        else:
            missing.append("javac")

        return len(missing) == 0, available, missing

    def _install_java_deps(self) -> bool:
        """Install Java dependencies."""
        if self.system == "linux":
            try:
                subprocess.run(["sudo", "apt-get", "update"], check=True, capture_output=True)
                subprocess.run(["sudo", "apt-get", "install", "-y", "default-jre", "default-jdk"],
                             check=True, capture_output=True)
                return True
            except subprocess.CalledProcessError:
                return False
        else:
            print("❌ Automatic Java installation not supported on this platform")
            return False

    def _check_nodejs_deps(self) -> Tuple[bool, List[str], List[str]]:
        """Check Node.js dependencies."""
        available = []
        missing = []

        if self._command_exists("node"):
            available.append("node")
        else:
            missing.append("node")

        if self._command_exists("npm"):
            available.append("npm")
        else:
            missing.append("npm")

        return len(missing) == 0, available, missing

    def _install_nodejs_deps(self) -> bool:
        """Install Node.js dependencies."""
        if self.system == "linux":
            try:
                subprocess.run(["curl", "-fsSL", "https://deb.nodesource.com/setup_lts.x", "|", "sudo", "-E", "bash", "-"],
                             check=True, capture_output=True)
                subprocess.run(["sudo", "apt-get", "install", "-y", "nodejs"],
                             check=True, capture_output=True)
                return True
            except subprocess.CalledProcessError:
                return False
        else:
            print("❌ Automatic Node.js installation not supported on this platform")
            return False

    def _check_cpp_deps(self) -> Tuple[bool, List[str], List[str]]:
        """Check C++ dependencies."""
        available = []
        missing = []

        if self._command_exists("gcc"):
            available.append("gcc")
        else:
            missing.append("gcc")

        if self._command_exists("cmake"):
            available.append("cmake")
        else:
            missing.append("cmake")

        return len(missing) == 0, available, missing

    def _install_cpp_deps(self) -> bool:
        """Install C++ dependencies."""
        if self.system == "linux":
            try:
                subprocess.run(["sudo", "apt-get", "update"], check=True, capture_output=True)
                subprocess.run(["sudo", "apt-get", "install", "-y", "build-essential", "cmake"],
                             check=True, capture_output=True)
                return True
            except subprocess.CalledProcessError:
                return False
        else:
            print("❌ Automatic C++ installation not supported on this platform")
            return False

    def _check_rust_deps(self) -> Tuple[bool, List[str], List[str]]:
        """Check Rust dependencies."""
        available = []
        missing = []

        if self._command_exists("cargo"):
            available.append("cargo")
        else:
            missing.append("cargo")

        if self._command_exists("rustc"):
            available.append("rustc")
        else:
            missing.append("rustc")

        return len(missing) == 0, available, missing

    def _install_rust_deps(self) -> bool:
        """Install Rust dependencies."""
        try:
            subprocess.run(["curl", "--proto", "=https", "--tlsv1.2", "-sSf",
                          "https://sh.rustup.rs", "|", "sh", "-s", "--", "-y"],
                         check=True, capture_output=True)
            return True
        except subprocess.CalledProcessError:
            return False

    def _check_go_deps(self) -> Tuple[bool, List[str], List[str]]:
        """Check Go dependencies."""
        available = []
        missing = []

        if self._command_exists("go"):
            available.append("go")
        else:
            missing.append("go")

        return len(missing) == 0, available, missing

    def _install_go_deps(self) -> bool:
        """Install Go dependencies."""
        if self.system == "linux":
            try:
                subprocess.run(["sudo", "apt-get", "update"], check=True, capture_output=True)
                subprocess.run(["sudo", "apt-get", "install", "-y", "golang-go"],
                             check=True, capture_output=True)
                return True
            except subprocess.CalledProcessError:
                return False
        else:
            print("❌ Automatic Go installation not supported on this platform")
            return False

    def _check_haskell_deps(self) -> Tuple[bool, List[str], List[str]]:
        """Check Haskell dependencies."""
        available = []
        missing = []

        if self._command_exists("stack"):
            available.append("stack")
        else:
            missing.append("stack")

        if self._command_exists("ghc"):
            available.append("ghc")
        else:
            missing.append("ghc")

        return len(missing) == 0, available, missing

    def _install_haskell_deps(self) -> bool:
        """Install Haskell dependencies."""
        if self.system == "linux":
            try:
                subprocess.run(["sudo", "apt-get", "update"], check=True, capture_output=True)
                subprocess.run(["sudo", "apt-get", "install", "-y", "haskell-stack"],
                             check=True, capture_output=True)
                return True
            except subprocess.CalledProcessError:
                return False
        else:
            print("❌ Automatic Haskell installation not supported on this platform")
            return False

    # Simplified implementations for other languages
    def _check_clojure_deps(self) -> Tuple[bool, List[str], List[str]]:
        available = []
        missing = []
        if self._command_exists("lein"):
            available.append("lein")
        else:
            missing.append("lein")
        return len(missing) == 0, available, missing

    def _install_clojure_deps(self) -> bool:
        print("📦 Please install Leiningen from: https://leiningen.org/")
        return False

    def _check_elixir_deps(self) -> Tuple[bool, List[str], List[str]]:
        available = []
        missing = []
        if self._command_exists("elixir"):
            available.append("elixir")
        else:
            missing.append("elixir")
        return len(missing) == 0, available, missing

    def _install_elixir_deps(self) -> bool:
        print("📦 Please install Elixir from: https://elixir-lang.org/install.html")
        return False

    def _check_erlang_deps(self) -> Tuple[bool, List[str], List[str]]:
        available = []
        missing = []
        if self._command_exists("erl"):
            available.append("erl")
        else:
            missing.append("erl")
        return len(missing) == 0, available, missing

    def _install_erlang_deps(self) -> bool:
        if self.system == "linux":
            try:
                subprocess.run(["sudo", "apt-get", "update"], check=True, capture_output=True)
                subprocess.run(["sudo", "apt-get", "install", "-y", "erlang"],
                             check=True, capture_output=True)
                return True
            except subprocess.CalledProcessError:
                return False
        return False

    # Placeholder implementations for remaining languages
    def _check_lua_deps(self) -> Tuple[bool, List[str], List[str]]:
        return (self._command_exists("lua"), ["lua"] if self._command_exists("lua") else [], ["lua"] if not self._command_exists("lua") else [])

    def _install_lua_deps(self) -> bool:
        if self.system == "linux":
            try:
                subprocess.run(["sudo", "apt-get", "update"], check=True, capture_output=True)
                subprocess.run(["sudo", "apt-get", "install", "-y", "lua5.3"],
                             check=True, capture_output=True)
                return True
            except subprocess.CalledProcessError:
                return False
        return False

    def _check_perl_deps(self) -> Tuple[bool, List[str], List[str]]:
        return (self._command_exists("perl"), ["perl"] if self._command_exists("perl") else [], ["perl"] if not self._command_exists("perl") else [])

    def _install_perl_deps(self) -> bool:
        if self.system == "linux":
            try:
                subprocess.run(["sudo", "apt-get", "update"], check=True, capture_output=True)
                subprocess.run(["sudo", "apt-get", "install", "-y", "perl"],
                             check=True, capture_output=True)
                return True
            except subprocess.CalledProcessError:
                return False
        return False

    def _check_r_deps(self) -> Tuple[bool, List[str], List[str]]:
        return (self._command_exists("R"), ["R"] if self._command_exists("R") else [], ["R"] if not self._command_exists("R") else [])

    def _install_r_deps(self) -> bool:
        if self.system == "linux":
            try:
                subprocess.run(["sudo", "apt-get", "update"], check=True, capture_output=True)
                subprocess.run(["sudo", "apt-get", "install", "-y", "r-base"],
                             check=True, capture_output=True)
                return True
            except subprocess.CalledProcessError:
                return False
        return False

    def _check_racket_deps(self) -> Tuple[bool, List[str], List[str]]:
        return (self._command_exists("racket"), ["racket"] if self._command_exists("racket") else [], ["racket"] if not self._command_exists("racket") else [])

    def _install_racket_deps(self) -> bool:
        print("📦 Please install Racket from: https://racket-lang.org/")
        return False

    def _check_fortran_deps(self) -> Tuple[bool, List[str], List[str]]:
        return (self._command_exists("gfortran"), ["gfortran"] if self._command_exists("gfortran") else [], ["gfortran"] if not self._command_exists("gfortran") else [])

    def _install_fortran_deps(self) -> bool:
        if self.system == "linux":
            try:
                subprocess.run(["sudo", "apt-get", "update"], check=True, capture_output=True)
                subprocess.run(["sudo", "apt-get", "install", "-y", "gfortran"],
                             check=True, capture_output=True)
                return True
            except subprocess.CalledProcessError:
                return False
        return False

    def _check_ada_deps(self) -> Tuple[bool, List[str], List[str]]:
        return (self._command_exists("gnat"), ["gnat"] if self._command_exists("gnat") else [], ["gnat"] if not self._command_exists("gnat") else [])

    def _install_ada_deps(self) -> bool:
        if self.system == "linux":
            try:
                subprocess.run(["sudo", "apt-get", "update"], check=True, capture_output=True)
                subprocess.run(["sudo", "apt-get", "install", "-y", "gnat"],
                             check=True, capture_output=True)
                return True
            except subprocess.CalledProcessError:
                return False
        return False

    def _check_assembly_deps(self) -> Tuple[bool, List[str], List[str]]:
        available = []
        missing = []
        if self._command_exists("nasm"):
            available.append("nasm")
        else:
            missing.append("nasm")
        if self._command_exists("ld"):
            available.append("ld")
        else:
            missing.append("ld")
        return len(missing) == 0, available, missing

    def _install_assembly_deps(self) -> bool:
        if self.system == "linux":
            try:
                subprocess.run(["sudo", "apt-get", "update"], check=True, capture_output=True)
                subprocess.run(["sudo", "apt-get", "install", "-y", "nasm", "binutils"],
                             check=True, capture_output=True)
                return True
            except subprocess.CalledProcessError:
                return False
        return False

    def _check_brainfuck_deps(self) -> Tuple[bool, List[str], List[str]]:
        return self._check_python_deps()  # Brainfuck uses Python interpreter

    def _install_brainfuck_deps(self) -> bool:
        return self._install_python_deps()

    def _check_crystal_deps(self) -> Tuple[bool, List[str], List[str]]:
        return (self._command_exists("crystal"), ["crystal"] if self._command_exists("crystal") else [], ["crystal"] if not self._command_exists("crystal") else [])

    def _install_crystal_deps(self) -> bool:
        print("📦 Please install Crystal from: https://crystal-lang.org/install/")
        return False

    def _check_nim_deps(self) -> Tuple[bool, List[str], List[str]]:
        return (self._command_exists("nim"), ["nim"] if self._command_exists("nim") else [], ["nim"] if not self._command_exists("nim") else [])

    def _install_nim_deps(self) -> bool:
        print("📦 Please install Nim from: https://nim-lang.org/install.html")
        return False

    def _check_ocaml_deps(self) -> Tuple[bool, List[str], List[str]]:
        return (self._command_exists("ocaml"), ["ocaml"] if self._command_exists("ocaml") else [], ["ocaml"] if not self._command_exists("ocaml") else [])

    def _install_ocaml_deps(self) -> bool:
        if self.system == "linux":
            try:
                subprocess.run(["sudo", "apt-get", "update"], check=True, capture_output=True)
                subprocess.run(["sudo", "apt-get", "install", "-y", "ocaml"],
                             check=True, capture_output=True)
                return True
            except subprocess.CalledProcessError:
                return False
        return False

    def _check_pascal_deps(self) -> Tuple[bool, List[str], List[str]]:
        return (self._command_exists("fpc"), ["fpc"] if self._command_exists("fpc") else [], ["fpc"] if not self._command_exists("fpc") else [])

    def _install_pascal_deps(self) -> bool:
        if self.system == "linux":
            try:
                subprocess.run(["sudo", "apt-get", "update"], check=True, capture_output=True)
                subprocess.run(["sudo", "apt-get", "install", "-y", "fpc"],
                             check=True, capture_output=True)
                return True
            except subprocess.CalledProcessError:
                return False
        return False

    def _check_prolog_deps(self) -> Tuple[bool, List[str], List[str]]:
        return (self._command_exists("swipl"), ["swipl"] if self._command_exists("swipl") else [], ["swipl"] if not self._command_exists("swipl") else [])

    def _install_prolog_deps(self) -> bool:
        if self.system == "linux":
            try:
                subprocess.run(["sudo", "apt-get", "update"], check=True, capture_output=True)
                subprocess.run(["sudo", "apt-get", "install", "-y", "swi-prolog"],
                             check=True, capture_output=True)
                return True
            except subprocess.CalledProcessError:
                return False
        return False

    def _check_shell_deps(self) -> Tuple[bool, List[str], List[str]]:
        available = []
        missing = []
        for cmd in ["bash", "bc", "awk"]:
            if self._command_exists(cmd):
                available.append(cmd)
            else:
                missing.append(cmd)
        return len(missing) == 0, available, missing

    def _install_shell_deps(self) -> bool:
        if self.system == "linux":
            try:
                subprocess.run(["sudo", "apt-get", "update"], check=True, capture_output=True)
                subprocess.run(["sudo", "apt-get", "install", "-y", "bc", "gawk"],
                             check=True, capture_output=True)
                return True
            except subprocess.CalledProcessError:
                return False
        return False

    def _check_sql_deps(self) -> Tuple[bool, List[str], List[str]]:
        available = []
        missing = []
        if self._command_exists("sqlite3"):
            available.append("sqlite3")
        else:
            missing.append("sqlite3")
        return len(missing) == 0, available, missing

    def _install_sql_deps(self) -> bool:
        if self.system == "linux":
            try:
                subprocess.run(["sudo", "apt-get", "update"], check=True, capture_output=True)
                subprocess.run(["sudo", "apt-get", "install", "-y", "sqlite3"],
                             check=True, capture_output=True)
                return True
            except subprocess.CalledProcessError:
                return False
        return False

    def _check_typescript_deps(self) -> Tuple[bool, List[str], List[str]]:
        available = []
        missing = []
        for cmd in ["node", "npm", "tsc"]:
            if self._command_exists(cmd):
                available.append(cmd)
            else:
                missing.append(cmd)
        return len(missing) == 0, available, missing

    def _install_typescript_deps(self) -> bool:
        # Node.js should already be installed by JavaScript deps
        if not self._command_exists("tsc"):
            try:
                subprocess.run(["npm", "install", "-g", "typescript"],
                             check=True, capture_output=True)
                return True
            except subprocess.CalledProcessError:
                return False
        return True

    def _check_zig_deps(self) -> Tuple[bool, List[str], List[str]]:
        return (self._command_exists("zig"), ["zig"] if self._command_exists("zig") else [], ["zig"] if not self._command_exists("zig") else [])

    def _install_zig_deps(self) -> bool:
        print("📦 Please install Zig from: https://ziglang.org/download/")
        return False

    def _check_v_deps(self) -> Tuple[bool, List[str], List[str]]:
        return (self._command_exists("v"), ["v"] if self._command_exists("v") else [], ["v"] if not self._command_exists("v") else [])

    def _install_v_deps(self) -> bool:
        print("📦 Please install V from: https://github.com/vlang/v")
        return False

    def _check_odin_deps(self) -> Tuple[bool, List[str], List[str]]:
        return (self._command_exists("odin"), ["odin"] if self._command_exists("odin") else [], ["odin"] if not self._command_exists("odin") else [])

    def _install_odin_deps(self) -> bool:
        print("📦 Please install Odin from: https://github.com/odin-lang/Odin")
        return False

    def _command_exists(self, command: str) -> bool:
        """Check if a command exists."""
        try:
            subprocess.run(["which", command], capture_output=True, check=True)
            return True
        except subprocess.CalledProcessError:
            return False

    def _check_single_command(self, command: str) -> Tuple[bool, List[str], List[str]]:
        """Check availability of a single command."""
        exists = self._command_exists(command)
        return (exists, [command] if exists else [], [] if exists else [command])

    def _print_install_url(self, name: str, url: str) -> bool:
        """Print install URL and return False (manual install required)."""
        print(f"📦 Please install {name} from: {url}")
        return False

    def check_all_dependencies(self) -> Dict[str, Tuple[bool, List[str], List[str]]]:
        """Check dependencies for all languages."""
        results = {}
        for language in self.dependencies.keys():
            results[language] = self.check_language_dependencies(language)
        return results

    def generate_dependency_report(self) -> str:
        """Generate a comprehensive dependency report."""
        results = self.check_all_dependencies()

        report = "🧪 Active Inference Dependencies Report\n"
        report += "=" * 50 + "\n\n"

        total_languages = len(results)
        fully_available = sum(1 for result in results.values() if result[0])

        report += f"📊 Summary:\n"
        report += f"   Total Languages: {total_languages}\n"
        report += f"   Fully Available: {fully_available}\n"
        report += f"   Missing Some: {total_languages - fully_available}\n\n"

        report += "🔍 Detailed Results:\n"
        report += "-" * 30 + "\n"

        for language, (is_complete, available, missing) in results.items():
            status = "✅" if is_complete else "❌"
            report += f"{status} {language.capitalize()}:\n"

            if available:
                report += f"   ✅ Available: {', '.join(available)}\n"
            if missing:
                report += f"   ❌ Missing: {', '.join(missing)}\n"
            report += "\n"

        return report

def main():
    """Main function for dependency management."""
    checker = DependencyChecker()

    if len(sys.argv) > 1:
        language = sys.argv[1].lower()
        if language == "--all":
            # Check all dependencies
            report = checker.generate_dependency_report()
            print(report)

            # Save to file
            with open("dependency_report.txt", "w") as f:
                f.write(report)
            print("📄 Report saved to 'dependency_report.txt'")

        elif language == "--install":
            # Interactive installation
            if len(sys.argv) > 2:
                target_lang = sys.argv[2].lower()
                print(f"📦 Installing dependencies for {target_lang}...")
                if checker.install_language_dependencies(target_lang):
                    print(f"✅ Successfully installed {target_lang} dependencies")
                else:
                    print(f"❌ Failed to install {target_lang} dependencies")
            else:
                print("❌ Please specify a language to install dependencies for")
                print("   Example: python config_manager.py --install python")
        else:
            # Check specific language
            is_complete, available, missing = checker.check_language_dependencies(language)
            print(f"🔍 Checking {language} dependencies...")
            print(f"   Status: {'✅ Complete' if is_complete else '❌ Incomplete'}")
            if available:
                print(f"   ✅ Available: {', '.join(available)}")
            if missing:
                print(f"   ❌ Missing: {', '.join(missing)}")
    else:
        print("🧠 Active Inference Dependency Manager")
        print("Usage:")
        print("  Check all dependencies: python config_manager.py --all")
        print("  Check specific language: python config_manager.py <language>")
        print("  Install dependencies: python config_manager.py --install <language>")
        print("\nSupported languages:")
        deps = list(checker.dependencies.keys())
        for i in range(0, len(deps), 5):
            print(f"  {' '.join(deps[i:i+5])}")

if __name__ == "__main__":
    main()

#!/bin/bash
# ============================================================================
# Active InferAnts — Language Dependencies Setup Script
# ============================================================================
# Installs all required language runtimes and tools for the 50-language
# Active Inference implementation suite.
#
# Usage:
#   ./setup_dependencies.sh          # Install all missing dependencies
#   ./setup_dependencies.sh --check  # Check only (no install)
#   ./setup_dependencies.sh --list   # List all languages and install status
#
# Requires: macOS with Homebrew (or Linux with apt/dnf)
# ============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'
BLUE='\033[0;34m'; CYAN='\033[0;36m'; NC='\033[0m'
BOLD='\033[1m'

# ── Language → Brew Package → Check Command mapping ──────────────────────────
#
# Format: "language_name|brew_package|check_command|install_note"
# Use "SKIP" for brew_package if not installable via brew
# Use "CASK" prefix for brew cask installs

LANGUAGES=(
    "Python|python3|python3|Pre-installed on macOS"
    "Java|openjdk|java|JDK for JVM languages"
    "JavaScript|node|node|Node.js runtime"
    "C++|gcc|gcc|GNU Compiler Collection"
    "C|gcc|gcc|GNU C Compiler"
    "Rust|rustup|rustc|Install then run: rustup-init"
    "Golang|go|go|Go programming language"
    "Haskell|haskell-stack|stack|Haskell Tool Stack"
    "Clojure|leiningen|lein|Clojure build tool"
    "Elixir|elixir|elixir|Elixir (installs Erlang automatically)"
    "Erlang|erlang|erl|Erlang/OTP"
    "Lua|lua|lua|Lua scripting language"
    "Perl|perl|perl|Pre-installed on macOS"
    "R|r|R|R statistical computing"
    "Racket|minimal-racket|racket|Racket (minimal install)"
    "Fortran|gcc|gfortran|GNU Fortran (part of GCC)"
    "Ada|SKIP|gnat|Install via: brew install gcc (includes gnat)"
    "Assembly|nasm|nasm|Netwide Assembler"
    "Brainfuck|python3|python3|Uses Python interpreter"
    "Crystal|crystal|crystal|Crystal language"
    "Nim|nim|nim|Nim language"
    "OCaml|ocaml|ocaml|OCaml compiler"
    "Pascal|fpc|fpc|Free Pascal Compiler"
    "Prolog|swi-prolog|swipl|SWI-Prolog"
    "Shell|bash|bash|Pre-installed"
    "SQL|sqlite|sqlite3|SQLite database"
    "TypeScript|typescript|tsc|TypeScript compiler (also needs node)"
    "Zig|zig|zig|Zig language"
    "V|vlang|v|V language"
    "Odin|odin|odin|Odin language"
    "Kotlin|kotlin|kotlin|Kotlin compiler"
    "Scala|scala|scala|Scala language (JVM)"
    "Swift|swift|swift|Pre-installed on macOS"
    "CSharp|dotnet-sdk|dotnet|.NET SDK (C# and F#)"
    "FSharp|dotnet-sdk|dotnet|.NET SDK (C# and F#)"
    "MATLAB|SKIP|matlab|Commercial: mathworks.com/products/matlab"
    "Ruby|ruby|ruby|Pre-installed on macOS"
    "PHP|php|php|PHP interpreter"
    "Jock|SKIP|urbit|Niche: urbit.org/getting-started"
    "D|dmd|dmd|D language compiler"
    "Dart|dart-sdk|dart|Dart SDK"
    "Groovy|groovy|groovy|Groovy (JVM scripting)"
    "CommonLisp|sbcl|sbcl|Steel Bank Common Lisp"
    "ObjectiveC|SKIP|clang|Pre-installed with Xcode CLT"
    "PowerShell|powershell|pwsh|PowerShell Core"
    "Scheme|chibi-scheme|chibi-scheme|Chibi-Scheme (R7RS)"
    "COBOL|gnucobol|cobc|GnuCOBOL compiler"
    "Solidity|solidity|solc|Solidity compiler"
    "Tcl|tcl-tk|tclsh|Tcl/Tk"
)

# ── Helper Functions ─────────────────────────────────────────────────────────

check_command() {
    command -v "$1" &> /dev/null
}

print_header() {
    echo -e "\n${BOLD}${BLUE}============================================${NC}"
    echo -e "${BOLD}${BLUE}  Active InferAnts — Dependency Manager${NC}"
    echo -e "${BOLD}${BLUE}  50 Language Implementations${NC}"
    echo -e "${BOLD}${BLUE}============================================${NC}\n"
}

# ── Check Mode ───────────────────────────────────────────────────────────────

do_check() {
    print_header
    local available=0 missing=0 skipped=0

    for entry in "${LANGUAGES[@]}"; do
        IFS='|' read -r name brew_pkg cmd note <<< "$entry"
        if check_command "$cmd"; then
            echo -e "  ${GREEN}✅${NC} ${name}: $(command -v "$cmd")"
            ((available++))
        elif [[ "$brew_pkg" == "SKIP" ]]; then
            echo -e "  ${YELLOW}⚠️${NC}  ${name}: ${note}"
            ((skipped++))
        else
            echo -e "  ${RED}❌${NC} ${name}: missing '${cmd}' — brew install ${brew_pkg}"
            ((missing++))
        fi
    done

    echo -e "\n${BOLD}Summary:${NC}"
    echo -e "  ${GREEN}Available: ${available}${NC}"
    echo -e "  ${RED}Missing:   ${missing}${NC}"
    echo -e "  ${YELLOW}Skipped:   ${skipped}${NC} (commercial/niche)"
    echo -e "  Total:     ${#LANGUAGES[@]}"

    return $missing
}

# ── List Mode ────────────────────────────────────────────────────────────────

do_list() {
    print_header
    printf "%-15s %-20s %-12s %s\n" "Language" "Brew Package" "Status" "Note"
    printf "%-15s %-20s %-12s %s\n" "--------" "------------" "------" "----"

    for entry in "${LANGUAGES[@]}"; do
        IFS='|' read -r name brew_pkg cmd note <<< "$entry"
        if check_command "$cmd"; then
            status="${GREEN}installed${NC}"
        elif [[ "$brew_pkg" == "SKIP" ]]; then
            status="${YELLOW}manual${NC}"
        else
            status="${RED}missing${NC}"
        fi
        printf "%-15s %-20s " "$name" "$brew_pkg"
        echo -e "${status}   ${note}"
    done
}

# ── Install Mode ─────────────────────────────────────────────────────────────

do_install() {
    print_header

    # Check for package manager
    if ! check_command brew; then
        echo -e "${RED}❌ Homebrew not found. Install from: https://brew.sh${NC}"
        exit 1
    fi

    echo -e "${CYAN}🔍 Scanning for missing dependencies...${NC}\n"

    local to_install=() installed=0 already=0 skipped=0

    for entry in "${LANGUAGES[@]}"; do
        IFS='|' read -r name brew_pkg cmd note <<< "$entry"
        if check_command "$cmd"; then
            ((already++))
            continue
        fi
        if [[ "$brew_pkg" == "SKIP" ]]; then
            echo -e "  ${YELLOW}⚠️${NC}  ${name}: ${note}"
            ((skipped++))
            continue
        fi
        # Avoid duplicates (e.g., dotnet-sdk listed twice for C# and F#)
        local found=0
        for pkg in "${to_install[@]+"${to_install[@]}"}"; do
            if [[ "$pkg" == "$brew_pkg" ]]; then found=1; break; fi
        done
        if [[ $found -eq 0 ]]; then
            to_install+=("$brew_pkg")
            echo -e "  ${BLUE}📦${NC} Will install: ${brew_pkg} (for ${name})"
        fi
    done

    echo -e "\n${BOLD}Already installed: ${already}${NC}"
    echo -e "${BOLD}Skipped (manual):  ${skipped}${NC}"
    echo -e "${BOLD}To install:        ${#to_install[@]}${NC}\n"

    if [[ ${#to_install[@]} -eq 0 ]]; then
        echo -e "${GREEN}✅ All installable dependencies are already present!${NC}"
        return 0
    fi

    echo -e "${CYAN}🚀 Installing ${#to_install[@]} packages via Homebrew...${NC}\n"
    brew install "${to_install[@]}" 2>&1

    # Post-install: rustup needs initialization
    if check_command rustup && ! check_command rustc; then
        echo -e "\n${CYAN}🦀 Initializing Rust toolchain...${NC}"
        rustup-init -y --no-modify-path 2>&1
    fi

    # Post-install: TypeScript needs global tsc
    if check_command npm && ! check_command tsc; then
        echo -e "\n${CYAN}📘 Installing TypeScript compiler globally...${NC}"
        npm install -g typescript 2>&1
    fi

    echo -e "\n${GREEN}✅ Installation complete!${NC}"
    echo -e "${CYAN}Run './setup_dependencies.sh --check' to verify.${NC}"
}

# ── Main ─────────────────────────────────────────────────────────────────────

case "${1:-}" in
    --check)  do_check ;;
    --list)   do_list ;;
    --help|-h)
        echo "Usage: $0 [--check|--list|--help]"
        echo "  (no args)  Install all missing dependencies"
        echo "  --check    Check dependency status only"
        echo "  --list     List all languages with status"
        echo "  --help     Show this help"
        ;;
    *)        do_install ;;
esac

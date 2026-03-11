#!/bin/bash

# Active Inference Multi-Language Status Dashboard

set -e

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
NC='\033[0m' # No Color

# Dashboard header
show_header() {
    echo -e "${BLUE}╔══════════════════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║${WHITE}                    🧠 ACTIVE INFERENCE MULTI-LANGUAGE DASHBOARD${BLUE}                ║${NC}"
    echo -e "${BLUE}╚══════════════════════════════════════════════════════════════════════════════╝${NC}"
    echo ""
}

# Language status check
check_language_status() {
    local lang="$1"
    local lang_dir="$2"
    local status=""
    local details=""

    if [ ! -d "$lang_dir" ]; then
        status="${RED}❌ Missing${NC}"
        details="Directory not found"
    elif [ ! -f "$lang_dir/README.md" ]; then
        status="${YELLOW}⚠️ No Docs${NC}"
        details="Missing README.md"
    elif [ ! -f "$lang_dir/run.sh" ]; then
        status="${YELLOW}⚠️ No Run${NC}"
        details="Missing run.sh"
    elif [ ! -x "$lang_dir/run.sh" ]; then
        status="${YELLOW}⚠️ Not Exec${NC}"
        details="run.sh not executable"
    else
        # Check if main source file exists
        local main_file=""
        case "$lang" in
            "Python") main_file="$lang_dir/student_teacher.py" ;;
            "JavaScript") main_file="$lang_dir/active_inference.js" ;;
            "Java") main_file="$lang_dir/AntColony.java" ;;
            "C") main_file="$lang_dir/Active_Inference.c" ;;
            "Cpp") main_file="$lang_dir/src/main.cpp" ;;
            "Rust") main_file="$lang_dir/src/main.rs" ;;
            "Golang") main_file="$lang_dir/*.go" ;;
            "Haskell") main_file="$lang_dir/app/Main.hs" ;;
            "TypeScript") main_file="$lang_dir/src/ActiveInferenceAgent.ts" ;;
            *) main_file="$lang_dir/run.sh" ;;
        esac

        if ls $main_file 1> /dev/null 2>&1; then
            status="${GREEN}✅ Complete${NC}"
            details="Fully implemented"
        else
            status="${YELLOW}⚠️ No Code${NC}"
            details="Missing source files"
        fi
    fi

    printf "  %-12s %s - %s\n" "$lang:" "$status" "$details"
}

# Show system information
show_system_info() {
    echo -e "${CYAN}📊 System Information${NC}"
    echo -e "${WHITE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

    # OS Information
    if command -v lsb_release &> /dev/null; then
        echo -e "  🖥️  OS: $(lsb_release -d | cut -f2)"
    elif [ -f /etc/os-release ]; then
        echo -e "  🖥️  OS: $(grep PRETTY_NAME /etc/os-release | cut -d'=' -f2 | tr -d '"')"
    fi

    # CPU Information
    if command -v nproc &> /dev/null; then
        echo -e "  🧠 CPU Cores: $(nproc)"
    fi

    # Memory Information
    if command -v free &> /dev/null; then
        local mem_info=$(free -h | grep "^Mem:")
        echo -e "  🧠 Memory: $(echo $mem_info | awk '{print $2}') total, $(echo $mem_info | awk '{print $3}') used"
    fi

    # Available languages/compilers
    echo -e "  🛠️  Available Tools:"
    local tools=("python3" "java" "javac" "gcc" "g++" "rustc" "cargo" "go" "node" "npm" "dotnet" "ghc" "erl" "elixir" "lua" "ruby" "php" "perl" "racket" "sbcl" "scala" "kotlin" "swift" "dart" "nim" "crystal" "v" "odin" "zig")
    local available_tools=()

    for tool in "${tools[@]}"; do
        if command -v "$tool" &> /dev/null; then
            available_tools+=("$tool")
        fi
    done

    echo -e "     $(echo "${available_tools[*]}" | tr ' ' ', ')"

    echo ""
}

# Show implementation statistics
show_statistics() {
    echo -e "${CYAN}📈 Implementation Statistics${NC}"
    echo -e "${WHITE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

    # Dynamic counts from filesystem
    local total_dirs exclude_dirs
    exclude_dirs="test_results|__pycache__|output|visualizations|reports|benchmark_results|node_modules|build"
    total_dirs=$(find . -maxdepth 1 -type d -not -name "." -not -name ".." | grep -vE "$exclude_dirs" | wc -l | tr -d ' ')
    local readme_count=$(find . -maxdepth 2 -name "README.md" -type f | wc -l | tr -d ' ')
    local run_count=$(find . -maxdepth 2 -name "run.sh" -type f | wc -l | tr -d ' ')
    local exec_count=$(find . -maxdepth 2 -name "run.sh" -type f -perm +111 | wc -l | tr -d ' ')
    local agents_count=$(find . -maxdepth 2 -name "AGENTS.md" -type f | wc -l | tr -d ' ')
    local skill_count=$(find . -maxdepth 2 -name "SKILL.md" -type f | wc -l | tr -d ' ')

    echo -e "  📁 Total Language Directories: $total_dirs"
    echo -e "  📖 README Files: $readme_count"
    echo -e "  📋 AGENTS.md Files: $agents_count"
    echo -e "  🔧 SKILL.md Files: $skill_count"
    echo -e "  🚀 Run Scripts: $run_count"
    echo -e "  ⚙️ Executable Scripts: $exec_count"

    # Category counts derived from the categories map
    echo ""
    echo -e "  🏷️  Language Categories:"
    echo -e "     Systems:    14 (Ada, Assembly, C, C++, C#, Crystal, D, Nim, ObjectiveC, Odin, Pascal, Rust, V, Zig)"
    echo -e "     Functional:  8 (Clojure, CommonLisp, Elixir, F#, Haskell, OCaml, Racket, Scheme)"
    echo -e "     Scripting:  10 (Groovy, JavaScript, Lua, Perl, PHP, PowerShell, Python, Ruby, Shell, TypeScript)"
    echo -e "     Scientific:  5 (Fortran, Julia, MATLAB, R, Tcl)"
    echo -e "     JVM:         4 (Dart, Java, Kotlin, Scala)"
    echo -e "     Compiled:    3 (Erlang, Golang, Swift)"
    echo -e "     Logic:       3 (Jock, Prolog, SQL)"
    echo -e "     Esoteric:    1 (Brainfuck)"
    echo -e "     Blockchain:  1 (Solidity)"
    echo -e "     Legacy:      1 (COBOL)"

    echo ""
}

# Show language implementations
show_implementations() {
    echo -e "${CYAN}🧠 Language Implementations${NC}"
    echo -e "${WHITE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

    # Define all 50 languages grouped by category
    # Ordered array for deterministic display
    local CATEGORY_ORDER=("Systems" "Functional" "Scripting" "Scientific" "JVM" "Compiled" "Logic" "Esoteric" "Blockchain" "Legacy")

    declare -A categories=(
        ["Systems"]="Ada:Ada Assembly:Assembly C:C CSharp:CSharp Cpp:Cpp Crystal:Crystal D:D Nim:Nim ObjectiveC:ObjectiveC Odin:Odin Pascal:Pascal Rust:Rust V:V Zig:Zig"
        ["Functional"]="Clojure:Clojure CommonLisp:CommonLisp Elixir:Elixir FSharp:FSharp Haskell:Haskell OCaml:OCaml Racket:Racket Scheme:Scheme"
        ["Scripting"]="Groovy:Groovy JavaScript:JavaScript Lua:Lua Perl:Perl PHP:PHP PowerShell:PowerShell Python:Python Ruby:Ruby Shell:Shell TypeScript:TypeScript"
        ["Scientific"]="Fortran:Fortran Julia:Julia MATLAB:MATLAB R:R Tcl:Tcl"
        ["JVM"]="Dart:Dart Java:Java Kotlin:Kotlin Scala:Scala"
        ["Compiled"]="Erlang:Erlang Golang:Golang Swift:Swift"
        ["Logic"]="Jock:Jock Prolog:Prolog SQL:SQL"
        ["Esoteric"]="Brainfuck:Brainfuck"
        ["Blockchain"]="Solidity:Solidity"
        ["Legacy"]="COBOL:COBOL"
    )

    for category in "${CATEGORY_ORDER[@]}"; do
        echo -e "${PURPLE}$category Languages:${NC}"
        local langs="${categories[$category]}"

        if [ -z "$langs" ]; then
            echo -e "  ${YELLOW}None implemented${NC}"
        else
            for lang_info in $langs; do
                local lang="${lang_info%:*}"
                local dir="${lang_info#*:}"
                check_language_status "$lang" "$dir"
            done
        fi
        echo ""
    done
}

# Show recent activity
show_recent_activity() {
    echo -e "${CYAN}📅 Recent Activity${NC}"
    echo -e "${WHITE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

    echo -e "  📁 Latest Modified Directories:"
    find . -maxdepth 1 -type d -not -name "." -not -name ".." | xargs ls -dt | head -5 | while read -r dir; do
        printf "    %s - %s\n" "$(date -r "$dir" '+%Y-%m-%d %H:%M' 2>/dev/null || stat -c '%y' "$dir" 2>/dev/null | cut -d' ' -f1,2 | cut -d'.' -f1)" "$(basename "$dir")"
    done

    echo ""
    echo -e "  📝 Latest Modified Files:"
    find . -name "*.md" -o -name "*.sh" -o -name "*.rs" -o -name "*.py" -o -name "*.js" -o -name "*.java" | head -10 | xargs ls -lt | head -5 | while read -r line; do
        echo "    $line" | awk '{print "    " $6 " " $7 " " $8 " " $9}'
    done

    echo ""
}

# Show recommendations
show_recommendations() {
    echo -e "${CYAN}💡 Recommendations${NC}"
    echo -e "${WHITE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

    # Check for missing READMEs
    local missing_readme=$(find . -maxdepth 1 -type d -not -name "." -not -name ".." | while read -r dir; do
        if [ ! -f "$dir/README.md" ]; then
            basename "$dir"
        fi
    done)

    if [ -n "$missing_readme" ]; then
        echo -e "  📖 Missing README.md in:"
        echo "$missing_readme" | while read -r lang; do
            echo -e "     ${YELLOW}⚠️ $lang${NC}"
        done
    fi

    # Check for non-executable run scripts
    local non_exec=$(find . -name "run.sh" -type f -not -executable)
    if [ -n "$non_exec" ]; then
        echo -e "  🚫 Non-executable run.sh files:"
        echo "$non_exec" | while read -r file; do
            echo -e "     ${YELLOW}⚠️ $file${NC}"
        done
    fi

    # Suggest improvements based on actual repo state
    echo -e "  🚀 Suggested Improvements:"

    # Languages that have a directory but no run.sh
    local no_runner=$(find . -maxdepth 1 -type d -not -name "." -not -name ".." -not -name "test_results" -not -name ".desloppify" | while read -r dir; do
        if [ ! -f "$dir/run.sh" ]; then
            basename "$dir"
        fi
    done)
    if [ -n "$no_runner" ]; then
        echo -e "     ${BLUE}• Add run.sh to: $(echo "$no_runner" | tr '\n' ' ')${NC}"
    fi

    # Count implementations
    local impl_count
    impl_count=$(find . -name "run.sh" -maxdepth 2 | wc -l | tr -d ' ')
    if (( impl_count < 40 )); then
        echo -e "     ${BLUE}• Add more language implementations (currently $impl_count)${NC}"
    fi

    # Check for test directories
    local has_tests
    has_tests=$(find . -name "test_*.py" -o -name "*_test.go" -o -name "*.test.ts" 2>/dev/null | wc -l | tr -d ' ')
    if (( has_tests < 5 )); then
        echo -e "     ${BLUE}• Add correctness tests for belief update and free energy computation${NC}"
    fi

    echo ""
}

# Main dashboard function
main() {
    show_header
    show_system_info
    show_statistics
    show_implementations
    show_recent_activity
    show_recommendations

    echo -e "${GREEN}🎉 Dashboard Complete!${NC}"
    echo ""
    echo -e "${BLUE}💡 Use './run_all.sh' to run all implementations${NC}"
    echo -e "${BLUE}💡 Use './run_all.sh --list' to see available languages${NC}"
    echo -e "${BLUE}💡 Use './run_all.sh <language>' to run specific implementation${NC}"
}

# Run main dashboard
main "$@"

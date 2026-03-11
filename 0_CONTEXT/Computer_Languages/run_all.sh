#!/bin/bash

# Active Inference Multi-Language Runner
# Reads language definitions from languages.json (single source of truth)

echo "🧠 Active Inference Multi-Language Demo"
echo "======================================"
echo ""

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Resolve script directory for reliable path resolution
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LANGUAGES_JSON="${SCRIPT_DIR}/languages.json"

# Load language list from canonical languages.json
if [ ! -f "$LANGUAGES_JSON" ]; then
    echo -e "${RED}❌ Error: languages.json not found at ${LANGUAGES_JSON}${NC}"
    exit 1
fi

# Parse languages.json into Name:Directory pairs (POSIX-compatible, no mapfile)
LANGUAGES=()
while IFS= read -r line; do
    LANGUAGES+=("$line")
done < <(python3 -c "
import json, sys
with open('${LANGUAGES_JSON}') as f:
    data = json.load(f)
for lang in data['languages']:
    print(f\"{lang['name']}:{lang['directory']}\")
")

# Function to run a single language implementation
run_language() {
    local lang_info="$1"
    local lang_name="${lang_info%:*}"
    local lang_dir="${lang_info#*:}"

    echo -e "${BLUE}🔄 Running $lang_name implementation...${NC}"
    echo -e "${CYAN}========================================${NC}"

    if [ -d "$lang_dir" ] && [ -f "$lang_dir/run.sh" ]; then
        # Run in subshell to isolate CWD changes
        if (cd "$lang_dir" && ./run.sh); then
            echo -e "${GREEN}✅ $lang_name completed successfully!${NC}"
        else
            echo -e "${RED}❌ $lang_name failed!${NC}"
            return 1
        fi
    else
        echo -e "${YELLOW}⚠️ $lang_name implementation not found or missing run.sh${NC}"
    fi

    echo ""
}

# Function to show usage
show_usage() {
    echo "Usage: $0 [OPTIONS] [LANGUAGE]"
    echo ""
    echo "Options:"
    echo "  -h, --help          Show this help message"
    echo "  -l, --list          List all available language implementations"
    echo "  -s, --sequential    Run implementations sequentially (default)"
    echo "  -p, --parallel      Run implementations in parallel"
    echo "  --no-color          Disable colored output"
    echo ""
    echo "If LANGUAGE is specified, only run that implementation."
    echo "Otherwise, run all implementations."
    echo ""
    echo "Examples:"
    echo "  $0                   # Run all implementations"
    echo "  $0 python           # Run only Python implementation"
    echo "  $0 --parallel       # Run all in parallel"
    echo "  $0 --list           # List all available languages"
}

# Function to list available languages
list_languages() {
    echo "Available language implementations:"
    echo ""

    for lang_info in "${LANGUAGES[@]}"; do
        lang_name="${lang_info%:*}"
        lang_dir="${lang_info#*:}"

        if [ -d "$lang_dir" ] && [ -f "$lang_dir/run.sh" ]; then
            status="${GREEN}✅ Available${NC}"
        elif [ -d "$lang_dir" ]; then
            status="${YELLOW}⚠️ No run.sh${NC}"
        else
            status="${RED}❌ Not found${NC}"
        fi

        printf "  %-12s %s\n" "$lang_name:" "$status"
    done
}

# Parse command line arguments
SEQUENTIAL=true
SPECIFIC_LANG=""
SHOW_LIST=false

while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            show_usage
            exit 0
            ;;
        -l|--list)
            SHOW_LIST=true
            shift
            ;;
        -s|--sequential)
            SEQUENTIAL=true
            shift
            ;;
        -p|--parallel)
            SEQUENTIAL=false
            shift
            ;;
        --no-color)
            RED=''
            GREEN=''
            YELLOW=''
            BLUE=''
            PURPLE=''
            CYAN=''
            NC=''
            shift
            ;;
        *)
            SPECIFIC_LANG="$1"
            shift
            ;;
    esac
done

# Show list if requested
if [ "$SHOW_LIST" = true ]; then
    list_languages
    exit 0
fi

# Make all run.sh scripts executable
echo -e "${BLUE}🔧 Making run scripts executable...${NC}"
find . -name "run.sh" -type f -exec chmod +x {} \;

echo ""
echo -e "${PURPLE}🚀 Starting Active Inference Multi-Language Demo${NC}"
echo -e "${PURPLE}================================================${NC}"
echo ""

# Track success/failure
SUCCESS_COUNT=0
FAILURE_COUNT=0
TOTAL_RUN=0

# Run specific language or all languages
if [ -n "$SPECIFIC_LANG" ]; then
    # Find the specific language (case-insensitive)
    SPECIFIC_LANG_LOWER=$(echo "$SPECIFIC_LANG" | tr '[:upper:]' '[:lower:]')
    for lang_info in "${LANGUAGES[@]}"; do
        lang_name="${lang_info%:*}"
        lang_name_lower=$(echo "$lang_name" | tr '[:upper:]' '[:lower:]')
        if [ "$lang_name_lower" = "$SPECIFIC_LANG_LOWER" ]; then
            if run_language "$lang_info"; then
                ((SUCCESS_COUNT++))
            else
                ((FAILURE_COUNT++))
            fi
            break
        fi
    done
else
    # Run all languages
    if [ "$SEQUENTIAL" = true ]; then
        echo -e "${BLUE}Running implementations sequentially...${NC}"
        echo ""

        for lang_info in "${LANGUAGES[@]}"; do
            if run_language "$lang_info"; then
                ((SUCCESS_COUNT++))
            else
                ((FAILURE_COUNT++))
            fi
        done
    else
        echo -e "${BLUE}Running implementations in parallel...${NC}"
        echo ""

        # Run in parallel using background processes
        pids=()

        for lang_info in "${LANGUAGES[@]}"; do
            run_language "$lang_info" &
            pids+=($!)
        done

        # Wait for all processes to complete
        for pid in "${pids[@]}"; do
            if wait "$pid"; then
                ((SUCCESS_COUNT++))
            else
                ((FAILURE_COUNT++))
            fi
        done
    fi
fi

# Show final results
echo ""
echo -e "${PURPLE}📊 Final Results${NC}"
echo -e "${PURPLE}================${NC}"
echo -e "${GREEN}✅ Successful implementations: $SUCCESS_COUNT${NC}"
if [ $FAILURE_COUNT -gt 0 ]; then
    echo -e "${RED}❌ Failed implementations: $FAILURE_COUNT${NC}"
fi

TOTAL_RUN=$((SUCCESS_COUNT + FAILURE_COUNT))
echo -e "${BLUE}📈 Total implementations run: $TOTAL_RUN of ${#LANGUAGES[@]}${NC}"

if [ $FAILURE_COUNT -eq 0 ] && [ $TOTAL_RUN -gt 0 ]; then
    echo ""
    echo -e "${GREEN}🎉 All implementations completed successfully!${NC}"
    echo -e "${GREEN}🧠 Active Inference is truly multi-lingual!${NC}"
fi

echo ""
echo -e "${CYAN}💡 Tip: Use '$0 --list' to see all available implementations${NC}"
echo -e "${CYAN}💡 Tip: Use '$0 <language>' to run a specific implementation${NC}"

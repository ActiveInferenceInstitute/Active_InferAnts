#!/usr/bin/env bash
# Single gate entry point for Active InferAnts.
#
# Every arm here is the exact command CI runs (`.github/workflows/ci.yml` calls
# `./run.sh <arm>`); there is no second copy of any command. Documentation:
# docs/RUN_GUIDE.md.
#
# Usage: ./run.sh <arm> [arm...]     ./run.sh            # list arms
#
#   setup       install the one environment (requirements-dev.txt)
#   lint        ruff check + ruff format --check + compile sweep
#   test-fast   pytest -m "not gnn"   (no GNN checkout needed)
#   test-full   pytest                (adds the gnn-marked module)
#   docs        mkdocs build --strict, relative links, generated-doc freshness
#   gnn         provision the pinned GNN parser, then the conformance checks
#   metrics     re-measure every arm and rewrite docs/_generated/gate_metrics.md
#   gate        lint, test-fast, docs, gnn   (== test-full, without overlap)
#
# Interpreter: $PYTHON if set, else .venv/bin/python, else python3.
set -euo pipefail

ROOT=$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
cd "$ROOT"

if [ -n "${PYTHON:-}" ]; then
    PY=$PYTHON
elif [ -x "$ROOT/.venv/bin/python" ]; then
    PY=$ROOT/.venv/bin/python
else
    PY=python3
fi

# The lint surface: executable code this repository maintains. The
# multi-language implementation corpus under 0_CONTEXT/, the research corpora
# under 1_PREPARE/, and the third-party integrations under 9_OTHER/ are not
# lint-clean today and are outside the gate (counts: docs/RUN_GUIDE.md).
LINT_PATHS=(
    active_infer_ants
    tests
    scripts
    gnn_conformance.py
    2_OPERATE
    3_MEASURE
    4_REPORT
    5_FOLLOWUP
    6_API
)

GNN_ROOT=${GNN_ROOT:-$ROOT/.cache/gnn}
PIN=$ROOT/gnn/upstream.json

# name|one-line description; the same list drives `./run.sh` with no arguments.
arm_help=(
    "setup|install the one environment (requirements-dev.txt)"
    "lint|ruff check + ruff format --check + compile sweep"
    "test-fast|pytest -m 'not gnn' (no GNN checkout needed)"
    "test-full|pytest (adds the gnn-marked module)"
    "docs|mkdocs --strict, relative links, generated-doc freshness"
    "gnn|provision the pinned GNN parser, then the conformance checks"
    "metrics|re-measure every arm, rewrite docs/_generated/gate_metrics.md"
    "gate|lint, test-fast, docs, gnn (== test-full, without overlap)"
)

usage() {
    printf 'Usage: ./run.sh <arm> [arm...]     ./run.sh    # list arms\n\n'
    printf 'Every arm is the exact command CI runs (.github/workflows/ci.yml).\n'
    printf 'Documentation: docs/RUN_GUIDE.md\n\n'
    local entry
    for entry in "${arm_help[@]}"; do
        printf '  %-10s %s\n' "${entry%%|*}" "${entry#*|}"
    done
    printf '\nInterpreter: $PYTHON if set, else .venv/bin/python, else python3.\n'
}

section() {
    printf '\n== %s ==\n' "$1"
}

setup() {
    section "setup: $PY -m pip install -r requirements-dev.txt"
    "$PY" -m pip install -r requirements-dev.txt
}

lint() {
    section "lint: ruff on the maintained surface"
    "$PY" -m ruff check "${LINT_PATHS[@]}"
    "$PY" -m ruff format --check "${LINT_PATHS[@]}"
    section "lint: compile sweep over every tracked Python file"
    ./scripts/check_compile.sh
}

test_fast() {
    section "test-fast: pytest -m 'not gnn'"
    "$PY" -m pytest -q -m "not gnn"
}

test_full() {
    section "test-full: pytest"
    "$PY" -m pytest -q
}

docs() {
    section "docs: mkdocs build --strict"
    NO_MKDOCS_2_WARNING=1 "$PY" -m mkdocs build --strict --quiet
    section "docs: relative links"
    "$PY" scripts/check_doc_links.py
    section "docs: generated files are current"
    "$PY" scripts/docgen/doc_index.py --check
    "$PY" scripts/docgen/gate_metrics.py --check
    echo "docs: site built, relative links checked, generated files current"
}

provision_gnn() {
    local commit tag head
    commit=$("$PY" -c 'import json,sys;print(json.load(open(sys.argv[1]))["commit"])' "$PIN")
    tag=$("$PY" -c 'import json,sys;print(json.load(open(sys.argv[1]))["tag"])' "$PIN")
    head=$(git -C "$GNN_ROOT" rev-parse HEAD 2>/dev/null || true)
    if [ "$head" = "$commit" ] && [ -x "$GNN_ROOT/.venv/bin/python" ]; then
        echo "gnn: reusing $GNN_ROOT at $commit"
        return
    fi
    section "gnn: provisioning the pinned parser at $tag ($commit)"
    rm -rf "$GNN_ROOT"
    mkdir -p "$(dirname "$GNN_ROOT")"
    git init --quiet "$GNN_ROOT"
    git -C "$GNN_ROOT" remote add origin \
        https://github.com/ActiveInferenceInstitute/Generalized_Notation_Notation.git
    # A pin that no longer resolves upstream fails here rather than skipping.
    git -C "$GNN_ROOT" fetch --depth 1 origin "$commit" "refs/tags/$tag:refs/tags/$tag"
    git -C "$GNN_ROOT" checkout --quiet --detach "$commit"
    "$PY" -m venv "$GNN_ROOT/.venv"
    "$GNN_ROOT/.venv/bin/python" -m pip install --quiet numpy defusedxml
}

gnn() {
    provision_gnn
    export GNN_ROOT
    section "gnn: validate_gnn_spec.py"
    "$PY" scripts/validate_gnn_spec.py
    section "gnn: pytest -m gnn"
    "$PY" -m pytest -q -m gnn
}

metrics() {
    section "metrics: measuring every arm"
    "$PY" scripts/docgen/gate_metrics.py --write
}

gate() {
    lint
    test_fast
    docs
    gnn
}

if [ $# -eq 0 ]; then
    usage
    exit 0
fi

for arm in "$@"; do
    case "$arm" in
        setup) setup ;;
        lint) lint ;;
        test-fast) test_fast ;;
        test-full) test_full ;;
        docs) docs ;;
        gnn) gnn ;;
        metrics) metrics ;;
        gate) gate ;;
        -h|--help|help) usage ;;
        *) echo "run.sh: unknown arm '$arm'" >&2; usage >&2; exit 2 ;;
    esac
done

#!/usr/bin/env bash
# Single gate entry point for Active InferAnts.
#
# Every arm here is the exact command CI runs (`.github/workflows/ci.yml` calls
# `./run.sh <arm>`); there is no second copy of any command. Documentation:
# docs/RUN_GUIDE.md.
#
# Usage: ./run.sh <arm> [arm...]     ./run.sh            # fast tests
#
#   setup       sync the locked development environment (uv.lock)
#   lint        ruff check + ruff format --check + compile sweep
#   test-fast   pytest -m "not gnn"   (no GNN checkout needed)
#   test-full   pytest                (adds the gnn-marked module)
#   docs        mkdocs build --strict, relative links, generated-doc freshness
#   gnn         provision the pinned GNN parser, then the conformance checks
#   metrics     re-measure every arm and rewrite docs/_generated/gate_metrics.md
#   gate        lint, test-fast, docs, gnn   (full gate without overlap)
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

# GNN_ROOT is only honoured when the caller sets it, and then it is read-only.
# Unset, the gnn arm provisions its own cache under .cache/gnn/<pin commit>/.
PIN=$ROOT/gnn/upstream.json

# name|one-line description; the same list drives `./run.sh --help`.
arm_help=(
    "setup|sync the locked development environment (uv.lock)"
    "lint|ruff check + ruff format --check + compile sweep"
    "test-fast|pytest -m 'not gnn' (no GNN checkout needed)"
    "test-full|pytest (adds the gnn-marked module)"
    "docs|mkdocs --strict, relative links, generated-doc freshness"
    "gnn|shared importer check + pinned parser + conformance checks"
    "metrics|re-measure every arm, rewrite docs/_generated/gate_metrics.md"
    "gate|lint, test-fast, docs, gnn (== test-full, without overlap)"
)

usage() {
    printf 'Usage: ./run.sh <arm> [arm...]     ./run.sh    # fast tests\n\n'
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
    section "setup: uv sync --locked --extra dev --extra docs"
    uv sync --locked --extra dev --extra docs --python "${UV_PYTHON:-$PY}"
}

lint() {
    section "lint: ruff on the maintained surface"
    "$PY" -m ruff check "${LINT_PATHS[@]}"
    "$PY" -m ruff format --check "${LINT_PATHS[@]}"
    section "lint: compile sweep over every tracked Python file"
    PYTHON="$PY" ./scripts/check_compile.sh
}

test_fast() {
    section "test-fast: pytest -m 'not gnn'"
    "$PY" -m pytest -q -m "not gnn"
}

test_full() {
    prepare_gnn
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

pin_field() {
    "$PY" -c 'import json,sys;print(json.load(open(sys.argv[1]))[sys.argv[2]])' \
        "$PIN" "$1"
}

# A caller-supplied GNN_ROOT is read-only: verify it and refuse if it cannot be
# used. Nothing is created, replaced or removed inside it — it may be another
# repository's working copy with local work in it.
require_readonly_gnn_checkout() {
    local root=$1 commit=$2
    if [ ! -d "$root" ]; then
        echo "gnn: GNN_ROOT=$root does not exist; supply a checkout of the pin" >&2
        echo "     or unset GNN_ROOT to let ./run.sh provision its own cache" >&2
        return 2
    fi
    if ! git -C "$root" cat-file -e "$commit^{commit}" 2>/dev/null; then
        echo "gnn: GNN_ROOT=$root does not contain the pinned commit $commit" >&2
        echo "     (it is treated as read-only, so ./run.sh will not fetch into it)" >&2
        return 2
    fi
    if [ -n "${GNN_PYTHON:-}" ]; then
        if [ ! -x "$GNN_PYTHON" ]; then
            echo "gnn: GNN_PYTHON=$GNN_PYTHON is not executable" >&2
            return 2
        fi
    elif [ ! -x "$root/.venv/bin/python" ]; then
        if ! "$PY" -c "import defusedxml, numpy" >/dev/null 2>&1; then
            echo "gnn: GNN_ROOT=$root has no .venv and $PY lacks numpy/defusedxml" >&2
            echo "     set GNN_PYTHON, or unset GNN_ROOT to provision an owned cache" >&2
            return 2
        fi
    fi
    echo "gnn: using read-only GNN_ROOT=$root at $commit"
}

# Provision into a directory this script just created: no recursive replacement
# of an existing path, so a stale or foreign cache can never be erased.
provision_owned_gnn_cache() {
    local commit=$1 tag=$2 cache target
    cache=$ROOT/.cache/gnn/$commit
    if [ -d "$cache/.git" ] && [ -x "$cache/.venv/bin/python" ] &&
        [ "$(git -C "$cache" rev-parse HEAD 2>/dev/null)" = "$commit" ]; then
        GNN_ROOT=$cache
        echo "gnn: reusing owned cache $cache at $commit"
        return
    fi
    section "gnn: provisioning the pinned parser at $tag ($commit)"
    mkdir -p "$ROOT/.cache/gnn"
    # `mkdir` fails if the path exists, so an incomplete or foreign cache is
    # never replaced — the arm provisions beside it instead.
    if mkdir "$cache" 2>/dev/null; then
        target=$cache
    else
        target=$(mktemp -d "$ROOT/.cache/gnn/${commit}.XXXXXX")
    fi
    git init --quiet "$target"
    git -C "$target" remote add origin \
        https://github.com/ActiveInferenceInstitute/Generalized_Notation_Notation.git
    # A pin that no longer resolves upstream fails here rather than skipping.
    git -C "$target" fetch --depth 1 origin "$commit" "refs/tags/$tag:refs/tags/$tag"
    git -C "$target" checkout --quiet --detach "$commit"
    "$PY" -m venv "$target/.venv"
    # numpy/defusedxml for the extractor, PyYAML for the specification parser
    # the reader drives (without it the parser falls back and warns per file).
    "$target/.venv/bin/python" -m pip install --quiet numpy defusedxml pyyaml
    GNN_ROOT=$target
    echo "gnn: provisioned $GNN_ROOT at $commit"
}

prepare_gnn() {
    local commit tag
    commit=$(pin_field commit)
    tag=$(pin_field tag)
    if [ -n "${GNN_ROOT:-}" ]; then
        require_readonly_gnn_checkout "$GNN_ROOT" "$commit"
    else
        provision_owned_gnn_cache "$commit" "$tag"
    fi
    export GNN_ROOT
}

# The shared reader from the GNN-FEP contract, called from the environment the
# arm already built: the pinned checkout supplies the module and the parser, so
# this repository carries no copy of either. `python -m gnn.importers check
# --repo .` is the arm the GNN-FEP member table records for this repository; the
# pointer flags are added because `.github/GNN.md` names the pin, the revision,
# this workflow and this job key (GNN-FEP migration step 1).
gnn_reader() {
    local python
    if [ -n "${GNN_PYTHON:-}" ]; then
        python=$GNN_PYTHON
    elif [ -x "$GNN_ROOT/.venv/bin/python" ]; then
        python=$GNN_ROOT/.venv/bin/python
    else
        python=$PY
    fi
    section "gnn: importers check (shared reader at the pinned revision)"
    PYTHONPATH="$GNN_ROOT/src${PYTHONPATH:+:$PYTHONPATH}" \
        "$python" -m gnn.importers check --repo . --require-pointer \
        --workflow .github/workflows/ci.yml --job gnn-conformance
}

gnn() {
    prepare_gnn
    gnn_reader
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
    test_fast
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

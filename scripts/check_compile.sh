#!/usr/bin/env bash
# Compile-check every tracked Python source (space-safe). Exits non-zero on any
# syntax error. Used by the pre-commit "py-compile" hook and local QA.
set -u

root="$(git rev-parse --show-toplevel 2>/dev/null || echo .)"
failed=0

while IFS= read -r -d '' f; do
    if [ -f "$f" ]; then
        python3 -m py_compile "$f" || { echo "COMPILE FAIL: $f" >&2; failed=1; }
    fi
done < <(cd "$root" && git ls-files -z '*.py')

exit $failed

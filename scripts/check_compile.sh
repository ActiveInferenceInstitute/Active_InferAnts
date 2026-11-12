#!/usr/bin/env bash
# Compile every tracked Python source in one interpreter, including spaced paths.
set -euo pipefail
"${PYTHON:-python3}" - <<'PY'
import pathlib
import py_compile
import subprocess
import sys

paths = subprocess.check_output(
    ["git", "ls-files", "-z", "*.py"], stdin=subprocess.DEVNULL
).decode().split("\0")
failed = False
for name in filter(None, paths):
    if pathlib.Path(name).is_file():
        try:
            py_compile.compile(name, doraise=True)
        except py_compile.PyCompileError as exc:
            print(f"COMPILE FAIL: {name}: {exc}", file=sys.stderr)
            failed = True
sys.exit(int(failed))
PY

#!/bin/bash
set -e
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
echo "🧠 Running Common Lisp Active Inference implementation..."
if command -v sbcl &> /dev/null; then
    sbcl --script "$SCRIPT_DIR/active_inference.lisp"
elif command -v clisp &> /dev/null; then
    clisp "$SCRIPT_DIR/active_inference.lisp"
elif command -v ecl &> /dev/null; then
    ecl --shell "$SCRIPT_DIR/active_inference.lisp"
else
    echo "❌ No Common Lisp implementation found. Install SBCL: https://www.sbcl.org/"
    exit 1
fi

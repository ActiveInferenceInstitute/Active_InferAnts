#!/bin/bash
set -e
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
echo "🧠 Running Tcl Active Inference implementation..."
if command -v tclsh &> /dev/null; then
    tclsh "$SCRIPT_DIR/active_inference.tcl"
else
    echo "❌ Tcl not found. Install: https://www.tcl-lang.org/"
    exit 1
fi

#!/bin/bash
# Active Inference - D Implementation Runner
set -e
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
echo "🧠 Running D Active Inference implementation..."

if command -v dmd &> /dev/null; then
    cd "$SCRIPT_DIR"
    dmd -run active_inference.d
elif command -v ldc2 &> /dev/null; then
    cd "$SCRIPT_DIR"
    ldc2 -run active_inference.d
elif command -v gdc &> /dev/null; then
    cd "$SCRIPT_DIR"
    gdc -o active_inference active_inference.d && ./active_inference
else
    echo "❌ No D compiler found. Install: https://dlang.org/download.html"
    exit 1
fi

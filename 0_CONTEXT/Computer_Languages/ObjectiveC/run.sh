#!/bin/bash
set -e
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
echo "🧠 Running Objective-C Active Inference implementation..."
if command -v clang &> /dev/null; then
    clang -framework Foundation -o "$SCRIPT_DIR/active_inference" "$SCRIPT_DIR/active_inference.m" -lm
    "$SCRIPT_DIR/active_inference"
else
    echo "❌ clang not found. Install Xcode Command Line Tools."
    exit 1
fi

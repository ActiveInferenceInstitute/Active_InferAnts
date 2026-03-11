#!/bin/bash
set -e
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
echo "🧠 Running Groovy Active Inference implementation..."
if command -v groovy &> /dev/null; then
    groovy "$SCRIPT_DIR/active_inference.groovy"
else
    echo "❌ Groovy not found. Install: https://groovy-lang.org/install.html"
    exit 1
fi

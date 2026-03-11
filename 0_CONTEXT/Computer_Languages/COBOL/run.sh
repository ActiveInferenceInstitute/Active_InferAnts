#!/bin/bash
set -e
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
echo "🧠 Running COBOL Active Inference implementation..."
if command -v cobc &> /dev/null; then
    cobc -x -o "$SCRIPT_DIR/active_inference" "$SCRIPT_DIR/active_inference.cob" 2>/dev/null
    "$SCRIPT_DIR/active_inference"
else
    echo "❌ GnuCOBOL not found. Install: https://gnucobol.sourceforge.io/"
    exit 1
fi

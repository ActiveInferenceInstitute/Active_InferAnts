#!/bin/bash
set -e
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
echo "🧠 Running Scheme Active Inference implementation..."
if command -v chibi-scheme &> /dev/null; then
    chibi-scheme "$SCRIPT_DIR/active_inference.scm"
elif command -v guile &> /dev/null; then
    guile --r7rs "$SCRIPT_DIR/active_inference.scm"
elif command -v chicken-csi &> /dev/null; then
    chicken-csi -script "$SCRIPT_DIR/active_inference.scm"
elif command -v gosh &> /dev/null; then
    gosh "$SCRIPT_DIR/active_inference.scm"
else
    echo "❌ No Scheme implementation found. Install chibi-scheme or Guile."
    exit 1
fi

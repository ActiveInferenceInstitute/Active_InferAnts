#!/bin/bash
# Active Inference - Dart Implementation Runner
set -e
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
echo "🧠 Running Dart Active Inference implementation..."

if command -v dart &> /dev/null; then
    dart run "$SCRIPT_DIR/active_inference.dart"
else
    echo "❌ Dart SDK not found. Install: https://dart.dev/get-dart"
    exit 1
fi

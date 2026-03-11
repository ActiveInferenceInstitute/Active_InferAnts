#!/bin/bash
set -e
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
echo "🧠 Running PowerShell Active Inference implementation..."
if command -v pwsh &> /dev/null; then
    pwsh -File "$SCRIPT_DIR/active_inference.ps1"
elif command -v powershell &> /dev/null; then
    powershell -File "$SCRIPT_DIR/active_inference.ps1"
else
    echo "❌ PowerShell not found. Install: https://github.com/PowerShell/PowerShell"
    exit 1
fi

#!/bin/bash

# Active Inference Shell Implementation Runner

set -e

echo "🐚 Shell Active Inference Demo"
echo "=============================="

# Check for required shell utilities
for cmd in bc awk sed grep sort uniq; do
    if ! command -v $cmd &> /dev/null; then
        echo "❌ Error: $cmd not found"
        echo "Please install POSIX utilities"
        exit 1
    fi
done

echo "✅ All required shell utilities found"

# Use the checked-in config.sh (must exist alongside this script)
if [ ! -f config.sh ]; then
    echo "❌ Error: config.sh not found in Shell directory"
    echo "Please ensure Shell/config.sh exists"
    exit 1
fi

# Run the simulation
echo "🚀 Running Shell active inference simulation..."
./Active_Shellference.sh

echo ""
echo "✅ Shell simulation completed successfully!"

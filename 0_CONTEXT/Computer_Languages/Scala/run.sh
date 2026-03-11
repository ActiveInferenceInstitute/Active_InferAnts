#!/bin/bash

# Active Inference Scala Demo Runner

set -e

echo "🧠 Active Inference Scala Implementation"
echo "======================================"

# Check for Scala/SBT
if ! command -v sbt &> /dev/null; then
    if ! command -v scala &> /dev/null; then
        echo "❌ Neither SBT nor Scala found"
        echo "Please install Scala/SBT:"
        echo "  Ubuntu/Debian: sudo apt-get install scala"
        echo "  macOS: brew install scala sbt"
        echo "  Or download from: https://www.scala-lang.org/download/"
        exit 1
    fi
fi

if command -v sbt &> /dev/null; then
    echo "✅ SBT found: $(sbt --version | head -1)"
    echo "🚀 Running Scala implementation with SBT..."

    # Compile and run with SBT
    sbt "runMain activeinference.ActiveInferenceDemo"

    if [ $? -eq 0 ]; then
        echo ""
        echo "✅ Scala simulation completed successfully!"
    else
        echo "❌ SBT execution failed."
        exit 1
    fi

elif command -v scala &> /dev/null; then
    echo "✅ Scala found: $(scala -version 2>&1 | head -1)"
    echo "🚀 Running Scala implementation..."

    # Compile and run with Scala directly
    scalac -d . src/main/scala/ActiveInferenceAgent.scala
    scala -cp . activeinference.ActiveInferenceDemo

    if [ $? -eq 0 ]; then
        echo ""
        echo "✅ Scala simulation completed successfully!"
    else
        echo "❌ Scala execution failed."
        exit 1
    fi
fi

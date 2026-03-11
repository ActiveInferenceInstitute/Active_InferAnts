#!/bin/bash

# Active Inference Julia Implementation Runner

set -e

echo "🔴 Julia Active Inference Demo"
echo "=============================="

# Check if Julia is installed
if ! command -v julia &> /dev/null; then
    echo "❌ Error: Julia not found"
    echo "Please install Julia from: https://julialang.org/downloads/"
    exit 1
fi

echo "✅ Julia found: $(julia --version)"

# Run the main implementation
echo "🚀 Running Julia active inference simulation..."
julia Julia_InferAnts.jl

# Run RxInfer version if available
if [ -f "RxInfer_Agent_Model.jl" ]; then
    echo "🧠 Running RxInfer active inference simulation..."
    julia RxInfer_Agent_Model.jl
fi

# Run Mountain Car integration if available
if [ -d "SideCar/MC_AI" ]; then
    echo "🏔️ Running Mountain Car reinforcement learning..."
    if ! (cd SideCar/MC_AI && julia run.jl); then
        echo "⚠️ Warning: Mountain Car simulation failed or not available"
    fi
fi

echo ""
echo "✅ Julia simulation completed successfully!"

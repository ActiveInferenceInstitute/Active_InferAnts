#!/bin/bash

# Active Inference C# Implementation Runner

set -e

echo "🔷 C# Active Inference Demo"
echo "============================"

# Check if .NET is installed
if ! command -v dotnet &> /dev/null; then
    echo "❌ Error: .NET SDK not found"
    echo "Please install .NET from: https://dotnet.microsoft.com/download"
    exit 1
fi

echo "✅ .NET found: $(dotnet --version)"

# Build the implementation
echo "🔨 Building C# implementation..."
dotnet build --configuration Release

# Run the simulation (set -e handles build failures above)
echo "🚀 Running C# active inference simulation..."
dotnet run --configuration Release

echo ""
echo "✅ C# simulation completed successfully!"

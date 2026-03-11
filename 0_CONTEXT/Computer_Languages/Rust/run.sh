#!/bin/bash

# Active Inference Rust Implementation Runner

set -e

echo "🦀 Rust Active Inference Demo"
echo "=============================="

# Check if Rust is installed
if ! command -v cargo &> /dev/null; then
    echo "❌ Error: Cargo not found"
    echo "Please install Rust from: https://rustup.rs/"
    exit 1
fi

echo "✅ Rust found: $(cargo --version)"

# Check if we're in the right directory
if [ ! -f "Cargo.toml" ]; then
    echo "❌ Error: Cargo.toml not found. Please run from the Rust implementation directory."
    exit 1
fi

# Create output directory
mkdir -p output

# Build the implementation
echo "🔨 Building Rust implementation..."
cargo build --release

# Run the simulation (set -e handles build failures above)
echo "🚀 Running Rust active inference simulation..."
cargo run --release

echo ""
echo "✅ Rust simulation completed successfully!"

# Check for output files
if [ -d "output" ] && [ "$(ls -A output)" ]; then
    echo "📁 Output files generated:"
    ls -la output/
fi

# Run tests if requested
if [ "$1" = "--test" ]; then
    echo "🧪 Running tests..."
    cargo test
fi

# Generate documentation if requested
if [ "$1" = "--docs" ]; then
    echo "📚 Generating documentation..."
    cargo doc --no-deps
    echo "   Documentation available in target/doc/"
fi

# Show performance info if requested
if [ "$1" = "--bench" ]; then
    echo "📊 Running benchmarks..."
    cargo bench 2>/dev/null || echo "   No benchmarks available"
fi

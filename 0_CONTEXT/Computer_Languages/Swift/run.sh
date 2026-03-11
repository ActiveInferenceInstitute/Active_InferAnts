#!/bin/bash

# Active Inference Swift Demo Runner

set -e

echo "🧠 Active Inference Swift Implementation"
echo "======================================="

# Check for Swift
if ! command -v swift &> /dev/null; then
    echo "❌ Swift not found"
    echo "Please install Swift:"
    echo "  macOS: xcode-select --install (installs Command Line Tools)"
    echo "  Ubuntu/Debian: sudo apt-get install swiftlang"
    echo "  CentOS/RHEL: sudo yum install swift-lang"
    echo "  Or download from: https://swift.org/download/"
    exit 1
fi

echo "✅ Swift found: $(swift --version | head -1)"

# Check Swift version (Swift 5.5+ recommended)
SWIFT_VERSION=$(swift --version | head -1 | grep -oE '[0-9]+\.[0-9]+' | head -1)
REQUIRED_VERSION="5.5"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$SWIFT_VERSION" | sort -V | head -n1)" = "$REQUIRED_VERSION" ]; then
    echo "✅ Swift version $SWIFT_VERSION meets requirements"
else
    echo "⚠️  Swift version $SWIFT_VERSION may not support all features (Swift 5.5+ recommended)"
fi

echo "🚀 Running Swift active inference simulation..."

# Check if Package.swift exists for Swift Package Manager
if [ -f "Package.swift" ]; then
    echo "📦 Using Swift Package Manager..."

    # Build and run with Swift Package Manager
    swift run

    if [ $? -eq 0 ]; then
        echo ""
        echo "✅ Swift simulation completed successfully!"
    else
        echo "❌ Swift Package Manager execution failed."
        exit 1
    fi

else
    echo "🔧 Using direct compilation..."

    # Compile and run directly
    swiftc -o ActiveInferenceSwift ActiveInferenceAgent.swift
    ./ActiveInferenceSwift

    if [ $? -eq 0 ]; then
        echo ""
        echo "✅ Swift simulation completed successfully!"
    else
        echo "❌ Swift compilation/execution failed."
        exit 1
    fi
fi

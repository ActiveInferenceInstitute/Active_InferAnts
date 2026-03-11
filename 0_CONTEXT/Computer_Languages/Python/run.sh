#!/bin/bash

# Active Inference Python Implementation Runner

set -e

echo "🐍 Python Active Inference Demo"
echo "==============================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 not found"
    echo "Please install Python 3 with: sudo apt-get install python3"
    exit 1
fi

echo "✅ Python found: $(python3 --version)"

# Install dependencies
echo "📦 Installing Python dependencies..."
if ! pip3 install -r requirements.txt; then
    echo "⚠️ Warning: Could not install packages globally, trying user install..."
    pip3 install --user -r requirements.txt || { echo "❌ Error: Could not install Python dependencies"; exit 1; }
fi

# Run the main implementation
echo "🚀 Running Python active inference simulation..."
python3 student_teacher.py

# Generate visualizations
echo "📊 Generating visualization plots..."
python3 -c "
from student_teacher import StudentTeacherPOMDP
import matplotlib.pyplot as plt

# Create and visualize matrices
pomdp = StudentTeacherPOMDP(4, 3, 2)
pomdp.plot_matrices()
plt.close('all')
print('Visualization plots generated in output/ directory')
"

echo ""
echo "✅ Python simulation completed successfully!"
echo "📁 Check the output/ directory for generated visualizations!"

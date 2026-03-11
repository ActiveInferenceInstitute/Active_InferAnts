#!/usr/bin/env python3
"""
Comprehensive Active Inference Multi-Language Reporting System

This system analyzes and visualizes results from all language implementations,
providing comprehensive benchmarking, comparison, and visualization capabilities.
"""

import os
import sys
import json
import subprocess
import time
import psutil
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any, Union
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def _configure_plot_style() -> None:
    """Configure matplotlib and seaborn global style — called at entry point, not import time."""
    plt.style.use('seaborn-v0_8-darkgrid')
    sns.set_palette("husl")


class LanguageImplementation:
    """Represents a single language implementation."""

    def __init__(self, name: str, directory: str):
        self.name = name
        self.directory = Path(directory)
        self.readme_path = self.directory / "README.md"
        self.run_script = self.directory / "run.sh"
        self.implemented = self._check_implementation()

    def _check_implementation(self) -> bool:
        """Check if implementation is properly set up."""
        has_readme = self.readme_path.exists()
        has_run_script = self.run_script.exists()
        run_script_executable = has_run_script and os.access(self.run_script, os.X_OK)

        return has_readme and run_script_executable

    def run_benchmark(self) -> Dict[str, Any]:
        """Run benchmark for this implementation."""
        if not self.implemented:
            return {"error": "Not implemented"}

        try:
            start_time = time.time()
            start_memory = psutil.Process().memory_info().rss

            # Run the implementation
            result = subprocess.run(
                [str(self.run_script)],
                capture_output=True,
                text=True,
                timeout=300,  # 5 minute timeout
                cwd=self.directory
            )

            end_time = time.time()
            end_memory = psutil.Process().memory_info().rss

            return {
                "success": result.returncode == 0,
                "execution_time": end_time - start_time,
                "memory_used": end_memory - start_memory,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "return_code": result.returncode
            }

        except subprocess.TimeoutExpired:
            return {"error": "Timeout"}
        except Exception as e:
            return {"error": str(e)}

class ActiveInferenceAnalyzer:
    """Comprehensive analyzer for all implementations."""

    def __init__(self, root_directory: Union[str, Path] = "."):
        self.root_directory = Path(root_directory)
        self.implementations = self._discover_implementations()
        self.results = {}

    def _discover_implementations(self) -> List[LanguageImplementation]:
        """Discover all language implementations."""
        implementations = []

        # Skip these directories
        skip_dirs = {"__pycache__", ".git", "output", "node_modules"}

        for item in self.root_directory.iterdir():
            if item.is_dir() and item.name not in skip_dirs:
                impl = LanguageImplementation(item.name, item)
                implementations.append(impl)

        return sorted(implementations, key=lambda x: x.name)

    def run_all_benchmarks(self) -> Dict[str, Dict[str, Any]]:
        """Run benchmarks for all implementations."""
        print("🧪 Running benchmarks for all implementations...")
        print("=" * 60)

        results = {}
        for impl in self.implementations:
            print(f"🔄 Testing {impl.name}...")
            result = impl.run_benchmark()
            results[impl.name] = result

            if result.get("success"):
                print(f"   ⏱️  Time: {result.get('execution_time', 0):.2f}s")
                print(f"   📊 Memory: {result.get('memory_used', 0) / 1024 / 1024:.1f} MB")
            else:
                print(f"   ❌ Failed: {result.get('error', 'Unknown error')}")

        self.results = results
        return results

    def generate_comprehensive_report(self) -> str:
        """Generate comprehensive HTML report."""
        total = len(self.implementations)
        implemented = sum(1 for impl in self.implementations if impl.implemented)
        html_content = f"<html><body><h1>Active Inference Report</h1>"
        html_content += f"<p>Total implementations: {total}</p>"
        html_content += f"<p>Implemented: {implemented} ({100*implemented/max(total,1):.1f}%)</p>"
        html_content += f"</body></html>"
        return html_content

    def create_visualizations(self):
        """Create comprehensive visualizations."""
        if not self.results:
            print("❌ No results to visualize. Run benchmarks first.")
            return

        # Prepare data
        successful_impls = {name: result for name, result in self.results.items()
                          if result.get("success", False)}

        if not successful_impls:
            print("❌ No successful implementations to visualize.")
            return

        # Create performance comparison plot
        self._create_performance_plot(successful_impls)

        # Create memory usage plot
        self._create_memory_plot(successful_impls)

        # Create implementation status plot
        self._create_status_plot()

        # Create language category analysis
        self._create_category_analysis()

        print("📊 Visualizations created in 'visualizations/' directory")

    def _create_performance_plot(self, successful_impls: Dict[str, Dict[str, Any]]):
        """Create performance comparison plot."""
        languages = list(successful_impls.keys())
        execution_times = [result["execution_time"] for result in successful_impls.values()]

        plt.figure(figsize=(12, 6))
        bars = plt.bar(languages, execution_times, color='skyblue')
        plt.title('Active Inference Implementation Performance Comparison', fontsize=16, fontweight='bold')
        plt.xlabel('Programming Language', fontsize=12)
        plt.ylabel('Execution Time (seconds)', fontsize=12)
        plt.xticks(rotation=45, ha='right')

        # Add value labels on bars
        for bar, time_val in zip(bars, execution_times):
            plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                    f'{time_val:.2f}', ha='center', va='bottom', fontsize=10)

        plt.tight_layout()
        plt.savefig('visualizations/performance_comparison.png', dpi=300, bbox_inches='tight')
        plt.close()

    def _create_memory_plot(self, successful_impls: Dict[str, Dict[str, Any]]):
        """Create memory usage plot."""
        languages = list(successful_impls.keys())
        memory_usage = [result["memory_used"] / 1024 / 1024 for result in successful_impls.values()]  # MB

        plt.figure(figsize=(12, 6))
        bars = plt.bar(languages, memory_usage, color='lightcoral')
        plt.title('Memory Usage Comparison', fontsize=16, fontweight='bold')
        plt.xlabel('Programming Language', fontsize=12)
        plt.ylabel('Memory Usage (MB)', fontsize=12)
        plt.xticks(rotation=45, ha='right')

        for bar, mem in zip(bars, memory_usage):
            plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                    f'{mem:.1f}', ha='center', va='bottom', fontsize=10)

        plt.tight_layout()
        plt.savefig('visualizations/memory_usage.png', dpi=300, bbox_inches='tight')
        plt.close()

    def _create_status_plot(self):
        """Create implementation status plot."""
        implemented = sum(1 for impl in self.implementations if impl.implemented)
        not_implemented = len(self.implementations) - implemented

        plt.figure(figsize=(8, 8))
        plt.pie([implemented, not_implemented],
                labels=[f'Implemented ({implemented})', f'Not Implemented ({not_implemented})'],
                autopct='%1.1f%%',
                colors=['#4CAF50', '#F44336'],
                startangle=90)
        plt.title('Implementation Status', fontsize=16, fontweight='bold')
        plt.axis('equal')
        plt.savefig('visualizations/implementation_status.png', dpi=300, bbox_inches='tight')
        plt.close()

    def _create_category_analysis(self):
        """Create language category analysis."""
        categories = {
            'Systems': ['Ada', 'Assembly', 'C', 'CSharp', 'Cpp', 'Crystal', 'Golang', 'Nim', 'Odin', 'Pascal', 'Rust', 'Swift', 'V', 'Zig'],
            'Functional': ['Clojure', 'Elixir', 'Erlang', 'FSharp', 'Haskell', 'OCaml', 'Racket'],
            'Scripting': ['JavaScript', 'Lua', 'Perl', 'PHP', 'Python', 'Ruby', 'Shell', 'TypeScript'],
            'Scientific': ['Fortran', 'Julia', 'MATLAB', 'R'],
            'JVM': ['Java', 'Kotlin', 'Scala'],
            'Logic': ['Prolog', 'SQL', 'Jock'],
            'Esoteric': ['Brainfuck']
        }

        category_counts = {}
        for category, langs in categories.items():
            count = sum(1 for lang in langs if any(impl.name == lang for impl in self.implementations))
            if count > 0:
                category_counts[category] = count

        if category_counts:
            plt.figure(figsize=(10, 6))
            bars = plt.bar(category_counts.keys(), category_counts.values(),
                         color='mediumpurple')
            plt.title('Language Categories', fontsize=16, fontweight='bold')
            plt.xlabel('Category', fontsize=12)
            plt.ylabel('Number of Languages', fontsize=12)
            plt.xticks(rotation=45, ha='right')

            for bar, count in zip(bars, category_counts.values()):
                plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                        str(count), ha='center', va='bottom', fontsize=10)

            plt.tight_layout()
            plt.savefig('visualizations/language_categories.png', dpi=300, bbox_inches='tight')
            plt.close()

    def generate_summary_report(self) -> str:
        """Generate summary report."""
        total_impls = len(self.implementations)
        implemented = sum(1 for impl in self.implementations if impl.implemented)
        successful_runs = sum(1 for result in self.results.values() if result.get("success", False))

        report = f"""\n{'='*60}
🧠 Active Inference Multi-Language Analysis Summary
{'='*60}
📁 Total implementations discovered: {total_impls}
✅ Fully implemented: {implemented} ({100*implemented/max(total_impls,1):.1f}%)
🧪 Successful benchmark runs: {successful_runs}
{'='*60}
"""
        return report

    def export_results_to_json(self, filename: str = "benchmark_results.json"):
        """Export results to JSON."""
        # Add metadata
        export_data = {
            "timestamp": datetime.now().isoformat(),
            "total_implementations": len(self.implementations),
            "results": self.results,
            "system_info": {
                "python_version": sys.version,
                "platform": sys.platform
            }
        }

        with open(filename, 'w') as f:
            json.dump(export_data, f, indent=2, default=str)

        print(f"📄 Results exported to {filename}")

def main():
    """Main function."""
    _configure_plot_style()
    print("🧠 Active Inference Multi-Language Analysis System")
    print("=" * 60)

    # Create output directory
    Path("visualizations").mkdir(exist_ok=True)

    # Initialize analyzer
    analyzer = ActiveInferenceAnalyzer()

    # Show discovered implementations
    print("📁 Discovered implementations:")
    for impl in analyzer.implementations:
        status = "✅" if impl.implemented else "❌"
        print(f"   {status} {impl.name}")
    print()

    # Run benchmarks
    results = analyzer.run_all_benchmarks()

    # Generate visualizations
    analyzer.create_visualizations()

    # Export results
    analyzer.export_results_to_json()

    # Generate summary
    summary = analyzer.generate_summary_report()
    print("\n" + summary)

    # Save summary to file
    with open("analysis_summary.txt", "w") as f:
        f.write(summary)

    print("📊 Complete analysis saved to 'analysis_summary.txt'")
    print("📁 Visualizations saved to 'visualizations/' directory")

if __name__ == "__main__":
    main()

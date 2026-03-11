#!/usr/bin/env python3
"""
Advanced Benchmarking Suite for Active Inference Multi-Language Implementation

This suite provides comprehensive performance analysis, statistical comparison,
and optimization recommendations across all language implementations.
"""

import os
import sys
import json
import time
import psutil
import subprocess
import statistics
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, asdict
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@dataclass
class PerformanceMetrics:
    """Detailed performance metrics for a single benchmark run"""
    language: str
    benchmark_name: str
    execution_time: float
    cpu_usage_percent: float
    peak_memory_mb: float
    average_memory_mb: float
    compile_time: float = 0.0
    startup_time: float = 0.0
    final_belief_entropy: float = 0.0
    free_energy_convergence: float = 0.0
    action_selection_diversity: float = 0.0
    simulation_steps: int = 0
    timestamp: str = ""

@dataclass
class BenchmarkConfig:
    """Configuration for a benchmark run"""
    name: str
    description: str
    iterations: int = 5
    timeout: int = 120
    parameters: Optional[Dict[str, Any]] = None

    def __post_init__(self):
        if self.parameters is None:
            self.parameters = {}

@dataclass
class StatisticalSummary:
    """Statistical summary of benchmark results"""
    mean: float
    median: float
    std_dev: float
    min_value: float
    max_value: float
    confidence_interval_95: Tuple[float, float]
    outliers: List[float]

@dataclass
class LanguageComparison:
    """Comparison data between languages"""
    metric_name: str
    rankings: List[Tuple[str, float]]
    best_performer: str
    worst_performer: str
    relative_performance: Dict[str, float]  # normalized to best
    statistical_significance: Dict[str, bool]  # vs best performer

@dataclass
class BenchmarkReport:
    """Complete benchmark report"""
    timestamp: str
    benchmark_configs: List[BenchmarkConfig]
    performance_results: Dict[str, List[PerformanceMetrics]]
    statistical_summaries: Dict[str, Dict[str, StatisticalSummary]]
    language_comparisons: Dict[str, LanguageComparison]
    system_info: Dict[str, Any]
    recommendations: List[str]

class AdvancedBenchmarkSuite:
    """Advanced benchmarking suite with statistical analysis"""

    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.languages_dir = self.project_root / "0_CONTEXT" / "Computer_Languages"
        self.results_dir = self.project_root / "benchmark_results"
        self.plots_dir = self.results_dir / "plots"
        self.results_dir.mkdir(exist_ok=True)
        self.plots_dir.mkdir(exist_ok=True)

        # Define benchmark configurations
        self.benchmark_configs = [
            BenchmarkConfig(
                name="basic_simulation",
                description="Basic 20-step simulation",
                iterations=3,
                timeout=60,
                parameters={"steps": 20}
            ),
            BenchmarkConfig(
                name="extended_simulation",
                description="Extended 100-step simulation",
                iterations=3,
                timeout=120,
                parameters={"steps": 100}
            ),
            BenchmarkConfig(
                name="memory_stress_test",
                description="Memory-intensive simulation",
                iterations=2,
                timeout=180,
                parameters={"steps": 50, "high_precision": True}
            ),
            BenchmarkConfig(
                name="startup_performance",
                description="Measure startup and initialization time",
                iterations=5,
                timeout=30,
                parameters={"minimal_run": True}
            )
        ]

    def get_system_info(self) -> Dict[str, Any]:
        """Gather system information for benchmarking context"""
        return {
            "platform": sys.platform,
            "python_version": sys.version,
            "cpu_count": os.cpu_count(),
            "total_memory_gb": round(psutil.virtual_memory().total / (1024**3), 2),
            "available_memory_gb": round(psutil.virtual_memory().available / (1024**3), 2),
            "hostname": os.uname().nodename if hasattr(os, 'uname') else "unknown"
        }

    def measure_memory_usage(self, process: subprocess.Popen) -> Tuple[float, float]:
        """Monitor memory usage of a process"""
        try:
            proc = psutil.Process(process.pid)
            memory_samples = []

            while process.poll() is None:
                try:
                    memory_mb = proc.memory_info().rss / (1024 * 1024)
                    memory_samples.append(memory_mb)
                    time.sleep(0.1)
                except psutil.NoSuchProcess:
                    break

            if memory_samples:
                return max(memory_samples), statistics.mean(memory_samples)
            else:
                return 0.0, 0.0

        except Exception as e:
            logger.warning(f"Failed to monitor memory usage: {e}")
            return 0.0, 0.0

    def run_single_benchmark(self, language: str, config: BenchmarkConfig) -> List[PerformanceMetrics]:
        """Run a single benchmark for a language"""
        results = []
        language_path = self.languages_dir / language

        if not language_path.exists():
            logger.warning(f"Language implementation not found: {language}")
            return results

        run_script = language_path / "run.sh"
        if not run_script.exists():
            logger.warning(f"Run script not found for {language}")
            return results

        logger.info(f"Running {config.name} benchmark for {language} ({config.iterations} iterations)")

        for iteration in range(config.iterations):
            try:
                start_time = time.time()

                # Start process and monitor resources
                process = subprocess.Popen(
                    [str(run_script)],
                    cwd=str(language_path),
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )

                # Monitor memory usage
                peak_memory, avg_memory = self.measure_memory_usage(process)

                # Wait for completion
                try:
                    stdout, stderr = process.communicate(timeout=config.timeout)
                    execution_time = time.time() - start_time

                    # Parse output for additional metrics
                    metrics = self.parse_output_metrics(language, stdout)

                    result = PerformanceMetrics(
                        language=language,
                        benchmark_name=config.name,
                        execution_time=execution_time,
                        cpu_usage_percent=0.0,  # Would need more complex monitoring
                        peak_memory_mb=peak_memory,
                        average_memory_mb=avg_memory,
                        final_belief_entropy=metrics.get('entropy', 0.0),
                        free_energy_convergence=metrics.get('free_energy', 0.0),
                        action_selection_diversity=metrics.get('action_diversity', 0.0),
                        simulation_steps=config.parameters.get('steps', 0),
                        timestamp=time.strftime('%Y-%m-%d %H:%M:%S')
                    )

                    results.append(result)
                    logger.debug(f"Iteration {iteration + 1}/{config.iterations} completed in {execution_time:.2f}s")

                except subprocess.TimeoutExpired:
                    process.kill()
                    logger.error(f"Benchmark {config.name} for {language} timed out (iteration {iteration + 1})")

            except Exception as e:
                logger.error(f"Error running benchmark {config.name} for {language}: {e}")

        return results

    def parse_output_metrics(self, language: str, output: str) -> Dict[str, float]:
        """Parse language-specific metrics from output"""
        metrics = {}

        try:
            if language == 'Python':
                for line in output.split('\n'):
                    if 'Current Entropy:' in line:
                        metrics['entropy'] = float(line.split(':')[1].strip())
                    elif 'Average Free Energy:' in line:
                        metrics['free_energy'] = float(line.split(':')[1].strip())
                    elif 'Action Diversity:' in line:
                        metrics['action_diversity'] = float(line.split(':')[1].strip())

            elif language == 'Rust':
                for line in output.split('\n'):
                    if 'Current Entropy:' in line:
                        metrics['entropy'] = float(line.split(':')[1].strip())
                    elif 'Average Free Energy:' in line:
                        metrics['free_energy'] = float(line.split(':')[1].strip())
                    elif 'Action Diversity:' in line:
                        metrics['action_diversity'] = float(line.split(':')[1].strip())

            elif language == 'Java':
                # Add Java-specific parsing
                pass

            # Add parsers for other languages as needed

        except Exception as e:
            logger.warning(f"Failed to parse metrics for {language}: {e}")

        return metrics

    def calculate_statistical_summary(self, values: List[float]) -> StatisticalSummary:
        """Calculate statistical summary for a list of values"""
        if not values:
            return StatisticalSummary(0, 0, 0, 0, 0, (0, 0), [])

        mean_val = statistics.mean(values)
        median_val = statistics.median(values)
        std_dev = statistics.stdev(values) if len(values) > 1 else 0
        min_val = min(values)
        max_val = max(values)

        # Calculate 95% confidence interval
        if len(values) > 1:
            se = std_dev / (len(values) ** 0.5)
            ci_lower = mean_val - 1.96 * se
            ci_upper = mean_val + 1.96 * se
        else:
            ci_lower = ci_upper = mean_val

        # Identify outliers (values more than 2 std devs from mean)
        outliers = [v for v in values if abs(v - mean_val) > 2 * std_dev]

        return StatisticalSummary(
            mean=mean_val,
            median=median_val,
            std_dev=std_dev,
            min_value=min_val,
            max_value=max_val,
            confidence_interval_95=(ci_lower, ci_upper),
            outliers=outliers
        )

    def compare_languages(self, results: Dict[str, List[PerformanceMetrics]], metric_name: str) -> LanguageComparison:
        """Compare languages across a specific metric"""
        language_averages = {}

        for language, metrics in results.items():
            values = [getattr(m, metric_name) for m in metrics if getattr(m, metric_name) > 0]
            if values:
                language_averages[language] = statistics.mean(values)

        if not language_averages:
            return LanguageComparison(metric_name, [], "", "", {}, {})

        # Sort by performance (ascending for time, descending for diversity/accuracy)
        reverse_order = metric_name in ['action_selection_diversity', 'final_belief_entropy']
        rankings = sorted(language_averages.items(), key=lambda x: x[1], reverse=reverse_order)

        best_performer = rankings[0][0] if rankings else ""
        worst_performer = rankings[-1][0] if len(rankings) > 1 else ""

        # Calculate relative performance (normalized to best)
        if rankings and rankings[0][1] != 0:
            best_value = rankings[0][1]
            relative_performance = {}
            for lang, value in language_averages.items():
                if reverse_order:
                    relative_performance[lang] = value / best_value
                else:
                    relative_performance[lang] = best_value / value
        else:
            relative_performance = {lang: 1.0 for lang in language_averages.keys()}

        # Statistical significance (simplified t-test approximation)
        statistical_significance = {}
        if len(rankings) > 1 and best_performer in language_averages:
            best_values = [getattr(m, metric_name) for m in results[best_performer] if getattr(m, metric_name) > 0]
            best_mean = statistics.mean(best_values) if best_values else 0
            best_std = statistics.stdev(best_values) if len(best_values) > 1 else 0

            for language in language_averages.keys():
                if language != best_performer:
                    lang_values = [getattr(m, metric_name) for m in results[language] if getattr(m, metric_name) > 0]
                    if lang_values and best_std > 0:
                        lang_mean = statistics.mean(lang_values)
                        # Simplified significance test
                        effect_size = abs(lang_mean - best_mean) / best_std
                        statistical_significance[language] = effect_size > 0.5  # Cohen's d > 0.5
                    else:
                        statistical_significance[language] = False

        return LanguageComparison(
            metric_name=metric_name,
            rankings=rankings,
            best_performer=best_performer,
            worst_performer=worst_performer,
            relative_performance=relative_performance,
            statistical_significance=statistical_significance
        )

    def create_performance_plots(self, results: Dict[str, List[PerformanceMetrics]], report: BenchmarkReport):
        """Create comprehensive performance visualization plots"""
        try:
            # Set up the plotting style
            plt.style.use('seaborn-v0_8')
            sns.set_palette("husl")

            # 1. Execution Time Comparison
            plt.figure(figsize=(12, 8))
            languages = list(results.keys())
            execution_times = [statistics.mean([m.execution_time for m in results[lang]]) for lang in languages]

            bars = plt.bar(languages, execution_times, color=sns.color_palette("husl", len(languages)))
            plt.title('Execution Time Comparison Across Languages', fontsize=16, fontweight='bold')
            plt.ylabel('Execution Time (seconds)', fontsize=12)
            plt.xlabel('Programming Language', fontsize=12)
            plt.xticks(rotation=45, ha='right')

            # Add value labels on bars
            for bar, time in zip(bars, execution_times):
                plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                        f'{time:.3f}', ha='center', va='bottom', fontsize=10)

            plt.tight_layout()
            plt.savefig(self.plots_dir / 'execution_time_comparison.png', dpi=300, bbox_inches='tight')
            plt.close()

            # 2. Memory Usage Comparison
            plt.figure(figsize=(12, 8))
            peak_memory = [statistics.mean([m.peak_memory_mb for m in results[lang]]) for lang in languages]

            bars = plt.bar(languages, peak_memory, color=sns.color_palette("coolwarm", len(languages)))
            plt.title('Peak Memory Usage Comparison', fontsize=16, fontweight='bold')
            plt.ylabel('Peak Memory Usage (MB)', fontsize=12)
            plt.xlabel('Programming Language', fontsize=12)
            plt.xticks(rotation=45, ha='right')

            for bar, mem in zip(bars, peak_memory):
                plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                        f'{mem:.1f}', ha='center', va='bottom', fontsize=10)

            plt.tight_layout()
            plt.savefig(self.plots_dir / 'memory_usage_comparison.png', dpi=300, bbox_inches='tight')
            plt.close()

            # 3. Multi-metric Radar Chart
            if len(languages) >= 3:
                self.create_radar_chart(results, languages)

            # 4. Performance Distribution Box Plot
            self.create_box_plot(results, languages)

            logger.info(f"Performance plots saved to {self.plots_dir}")

        except Exception as e:
            logger.error(f"Failed to create performance plots: {e}")

    def create_radar_chart(self, results: Dict[str, List[PerformanceMetrics]], languages: List[str]):
        """Create a radar chart comparing multiple metrics"""
        try:
            # Normalize metrics for radar chart
            metrics = ['execution_time', 'peak_memory_mb', 'final_belief_entropy']
            metric_names = ['Speed', 'Memory\nEfficiency', 'Belief\nAccuracy']

            # Calculate normalized values (0-1 scale, higher is better for all)
            normalized_data = {}
            for lang in languages:
                values = []
                for metric in metrics:
                    raw_values = [getattr(m, metric) for m in results[lang] if getattr(m, metric) > 0]
                    if raw_values:
                        mean_val = statistics.mean(raw_values)
                        if metric == 'execution_time':
                            # Invert execution time (lower is better)
                            mean_val = 1 / (1 + mean_val)  # Transform to 0-1 scale
                        elif metric == 'peak_memory_mb':
                            # Invert memory usage (lower is better)
                            mean_val = 1 / (1 + mean_val)
                        # belief_entropy is already in good range
                        values.append(mean_val)
                    else:
                        values.append(0)
                normalized_data[lang] = values

            # Create radar chart
            angles = np.linspace(0, 2 * np.pi, len(metrics), endpoint=False).tolist()
            angles += angles[:1]  # Close the circle

            fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection='polar'))

            for lang in languages:
                values = normalized_data[lang]
                values += values[:1]  # Close the circle
                ax.plot(angles, values, 'o-', linewidth=2, label=lang, markersize=6)
                ax.fill(angles, values, alpha=0.1)

            ax.set_xticks(angles[:-1])
            ax.set_xticklabels(metric_names, fontsize=12)
            ax.set_ylim(0, 1)
            ax.set_title('Multi-Metric Performance Comparison', fontsize=16, fontweight='bold', pad=20)
            ax.grid(True)
            ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))

            plt.tight_layout()
            plt.savefig(self.plots_dir / 'radar_performance_comparison.png', dpi=300, bbox_inches='tight')
            plt.close()

        except Exception as e:
            logger.warning(f"Failed to create radar chart: {e}")

    def create_box_plot(self, results: Dict[str, List[PerformanceMetrics]], languages: List[str]):
        """Create box plot showing performance distribution"""
        try:
            fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))

            # Execution time
            execution_data = [[m.execution_time for m in results[lang]] for lang in languages]
            ax1.boxplot(execution_data, labels=languages)
            ax1.set_title('Execution Time Distribution', fontweight='bold')
            ax1.set_ylabel('Time (seconds)')
            ax1.tick_params(axis='x', rotation=45)

            # Memory usage
            memory_data = [[m.peak_memory_mb for m in results[lang]] for lang in languages]
            ax2.boxplot(memory_data, labels=languages)
            ax2.set_title('Memory Usage Distribution', fontweight='bold')
            ax2.set_ylabel('Peak Memory (MB)')
            ax2.tick_params(axis='x', rotation=45)

            # Belief entropy
            entropy_data = [[m.final_belief_entropy for m in results[lang] if m.final_belief_entropy > 0] for lang in languages]
            if any(entropy_data):
                ax3.boxplot(entropy_data, labels=languages)
                ax3.set_title('Belief Entropy Distribution', fontweight='bold')
                ax3.set_ylabel('Entropy')
                ax3.tick_params(axis='x', rotation=45)

            # Free energy convergence
            free_energy_data = [[m.free_energy_convergence for m in results[lang] if m.free_energy_convergence > 0] for lang in languages]
            if any(free_energy_data):
                ax4.boxplot(free_energy_data, labels=languages)
                ax4.set_title('Free Energy Convergence', fontweight='bold')
                ax4.set_ylabel('Free Energy')
                ax4.tick_params(axis='x', rotation=45)

            plt.suptitle('Performance Distribution Analysis', fontsize=16, fontweight='bold', y=0.98)
            plt.tight_layout()
            plt.savefig(self.plots_dir / 'performance_distributions.png', dpi=300, bbox_inches='tight')
            plt.close()

        except Exception as e:
            logger.warning(f"Failed to create box plot: {e}")

    def run_benchmark_suite(self) -> BenchmarkReport:
        """Run the complete benchmark suite"""
        logger.info("Starting advanced benchmark suite...")

        start_time = time.time()
        performance_results = {}
        statistical_summaries = {}

        # Get system information
        system_info = self.get_system_info()
        logger.info(f"System: {system_info['platform']}, CPU: {system_info['cpu_count']} cores, RAM: {system_info['total_memory_gb']}GB")

        # Discover available implementations
        implementations = {}
        if self.languages_dir.exists():
            for item in self.languages_dir.iterdir():
                if item.is_dir():
                    run_script = item / "run.sh"
                    if run_script.exists():
                        implementations[item.name] = item

        logger.info(f"Found {len(implementations)} language implementations")

        # Run benchmarks for each language
        for language, language_path in implementations.items():
            logger.info(f"Benchmarking {language}...")
            language_results = []

            for config in self.benchmark_configs:
                results = self.run_single_benchmark(language, config)
                language_results.extend(results)

            if language_results:
                performance_results[language] = language_results

        # Calculate statistical summaries
        for language, results in performance_results.items():
            language_stats = {}

            # Group by benchmark name
            benchmark_groups = {}
            for result in results:
                if result.benchmark_name not in benchmark_groups:
                    benchmark_groups[result.benchmark_name] = []
                benchmark_groups[result.benchmark_name].append(result)

            # Calculate stats for each metric per benchmark
            for benchmark_name, benchmark_results in benchmark_groups.items():
                for metric_name in ['execution_time', 'peak_memory_mb', 'final_belief_entropy']:
                    values = [getattr(r, metric_name) for r in benchmark_results if getattr(r, metric_name) > 0]
                    if values:
                        language_stats[f"{benchmark_name}_{metric_name}"] = self.calculate_statistical_summary(values)

            statistical_summaries[language] = language_stats

        # Generate language comparisons
        language_comparisons = {}
        for metric_name in ['execution_time', 'peak_memory_mb']:
            comparison = self.compare_languages(performance_results, metric_name)
            language_comparisons[metric_name] = comparison

        # Generate recommendations
        recommendations = self.generate_recommendations(performance_results, statistical_summaries)

        # Create performance plots
        self.create_performance_plots(performance_results, None)

        report = BenchmarkReport(
            timestamp=time.strftime('%Y-%m-%d %H:%M:%S'),
            benchmark_configs=self.benchmark_configs,
            performance_results=performance_results,
            statistical_summaries=statistical_summaries,
            language_comparisons=language_comparisons,
            system_info=system_info,
            recommendations=recommendations
        )

        logger.info("Benchmark suite completed")
        return report

    def generate_recommendations(self, results: Dict[str, List[PerformanceMetrics]], stats: Dict) -> List[str]:
        """Generate optimization recommendations"""
        recommendations = []

        if not results:
            return recommendations

        # Identify slowest language
        execution_times = []
        for language, metrics in results.items():
            avg_time = statistics.mean([m.execution_time for m in metrics if m.execution_time > 0])
            if avg_time > 0:
                execution_times.append((language, avg_time))

        if execution_times:
            execution_times.sort(key=lambda x: x[1])
            slowest = execution_times[-1][0]
            fastest = execution_times[0][0]
            speedup_ratio = execution_times[-1][1] / execution_times[0][1]

            if speedup_ratio > 2:
                recommendations.append(
                    f"Consider optimizing {slowest} implementation "
                    f"(~{speedup_ratio:.1f}x slower than {fastest})"
                )

        # Memory efficiency recommendations
        memory_usage = []
        for language, metrics in results.items():
            avg_memory = statistics.mean([m.peak_memory_mb for m in metrics if m.peak_memory_mb > 0])
            if avg_memory > 0:
                memory_usage.append((language, avg_memory))

        if memory_usage:
            memory_usage.sort(key=lambda x: x[1])
            highest_memory = memory_usage[-1][0]

            recommendations.append(
                f"Review memory usage in {highest_memory} "
                "(consider memory pooling or optimization)"
            )

        # General recommendations
        recommendations.extend([
            "Implement parallel processing for CPU-intensive languages",
            "Consider JIT compilation for dynamic languages",
            "Profile memory allocation patterns",
            "Use SIMD instructions where applicable",
            "Implement caching for repeated computations"
        ])

        return recommendations

    def save_report(self, report: BenchmarkReport, filename: str = None):
        """Save benchmark report to file"""
        if filename is None:
            filename = f"benchmark_report_{int(time.time())}.json"

        report_path = self.results_dir / filename

        # Convert complex objects to serializable format
        serializable_report = {
            'timestamp': report.timestamp,
            'benchmark_configs': [asdict(config) for config in report.benchmark_configs],
            'performance_results': {lang: [asdict(result) for result in results]
                                  for lang, results in report.performance_results.items()},
            'statistical_summaries': report.statistical_summaries,
            'language_comparisons': {metric: asdict(comparison)
                                   for metric, comparison in report.language_comparisons.items()},
            'system_info': report.system_info,
            'recommendations': report.recommendations
        }

        with open(report_path, 'w') as f:
            json.dump(serializable_report, f, indent=2, default=str)

        logger.info(f"Benchmark report saved to {report_path}")

    def print_summary(self, report: BenchmarkReport):
        """Print a comprehensive benchmark summary"""
        print("\n" + "="*80)
        print("🚀 ADVANCED BENCHMARK SUITE RESULTS")
        print("="*80)
        print(f"Timestamp: {report.timestamp}")
        print(f"System: {report.system_info['platform']} ({report.system_info['cpu_count']} cores, {report.system_info['total_memory_gb']}GB RAM)")
        print()

        if report.performance_results:
            print("📊 LANGUAGE PERFORMANCE SUMMARY:")
            print("-" * 60)

            # Overall performance table
            print(f"{'Language':<20s} {'Avg Time (s)':<15s} {'Avg Memory (MB)':<18s} {'Entropy':<10s}")
            print("-" * 60)

            for language, results in report.performance_results.items():
                if results:
                    avg_time = statistics.mean([r.execution_time for r in results if r.execution_time > 0])
                    avg_memory = statistics.mean([r.peak_memory_mb for r in results if r.peak_memory_mb > 0])
                    avg_entropy = statistics.mean([r.final_belief_entropy for r in results if r.final_belief_entropy > 0])

                    print(f"{language:<20s} {avg_time:<15.3f} {avg_memory:<18.1f} {avg_entropy:<10.4f}")

        if report.language_comparisons:
            print("\n🏆 PERFORMANCE RANKINGS:")
            print("-" * 40)

            for metric, comparison in report.language_comparisons.items():
                if comparison.rankings:
                    print(f"\n{metric.replace('_', ' ').title()}:")
                    for i, (lang, value) in enumerate(comparison.rankings[:5]):  # Top 5
                        if metric == 'execution_time':
                            print(f"  {i+1:2d}. {lang:<15s} {value:.3f}s")
                        else:
                            print(f"  {i+1:2d}. {lang:<15s} {value:.1f}MB")

        if report.recommendations:
            print("\n💡 OPTIMIZATION RECOMMENDATIONS:")
            print("-" * 50)
            for i, rec in enumerate(report.recommendations, 1):
                print(f"{i}. {rec}")

        print("\n" + "="*80)
        print("📁 Detailed results and plots saved to benchmark_results/ directory")
        print("="*80)

def main():
    import argparse

    parser = argparse.ArgumentParser(description='Advanced Benchmark Suite for Active Inference')
    parser.add_argument('--project-root', default='.',
                       help='Path to project root directory')
    parser.add_argument('--output', '-o',
                       help='Output filename for benchmark report')
    parser.add_argument('--languages', nargs='*',
                       help='Specific languages to benchmark')
    parser.add_argument('--quick', action='store_true',
                       help='Run quick benchmark (reduced iterations)')

    args = parser.parse_args()

    # Initialize benchmark suite
    suite = AdvancedBenchmarkSuite(args.project_root)

    if args.quick:
        # Reduce iterations for quick testing
        for config in suite.benchmark_configs:
            config.iterations = max(1, config.iterations // 2)

    # Run benchmarks
    report = suite.run_benchmark_suite()

    # Save report
    if args.output:
        suite.save_report(report, args.output)
    else:
        suite.save_report(report)

    # Print summary
    suite.print_summary(report)

if __name__ == '__main__':
    main()

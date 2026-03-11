#!/usr/bin/env python3
"""
Comprehensive Testing Suite for Active Inference Multi-Language Implementation

This suite provides automated testing, validation, and benchmarking for all
language implementations in the Active Inference project.
"""

import os
import sys
import json
import time
import subprocess
import statistics
import argparse
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, asdict
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('test_suite.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class TestResult:
    """Individual test result"""
    language: str
    test_name: str
    status: str  # 'PASS', 'FAIL', 'ERROR', 'SKIP'
    execution_time: float
    output: str
    error_message: str = ""
    exit_code: int = 0

@dataclass
class LanguageMetrics:
    """Performance metrics for a language implementation"""
    language: str
    compile_time: float = 0.0
    execution_time: float = 0.0
    peak_memory_mb: float = 0.0
    final_belief_entropy: float = 0.0
    free_energy_trend: List[float] = None
    action_diversity: float = 0.0

@dataclass
class TestSuiteReport:
    """Complete test suite report"""
    timestamp: str
    total_tests: int
    passed_tests: int
    failed_tests: int
    skipped_tests: int
    error_tests: int
    total_execution_time: float
    language_metrics: Dict[str, LanguageMetrics]
    test_results: List[TestResult]
    recommendations: List[str]

class ActiveInferenceTestSuite:
    """Comprehensive test suite for Active Inference implementations"""

    def __init__(self, project_root: str = None):
        if project_root:
            self.project_root = Path(project_root)
            self.languages_dir = self.project_root / "0_CONTEXT" / "Computer_Languages"
        else:
            # Auto-detect: test_suite.py lives in 0_CONTEXT/Computer_Languages/
            self.languages_dir = Path(__file__).parent
            self.project_root = self.languages_dir.parent.parent
        self.results_dir = self.languages_dir / "test_results"
        self.results_dir.mkdir(exist_ok=True)

        # Load language definitions from canonical languages.json, with hardcoded fallback
        self.expected_languages = self._load_expected_languages()

    def _load_expected_languages(self) -> Dict[str, Dict[str, Any]]:
        """Load expected languages from languages.json (canonical source)."""
        languages_json = self.languages_dir / "languages.json"
        if languages_json.exists():
            try:
                with open(languages_json) as f:
                    data = json.load(f)
                result = {}
                for lang in data['languages']:
                    result[lang['directory']] = {
                        'extension': lang.get('extension', ''),
                        'runner': lang.get('runner', 'bash run.sh'),
                        'has_compilation': lang.get('category', '') in ('systems', 'compiled'),
                    }
                logger.info(f"Loaded {len(result)} languages from languages.json")
                return result
            except (json.JSONDecodeError, KeyError) as e:
                logger.warning(f"Failed to parse languages.json: {e}, using hardcoded fallback")

        # Hardcoded fallback (kept in sync manually if languages.json is missing)
        return {
            'Python': {'extension': '.py', 'runner': 'python3', 'has_compilation': False},
            'Java': {'extension': '.java', 'runner': 'java', 'has_compilation': True},
            'JavaScript': {'extension': '.js', 'runner': 'node', 'has_compilation': False},
            'TypeScript': {'extension': '.ts', 'runner': 'ts-node', 'has_compilation': False},
            'C': {'extension': '.c', 'runner': './', 'has_compilation': True},
            'Cpp': {'extension': '.cpp', 'runner': './', 'has_compilation': True},
            'Rust': {'extension': '.rs', 'runner': 'cargo run --release', 'has_compilation': True},
            'Haskell': {'extension': '.hs', 'runner': 'runhaskell', 'has_compilation': False},
            'R': {'extension': '.R', 'runner': 'Rscript', 'has_compilation': False},
            'Shell': {'extension': '.sh', 'runner': 'bash', 'has_compilation': False},
            'Ada': {'extension': '.adb', 'runner': './', 'has_compilation': True},
            'Assembly': {'extension': '.asm', 'runner': './', 'has_compilation': True},
            'Brainfuck': {'extension': '.bf', 'runner': 'bf', 'has_compilation': False},
            'Clojure': {'extension': '.clj', 'runner': 'clj', 'has_compilation': False},
            'Crystal': {'extension': '.cr', 'runner': './', 'has_compilation': True},
            'CSharp': {'extension': '.cs', 'runner': 'dotnet run', 'has_compilation': True},
            'Elixir': {'extension': '.ex', 'runner': 'elixir', 'has_compilation': False},
            'Erlang': {'extension': '.erl', 'runner': 'erl', 'has_compilation': False},
            'FSharp': {'extension': '.fs', 'runner': 'dotnet run', 'has_compilation': True},
            'Fortran': {'extension': '.f90', 'runner': './', 'has_compilation': True},
            'Golang': {'extension': '.go', 'runner': 'go run', 'has_compilation': True},
            'Jock': {'extension': '.jock', 'runner': 'urbit', 'has_compilation': False},
            'Julia': {'extension': '.jl', 'runner': 'julia', 'has_compilation': False},
            'Kotlin': {'extension': '.kt', 'runner': 'kotlin', 'has_compilation': True},
            'Lua': {'extension': '.lua', 'runner': 'lua', 'has_compilation': False},
            'MATLAB': {'extension': '.m', 'runner': 'matlab -batch', 'has_compilation': False},
            'Nim': {'extension': '.nim', 'runner': './', 'has_compilation': True},
            'OCaml': {'extension': '.ml', 'runner': 'ocaml', 'has_compilation': False},
            'Odin': {'extension': '.odin', 'runner': './', 'has_compilation': True},
            'Pascal': {'extension': '.pas', 'runner': './', 'has_compilation': True},
            'Perl': {'extension': '.pl', 'runner': 'perl', 'has_compilation': False},
            'PHP': {'extension': '.php', 'runner': 'php', 'has_compilation': False},
            'Prolog': {'extension': '.pl', 'runner': 'swipl', 'has_compilation': False},
            'Racket': {'extension': '.rkt', 'runner': 'racket', 'has_compilation': False},
            'Ruby': {'extension': '.rb', 'runner': 'ruby', 'has_compilation': False},
            'SQL': {'extension': '.sql', 'runner': 'sqlite3', 'has_compilation': False},
            'V': {'extension': '.v', 'runner': './', 'has_compilation': True},
            'Zig': {'extension': '.zig', 'runner': './', 'has_compilation': True},
            'Scala': {'extension': '.scala', 'runner': 'scala', 'has_compilation': True},
            'Swift': {'extension': '.swift', 'runner': 'swift run', 'has_compilation': True},
        }

    def discover_implementations(self) -> Dict[str, Path]:
        """Discover all language implementations in the project"""
        implementations = {}

        if not self.languages_dir.exists():
            logger.error(f"Languages directory not found: {self.languages_dir}")
            return implementations

        for item in self.languages_dir.iterdir():
            if item.is_dir() and item.name in self.expected_languages:
                implementations[item.name] = item

        logger.info(f"Discovered {len(implementations)} language implementations")
        return implementations

    def validate_implementation_structure(self, language: str, path: Path) -> List[str]:
        """Validate that an implementation has the required structure"""
        issues = []

        # Check for README.md
        readme_path = path / "README.md"
        if not readme_path.exists():
            issues.append(f"Missing README.md in {language}")

        # Check for run.sh
        run_script = path / "run.sh"
        if not run_script.exists():
            issues.append(f"Missing run.sh in {language}")
        elif not os.access(run_script, os.X_OK):
            issues.append(f"run.sh is not executable in {language}")

        # Check for main implementation file
        config = self.expected_languages.get(language, {})
        if 'extension' in config:
            main_file = path / f"active_inference{config['extension']}"
            if not main_file.exists():
                # Try alternative naming patterns
                alt_files = list(path.glob(f"*{config['extension']}"))
                if not alt_files:
                    issues.append(f"No implementation file found in {language}")

        return issues

    def run_single_test(self, language: str, test_config: Dict[str, Any]) -> TestResult:
        """Run a single test for a language implementation"""
        start_time = time.time()
        result = TestResult(
            language=language,
            test_name=test_config.get('name', 'basic_test'),
            status='ERROR',
            execution_time=0.0,
            output="",
            error_message="",
            exit_code=-1
        )

        try:
            language_path = self.languages_dir / language
            run_script = language_path / "run.sh"

            if not run_script.exists():
                result.status = 'SKIP'
                result.error_message = "No run.sh script found"
                return result

            # Run the test with timeout
            timeout = test_config.get('timeout', 30)
            process = subprocess.run(
                [str(run_script.absolute())],
                cwd=str(language_path),
                capture_output=True,
                text=True,
                timeout=timeout
            )

            result.execution_time = time.time() - start_time
            result.exit_code = process.returncode
            result.output = process.stdout

            if process.returncode == 0:
                result.status = 'PASS'
                # Check for success indicators in output
                if "successfully" in process.stdout.lower() or "completed" in process.stdout.lower():
                    result.status = 'PASS'
                else:
                    result.status = 'FAIL'
                    result.error_message = "Test completed but success indicators not found"
            else:
                result.status = 'FAIL'
                result.error_message = process.stderr

        except subprocess.TimeoutExpired:
            result.status = 'ERROR'
            result.error_message = f"Test timed out after {timeout} seconds"
            result.execution_time = time.time() - start_time
        except Exception as e:
            result.status = 'ERROR'
            result.error_message = str(e)
            result.execution_time = time.time() - start_time

        return result

    def measure_performance(self, language: str) -> LanguageMetrics:
        """Measure performance metrics for a language implementation"""
        metrics = LanguageMetrics(language=language)

        try:
            language_path = self.languages_dir / language
            run_script = language_path / "run.sh"

            if not run_script.exists():
                return metrics

            # Run performance test
            start_time = time.time()
            process = subprocess.run(
                [str(run_script.absolute())],
                cwd=str(language_path),
                capture_output=True,
                text=True,
                timeout=60
            )
            metrics.execution_time = time.time() - start_time

            if process.returncode == 0:
                output = process.stdout

                # Extract metrics from output (language-specific parsing)
                if language == 'Python':
                    metrics.final_belief_entropy = self._extract_python_metrics(output)
                elif language == 'Rust':
                    metrics.final_belief_entropy = self._extract_rust_metrics(output)
                # Add parsers for other languages as needed

        except Exception as e:
            logger.error(f"Failed to measure performance for {language}: {e}")

        return metrics

    def _extract_python_metrics(self, output: str) -> float:
        """Extract metrics from Python implementation output"""
        try:
            # Look for entropy value in Python output
            for line in output.split('\n'):
                if 'Current Entropy:' in line:
                    return float(line.split(':')[1].strip())
        except:
            pass
        return 0.0

    def _extract_rust_metrics(self, output: str) -> float:
        """Extract metrics from Rust implementation output"""
        try:
            # Look for entropy value in Rust output
            for line in output.split('\n'):
                if 'Current Entropy:' in line:
                    return float(line.split(':')[1].strip())
        except:
            pass
        return 0.0

    def generate_cross_language_comparison(self, metrics: Dict[str, LanguageMetrics]) -> Dict[str, Any]:
        """Generate cross-language performance comparison"""
        comparison = {
            'execution_time_ranking': [],
            'memory_efficiency_ranking': [],
            'summary_stats': {}
        }

        if not metrics:
            return comparison

        # Sort by execution time
        execution_ranking = sorted(
            [(lang, m.execution_time) for lang, m in metrics.items()],
            key=lambda x: x[1]
        )
        comparison['execution_time_ranking'] = execution_ranking

        # Calculate summary statistics
        execution_times = [m.execution_time for m in metrics.values() if m.execution_time > 0]
        if execution_times:
            comparison['summary_stats'] = {
                'mean_execution_time': statistics.mean(execution_times),
                'median_execution_time': statistics.median(execution_times),
                'std_execution_time': statistics.stdev(execution_times) if len(execution_times) > 1 else 0,
                'fastest_language': execution_ranking[0][0],
                'slowest_language': execution_ranking[-1][0]
            }

        return comparison

    def generate_recommendations(self, results: List[TestResult], metrics: Dict[str, LanguageMetrics]) -> List[str]:
        """Generate recommendations based on test results and metrics"""
        recommendations = []

        # Check for failing tests
        failed_languages = [r.language for r in results if r.status == 'FAIL']
        if failed_languages:
            recommendations.append(f"Fix failing implementations in: {', '.join(set(failed_languages))}")

        # Check for slow implementations
        if metrics:
            execution_times = [(lang, m.execution_time) for lang, m in metrics.items() if m.execution_time > 0]
            if execution_times:
                fastest_time = min(t for _, t in execution_times)
                slow_languages = [lang for lang, t in execution_times if t > fastest_time * 2]
                if slow_languages:
                    recommendations.append(f"Consider optimizing slow implementations: {', '.join(slow_languages)}")

        # Check for missing implementations
        discovered = set(self.discover_implementations().keys())
        expected = set(self.expected_languages.keys())
        missing = expected - discovered
        if missing:
            recommendations.append(f"Implement missing languages: {', '.join(missing)}")

        return recommendations

    def run_full_test_suite(self) -> TestSuiteReport:
        """Run the complete test suite"""
        logger.info("Starting comprehensive test suite...")

        start_time = time.time()
        test_results = []
        language_metrics = {}

        # Discover implementations
        implementations = self.discover_implementations()

        # Basic validation tests
        for language, path in implementations.items():
            logger.info(f"Testing {language} implementation...")

            # Structure validation
            issues = self.validate_implementation_structure(language, path)
            if issues:
                for issue in issues:
                    test_results.append(TestResult(
                        language=language,
                        test_name="structure_validation",
                        status="FAIL",
                        execution_time=0.0,
                        output="",
                        error_message=issue
                    ))
            else:
                test_results.append(TestResult(
                    language=language,
                    test_name="structure_validation",
                    status="PASS",
                    execution_time=0.0,
                    output="Implementation structure is valid"
                ))

            # Functional test
            functional_test = self.run_single_test(language, {'name': 'functional_test', 'timeout': 60})
            test_results.append(functional_test)

            # Performance measurement
            metrics = self.measure_performance(language)
            language_metrics[language] = metrics

        # Cross-language comparison
        comparison = self.generate_cross_language_comparison(language_metrics)

        # Generate recommendations
        recommendations = self.generate_recommendations(test_results, language_metrics)

        # Calculate summary statistics
        total_tests = len(test_results)
        passed_tests = len([r for r in test_results if r.status == 'PASS'])
        failed_tests = len([r for r in test_results if r.status == 'FAIL'])
        skipped_tests = len([r for r in test_results if r.status == 'SKIP'])
        error_tests = len([r for r in test_results if r.status == 'ERROR'])

        report = TestSuiteReport(
            timestamp=time.strftime('%Y-%m-%d %H:%M:%S'),
            total_tests=total_tests,
            passed_tests=passed_tests,
            failed_tests=failed_tests,
            skipped_tests=skipped_tests,
            error_tests=error_tests,
            total_execution_time=time.time() - start_time,
            language_metrics=language_metrics,
            test_results=test_results,
            recommendations=recommendations
        )

        logger.info("Test suite completed")
        return report

    def save_report(self, report: TestSuiteReport, filename: str = None):
        """Save test report to file"""
        if filename is None:
            filename = f"test_report_{int(time.time())}.json"

        report_path = self.results_dir / filename

        # Convert dataclass to dict for JSON serialization
        report_dict = {
            'timestamp': report.timestamp,
            'total_tests': report.total_tests,
            'passed_tests': report.passed_tests,
            'failed_tests': report.failed_tests,
            'skipped_tests': report.skipped_tests,
            'error_tests': report.error_tests,
            'total_execution_time': report.total_execution_time,
            'language_metrics': {lang: asdict(metrics) for lang, metrics in report.language_metrics.items()},
            'test_results': [asdict(result) for result in report.test_results],
            'recommendations': report.recommendations
        }

        with open(report_path, 'w') as f:
            json.dump(report_dict, f, indent=2)

        logger.info(f"Report saved to {report_path}")

    def print_summary(self, report: TestSuiteReport):
        """Print a human-readable summary of the test results"""
        print("\n" + "="*60)
        print("🧪 ACTIVE INFERENCE TEST SUITE RESULTS")
        print("="*60)
        print(f"Timestamp: {report.timestamp}")
        print(f"Total Tests: {report.total_tests}")
        print(f"✅ Passed: {report.passed_tests}")
        print(f"❌ Failed: {report.failed_tests}")
        print(f"⏭️  Skipped: {report.skipped_tests}")
        print(f"🔥 Errors: {report.error_tests}")
        print(f"⏱️  Total Time: {report.total_execution_time:.2f}s")
        print()

        if report.language_metrics:
            print("📊 LANGUAGE PERFORMANCE:")
            print("-" * 40)
            for lang, metrics in report.language_metrics.items():
                if metrics.execution_time > 0:
                    print(f"  {lang:15s} {metrics.execution_time:.2f}s")

        if report.recommendations:
            print("\n💡 RECOMMENDATIONS:")
            print("-" * 40)
            for rec in report.recommendations:
                print(f"• {rec}")

        print("\n" + "="*60)

def main():
    parser = argparse.ArgumentParser(description='Active Inference Test Suite')
    # Default project root is two levels up from this file's location
    # (this script lives at <repo>/0_CONTEXT/Computer_Languages/test_suite.py)
    _default_project_root = str(Path(__file__).resolve().parent.parent.parent)
    parser.add_argument('--project-root', default=_default_project_root,
                       help='Path to project root directory')
    parser.add_argument('--output', '-o',
                       help='Output filename for test report')
    parser.add_argument('--quiet', '-q', action='store_true',
                       help='Suppress detailed output')

    args = parser.parse_args()

    # Initialize test suite
    test_suite = ActiveInferenceTestSuite(args.project_root)

    # Run tests
    report = test_suite.run_full_test_suite()

    # Save report
    if args.output:
        test_suite.save_report(report, args.output)
    else:
        test_suite.save_report(report)

    # Print summary
    if not args.quiet:
        test_suite.print_summary(report)

    # Exit with appropriate code
    if report.failed_tests > 0 or report.error_tests > 0:
        sys.exit(1)
    else:
        sys.exit(0)

if __name__ == '__main__':
    main()

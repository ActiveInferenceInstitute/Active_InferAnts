#!/usr/bin/env python3
"""
Master Controller for Active Inference Multi-Language System

This is the central orchestration script that provides comprehensive control
over all language implementations, including benchmarking, reporting, and
visualization capabilities.
"""

import os
import sys
import argparse
import subprocess
import logging
from pathlib import Path
from datetime import datetime
import json

logger = logging.getLogger(__name__)

class ActiveInferenceController:
    """Master controller for all Active Inference implementations."""

    def __init__(self):
        self.root_dir = Path(__file__).parent
        self.output_dir = self.root_dir / "output"
        self.output_dir.mkdir(exist_ok=True)

        # Load language registry from canonical source
        self.languages_json = self.root_dir / "languages.json"
        self._language_dirs = self._load_language_dirs()

        # Available commands
        self.commands = {
            "status": self.show_status,
            "run": self.run_implementations,
            "benchmark": self.run_benchmarks,
            "report": self.generate_report,
            "visualize": self.create_visualizations,
            "deps": self.manage_dependencies,
            "test": self.test_implementations,
            "clean": self.clean_outputs,
            "setup": self.setup_environment
        }

    def _load_language_dirs(self) -> dict:
        """Load language name → directory mapping from languages.json."""
        if self.languages_json.exists():
            with open(self.languages_json) as f:
                data = json.load(f)
            return {lang['name'].lower(): lang['directory'] for lang in data['languages']}
        else:
            logger.warning("languages.json not found, falling back to directory discovery")
            return {}

    def show_status(self, args):
        """Show comprehensive status dashboard."""
        print("🧠 Active Inference Multi-Language Status")
        print("=" * 50)

        dashboard_script = self.root_dir / "status_dashboard.sh"
        if dashboard_script.exists():
            subprocess.run(["bash", str(dashboard_script)], cwd=str(self.root_dir))
        else:
            print("❌ Status dashboard not found")

    def run_implementations(self, args):
        """Run language implementations."""
        if args.language:
            # Run specific language
            self._run_language(args.language)
        else:
            # Run all implementations
            self._run_all_languages()

    def run_benchmarks(self, args):
        """Run comprehensive benchmarks."""
        print("🧪 Running comprehensive benchmarks...")

        # Run Python benchmarking system
        analyzer_script = self.root_dir / "reporting_system.py"
        if analyzer_script.exists():
            cmd = [sys.executable, str(analyzer_script)]
            subprocess.run(cmd)
        else:
            print("❌ Benchmarking system not found")

    def generate_report(self, args):
        """Generate comprehensive reports."""
        print("📊 Generating comprehensive reports...")

        # Run reporting system
        report_script = self.root_dir / "reporting_system.py"
        if report_script.exists():
            cmd = [sys.executable, str(report_script)]
            subprocess.run(cmd)

        # Generate dependency report
        deps_script = self.root_dir / "config_manager.py"
        if deps_script.exists():
            cmd = [sys.executable, str(deps_script), "--all"]
            result = subprocess.run(cmd, capture_output=True, text=True)
            with open(self.output_dir / "dependency_report.txt", "w") as f:
                f.write(result.stdout)

        print("📄 Reports generated in 'output/' directory")

    def create_visualizations(self, args):
        """Create comprehensive visualizations."""
        print("📈 Creating visualizations...")

        # Run reporting system which includes visualizations
        report_script = self.root_dir / "reporting_system.py"
        if report_script.exists():
            cmd = [sys.executable, str(report_script)]
            subprocess.run(cmd)
        else:
            print("❌ Visualization system not found")

    def manage_dependencies(self, args):
        """Manage dependencies for all languages."""
        deps_script = self.root_dir / "config_manager.py"
        if deps_script.exists():
            if args.language:
                cmd = [sys.executable, str(deps_script), "--install", args.language]
            else:
                cmd = [sys.executable, str(deps_script), "--all"]
            subprocess.run(cmd)
        else:
            print("❌ Dependency manager not found")

    def test_implementations(self, args):
        """Test language implementations."""
        print("🧪 Testing implementations...")

        # Run the run_all.sh script
        run_all_script = self.root_dir / "run_all.sh"
        if run_all_script.exists():
            if args.language:
                cmd = [str(run_all_script), args.language]
            else:
                cmd = [str(run_all_script), "--sequential"]
            subprocess.run(cmd)
        else:
            print("❌ Test runner not found")

    def clean_outputs(self, args):
        """Clean output files and directories."""
        print("🧹 Cleaning output files...")

        # Clean common output files
        patterns = [
            "**/*.png", "**/*.jpg", "**/*.pdf", "**/*.svg",
            "**/output/**", "**/visualizations/**",
            "**/*.log", "**/*.tmp", "**/*.cache",
            "**/node_modules/**", "**/target/**", "**/build/**",
            "**/*.o", "**/*.exe", "**/*.class"
        ]

        cleaned = 0
        for pattern in patterns:
            for file in self.root_dir.glob(pattern):
                if file.is_file():
                    file.unlink()
                    cleaned += 1

        # Clean empty directories
        for dir_path in self.root_dir.rglob("*"):
            if dir_path.is_dir() and not any(dir_path.iterdir()):
                dir_path.rmdir()
                cleaned += 1

        print(f"✅ Cleaned {cleaned} files and directories")

    def setup_environment(self, args):
        """Setup the environment for all implementations."""
        print("🔧 Setting up environment...")

        # Make all run.sh scripts executable
        for script in self.root_dir.rglob("run.sh"):
            os.chmod(script, 0o755)

        # Make main scripts executable
        main_scripts = [
            "run_all.sh",
            "setup_dependencies.sh",
            "status_dashboard.sh",
            "reporting_system.py",
            "config_manager.py",
            "master_controller.py"
        ]

        for script_name in main_scripts:
            script_path = self.root_dir / script_name
            if script_path.exists():
                os.chmod(script_path, 0o755)

        # Create necessary directories
        dirs = ["output", "visualizations", "reports"]
        for dir_name in dirs:
            (self.root_dir / dir_name).mkdir(exist_ok=True)

        # Run dependency installer check
        setup_script = self.root_dir / "setup_dependencies.sh"
        if setup_script.exists():
            print("\n📦 Checking language dependencies...")
            subprocess.run(["bash", str(setup_script), "--check"], cwd=str(self.root_dir))

        print("\n✅ Environment setup complete")
        print("💡 Run './setup_dependencies.sh' to install missing dependencies")

    def _run_language(self, language: str):
        """Run a specific language implementation."""
        # Look up directory name from languages.json
        lang_lower = language.lower()
        dir_name = self._language_dirs.get(lang_lower, language)
        lang_dir = self.root_dir / dir_name
        run_script = lang_dir / "run.sh"

        if run_script.exists():
            print(f"🚀 Running {language} implementation...")
            subprocess.run(["bash", str(run_script)], cwd=str(lang_dir))
        else:
            print(f"❌ {language} implementation not found at {lang_dir}")

    def _run_all_languages(self):
        """Run all language implementations."""
        run_all_script = self.root_dir / "run_all.sh"
        if run_all_script.exists():
            print("🚀 Running all implementations...")
            subprocess.run([str(run_all_script), "--sequential"])
        else:
            print("❌ run_all.sh not found")

def create_argument_parser():
    """Create the argument parser."""
    parser = argparse.ArgumentParser(
        description="🧠 Active Inference Multi-Language Controller",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python master_controller.py status              # Show status dashboard
  python master_controller.py run                 # Run all implementations
  python master_controller.py run python          # Run Python implementation
  python master_controller.py benchmark           # Run benchmarks
  python master_controller.py report              # Generate reports
  python master_controller.py deps --all          # Check all dependencies
  python master_controller.py deps python         # Check Python dependencies
  python master_controller.py setup               # Setup environment
  python master_controller.py clean               # Clean output files
        """
    )

    parser.add_argument(
        "command",
        choices=["status", "run", "benchmark", "report", "visualize", "deps", "test", "clean", "setup"],
        help="Command to execute"
    )

    parser.add_argument(
        "language",
        nargs="?",
        help="Specific language for commands that support it"
    )

    parser.add_argument(
        "--output-dir",
        default="./output",
        help="Output directory for results"
    )

    return parser

def main():
    """Main function."""
    parser = create_argument_parser()
    args = parser.parse_args()

    # Initialize controller
    controller = ActiveInferenceController()

    # Execute command
    if args.command in controller.commands:
        controller.commands[args.command](args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()

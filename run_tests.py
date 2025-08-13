#!/usr/bin/env python3
"""
Test Runner Script for Snake Game

This script provides an easy way to run different types of tests
and generate various reports.
"""

import sys
import os
import subprocess
import argparse
from pathlib import Path


def run_command(cmd, description):
    """Run a command and handle errors."""
    print(f"\n🔄 {description}...")
    print(f"Running: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(f"✅ {description} completed successfully")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed with exit code {e.returncode}")
        if e.stdout:
            print("STDOUT:", e.stdout)
        if e.stderr:
            print("STDERR:", e.stderr)
        return False


def install_dependencies():
    """Install test dependencies."""
    print("📦 Installing test dependencies...")
    return run_command([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                      "Installing dependencies")


def run_unit_tests():
    """Run unit tests."""
    return run_command([sys.executable, "-m", "pytest", "tests/", "-v", "--tb=short", "-m", "unit"], 
                      "Running unit tests")


def run_integration_tests():
    """Run integration tests."""
    return run_command([sys.executable, "-m", "pytest", "tests/", "-v", "--tb=short", "-m", "integration"], 
                      "Running integration tests")


def run_ui_tests():
    """Run UI tests."""
    return run_command([sys.executable, "-m", "pytest", "tests/", "-v", "--tb=short", "-m", "ui"], 
                      "Running UI tests")


def run_all_tests():
    """Run all tests."""
    return run_command([sys.executable, "-m", "pytest", "tests/", "-v", "--tb=short"], 
                      "Running all tests")


def run_tests_with_coverage():
    """Run tests with coverage reporting."""
    return run_command([sys.executable, "-m", "pytest", "tests/", "--cov=src", "--cov-report=term-missing", 
                       "--cov-report=html:htmlcov", "--cov-report=xml"], 
                      "Running tests with coverage")


def run_specific_test_file(test_file):
    """Run a specific test file."""
    if not os.path.exists(test_file):
        print(f"❌ Test file {test_file} not found")
        return False
    
    return run_command([sys.executable, "-m", "pytest", test_file, "-v", "--tb=short"], 
                      f"Running {test_file}")


def run_code_quality_checks():
    """Run code quality checks."""
    print("🔍 Running code quality checks...")
    
    checks = [
        (["black", "--check", "--diff", "src/", "tests/"], "Code formatting check"),
        (["flake8", "src/", "tests/", "--max-line-length=88", "--extend-ignore=E203,W503"], "Linting"),
        (["mypy", "src/", "--ignore-missing-imports", "--no-strict-optional"], "Type checking")
    ]
    
    all_passed = True
    for cmd, description in checks:
        if not run_command(cmd, description):
            all_passed = False
    
    return all_passed


def generate_test_report():
    """Generate a comprehensive test report."""
    print("📊 Generating test report...")
    
    # Run tests with coverage
    if not run_tests_with_coverage():
        print("❌ Failed to generate coverage report")
        return False
    
    # Generate HTML report summary
    coverage_dir = Path("htmlcov")
    if coverage_dir.exists():
        index_file = coverage_dir / "index.html"
        if index_file.exists():
            print(f"📈 Coverage report generated: {index_file.absolute()}")
            print("Open the HTML file in your browser to view detailed coverage")
    
    return True


def main():
    """Main function to parse arguments and run tests."""
    parser = argparse.ArgumentParser(description="Snake Game Test Runner")
    parser.add_argument("--unit", action="store_true", help="Run unit tests only")
    parser.add_argument("--integration", action="store_true", help="Run integration tests only")
    parser.add_argument("--ui", action="store_true", help="Run UI tests only")
    parser.add_argument("--coverage", action="store_true", help="Run tests with coverage")
    parser.add_argument("--quality", action="store_true", help="Run code quality checks")
    parser.add_argument("--install", action="store_true", help="Install dependencies")
    parser.add_argument("--file", type=str, help="Run a specific test file")
    parser.add_argument("--all", action="store_true", help="Run all tests and quality checks")
    
    args = parser.parse_args()
    
    print("🐍 Snake Game Test Runner")
    print("=" * 40)
    
    # Install dependencies if requested
    if args.install:
        if not install_dependencies():
            sys.exit(1)
    
    # Run specific test types
    if args.unit:
        if not run_unit_tests():
            sys.exit(1)
    elif args.integration:
        if not run_integration_tests():
            sys.exit(1)
    elif args.ui:
        if not run_ui_tests():
            sys.exit(1)
    elif args.coverage:
        if not run_tests_with_coverage():
            sys.exit(1)
    elif args.quality:
        if not run_code_quality_checks():
            sys.exit(1)
    elif args.file:
        if not run_specific_test_file(args.file):
            sys.exit(1)
    elif args.all:
        # Run everything
        if not install_dependencies():
            sys.exit(1)
        if not run_code_quality_checks():
            sys.exit(1)
        if not run_tests_with_coverage():
            sys.exit(1)
    else:
        # Default: run all tests
        if not run_all_tests():
            sys.exit(1)
    
    print("\n🎉 All requested operations completed successfully!")


if __name__ == "__main__":
    main()

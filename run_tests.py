#!/usr/bin/env python3
"""
Test runner script for the Flask personal website.
This script provides an easy way to run all tests with different configurations.
"""
import subprocess
import sys
import os


def run_tests():
    """Run all tests with coverage."""
    print("Running Flask Personal Website Tests")
    print("=" * 50)
    
    # Change to the project directory
    project_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_dir)
    
    try:
        # Run tests with coverage
        result = subprocess.run([
            sys.executable, '-m', 'pytest', 
            'tests/', 
            '--cov=app', 
            '--cov-report=html', 
            '--cov-report=term-missing',
            '-v'
        ], check=True, capture_output=False)
        
        print("\n" + "=" * 50)
        print("✅ All tests passed successfully!")
        print("📊 Coverage report generated in htmlcov/ directory")
        print("🔍 Open htmlcov/index.html in your browser to view detailed coverage")
        
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Tests failed with exit code {e.returncode}")
        sys.exit(1)
    except FileNotFoundError:
        print("❌ pytest not found. Please install it with: pip install pytest pytest-flask pytest-cov")
        sys.exit(1)


def run_quick_tests():
    """Run tests without coverage for faster execution."""
    print("Running Quick Tests (no coverage)")
    print("=" * 50)
    
    project_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_dir)
    
    try:
        result = subprocess.run([
            sys.executable, '-m', 'pytest', 
            'tests/', 
            '-v'
        ], check=True)
        
        print("\n" + "=" * 50)
        print("✅ All tests passed successfully!")
        
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Tests failed with exit code {e.returncode}")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--quick":
        run_quick_tests()
    else:
        run_tests()

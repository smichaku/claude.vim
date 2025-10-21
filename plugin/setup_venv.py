#!/usr/bin/env python3
"""
Virtual environment setup script for claude.vim plugin.
Creates and manages a virtual environment with required dependencies.
"""

import os
import subprocess
import sys
import venv
from pathlib import Path

def get_plugin_dir():
    """Get the plugin directory containing this script."""
    return Path(__file__).parent

def get_venv_dir():
    """Get the path to the virtual environment directory."""
    return get_plugin_dir() / "venv"

def get_venv_python():
    """Get the path to the Python executable in the virtual environment."""
    venv_dir = get_venv_dir()
    if os.name == 'nt':  # Windows
        return venv_dir / "Scripts" / "python.exe"
    else:  # Unix-like systems
        return venv_dir / "bin" / "python"

def create_venv():
    """Create the virtual environment."""
    venv_dir = get_venv_dir()
    print(f"Creating virtual environment at {venv_dir}")
    venv.create(venv_dir, with_pip=True)

def install_requirements():
    """Install requirements from requirements.txt."""
    plugin_dir = get_plugin_dir()
    requirements_file = plugin_dir.parent / "requirements.txt"
    venv_python = get_venv_python()

    if not requirements_file.exists():
        print(f"Warning: {requirements_file} not found")
        return

    print(f"Installing requirements from {requirements_file}")
    subprocess.run([
        str(venv_python), "-m", "pip", "install", "-r", str(requirements_file)
    ], check=True)

def setup_venv():
    """Set up the virtual environment if it doesn't exist or is outdated."""
    venv_dir = get_venv_dir()
    venv_python = get_venv_python()

    # Check if virtual environment exists and has the right Python version
    needs_setup = False

    if not venv_dir.exists():
        needs_setup = True
        print("Virtual environment does not exist")
    elif not venv_python.exists():
        needs_setup = True
        print("Virtual environment Python executable not found")
    else:
        # Check if boto3 is installed
        try:
            result = subprocess.run([
                str(venv_python), "-c", "import boto3; print(boto3.__version__)"
            ], capture_output=True, text=True, check=True)
            print(f"Virtual environment ready with boto3 {result.stdout.strip()}")
        except subprocess.CalledProcessError:
            needs_setup = True
            print("boto3 not found in virtual environment")

    if needs_setup:
        if venv_dir.exists():
            print("Removing existing virtual environment")
            import shutil
            shutil.rmtree(venv_dir)

        create_venv()
        install_requirements()
        print("Virtual environment setup complete")

    return str(venv_python)

if __name__ == "__main__":
    try:
        python_path = setup_venv()
        print(f"Python executable: {python_path}")
    except Exception as e:
        print(f"Error setting up virtual environment: {e}", file=sys.stderr)
        sys.exit(1)
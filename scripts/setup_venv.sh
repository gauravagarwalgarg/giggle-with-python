#!/bin/bash
# Create Python virtual environment, install requirements, and show activation command.
# Usage: bash scripts/setup_venv.sh [requirements_file]

set -e

VENV_DIR=".venv"
REQUIREMENTS="${1:-requirements.txt}"
PYTHON="${PYTHON:-python3}"

echo "=== Python Virtual Environment Setup ==="
echo ""

# Check Python version
PYTHON_VERSION=$($PYTHON --version 2>&1)
echo "Using: $PYTHON_VERSION"

# Create virtual environment
if [ -d "$VENV_DIR" ]; then
    echo "Virtual environment already exists at $VENV_DIR"
    read -p "Recreate? [y/N] " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -rf "$VENV_DIR"
        $PYTHON -m venv "$VENV_DIR"
        echo "✓ Recreated virtual environment"
    fi
else
    $PYTHON -m venv "$VENV_DIR"
    echo "✓ Created virtual environment at $VENV_DIR"
fi

# Activate
source "$VENV_DIR/bin/activate"
echo "✓ Activated virtual environment"

# Upgrade pip
pip install --upgrade pip --quiet
echo "✓ Upgraded pip to $(pip --version | awk '{print $2}')"

# Install requirements if file exists
if [ -f "$REQUIREMENTS" ]; then
    echo "Installing from $REQUIREMENTS..."
    pip install -r "$REQUIREMENTS" --quiet
    echo "✓ Installed requirements from $REQUIREMENTS"
else
    echo "No $REQUIREMENTS found, skipping dependency install"
fi

# Install dev tools
echo "Installing dev tools..."
pip install ruff mypy black pytest --quiet
echo "✓ Installed: ruff, mypy, black, pytest"

echo ""
echo "=== Setup Complete ==="
echo ""
echo "To activate this environment:"
echo "  source $VENV_DIR/bin/activate"
echo ""
echo "To deactivate:"
echo "  deactivate"
echo ""
echo "Python: $(which python)"
echo "Pip:    $(which pip)"

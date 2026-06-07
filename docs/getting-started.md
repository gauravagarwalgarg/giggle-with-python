# Getting Started

How to use this repository, set up your environment, and run examples.

## Prerequisites

- Python 3.10+ (for match/case and modern type syntax)
- pip (comes with Python)
- git

Check your version:
```bash
python3 --version  # Should be 3.10+
pip --version
```

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/GauravAgarwalGarg/GiggleWithPython.git
cd GiggleWithPython
```

### 2. Create a virtual environment

```bash
# Quick setup (automated)
bash scripts/setup_venv.sh

# Or manually:
python3 -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows
pip install --upgrade pip
```

### 3. Install dependencies

Each section has its own `requirements.txt`:

```bash
# Fundamentals no deps needed (stdlib only)

# Data analytics
pip install -r data-analytics/requirements.txt

# Frameworks (pick one)
pip install -r frameworks/flask/requirements.txt
pip install -r frameworks/fastapi/requirements.txt

# Automation
pip install -r automation/requirements.txt

# Testing
pip install -r testing/requirements.txt
```

## Running Examples

Every Python file has a `if __name__ == "__main__":` block with runnable demos:

```bash
# Run any file directly
python fundamentals/data_types.py
python fundamentals/functions.py
python snippets/regex_patterns.py
python data-analytics/numpy_basics.py

# Run Flask app
python frameworks/flask/app.py
# Visit http://localhost:5000

# Run FastAPI app
python frameworks/fastapi/main.py
# Visit http://localhost:8000/docs

# Run tests
pytest testing/ -v
```

## Project Structure

```
GiggleWithPython/
├── fundamentals/      # Python language fundamentals (stdlib only)
├── frameworks/        # Web frameworks (Django, Flask, FastAPI)
├── data-analytics/    # Data science (Pandas, NumPy, Matplotlib, SciPy)
├── snippets/          # Reusable utility code
├── automation/        # DevOps helpers (Docker, AWS, SSH)
├── testing/           # Pytest patterns and examples
├── scripts/           # Shell scripts and one-liners
└── docs/              # Documentation
```

## Development Tools

### Linting and Formatting

```bash
# Run all checks
bash scripts/lint.sh

# Or individually:
ruff check .               # Lint
ruff format .              # Format (replaces black)
mypy fundamentals/ --ignore-missing-imports  # Type check
```

### Recommended VS Code Extensions

- Python (Microsoft)
- Pylance (type checking)
- Ruff (linting + formatting)
- Python Test Explorer

### Recommended `.vscode/settings.json`

```json
{
    "python.defaultInterpreterPath": ".venv/bin/python",
    "python.testing.pytestEnabled": true,
    "editor.formatOnSave": true,
    "[python]": {
        "editor.defaultFormatter": "charliermarsh.ruff"
    }
}
```

## Tips

1. **Start with fundamentals/** if you're learning Python, work through these files in order
2. **Copy snippets** the `snippets/` directory is designed to be copy-pasted into your projects
3. **Run everything** every file is designed to produce output when run directly
4. **Read the docstrings** each function explains WHY, not just WHAT
5. **Use the type hints** run `mypy` to catch bugs before runtime

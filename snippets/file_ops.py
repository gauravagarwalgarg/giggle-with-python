"""
File Operations read/write JSON, YAML, CSV, and .env files.

Copy-paste ready patterns for common file I/O tasks.
"""
import csv
import json
import os
from pathlib import Path
from typing import Any


# =============================================================================
# JSON the universal data exchange format
# =============================================================================

def read_json(filepath: str) -> dict | list:
    """Read JSON file with error handling."""
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {filepath}")
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def write_json(filepath: str, data: Any, indent: int = 2) -> None:
    """Write data as pretty-printed JSON."""
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=indent, ensure_ascii=False, default=str)


def append_to_json_array(filepath: str, item: Any) -> None:
    """Append an item to a JSON array file."""
    try:
        data = read_json(filepath)
        if not isinstance(data, list):
            raise ValueError("File doesn't contain a JSON array")
    except FileNotFoundError:
        data = []

    data.append(item)
    write_json(filepath, data)


# =============================================================================
# YAML configuration files (requires pip install pyyaml)
# =============================================================================

def read_yaml(filepath: str) -> dict:
    """Read YAML file."""
    try:
        import yaml
    except ImportError:
        raise ImportError("Install PyYAML: pip install pyyaml")

    with open(filepath, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def write_yaml(filepath: str, data: dict) -> None:
    """Write data as YAML."""
    try:
        import yaml
    except ImportError:
        raise ImportError("Install PyYAML: pip install pyyaml")

    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)


# =============================================================================
# CSV tabular data
# =============================================================================

def read_csv(filepath: str) -> list[dict]:
    """Read CSV file as list of dicts (one per row)."""
    with open(filepath, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        return list(reader)


def write_csv(filepath: str, rows: list[dict], fieldnames: list[str] = None) -> None:
    """Write list of dicts as CSV."""
    if not rows:
        return

    if fieldnames is None:
        fieldnames = list(rows[0].keys())

    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def append_csv_row(filepath: str, row: dict) -> None:
    """Append a single row to an existing CSV file."""
    file_exists = Path(filepath).exists()
    with open(filepath, "a", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=row.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)


# =============================================================================
# .ENV FILES environment variable configuration
# =============================================================================

def read_env(filepath: str = ".env") -> dict[str, str]:
    """Parse .env file into a dict.

    Handles:
    - Comments (lines starting with #)
    - Quoted values
    - Empty lines
    - KEY=VALUE format
    """
    env_vars = {}
    path = Path(filepath)

    if not path.exists():
        return env_vars

    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            # Skip empty lines and comments
            if not line or line.startswith("#"):
                continue

            # Split on first = sign
            if "=" not in line:
                continue

            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip()

            # Remove surrounding quotes
            if (value.startswith('"') and value.endswith('"')) or \
               (value.startswith("'") and value.endswith("'")):
                value = value[1:-1]

            env_vars[key] = value

    return env_vars


def write_env(filepath: str, env_vars: dict[str, str]) -> None:
    """Write dict as .env file."""
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for key, value in env_vars.items():
            # Quote values that contain spaces or special chars
            if " " in value or "#" in value or "=" in value:
                value = f'"{value}"'
            f.write(f"{key}={value}\n")


def load_env(filepath: str = ".env") -> None:
    """Load .env file into os.environ (like python-dotenv)."""
    env_vars = read_env(filepath)
    for key, value in env_vars.items():
        if key not in os.environ:  # Don't override existing env vars
            os.environ[key] = value


# =============================================================================
# GENERAL FILE UTILITIES
# =============================================================================

def read_text(filepath: str) -> str:
    """Read entire file as string."""
    return Path(filepath).read_text(encoding="utf-8")


def write_text(filepath: str, content: str) -> None:
    """Write string to file (creates dirs if needed)."""
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def read_lines(filepath: str, strip: bool = True) -> list[str]:
    """Read file as list of lines."""
    with open(filepath, "r", encoding="utf-8") as f:
        if strip:
            return [line.strip() for line in f if line.strip()]
        return f.readlines()


def file_exists(filepath: str) -> bool:
    """Check if file exists."""
    return Path(filepath).exists()


def ensure_dir(dirpath: str) -> Path:
    """Create directory (and parents) if it doesn't exist."""
    path = Path(dirpath)
    path.mkdir(parents=True, exist_ok=True)
    return path


if __name__ == "__main__":
    print("=" * 60)
    print("File Operations Demo")
    print("=" * 60)

    # JSON demo
    print("\n--- JSON ---")
    data = {"name": "Gaurav", "skills": ["Python", "Django", "AWS"]}
    write_json("/tmp/demo.json", data)
    loaded = read_json("/tmp/demo.json")
    print(f"  Written and read: {loaded}")

    # CSV demo
    print("\n--- CSV ---")
    rows = [
        {"name": "Alice", "age": "30", "city": "Mumbai"},
        {"name": "Bob", "age": "25", "city": "Delhi"},
    ]
    write_csv("/tmp/demo.csv", rows)
    loaded_csv = read_csv("/tmp/demo.csv")
    print(f"  Written and read: {loaded_csv}")

    # .env demo
    print("\n--- .env ---")
    env = {"DB_HOST": "localhost", "DB_PORT": "5432", "SECRET": "my secret value"}
    write_env("/tmp/.env.demo", env)
    loaded_env = read_env("/tmp/.env.demo")
    print(f"  Written and read: {loaded_env}")

    print("\nDone!")

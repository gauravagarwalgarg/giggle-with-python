"""
CSV and JSON Operations practical data file handling.

Copy-paste ready recipes for reading, writing, and transforming
CSV and JSON files. Common patterns for ETL scripts and data pipelines.

Adapted from code_snippets/Python-CSV and code_snippets/Python-JSON.
"""
import csv
import json
from io import StringIO
from pathlib import Path
from typing import Any


# =============================================================================
# CSV READING
# =============================================================================

def read_csv_as_dicts(filepath: str) -> list[dict]:
    """Read CSV into a list of dictionaries (one per row).

    Uses DictReader which maps each row to a dict using header names.
    Adapted from code_snippets/Python-CSV/parse_csv.py.
    """
    with open(filepath, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)


def read_csv_as_lists(filepath: str, skip_header: bool = False) -> list[list[str]]:
    """Read CSV into a list of lists (raw rows)."""
    with open(filepath, "r", newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        if skip_header:
            next(reader)
        return list(reader)


def read_csv_with_types(filepath: str, type_map: dict[str, type]) -> list[dict]:
    """Read CSV and convert columns to specified types.

    Example: type_map = {"age": int, "salary": float, "active": bool}
    """
    rows = read_csv_as_dicts(filepath)
    for row in rows:
        for col, col_type in type_map.items():
            if col in row and row[col]:
                if col_type == bool:
                    row[col] = row[col].lower() in ("true", "1", "yes")
                else:
                    row[col] = col_type(row[col])
    return rows


# =============================================================================
# CSV WRITING
# =============================================================================

def write_csv(filepath: str, data: list[dict], fieldnames: list[str] | None = None):
    """Write a list of dicts to CSV.

    Adapted from code_snippets/Python-CSV/parse_csv.py.
    """
    if not data:
        return

    if fieldnames is None:
        fieldnames = list(data[0].keys())

    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)


def write_csv_tab_separated(filepath: str, data: list[dict], fieldnames: list[str]):
    """Write tab-separated CSV (TSV).

    Adapted from code_snippets/Python-CSV delimiter pattern.
    """
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()
        writer.writerows(data)


def append_csv_row(filepath: str, row: dict):
    """Append a single row to an existing CSV file."""
    file_exists = Path(filepath).exists()
    with open(filepath, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=row.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)


# =============================================================================
# CSV TRANSFORMATION PATTERNS
# =============================================================================

def filter_csv_columns(
    input_path: str,
    output_path: str,
    keep_columns: list[str],
):
    """Copy CSV keeping only specified columns.

    Adapted from code_snippets/Python-CSV/parse_csv.py where columns
    were removed from rows before writing.
    """
    with open(input_path, "r", newline="", encoding="utf-8") as infile:
        reader = csv.DictReader(infile)

        with open(output_path, "w", newline="", encoding="utf-8") as outfile:
            writer = csv.DictWriter(outfile, fieldnames=keep_columns)
            writer.writeheader()

            for row in reader:
                filtered = {k: row[k] for k in keep_columns if k in row}
                writer.writerow(filtered)


def csv_to_json(csv_path: str, json_path: str):
    """Convert CSV file to JSON array."""
    data = read_csv_as_dicts(csv_path)
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def json_to_csv(json_path: str, csv_path: str):
    """Convert JSON array to CSV file."""
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if isinstance(data, list) and data:
        write_csv(csv_path, data)


# =============================================================================
# JSON READING
# =============================================================================

def read_json(filepath: str) -> Any:
    """Read and parse a JSON file.

    Adapted from code_snippets/Python-JSON/json_demo.py.
    """
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def read_json_safe(filepath: str, default: Any = None) -> Any:
    """Read JSON file with error handling."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return default
    except json.JSONDecodeError as e:
        print(f"Invalid JSON in {filepath}: {e}")
        return default


def read_jsonl(filepath: str) -> list[dict]:
    """Read JSON Lines format (one JSON object per line).

    Common in log files and streaming data.
    """
    records = []
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                records.append(json.loads(line))
    return records


# =============================================================================
# JSON WRITING
# =============================================================================

def write_json(filepath: str, data: Any, indent: int = 2):
    """Write data to a JSON file.

    Adapted from code_snippets/Python-JSON/json_demo.py.
    """
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=indent, ensure_ascii=False)


def write_jsonl(filepath: str, records: list[dict]):
    """Write JSON Lines format (one JSON object per line)."""
    with open(filepath, "w", encoding="utf-8") as f:
        for record in records:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")


def pretty_print_json(data: Any) -> str:
    """Return pretty-printed JSON string."""
    return json.dumps(data, indent=2, ensure_ascii=False, default=str)


# =============================================================================
# JSON TRANSFORMATION PATTERNS
# =============================================================================

def transform_json(
    input_path: str,
    output_path: str,
    transform_fn,
):
    """Read JSON, apply transformation, write result.

    Adapted from code_snippets/Python-JSON/json_demo.py pattern of
    loading, modifying, and saving JSON data.
    """
    data = read_json(input_path)
    transformed = transform_fn(data)
    write_json(output_path, transformed)


def merge_json_files(filepaths: list[str], output_path: str):
    """Merge multiple JSON files (assumes each contains a list)."""
    merged = []
    for fp in filepaths:
        data = read_json(fp)
        if isinstance(data, list):
            merged.extend(data)
        else:
            merged.append(data)
    write_json(output_path, merged)


def flatten_nested_json(data: dict, prefix: str = "") -> dict:
    """Flatten nested JSON into dot-notation keys.

    {"a": {"b": 1, "c": 2}} → {"a.b": 1, "a.c": 2}
    """
    flat = {}
    for key, value in data.items():
        full_key = f"{prefix}.{key}" if prefix else key
        if isinstance(value, dict):
            flat.update(flatten_nested_json(value, full_key))
        else:
            flat[full_key] = value
    return flat


# =============================================================================
# STRING-BASED CSV (for APIs that return CSV text)
# =============================================================================

def parse_csv_string(csv_text: str) -> list[dict]:
    """Parse CSV from a string (e.g., API response body)."""
    reader = csv.DictReader(StringIO(csv_text))
    return list(reader)


def dicts_to_csv_string(data: list[dict]) -> str:
    """Convert list of dicts to CSV string."""
    if not data:
        return ""
    output = StringIO()
    writer = csv.DictWriter(output, fieldnames=data[0].keys())
    writer.writeheader()
    writer.writerows(data)
    return output.getvalue()


if __name__ == "__main__":
    import tempfile
    import os

    print("=" * 60)
    print("CSV & JSON Operations Demo")
    print("=" * 60)

    # Create temp directory for demo files
    tmp_dir = tempfile.mkdtemp()

    # --- CSV Demo ---
    print("\n--- CSV Operations ---")

    # Write sample CSV
    csv_path = os.path.join(tmp_dir, "people.csv")
    people = [
        {"first_name": "John", "last_name": "Doe", "email": "john@example.com", "age": "30"},
        {"first_name": "Jane", "last_name": "Smith", "email": "jane@example.com", "age": "25"},
        {"first_name": "Bob", "last_name": "Wilson", "email": "bob@example.com", "age": "35"},
    ]
    write_csv(csv_path, people)
    print(f"  Wrote {len(people)} records to CSV")

    # Read it back
    loaded = read_csv_as_dicts(csv_path)
    print(f"  Read back: {loaded[0]}")

    # Filter columns (like code_snippets/Python-CSV/parse_csv.py)
    filtered_path = os.path.join(tmp_dir, "names_only.csv")
    filter_csv_columns(csv_path, filtered_path, ["first_name", "last_name"])
    print(f"  Filtered to names only: {read_csv_as_dicts(filtered_path)[0]}")

    # --- JSON Demo ---
    print("\n--- JSON Operations ---")

    # Write sample JSON
    json_path = os.path.join(tmp_dir, "config.json")
    config = {
        "database": {"host": "localhost", "port": 5432},
        "features": ["auth", "logging", "cache"],
        "debug": True,
    }
    write_json(json_path, config)
    print(f"  Wrote config to JSON")

    # Read and transform
    loaded_json = read_json(json_path)
    print(f"  Read back: {loaded_json['database']}")

    # Flatten nested JSON
    flat = flatten_nested_json(config)
    print(f"  Flattened: {flat}")

    # CSV to JSON conversion
    json_from_csv = os.path.join(tmp_dir, "people.json")
    csv_to_json(csv_path, json_from_csv)
    print(f"  Converted CSV → JSON")

    # --- Parse CSV from string ---
    print("\n--- String Parsing ---")
    csv_text = "name,score\nAlice,95\nBob,87\nCharlie,92"
    parsed = parse_csv_string(csv_text)
    print(f"  Parsed from string: {parsed}")

    # Cleanup
    import shutil
    shutil.rmtree(tmp_dir)
    print(f"\n  Cleaned up temp files")

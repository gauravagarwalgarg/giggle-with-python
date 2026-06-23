"""
File Renaming and Bulk Operations batch rename, organize, and manage files.

Practical scripts for renaming files in bulk, organizing directories,
and performing common file system operations.

Adapted from code_snippets/Automation/rename.py.
"""
import os
import re
import shutil
from pathlib import Path
from datetime import datetime


# =============================================================================
# BASIC FILE RENAMING
# =============================================================================

def rename_with_pattern(
    directory: str,
    pattern: str,
    replacement: str,
    dry_run: bool = True,
) -> list[tuple[str, str]]:
    """Rename files using regex pattern substitution.

    Args:
        directory: Path to directory containing files
        pattern: Regex pattern to match in filenames
        replacement: Replacement string (supports \\1, \\2 groups)
        dry_run: If True, only print what would happen

    Returns:
        List of (old_name, new_name) tuples
    """
    changes = []
    regex = re.compile(pattern)

    for filename in sorted(os.listdir(directory)):
        if filename.startswith("."):
            continue

        new_name = regex.sub(replacement, filename)
        if new_name != filename:
            changes.append((filename, new_name))
            if not dry_run:
                old_path = os.path.join(directory, filename)
                new_path = os.path.join(directory, new_name)
                os.rename(old_path, new_path)

    return changes


def rename_sequential(
    directory: str,
    prefix: str = "",
    start: int = 1,
    zero_pad: int = 2,
    dry_run: bool = True,
) -> list[tuple[str, str]]:
    """Rename files with sequential numbers.

    Adapted from code_snippets/Automation/rename.py number padding pattern.

    Example: photo.jpg → vacation_01.jpg, video.mp4 → vacation_02.mp4
    """
    changes = []
    files = sorted(
        f for f in os.listdir(directory)
        if not f.startswith(".") and os.path.isfile(os.path.join(directory, f))
    )

    for i, filename in enumerate(files, start=start):
        _, ext = os.path.splitext(filename)
        number = str(i).zfill(zero_pad)
        new_name = f"{prefix}{number}{ext}"
        changes.append((filename, new_name))

        if not dry_run:
            old_path = os.path.join(directory, filename)
            new_path = os.path.join(directory, new_name)
            os.rename(old_path, new_path)

    return changes


def rename_strip_whitespace(directory: str, dry_run: bool = True) -> list[tuple[str, str]]:
    """Remove leading/trailing whitespace and replace spaces with underscores.

    Adapted from code_snippets/Automation/rename.py strip() pattern.
    """
    changes = []

    for filename in os.listdir(directory):
        if filename.startswith("."):
            continue

        name, ext = os.path.splitext(filename)
        new_name = name.strip().replace(" ", "_") + ext

        if new_name != filename:
            changes.append((filename, new_name))
            if not dry_run:
                old_path = os.path.join(directory, filename)
                new_path = os.path.join(directory, new_name)
                os.rename(old_path, new_path)

    return changes


# =============================================================================
# STRUCTURED RENAMING (parse and reformat)
# =============================================================================

def rename_reformat(
    directory: str,
    separator: str = "-",
    output_format: str = "{number}-{title}",
    dry_run: bool = True,
) -> list[tuple[str, str]]:
    """Parse structured filenames and reformat them.

    Adapted from code_snippets/Automation/rename.py where filenames like
    'Title - Course - #1.mp4' were parsed and reformatted to '01-Title.mp4'.

    Handles filenames with format: 'part1{sep}part2{sep}part3.ext'
    """
    changes = []

    for filename in sorted(os.listdir(directory)):
        if filename.startswith("."):
            continue

        name, ext = os.path.splitext(filename)
        parts = name.split(separator)

        if len(parts) < 2:
            continue  # Skip files that don't match expected format

        # Clean up parts
        parts = [p.strip() for p in parts]

        # Try to find a number part
        number = ""
        title = ""
        course = ""

        for part in parts:
            # Check if this part looks like a number
            stripped = re.sub(r"[^0-9]", "", part)
            if stripped and not number:
                number = stripped.zfill(2)
            elif not title:
                title = part
            else:
                course = part

        if number and title:
            new_name = output_format.format(
                number=number,
                title=title,
                course=course,
            ) + ext
            changes.append((filename, new_name))

            if not dry_run:
                old_path = os.path.join(directory, filename)
                new_path = os.path.join(directory, new_name)
                os.rename(old_path, new_path)

    return changes


# =============================================================================
# FILE ORGANIZATION
# =============================================================================

def organize_by_extension(
    directory: str,
    dry_run: bool = True,
) -> dict[str, list[str]]:
    """Move files into subdirectories based on their extension.

    Example: photos/ gets .jpg and .png, documents/ gets .pdf and .docx
    """
    extension_map = {
        "images": {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp"},
        "documents": {".pdf", ".doc", ".docx", ".txt", ".md", ".rtf"},
        "videos": {".mp4", ".avi", ".mkv", ".mov", ".wmv"},
        "audio": {".mp3", ".wav", ".flac", ".aac", ".ogg"},
        "archives": {".zip", ".tar", ".gz", ".rar", ".7z"},
        "code": {".py", ".js", ".ts", ".java", ".cpp", ".h", ".go", ".rs"},
        "data": {".csv", ".json", ".xml", ".yaml", ".yml", ".sql"},
    }

    organized = {}

    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if not os.path.isfile(filepath) or filename.startswith("."):
            continue

        _, ext = os.path.splitext(filename)
        ext = ext.lower()

        # Find the right category
        target_dir = "other"
        for category, extensions in extension_map.items():
            if ext in extensions:
                target_dir = category
                break

        organized.setdefault(target_dir, []).append(filename)

        if not dry_run:
            dest_dir = os.path.join(directory, target_dir)
            os.makedirs(dest_dir, exist_ok=True)
            shutil.move(filepath, os.path.join(dest_dir, filename))

    return organized


def organize_by_date(
    directory: str,
    date_format: str = "%Y-%m",
    dry_run: bool = True,
) -> dict[str, list[str]]:
    """Organize files into subdirectories by modification date."""
    organized = {}

    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if not os.path.isfile(filepath) or filename.startswith("."):
            continue

        # Get modification time
        mtime = os.path.getmtime(filepath)
        date_str = datetime.fromtimestamp(mtime).strftime(date_format)

        organized.setdefault(date_str, []).append(filename)

        if not dry_run:
            dest_dir = os.path.join(directory, date_str)
            os.makedirs(dest_dir, exist_ok=True)
            shutil.move(filepath, os.path.join(dest_dir, filename))

    return organized


# =============================================================================
# BULK OPERATIONS
# =============================================================================

def find_duplicates(directory: str) -> dict[str, list[str]]:
    """Find files with identical content using hash comparison."""
    import hashlib

    hash_map: dict[str, list[str]] = {}

    for root, _, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename)
            try:
                with open(filepath, "rb") as f:
                    file_hash = hashlib.md5(f.read()).hexdigest()
                hash_map.setdefault(file_hash, []).append(filepath)
            except (PermissionError, OSError):
                continue

    # Return only entries with duplicates
    return {h: paths for h, paths in hash_map.items() if len(paths) > 1}


def batch_replace_in_files(
    directory: str,
    pattern: str,
    replacement: str,
    file_extensions: tuple[str, ...] = (".txt", ".md", ".py"),
    dry_run: bool = True,
) -> list[str]:
    """Replace text pattern across multiple files."""
    modified = []
    regex = re.compile(pattern)

    for root, _, files in os.walk(directory):
        for filename in files:
            if not filename.endswith(file_extensions):
                continue

            filepath = os.path.join(root, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()

            new_content = regex.sub(replacement, content)
            if new_content != content:
                modified.append(filepath)
                if not dry_run:
                    with open(filepath, "w", encoding="utf-8") as f:
                        f.write(new_content)

    return modified


if __name__ == "__main__":
    import tempfile

    print("=" * 60)
    print("File Renamer Demo")
    print("=" * 60)

    # Create temp directory with sample files
    tmp_dir = tempfile.mkdtemp()

    # Create sample files
    sample_files = [
        "My Document - Course - #1.txt",
        "My Document - Course - #2.txt",
        "My Document - Course - #10.txt",
        "photo.jpg",
        "report.pdf",
        "script.py",
        "data.csv",
        "notes.md",
    ]
    for f in sample_files:
        Path(os.path.join(tmp_dir, f)).touch()

    # Demo: Sequential rename
    print("\n--- Sequential Rename (dry run) ---")
    changes = rename_sequential(tmp_dir, prefix="file_", zero_pad=3, dry_run=True)
    for old, new in changes[:5]:
        print(f"  {old} → {new}")

    # Demo: Strip whitespace
    print("\n--- Strip Whitespace (dry run) ---")
    changes = rename_strip_whitespace(tmp_dir, dry_run=True)
    for old, new in changes[:5]:
        print(f"  {old} → {new}")

    # Demo: Organize by extension
    print("\n--- Organize by Extension (dry run) ---")
    organized = organize_by_extension(tmp_dir, dry_run=True)
    for category, files in organized.items():
        print(f"  {category}/: {files}")

    # Demo: Reformat structured names
    print("\n--- Reformat Names (dry run) ---")
    changes = rename_reformat(tmp_dir, separator="-", dry_run=True)
    for old, new in changes:
        print(f"  {old} → {new}")

    # Cleanup
    shutil.rmtree(tmp_dir)
    print(f"\n  Cleaned up temp directory")
    print("\n  TIP: Always use dry_run=True first to preview changes!")

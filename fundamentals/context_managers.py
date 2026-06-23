"""
Context Managers in Python with statement, __enter__/__exit__, @contextmanager.

Context managers ensure resources are properly acquired and released,
even when exceptions occur. The with statement makes this clean and safe.

Adapted from code_snippets/Python-Context-Managers.
"""
import os
import time
import sqlite3
from contextlib import contextmanager, suppress
from typing import Generator


# =============================================================================
# CLASS-BASED CONTEXT MANAGERS (__enter__ / __exit__)
# =============================================================================

class FileManager:
    """Basic context manager for file handling.

    The with statement calls __enter__ on entry and __exit__ on exit,
    even if an exception is raised inside the block.
    """

    def __init__(self, filename: str, mode: str = "r"):
        self.filename = filename
        self.mode = mode
        self.file = None

    def __enter__(self):
        """Called when entering the with block. Returns the resource."""
        self.file = open(self.filename, self.mode)
        return self.file

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Called when exiting the with block (even on exception).

        Args:
            exc_type: Exception class (or None if no exception)
            exc_val: Exception instance (or None)
            exc_tb: Traceback object (or None)

        Returns:
            True to suppress the exception, False to propagate it.
        """
        if self.file:
            self.file.close()
        return False  # Don't suppress exceptions


class Timer:
    """Context manager that measures execution time."""

    def __init__(self, label: str = "Block"):
        self.label = label
        self.start = 0.0
        self.elapsed = 0.0

    def __enter__(self):
        self.start = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.elapsed = time.perf_counter() - self.start
        print(f"{self.label} took {self.elapsed:.4f}s")
        return False


class DatabaseConnection:
    """Context manager for database connections with auto-commit/rollback."""

    def __init__(self, db_path: str):
        self.db_path = db_path
        self.conn = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_path)
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            # Exception occurred: rollback
            self.conn.rollback()
        else:
            # No exception: commit
            self.conn.commit()
        self.conn.close()
        return False


# =============================================================================
# GENERATOR-BASED CONTEXT MANAGERS (@contextmanager)
# =============================================================================

@contextmanager
def change_dir(destination: str) -> Generator[str, None, None]:
    """Temporarily change working directory, then restore it.

    Adapted from code_snippets/Python-Context-Managers/cm_demo.py.
    The yield separates setup from cleanup. Code before yield is __enter__,
    code after yield is __exit__.
    """
    original = os.getcwd()
    try:
        os.chdir(destination)
        yield destination
    finally:
        os.chdir(original)


@contextmanager
def temporary_env_var(key: str, value: str) -> Generator[None, None, None]:
    """Set an environment variable temporarily, restore on exit."""
    original = os.environ.get(key)
    os.environ[key] = value
    try:
        yield
    finally:
        if original is None:
            del os.environ[key]
        else:
            os.environ[key] = original


@contextmanager
def open_file(filename: str, mode: str = "r"):
    """Simple file context manager using @contextmanager.

    Equivalent to the built-in open() context manager behavior.
    """
    f = open(filename, mode)
    try:
        yield f
    finally:
        f.close()


@contextmanager
def managed_resource(name: str):
    """Template for any acquire/release pattern."""
    print(f"Acquiring {name}")
    resource = {"name": name, "acquired": True}
    try:
        yield resource
    finally:
        resource["acquired"] = False
        print(f"Releasing {name}")


# =============================================================================
# PRACTICAL PATTERNS
# =============================================================================

@contextmanager
def atomic_write(filepath: str) -> Generator:
    """Write to a temp file, then atomically rename on success.

    If an exception occurs, the original file is untouched.
    """
    import tempfile
    from pathlib import Path

    path = Path(filepath)
    tmp_path = path.with_suffix(".tmp")

    try:
        with open(tmp_path, "w") as f:
            yield f
        # Only rename if no exception occurred
        tmp_path.replace(path)
    except Exception:
        # Clean up temp file on failure
        if tmp_path.exists():
            tmp_path.unlink()
        raise


@contextmanager
def suppress_output():
    """Suppress stdout/stderr temporarily."""
    import sys
    from io import StringIO

    old_stdout, old_stderr = sys.stdout, sys.stderr
    sys.stdout = StringIO()
    sys.stderr = StringIO()
    try:
        yield
    finally:
        sys.stdout = old_stdout
        sys.stderr = old_stderr


# =============================================================================
# BUILT-IN CONTEXT MANAGER UTILITIES
# =============================================================================

def demonstrate_builtins():
    """Show useful context managers from the standard library."""

    # suppress() silently ignore specific exceptions
    with suppress(FileNotFoundError):
        os.remove("nonexistent_file.txt")
        # No exception raised even though file doesn't exist

    # contextlib.redirect_stdout capture print output
    from contextlib import redirect_stdout
    from io import StringIO

    buffer = StringIO()
    with redirect_stdout(buffer):
        print("This goes to buffer, not console")
    captured = buffer.getvalue()

    # contextlib.closing for objects with close() but no __exit__
    from contextlib import closing
    from urllib.request import urlopen

    # with closing(urlopen("http://example.com")) as page:
    #     html = page.read()

    return captured


# =============================================================================
# NESTED AND STACKED CONTEXT MANAGERS
# =============================================================================

def copy_file_safe(source: str, destination: str):
    """Nested context managers the classic pattern."""
    with open(source, "r") as src:
        with open(destination, "w") as dst:
            for line in src:
                dst.write(line)


def copy_file_stacked(source: str, destination: str):
    """Python 3.10+ parenthesized context managers."""
    with (
        open(source, "r") as src,
        open(destination, "w") as dst,
    ):
        for line in src:
            dst.write(line)


if __name__ == "__main__":
    print("=" * 60)
    print("Context Managers Demo")
    print("=" * 60)

    # Timer context manager
    print("\n--- Timer ---")
    with Timer("Sleep test") as t:
        time.sleep(0.1)
    print(f"  Measured: {t.elapsed:.4f}s")

    # Change directory
    print("\n--- Change Directory ---")
    original_dir = os.getcwd()
    print(f"  Before: {os.getcwd()}")
    with change_dir("/tmp"):
        print(f"  Inside: {os.getcwd()}")
    print(f"  After:  {os.getcwd()}")

    # Temporary env var
    print("\n--- Temporary Env Var ---")
    with temporary_env_var("MY_SETTING", "temporary_value"):
        print(f"  Inside: MY_SETTING={os.environ.get('MY_SETTING')}")
    print(f"  Outside: MY_SETTING={os.environ.get('MY_SETTING', 'not set')}")

    # Managed resource
    print("\n--- Managed Resource ---")
    with managed_resource("database pool") as pool:
        print(f"  Using: {pool}")

    # Suppress exceptions
    print("\n--- Suppress ---")
    with suppress(ZeroDivisionError):
        result = 1 / 0  # No crash!
    print("  ZeroDivisionError was suppressed")

    # Built-in demos
    print("\n--- Built-in Utilities ---")
    captured = demonstrate_builtins()
    print(f"  Captured output: {captured.strip()!r}")

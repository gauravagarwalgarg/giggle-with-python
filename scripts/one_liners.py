"""
Python one-liners for daily use.

A collection of useful tricks, idioms, and patterns that fit in one line.
Run this file to see them all in action.
"""
import json
import os
import secrets
import sys
import time
from collections import Counter
from datetime import datetime
from pathlib import Path


# =============================================================================
# LIST OPERATIONS
# =============================================================================

# Flatten nested list
nested = [[1, 2], [3, 4], [5, 6]]
flat = [item for sublist in nested for item in sublist]

# Remove duplicates while preserving order
items = [3, 1, 4, 1, 5, 9, 2, 6, 5]
unique = list(dict.fromkeys(items))

# Transpose a matrix (list of lists)
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
transposed = list(map(list, zip(*matrix)))

# Chunk a list into groups of n
data = list(range(10))
chunks = [data[i:i+3] for i in range(0, len(data), 3)]

# Get top N items
numbers = [5, 3, 8, 1, 9, 2, 7]
import heapq
top_3 = heapq.nlargest(3, numbers)

# Interleave two lists
a, b = [1, 3, 5], [2, 4, 6]
interleaved = [x for pair in zip(a, b) for x in pair]


# =============================================================================
# DICT TRICKS
# =============================================================================

# Reverse a dict (swap keys and values)
original = {"a": 1, "b": 2, "c": 3}
reversed_dict = {v: k for k, v in original.items()}

# Merge multiple dicts (Python 3.9+)
d1, d2, d3 = {"a": 1}, {"b": 2}, {"c": 3}
merged = d1 | d2 | d3

# Count word frequency
text = "the quick brown fox jumps over the lazy dog the fox"
freq = Counter(text.split())

# Group items by key
from itertools import groupby
people = [("Alice", "Eng"), ("Bob", "Mkt"), ("Charlie", "Eng"), ("Diana", "Mkt")]
grouped = {k: [name for name, _ in g] for k, g in groupby(sorted(people, key=lambda x: x[1]), key=lambda x: x[1])}

# Filter dict by value
scores = {"Alice": 85, "Bob": 92, "Charlie": 67, "Diana": 95}
high_scores = {k: v for k, v in scores.items() if v >= 90}

# Sort dict by value
sorted_scores = dict(sorted(scores.items(), key=lambda x: x[1], reverse=True))


# =============================================================================
# STRING OPERATIONS
# =============================================================================

# Read file lines (stripped, no empty)
# lines = [l.strip() for l in open("file.txt") if l.strip()]

# Title case
title = "hello world from python".title()

# Remove multiple spaces
import re
clean = re.sub(r"\s+", " ", "  too   many   spaces  ").strip()

# Check if string is a palindrome
is_palindrome = lambda s: s == s[::-1]

# Caesar cipher (rotate by n)
rotate = lambda s, n: "".join(chr((ord(c) - 97 + n) % 26 + 97) if c.isalpha() else c for c in s.lower())


# =============================================================================
# FILE & SYSTEM
# =============================================================================

# Quick HTTP server (run in terminal)
# python3 -m http.server 8080

# Pretty print JSON (run in terminal)
# python3 -m json.tool < input.json

# Generate secure password/token
password = secrets.token_urlsafe(16)

# Get file size in human readable format
def human_size(size_bytes: int) -> str:
    for unit in ["B", "KB", "MB", "GB"]:
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} TB"

# Find all Python files in directory
py_files = list(Path(".").rglob("*.py"))

# Read JSON file in one line
# config = json.loads(Path("config.json").read_text())

# Environment variable with default
debug = os.getenv("DEBUG", "false").lower() == "true"


# =============================================================================
# FUNCTIONAL PATTERNS
# =============================================================================

# Timer decorator
def timer(func):
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        print(f"{func.__name__}: {time.perf_counter() - start:.4f}s")
        return result
    return wrapper

# Retry decorator (simple)
def retry(n=3):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for i in range(n):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if i == n - 1:
                        raise
        return wrapper
    return decorator

# Memoize (cache results)
from functools import lru_cache

@lru_cache(maxsize=128)
def fib(n):
    return n if n < 2 else fib(n-1) + fib(n-2)

# Pipeline / compose
from functools import reduce
pipeline = lambda *funcs: lambda x: reduce(lambda v, f: f(v), funcs, x)
transform = pipeline(str.strip, str.lower, str.title)


# =============================================================================
# DATA PROCESSING
# =============================================================================

# Flatten and deduplicate
all_tags = [["python", "code"], ["python", "tips"], ["code", "tricks"]]
unique_tags = list(set(tag for tags in all_tags for tag in tags))

# Running average
values = [10, 20, 30, 40, 50]
running_avg = [sum(values[:i+1])/(i+1) for i in range(len(values))]

# Cumulative sum
from itertools import accumulate
cumsum = list(accumulate(values))

# Zip with index (enumerate alternative)
indexed = list(enumerate(["a", "b", "c"], start=1))

# pairwise iteration
pairs = list(zip(values, values[1:]))  # [(10,20), (20,30), (30,40), (40,50)]


# =============================================================================
# DATETIME
# =============================================================================

# Current ISO timestamp
now_iso = datetime.now().isoformat()

# Unix timestamp to datetime
# from_unix = datetime.fromtimestamp(1718433000)

# Days between two dates
from datetime import date
days_in_year = (date(2025, 1, 1) - date(2024, 1, 1)).days


if __name__ == "__main__":
    print("=" * 60)
    print("Python One-Liners")
    print("=" * 60)

    print(f"\n--- Lists ---")
    print(f"  Flatten: {flat}")
    print(f"  Unique (ordered): {unique}")
    print(f"  Chunks of 3: {chunks}")
    print(f"  Top 3: {top_3}")
    print(f"  Interleaved: {interleaved}")

    print(f"\n--- Dicts ---")
    print(f"  Reversed: {reversed_dict}")
    print(f"  Merged: {merged}")
    print(f"  Word freq: {freq.most_common(3)}")
    print(f"  High scores: {high_scores}")
    print(f"  Sorted: {sorted_scores}")

    print(f"\n--- Strings ---")
    print(f"  Title case: '{title}'")
    print(f"  Clean spaces: '{clean}'")
    print(f"  Palindrome 'racecar': {is_palindrome('racecar')}")
    print(f"  Caesar('hello', 3): '{rotate('hello', 3)}'")

    print(f"\n--- Functional ---")
    print(f"  fib(30): {fib(30)}")
    print(f"  pipeline: '{transform('  HELLO WORLD  ')}'")

    print(f"\n--- Data ---")
    print(f"  Running avg: {running_avg}")
    print(f"  Cumulative sum: {cumsum}")
    print(f"  Pairs: {pairs}")

    print(f"\n--- System ---")
    print(f"  Password: {password}")
    print(f"  Python files: {len(py_files)} found")
    print(f"  Days in 2024: {days_in_year}")

    print(f"\n--- Useful CLI commands ---")
    print(f"  python3 -m http.server 8080     # Quick HTTP server")
    print(f"  python3 -m json.tool < f.json   # Pretty print JSON")
    print(f"  python3 -m timeit 'sum(range(1000))'  # Benchmark")
    print(f"  python3 -m venv .venv           # Create virtualenv")
    print(f"  python3 -m pip list --outdated  # Check for updates")

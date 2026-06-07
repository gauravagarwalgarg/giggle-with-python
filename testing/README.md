# Testing Pytest Patterns

Practical testing patterns with pytest the standard testing framework for Python.

## Setup

```bash
pip install -r requirements.txt
```

## Running Tests

```bash
# Run all tests
pytest testing/ -v

# Run with coverage
pytest testing/ --cov --cov-report=term-missing

# Run specific test class
pytest testing/test_example.py::TestUserCreation -v

# Run by marker
pytest testing/ -m "not slow"
pytest testing/ -m integration

# Stop on first failure
pytest testing/ -x

# Show print output
pytest testing/ -s

# Parallel (install pytest-xdist)
pytest testing/ -n auto
```

## What's Covered

- **Fixtures**: Setup/teardown, scopes, dependency injection
- **Parametrize**: Data-driven tests with multiple inputs
- **Mocking**: unittest.mock with requests, files, external services
- **Markers**: slow, integration, skip, xfail
- **Exceptions**: Testing error cases with pytest.raises
- **Temp files**: Using tmp_path for isolated file tests

## Project Configuration

Add to `pyproject.toml`:

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
markers = [
    "slow: marks tests as slow",
    "integration: marks integration tests",
]
addopts = "--strict-markers --tb=short"

[tool.coverage.run]
source = ["src"]
omit = ["tests/*"]
```

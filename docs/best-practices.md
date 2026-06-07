# Python Best Practices

Code style, project structure, packaging, and virtual environments.

## Code Style

### Follow PEP 8 (with pragmatism)

```python
# Good: descriptive names, consistent style
def calculate_monthly_revenue(transactions: list[dict], month: int) -> float:
    """Calculate total revenue for a given month."""
    return sum(
        t["amount"]
        for t in transactions
        if t["date"].month == month and t["type"] == "income"
    )

# Bad: cryptic names, inconsistent
def calc(t, m):
    s = 0
    for x in t:
        if x["date"].month == m:
            if x["type"] == "income":
                s += x["amount"]
    return s
```

### Naming Conventions

| Type | Convention | Example |
|------|-----------|---------|
| Variables, functions | snake_case | `user_name`, `get_users()` |
| Classes | PascalCase | `UserService`, `HTTPClient` |
| Constants | UPPER_SNAKE | `MAX_RETRIES`, `API_BASE_URL` |
| Private | _leading_underscore | `_internal_method()` |
| Modules | short_snake_case | `user_service.py` |

### Imports

```python
# Standard library
import os
import sys
from pathlib import Path
from typing import Any

# Third-party (blank line separator)
import requests
from fastapi import FastAPI
from pydantic import BaseModel

# Local
from .models import User
from .utils import validate_email
```

## Project Structure

### Small project (script/utility)
```
my-tool/
├── my_tool.py
├── requirements.txt
├── README.md
└── .gitignore
```

### Medium project (package)
```
my-project/
├── src/
│   └── my_project/
│       ├── __init__.py
│       ├── main.py
│       ├── models.py
│       ├── services.py
│       └── utils.py
├── tests/
│   ├── conftest.py
│   ├── test_main.py
│   └── test_services.py
├── pyproject.toml
├── README.md
└── .gitignore
```

### Large project (application)
```
my-app/
├── src/
│   └── my_app/
│       ├── __init__.py
│       ├── config.py
│       ├── api/
│       │   ├── __init__.py
│       │   ├── routes.py
│       │   └── middleware.py
│       ├── domain/
│       │   ├── __init__.py
│       │   ├── models.py
│       │   └── services.py
│       ├── infrastructure/
│       │   ├── __init__.py
│       │   ├── database.py
│       │   └── cache.py
│       └── utils/
│           └── __init__.py
├── tests/
│   ├── unit/
│   ├── integration/
│   └── conftest.py
├── scripts/
├── docs/
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yml
├── pyproject.toml
├── Makefile
└── README.md
```

## Virtual Environments

Always use a virtual environment. Never install packages globally.

```bash
# Create
python3 -m venv .venv

# Activate
source .venv/bin/activate    # Linux/Mac
.venv\Scripts\activate       # Windows

# Deactivate
deactivate

# Pin your dependencies
pip freeze > requirements.txt

# Or better use pip-compile for deterministic builds
pip install pip-tools
pip-compile requirements.in   # Creates requirements.txt with pinned versions
```

## Configuration

### Use pyproject.toml (modern standard)

```toml
[project]
name = "my-project"
version = "1.0.0"
requires-python = ">=3.10"
dependencies = [
    "fastapi>=0.100.0",
    "pydantic>=2.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0",
    "ruff>=0.4.0",
    "mypy>=1.10",
]

[tool.ruff]
target-version = "py310"
line-length = 100

[tool.ruff.lint]
select = ["E", "W", "F", "I", "UP", "B", "SIM"]

[tool.mypy]
python_version = "3.10"
strict = true
ignore_missing_imports = true

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "--strict-markers -v"
```

## Error Handling

```python
# Good: Specific exceptions, helpful messages
def get_user(user_id: int) -> User:
    try:
        user = db.query(User).get(user_id)
    except ConnectionError as e:
        logger.error(f"Database connection failed: {e}")
        raise ServiceUnavailableError("Cannot reach database") from e

    if user is None:
        raise UserNotFoundError(f"User {user_id} does not exist")

    return user

# Bad: Bare except, silencing errors
def get_user(user_id):
    try:
        return db.query(User).get(user_id)
    except:
        return None  # Hides bugs!
```

## Logging (not print)

```python
import logging

logger = logging.getLogger(__name__)

# Good
logger.info("Processing order", extra={"order_id": order.id, "total": order.total})
logger.error("Payment failed", exc_info=True)

# Bad
print(f"Processing order {order.id}")  # Lost in production
```

## Type Hints

Use type hints everywhere. They're documentation and catch bugs.

```python
# Good: Clear contract
def process_payment(
    amount: float,
    currency: str = "INR",
    *,
    idempotency_key: str | None = None,
) -> PaymentResult:
    ...

# Catch bugs at development time, not in production
# Run: mypy src/ --strict
```

## Security Basics

1. **Never hardcode secrets** use environment variables
2. **Validate all input** use Pydantic models
3. **Use parameterized queries** never f-string SQL
4. **Pin dependencies** avoid supply chain attacks
5. **Keep dependencies updated** `pip audit` for vulnerabilities

```python
# Good
cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))

# Bad (SQL injection!)
cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")
```

## Performance Tips

1. **Profile before optimizing** `python -m cProfile script.py`
2. **Use generators for large data** `yield` instead of building lists
3. **Use `__slots__` for many instances** saves memory
4. **Prefer list comprehensions** faster than loops + append
5. **Use appropriate data structures** `set` for membership, `deque` for queues
6. **Consider Polars** when Pandas is too slow

## Git Workflow

```bash
# Branch naming
feature/add-user-api
fix/login-timeout
chore/update-dependencies

# Commit messages (conventional commits)
feat: add user registration endpoint
fix: resolve timeout in payment processing
docs: update API documentation
refactor: extract email validation to utility
test: add unit tests for order service
```

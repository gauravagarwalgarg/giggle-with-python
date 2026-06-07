# Python Ecosystem Guide

When to use what, and which libraries to pick for your project.

## Web Frameworks Django vs Flask vs FastAPI

| Criteria | Django | Flask | FastAPI |
|----------|--------|-------|---------|
| **Best for** | Full-featured web apps | Small APIs, microservices | Modern async APIs |
| **Learning curve** | Steep (many concepts) | Gentle (minimal) | Moderate (async + Pydantic) |
| **Performance** | Good | Good | Excellent (async) |
| **Built-in features** | ORM, admin, auth, forms | Routing, templates | Validation, docs, DI |
| **Documentation** | Excellent | Good | Excellent |
| **Async support** | Partial (ASGI) | No (use Quart) | Native |
| **Database** | Django ORM | SQLAlchemy | SQLAlchemy/Tortoise |
| **API docs** | Manual (DRF has browsable API) | Manual (Swagger via extensions) | Auto-generated OpenAPI |

### Decision Matrix

**Choose Django when:**
- Building a content-heavy site (CMS, e-commerce, blog)
- You need an admin panel
- Team prefers conventions over configuration
- Building REST APIs with Django REST Framework
- Project will grow large (> 50 endpoints)

**Choose Flask when:**
- Building a small service (< 20 endpoints)
- Prototyping or building an MVP
- You want to pick your own tools (ORM, auth, etc.)
- Building microservices
- Simple server-rendered pages

**Choose FastAPI when:**
- Building a modern REST API
- Need automatic request validation
- Want auto-generated API documentation
- Working with async (many concurrent I/O operations)
- Serving ML models
- Building WebSocket applications

## Data Science Stack

| Library | Purpose | When to use |
|---------|---------|------------|
| **Pandas** | Data manipulation | Tabular data, CSV/Excel, SQL results |
| **NumPy** | Numerical computing | Math operations, arrays, linear algebra |
| **Matplotlib** | Plotting | Publication-quality charts, full control |
| **Seaborn** | Statistical plotting | Quick, beautiful statistical charts |
| **Plotly** | Interactive plots | Dashboards, web-based visualization |
| **SciPy** | Scientific computing | Statistics, optimization, signal processing |
| **Scikit-learn** | Machine learning | Classification, regression, clustering |
| **Polars** | Fast DataFrames | When Pandas is too slow (large datasets) |

## DevOps & Automation

| Library | Purpose |
|---------|---------|
| **boto3** | AWS SDK (S3, EC2, Lambda, etc.) |
| **docker** | Docker SDK (containers, images, compose) |
| **fabric** | SSH remote execution |
| **paramiko** | Low-level SSH |
| **ansible** | Configuration management (via CLI) |
| **terraform** | Infrastructure as Code (via subprocess) |
| **requests** | HTTP client |
| **httpx** | Async HTTP client |

## Testing

| Library | Purpose |
|---------|---------|
| **pytest** | Test framework (use this) |
| **pytest-cov** | Code coverage |
| **pytest-mock** | Mocking integration |
| **pytest-asyncio** | Async test support |
| **hypothesis** | Property-based testing |
| **factory_boy** | Test data factories |
| **responses** / **respx** | Mock HTTP requests |

## Databases

| Library | Use case |
|---------|----------|
| **SQLAlchemy** | SQL ORM + Core (most popular) |
| **Django ORM** | If using Django |
| **Tortoise ORM** | Async ORM (for FastAPI) |
| **SQLModel** | SQLAlchemy + Pydantic (by FastAPI creator) |
| **Alembic** | Database migrations |
| **Redis (redis-py)** | Caching, queues |
| **Motor** | Async MongoDB |

## Code Quality

| Tool | Purpose | Speed |
|------|---------|-------|
| **ruff** | Linter + formatter | ⚡ Fastest |
| **mypy** | Type checking | Fast |
| **black** | Code formatter | Good |
| **isort** | Import sorting | Good |
| **bandit** | Security linter | Good |
| **pre-commit** | Git hooks | |

**Recommendation**: Use `ruff` for linting + formatting (replaces flake8, black, isort, pyupgrade in one tool).

## Task Queues & Background Jobs

| Library | Use case |
|---------|----------|
| **Celery** | Distributed task queue (heavy, reliable) |
| **RQ (Redis Queue)** | Simple job queue |
| **Dramatiq** | Modern alternative to Celery |
| **APScheduler** | In-process scheduling |
| **Huey** | Lightweight task queue |

## CLI Tools

| Library | Use case |
|---------|----------|
| **argparse** | Stdlib, good for most CLIs |
| **click** | Decorator-based CLI framework |
| **typer** | Type-hint based CLI (by FastAPI creator) |
| **rich** | Beautiful terminal output |
| **textual** | TUI applications |

## Package Management

| Tool | Use case |
|------|----------|
| **pip + venv** | Standard (always works) |
| **poetry** | Dependency management + packaging |
| **uv** | Fast pip replacement (Rust-based) |
| **pipx** | Install CLI tools globally |
| **conda** | Data science environments |

**Recommendation**: Start with `pip + venv`. Move to `poetry` or `uv` for published packages.

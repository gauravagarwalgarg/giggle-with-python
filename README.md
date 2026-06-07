# GiggleWithPython 🐍

A comprehensive Python end-to-end development repository. From fundamentals to frameworks, data science to DevOps everything you need to be productive with Python.

## Directory Structure

```
GiggleWithPython/
│
├── fundamentals/              # Python from ground up
│   ├── data_types.py          # str, int, float, list, dict, set, tuple
│   ├── control_flow.py        # if/else, for, while, match/case (3.10+)
│   ├── functions.py           # args, kwargs, decorators, generators, closures
│   ├── oop.py                 # classes, inheritance, protocols, dataclasses
│   ├── async_await.py         # asyncio, aiohttp, concurrent.futures
│   └── typing_hints.py        # type hints, generics, TypeVar, Protocol
│
├── frameworks/
│   ├── django/                # Full-featured web framework (existing project)
│   ├── flask/                 # Lightweight micro-framework
│   │   └── app.py            # Routes, blueprints, CRUD, auth
│   └── fastapi/              # Modern async API framework
│       └── main.py           # Pydantic models, CRUD, dependency injection
│
├── data-analytics/            # Data science and analytics
│   ├── pandas_cheatsheet.py   # The 20 operations you use 80% of the time
│   ├── numpy_basics.py        # Arrays, broadcasting, linear algebra
│   ├── matplotlib_plots.py    # Line, bar, scatter, subplots, styling
│   └── scipy_stats.py         # Distributions, hypothesis testing, curve fitting
│
├── snippets/                  # Reusable Python recipes
│   ├── gitlab_api.py          # GitLab REST API: projects, MRs, pipelines
│   ├── file_ops.py            # Read/write JSON, YAML, CSV, .env
│   ├── http_requests.py       # Retry, auth, pagination, rate limiting
│   ├── logging_setup.py       # JSON structured logging, rotating files
│   ├── cli_argparse.py        # Subcommands, validation, env config
│   ├── datetime_utils.py      # Timezone handling, parsing, relative time
│   └── regex_patterns.py      # Email, IP, URL, phone, dates, text cleaning
│
├── automation/                # DevOps and scripting
│   ├── docker_utils.py        # Docker SDK: containers, builds, exec
│   ├── aws_boto3.py           # S3, EC2, Lambda, SSM, SQS
│   └── ssh_fabric.py          # Remote execution, deployment, file transfer
│
├── testing/                   # Pytest patterns
│   └── test_example.py        # Fixtures, parametrize, mock, markers
│
├── scripts/                   # Standalone utilities
│   ├── setup_venv.sh          # Create venv, install deps
│   ├── lint.sh                # Run ruff + mypy checks
│   └── one_liners.py          # Python tricks and idioms
│
├── docs/                      # Documentation
│   ├── getting-started.md     # Setup, running examples
│   ├── python-ecosystem.md    # Django vs Flask vs FastAPI, library guide
│   └── best-practices.md      # Code style, structure, packaging
│
├── .gitignore
├── requirements.txt           # Dev tools (ruff, mypy, pytest)
└── README.md                  # You are here
```

## Quick Start

```bash
# Clone
git clone https://github.com/GauravAgarwalGarg/GiggleWithPython.git
cd GiggleWithPython

# Setup environment
bash scripts/setup_venv.sh
source .venv/bin/activate

# Run any file
python fundamentals/data_types.py
python snippets/regex_patterns.py
python scripts/one_liners.py

# Run a web framework
pip install -r frameworks/fastapi/requirements.txt
python frameworks/fastapi/main.py
# → http://localhost:8000/docs

# Run tests
pip install -r testing/requirements.txt
pytest testing/ -v
```

## What's Inside

### Fundamentals
Python 3.10+ language features from basics to advanced. Covers data types, control flow, functions (decorators, generators, closures), OOP (protocols, dataclasses), async/await, and type hints with generics.

### Frameworks
Three web frameworks compared side-by-side:
- **Django** batteries-included, admin panel, ORM
- **Flask** micro-framework, pick your own tools
- **FastAPI** modern async, auto-docs, Pydantic validation

### Data Analytics
Quick-reference scripts for the data science stack. Pandas cheatsheet, NumPy operations, Matplotlib plotting, and SciPy statistics.

### Snippets
Copy-paste ready code for everyday tasks: API calls, file I/O, logging, CLI tools, datetime handling, and regex patterns.

### Automation
Scripts for infrastructure work: Docker container management, AWS operations (S3, EC2, Lambda), and SSH remote execution.

### Testing
Practical pytest patterns: fixtures, parametrize, mocking, markers, and project configuration.

## Requirements

- Python 3.10+ (for match/case and `X | Y` type syntax)
- Each section has its own `requirements.txt` install only what you need

## Philosophy

- **Practical over theoretical** every example is runnable
- **Comments explain WHY** not just what the code does
- **Copy-paste ready** take what you need for your projects
- **Progressive complexity** start simple, go deep when needed

## Contributing

1. Fork the repo
2. Create a feature branch
3. Add your examples with docstrings and `if __name__ == "__main__":` blocks
4. Run `bash scripts/lint.sh` before committing
5. Submit a PR

## License

MIT

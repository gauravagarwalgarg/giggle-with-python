# Snippets

Production-ready code snippets for common Python tasks. Copy, adapt, and use in your projects.

## Files

| File | Purpose | Key Functions |
|------|---------|---------------|
| `gitlab_api.py` | GitLab API integration | Auth, list projects, create MR, pipelines |
| `file_ops.py` | File operations | Read/write, copy, move, walk directory tree |
| `http_requests.py` | HTTP client patterns | GET/POST, sessions, retries, auth headers |
| `logging_setup.py` | Logging configuration | Formatters, handlers, rotating files, structured logging |
| `csv_json_ops.py` | CSV & JSON handling | Read/write CSV, parse JSON, transform data |
| `datetime_utils.py` | Date/time utilities | Parsing, formatting, timezones, arithmetic |
| `regex_patterns.py` | Regular expressions | Email, URL, phone, IP validation, extraction |
| `cli_argparse.py` | CLI argument parsing | argparse setup, subcommands, validation |
| `web_scraping.py` | Web scraping | BeautifulSoup, requests, pagination, rate limiting |

## Path

```
snippets/
├── cli_argparse.py
├── csv_json_ops.py
├── datetime_utils.py
├── file_ops.py
├── gitlab_api.py
├── http_requests.py
├── logging_setup.py
├── regex_patterns.py
└── web_scraping.py
```

## Usage Pattern

Each snippet file is self-contained with:

1. Imports at the top
2. Helper functions / classes
3. `if __name__ == "__main__":` demo block

Run any snippet directly: `python snippets/http_requests.py`

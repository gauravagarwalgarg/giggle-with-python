# Snippets Reusable Python Recipes

Copy-paste ready code for common tasks. Each file is standalone and well-documented.

## Files

| File | Use case |
|------|----------|
| `gitlab_api.py` | GitLab REST API list projects, create MRs, trigger pipelines |
| `file_ops.py` | Read/write JSON, YAML, CSV, .env files |
| `http_requests.py` | requests library retry, auth, pagination, rate limiting |
| `logging_setup.py` | Structured JSON logging, rotating files, context logging |
| `cli_argparse.py` | argparse patterns subcommands, validation, env config |
| `datetime_utils.py` | Timezone handling, parsing, formatting, relative time |
| `regex_patterns.py` | Common regex email, IP, URL, phone, dates, text cleaning |

## Usage

Each file can be imported as a module or run directly:

```bash
# Run demos
python snippets/file_ops.py
python snippets/datetime_utils.py
python snippets/regex_patterns.py

# Import in your code
from snippets.file_ops import read_json, write_json
from snippets.datetime_utils import relative_time
from snippets.regex_patterns import is_valid_email, slugify
```

## Dependencies

Most snippets use stdlib only. Exceptions:
- `http_requests.py` → `pip install requests`
- `gitlab_api.py` → `pip install requests`
- `file_ops.py` (YAML) → `pip install pyyaml`

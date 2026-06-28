# Testing

Python testing patterns using pytest and unittest.

## Files

| File | Framework | Topics |
|------|-----------|--------|
| `test_example.py` | pytest | Fixtures, parametrize, marks, conftest patterns |
| `test_unittest_example.py` | unittest | TestCase, setUp/tearDown, assertions, mock |

## Path

```
testing/
├── requirements.txt
├── test_example.py
└── test_unittest_example.py
```

## Running Tests

```bash
cd testing
pip install -r requirements.txt

# pytest
pytest test_example.py -v

# unittest
python -m unittest test_unittest_example.py -v
```

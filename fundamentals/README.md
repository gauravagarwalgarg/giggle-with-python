# Python Fundamentals

Core Python concepts from ground up. Each file is standalone and runnable.

## Files

| File | Topics |
|------|--------|
| `data_types.py` | str, int, float, list, dict, set, tuple, None |
| `control_flow.py` | if/else, for, while, match/case (3.10+), comprehensions |
| `functions.py` | args, kwargs, decorators, generators, closures, lambdas |
| `oop.py` | Classes, inheritance, protocols, dataclasses, dunder methods |
| `async_await.py` | asyncio, aiohttp patterns, concurrent.futures |
| `typing_hints.py` | Type hints, generics, TypeVar, Protocol, overload |

## Running

```bash
# Run any file directly
python fundamentals/data_types.py
python fundamentals/control_flow.py
python fundamentals/functions.py
python fundamentals/oop.py
python fundamentals/async_await.py
python fundamentals/typing_hints.py
```

## Requirements

- Python 3.10+ (for match/case and modern type syntax)
- No external dependencies all stdlib
- `aiohttp` optional for async HTTP examples

## Learning Path

1. Start with `data_types.py` understand what you're working with
2. `control_flow.py` learn to direct program execution
3. `functions.py` the building blocks of reusable code
4. `oop.py` organize code into objects and hierarchies
5. `typing_hints.py` make your code self-documenting
6. `async_await.py` handle I/O-bound concurrency

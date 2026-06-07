"""
Type Hints in Python type annotations, generics, TypeVar, Protocol.

Type hints don't affect runtime but enable:
- Better IDE autocompletion
- Static analysis with mypy
- Self-documenting code
- Catch bugs before they hit production

Python 3.9+ allows built-in types as generics (list[int] instead of List[int]).
Python 3.10+ adds the | union syntax (int | str instead of Union[int, str]).
"""
from __future__ import annotations

import sys
from collections.abc import Callable, Iterator, Sequence
from dataclasses import dataclass
from typing import (
    Any,
    Generic,
    Literal,
    NamedTuple,
    NewType,
    Optional,
    Protocol,
    TypeAlias,
    TypeGuard,
    TypeVar,
    overload,
    runtime_checkable,
)


# =============================================================================
# BASIC TYPE HINTS
# =============================================================================

# Variables
name: str = "Gaurav"
age: int = 30
scores: list[int] = [95, 87, 92]
config: dict[str, Any] = {"debug": True, "port": 8080}

# Functions
def greet(name: str) -> str:
    return f"Hello, {name}"

def process_items(items: list[str], limit: int = 10) -> list[str]:
    return items[:limit]

# Optional value could be None
def find_user(user_id: int) -> dict | None:  # Python 3.10+ syntax
    """Returns user dict or None if not found."""
    users = {1: {"name": "Alice"}, 2: {"name": "Bob"}}
    return users.get(user_id)

# Union types
def format_id(id: int | str) -> str:  # Python 3.10+
    return str(id).zfill(8)

# Collections
def merge_lists(a: list[int], b: list[int]) -> list[int]:
    return sorted(a + b)

def word_count(text: str) -> dict[str, int]:
    from collections import Counter
    return dict(Counter(text.lower().split()))


# =============================================================================
# TYPE ALIASES give complex types readable names
# =============================================================================

# Simple alias
JSON: TypeAlias = dict[str, Any]
Headers: TypeAlias = dict[str, str]
UserID: TypeAlias = int

# Complex nested types become readable
Matrix: TypeAlias = list[list[float]]
Callback: TypeAlias = Callable[[str, int], bool]
EventHandler: TypeAlias = Callable[[str, dict[str, Any]], None]

def make_request(url: str, headers: Headers) -> JSON:
    """Type aliases make signatures readable."""
    return {"url": url, "status": 200}

def transform_matrix(m: Matrix, fn: Callable[[float], float]) -> Matrix:
    return [[fn(cell) for cell in row] for row in m]


# =============================================================================
# NewType create distinct types from existing ones
# =============================================================================

# NewType creates types that are distinct to the type checker
# but have zero runtime overhead
UserId = NewType("UserId", int)
OrderId = NewType("OrderId", int)

def get_user(user_id: UserId) -> dict:
    """Type checker will catch if you pass OrderId here."""
    return {"id": user_id, "name": "User"}

# Usage:
# user_id = UserId(42)       # ✓
# order_id = OrderId(42)
# get_user(order_id)         # ✗ Type error! OrderId != UserId


# =============================================================================
# TypeVar AND GENERICS write type-safe generic functions
# =============================================================================

T = TypeVar("T")
K = TypeVar("K")
V = TypeVar("V")

def first(items: Sequence[T]) -> T | None:
    """Generic function works with any sequence type.

    The return type matches the element type of the input.
    """
    return items[0] if items else None

def get_or_default(mapping: dict[K, V], key: K, default: V) -> V:
    """Generic with multiple type vars."""
    return mapping.get(key, default)


# Bounded TypeVar restrict what types are allowed
from numbers import Number
Numeric = TypeVar("Numeric", int, float)  # Only int or float

def add(a: Numeric, b: Numeric) -> Numeric:
    return a + b


# Generic classes
class Stack(Generic[T]):
    """Type-safe stack Stack[int] only accepts/returns ints."""

    def __init__(self) -> None:
        self._items: list[T] = []

    def push(self, item: T) -> None:
        self._items.append(item)

    def pop(self) -> T:
        if not self._items:
            raise IndexError("Stack is empty")
        return self._items.pop()

    def peek(self) -> T | None:
        return self._items[-1] if self._items else None

    def __len__(self) -> int:
        return len(self._items)


class Result(Generic[T]):
    """Generic Result type like Rust's Result<T, E>."""

    def __init__(self, value: T | None = None, error: str | None = None):
        self._value = value
        self._error = error

    @property
    def is_ok(self) -> bool:
        return self._error is None

    @property
    def value(self) -> T:
        if self._error:
            raise ValueError(f"Result contains error: {self._error}")
        return self._value  # type: ignore

    @property
    def error(self) -> str | None:
        return self._error

    @classmethod
    def ok(cls, value: T) -> Result[T]:
        return cls(value=value)

    @classmethod
    def err(cls, error: str) -> Result[T]:
        return cls(error=error)


# =============================================================================
# PROTOCOLS structural typing (duck typing with type safety)
# =============================================================================

@runtime_checkable
class Comparable(Protocol):
    """Any object that supports < comparison."""
    def __lt__(self, other: Any) -> bool: ...

CT = TypeVar("CT", bound=Comparable)

def min_value(items: Sequence[CT]) -> CT:
    """Works with any type that supports comparison."""
    return min(items)


class Serializable(Protocol):
    """Protocol any class with these methods satisfies the type."""
    def to_dict(self) -> dict[str, Any]: ...
    def to_json(self) -> str: ...


class HasLength(Protocol):
    def __len__(self) -> int: ...


def print_length(obj: HasLength) -> None:
    """Accepts anything with __len__ lists, strings, dicts, custom classes."""
    print(f"Length: {len(obj)}")


# =============================================================================
# LITERAL restrict values to specific literals
# =============================================================================

def set_direction(direction: Literal["north", "south", "east", "west"]) -> None:
    """Only these exact string values are accepted."""
    print(f"Moving {direction}")

def create_connection(mode: Literal["r", "w", "rw"] = "r") -> None:
    """Literal is great for mode/flag parameters."""
    print(f"Connection mode: {mode}")


# =============================================================================
# TypeGuard narrow types in conditionals
# =============================================================================

def is_string_list(val: list[Any]) -> TypeGuard[list[str]]:
    """Type guard tells the type checker what a True return means.

    After `if is_string_list(x):`, x is narrowed to list[str].
    """
    return all(isinstance(item, str) for item in val)

def process(data: list[Any]) -> None:
    if is_string_list(data):
        # Type checker knows data is list[str] here
        print(", ".join(data))
    else:
        print("Not all strings")


# =============================================================================
# OVERLOAD different signatures for different input types
# =============================================================================

@overload
def parse_value(value: str) -> str: ...
@overload
def parse_value(value: int) -> int: ...
@overload
def parse_value(value: list) -> list: ...

def parse_value(value: str | int | list) -> str | int | list:
    """Overloaded function type checker knows the exact return type
    based on the input type.
    """
    if isinstance(value, str):
        return value.strip()
    elif isinstance(value, int):
        return abs(value)
    else:
        return list(value)


# =============================================================================
# NamedTuple typed tuples
# =============================================================================

class Coordinate(NamedTuple):
    """Typed, immutable, named tuple."""
    latitude: float
    longitude: float
    altitude: float = 0.0

    def distance_to(self, other: Coordinate) -> float:
        """Approximate distance in km using simple formula."""
        import math
        lat_diff = abs(self.latitude - other.latitude)
        lon_diff = abs(self.longitude - other.longitude)
        return math.sqrt(lat_diff**2 + lon_diff**2) * 111  # rough km


# =============================================================================
# CALLABLE TYPES typing functions as parameters
# =============================================================================

# Function that takes a string and returns bool
Predicate: TypeAlias = Callable[[str], bool]

def filter_strings(items: list[str], predicate: Predicate) -> list[str]:
    return [item for item in items if predicate(item)]

# Function with no args returning int
Factory: TypeAlias = Callable[[], int]

# Function with *args
AnyFunc: TypeAlias = Callable[..., Any]


# =============================================================================
# PRACTICAL EXAMPLES
# =============================================================================

@dataclass
class APIResponse(Generic[T]):
    """Generic API response wrapper used in real APIs."""
    data: T | None
    status: int
    message: str
    errors: list[str] = None  # type: ignore

    @property
    def success(self) -> bool:
        return 200 <= self.status < 300


def fetch_users() -> APIResponse[list[dict[str, Any]]]:
    """Returns a typed API response."""
    return APIResponse(
        data=[{"id": 1, "name": "Alice"}],
        status=200,
        message="OK"
    )


if __name__ == "__main__":
    print("=" * 60)
    print("Type Hints Demo")
    print("=" * 60)

    # Generics
    print("\n--- Generic Stack ---")
    int_stack: Stack[int] = Stack()
    int_stack.push(1)
    int_stack.push(2)
    int_stack.push(3)
    print(f"  Pop: {int_stack.pop()}, Peek: {int_stack.peek()}")

    # Result type
    print("\n--- Result Type ---")
    ok_result: Result[int] = Result.ok(42)
    err_result: Result[int] = Result.err("Something went wrong")
    print(f"  OK: {ok_result.value}, Error: {err_result.error}")

    # Protocol
    print("\n--- Protocols ---")
    print_length([1, 2, 3])
    print_length("hello")
    print_length({"a": 1, "b": 2})

    # NamedTuple
    print("\n--- NamedTuple ---")
    delhi = Coordinate(28.6139, 77.2090)
    mumbai = Coordinate(19.0760, 72.8777)
    print(f"  Delhi to Mumbai: ~{delhi.distance_to(mumbai):.0f} km")

    # API Response
    print("\n--- Generic API Response ---")
    response = fetch_users()
    print(f"  Status: {response.status}, Success: {response.success}")
    print(f"  Data: {response.data}")

    print(f"\n  Python version: {sys.version}")
    print("  Run 'mypy fundamentals/typing_hints.py' to type-check this file")

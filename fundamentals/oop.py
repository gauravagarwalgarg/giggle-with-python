"""
Object-Oriented Programming in Python classes, inheritance, protocols,
dataclasses, and dunder methods.

Python supports multiple paradigms, but OOP is central to its ecosystem.
This file covers practical patterns you'll use in production code.
"""
from __future__ import annotations

import math
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Protocol, runtime_checkable


# =============================================================================
# BASIC CLASSES attributes, methods, properties
# =============================================================================

class BankAccount:
    """A simple bank account demonstrating encapsulation.

    Convention: _single_underscore means "internal", __double means name-mangled.
    Python doesn't enforce private it trusts developers.
    """

    # Class variable shared across all instances
    interest_rate: float = 0.02

    def __init__(self, owner: str, balance: float = 0.0):
        """Constructor called when creating an instance."""
        self.owner = owner          # Public attribute
        self._balance = balance     # "Private by convention"
        self._transactions: list[float] = []

    @property
    def balance(self) -> float:
        """Property access like an attribute, but it's a method underneath.

        Useful for computed values or adding validation.
        """
        return self._balance

    def deposit(self, amount: float) -> None:
        """Instance method operates on self."""
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        self._balance += amount
        self._transactions.append(amount)

    def withdraw(self, amount: float) -> None:
        if amount > self._balance:
            raise ValueError("Insufficient funds")
        self._balance -= amount
        self._transactions.append(-amount)

    @classmethod
    def from_dict(cls, data: dict) -> BankAccount:
        """Class method alternative constructor.

        cls refers to the class itself, not an instance.
        """
        return cls(owner=data["owner"], balance=data.get("balance", 0.0))

    @staticmethod
    def validate_amount(amount: float) -> bool:
        """Static method doesn't access instance or class state.

        Logically belongs to the class but doesn't need self or cls.
        """
        return isinstance(amount, (int, float)) and amount > 0

    def __repr__(self) -> str:
        """Developer-friendly string representation."""
        return f"BankAccount(owner={self.owner!r}, balance={self._balance:.2f})"

    def __str__(self) -> str:
        """User-friendly string representation."""
        return f"{self.owner}'s account: ${self._balance:.2f}"


# =============================================================================
# INHERITANCE single, multiple, and mixins
# =============================================================================

class Shape(ABC):
    """Abstract base class cannot be instantiated directly.

    Forces subclasses to implement area() and perimeter().
    """

    @abstractmethod
    def area(self) -> float:
        ...

    @abstractmethod
    def perimeter(self) -> float:
        ...

    def describe(self) -> str:
        """Concrete method inherited by all subclasses."""
        return f"{self.__class__.__name__}: area={self.area():.2f}, perimeter={self.perimeter():.2f}"


class Circle(Shape):
    def __init__(self, radius: float):
        self.radius = radius

    def area(self) -> float:
        return math.pi * self.radius ** 2

    def perimeter(self) -> float:
        return 2 * math.pi * self.radius


class Rectangle(Shape):
    def __init__(self, width: float, height: float):
        self.width = width
        self.height = height

    def area(self) -> float:
        return self.width * self.height

    def perimeter(self) -> float:
        return 2 * (self.width + self.height)


class Square(Rectangle):
    """Inheritance a Square is a special Rectangle."""

    def __init__(self, side: float):
        super().__init__(side, side)  # Call parent constructor


# Mixins small classes that add behavior
class SerializableMixin:
    """Mixin that adds JSON serialization to any class."""

    def to_dict(self) -> dict:
        return {k: v for k, v in self.__dict__.items() if not k.startswith("_")}

    def to_json(self) -> str:
        import json
        return json.dumps(self.to_dict(), default=str)


class LoggableMixin:
    """Mixin that adds logging capability."""

    def log(self, message: str) -> None:
        print(f"[{self.__class__.__name__}] {message}")


class User(SerializableMixin, LoggableMixin):
    """Multiple inheritance with mixins."""

    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email


# =============================================================================
# PROTOCOLS structural typing (duck typing with type safety)
# =============================================================================

@runtime_checkable
class Drawable(Protocol):
    """Protocol any class with a draw() method satisfies this.

    No inheritance required! This is structural (duck) typing.
    """

    def draw(self) -> str:
        ...


class Canvas:
    """Accepts anything that has a draw() method no inheritance needed."""

    def render(self, items: list[Drawable]) -> None:
        for item in items:
            print(item.draw())


class Star:
    """Satisfies Drawable protocol without inheriting from it."""

    def draw(self) -> str:
        return "★"


class Heart:
    def draw(self) -> str:
        return "♥"


# =============================================================================
# DATACLASSES reduce boilerplate for data-holding classes
# =============================================================================

@dataclass
class Point:
    """Dataclass auto-generates __init__, __repr__, __eq__, and more."""
    x: float
    y: float

    def distance_to(self, other: Point) -> float:
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)


@dataclass(frozen=True)  # Immutable can be used as dict key
class Color:
    """Frozen dataclass attributes cannot be changed after creation."""
    r: int
    g: int
    b: int

    def hex(self) -> str:
        return f"#{self.r:02x}{self.g:02x}{self.b:02x}"


@dataclass
class Config:
    """Dataclass with defaults and field factories."""
    host: str = "localhost"
    port: int = 8080
    debug: bool = False
    tags: list[str] = field(default_factory=list)  # Mutable defaults need factory

    def __post_init__(self):
        """Validation after auto-generated __init__ runs."""
        if self.port < 1 or self.port > 65535:
            raise ValueError(f"Invalid port: {self.port}")


@dataclass(slots=True)  # Python 3.10+ uses __slots__ for memory efficiency
class Vector3D:
    """Slots dataclass faster attribute access, less memory."""
    x: float
    y: float
    z: float

    def magnitude(self) -> float:
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)

    def __add__(self, other: Vector3D) -> Vector3D:
        return Vector3D(self.x + other.x, self.y + other.y, self.z + other.z)


# =============================================================================
# DUNDER METHODS customize how objects behave with operators and builtins
# =============================================================================

class Matrix:
    """Demonstrate common dunder methods."""

    def __init__(self, rows: list[list[float]]):
        self.rows = rows
        self.n_rows = len(rows)
        self.n_cols = len(rows[0]) if rows else 0

    def __repr__(self) -> str:
        return f"Matrix({self.rows})"

    def __str__(self) -> str:
        return "\n".join(
            "  ".join(f"{val:6.2f}" for val in row)
            for row in self.rows
        )

    def __getitem__(self, index: tuple[int, int]) -> float:
        """Allow matrix[row, col] syntax."""
        row, col = index
        return self.rows[row][col]

    def __setitem__(self, index: tuple[int, int], value: float) -> None:
        row, col = index
        self.rows[row][col] = value

    def __len__(self) -> int:
        """Total number of elements."""
        return self.n_rows * self.n_cols

    def __add__(self, other: Matrix) -> Matrix:
        """Matrix addition with + operator."""
        if self.n_rows != other.n_rows or self.n_cols != other.n_cols:
            raise ValueError("Matrix dimensions must match")
        return Matrix([
            [self.rows[i][j] + other.rows[i][j] for j in range(self.n_cols)]
            for i in range(self.n_rows)
        ])

    def __mul__(self, scalar: float) -> Matrix:
        """Scalar multiplication with * operator."""
        return Matrix([
            [val * scalar for val in row]
            for row in self.rows
        ])

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Matrix):
            return NotImplemented
        return self.rows == other.rows

    def __contains__(self, value: float) -> bool:
        """Support 'in' operator."""
        return any(value in row for row in self.rows)

    def __iter__(self):
        """Iterate over all elements."""
        for row in self.rows:
            yield from row

    # Context manager protocol
    def __enter__(self):
        print("Matrix operations starting")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("Matrix operations complete")
        return False  # Don't suppress exceptions


# =============================================================================
# DESCRIPTORS control attribute access at the class level
# =============================================================================

class Validated:
    """Descriptor that validates values on assignment."""

    def __init__(self, min_val: float = float('-inf'), max_val: float = float('inf')):
        self.min_val = min_val
        self.max_val = max_val

    def __set_name__(self, owner, name):
        self.name = name
        self.private_name = f"_{name}"

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return getattr(obj, self.private_name, None)

    def __set__(self, obj, value):
        if not isinstance(value, (int, float)):
            raise TypeError(f"{self.name} must be a number")
        if not (self.min_val <= value <= self.max_val):
            raise ValueError(f"{self.name} must be between {self.min_val} and {self.max_val}")
        setattr(obj, self.private_name, value)


class Temperature:
    """Uses descriptors for validated attributes."""
    celsius = Validated(min_val=-273.15, max_val=1_000_000)

    def __init__(self, celsius: float):
        self.celsius = celsius  # Goes through descriptor __set__

    @property
    def fahrenheit(self) -> float:
        return self.celsius * 9 / 5 + 32


if __name__ == "__main__":
    print("=" * 60)
    print("OOP Demo")
    print("=" * 60)

    # Basic classes
    print("\n--- Bank Account ---")
    acc = BankAccount("Gaurav", 1000)
    acc.deposit(500)
    acc.withdraw(200)
    print(acc)
    print(repr(acc))

    # Inheritance
    print("\n--- Shapes (Inheritance) ---")
    shapes: list[Shape] = [Circle(5), Rectangle(4, 6), Square(3)]
    for shape in shapes:
        print(f"  {shape.describe()}")

    # Protocols
    print("\n--- Protocols (Duck Typing) ---")
    canvas = Canvas()
    canvas.render([Star(), Heart(), Star()])
    print(f"  Star satisfies Drawable? {isinstance(Star(), Drawable)}")

    # Dataclasses
    print("\n--- Dataclasses ---")
    p1 = Point(0, 0)
    p2 = Point(3, 4)
    print(f"  {p1} → {p2}: distance = {p1.distance_to(p2):.2f}")

    red = Color(255, 0, 0)
    print(f"  Red: {red} → {red.hex()}")

    v1 = Vector3D(1, 2, 3)
    v2 = Vector3D(4, 5, 6)
    print(f"  {v1} + {v2} = {v1 + v2}")

    # Dunder methods
    print("\n--- Matrix (Dunder Methods) ---")
    m = Matrix([[1, 2], [3, 4]])
    print(f"  Matrix:\n{m}")
    print(f"  m[0, 1] = {m[0, 1]}")
    print(f"  3 in m? {3 in m}")

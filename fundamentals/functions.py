"""
Functions in Python args, kwargs, decorators, generators, closures.

Functions are first-class objects in Python. You can pass them around,
return them from other functions, and assign them to variables.
"""
import functools
import time
from typing import Callable, Any


# =============================================================================
# BASIC FUNCTIONS args, kwargs, defaults
# =============================================================================

def greet(name: str, greeting: str = "Hello") -> str:
    """Positional and keyword arguments with defaults."""
    return f"{greeting}, {name}!"


def calculate_total(*items: float, tax_rate: float = 0.0) -> float:
    """*args collects positional arguments into a tuple.

    Keyword-only arguments come after *args.
    """
    subtotal = sum(items)
    return subtotal * (1 + tax_rate)


def create_user(**kwargs: Any) -> dict:
    """**kwargs collects keyword arguments into a dict.

    Useful for flexible APIs where you don't know all fields upfront.
    """
    defaults = {"role": "user", "active": True}
    return {**defaults, **kwargs}


# Forcing keyword-only arguments with bare *
def connect(host: str, port: int, *, timeout: int = 30, ssl: bool = True):
    """Arguments after * must be passed as keywords."""
    print(f"Connecting to {host}:{port} (timeout={timeout}, ssl={ssl})")


# Positional-only arguments (Python 3.8+) with /
def power(base, exp, /):
    """Arguments before / must be passed positionally."""
    return base ** exp


# =============================================================================
# DECORATORS modify function behavior without changing the function
# =============================================================================

def timer(func: Callable) -> Callable:
    """Measure execution time of a function."""
    @functools.wraps(func)  # Preserves original function metadata
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"{func.__name__} took {elapsed:.4f}s")
        return result
    return wrapper


def retry(max_attempts: int = 3, delay: float = 1.0):
    """Decorator factory a decorator that accepts arguments.

    Usage: @retry(max_attempts=5, delay=2.0)
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    print(f"Attempt {attempt}/{max_attempts} failed: {e}")
                    if attempt < max_attempts:
                        time.sleep(delay)
            raise last_exception
        return wrapper
    return decorator


def cache_result(func: Callable) -> Callable:
    """Simple memoization decorator (use functools.lru_cache in production)."""
    _cache: dict = {}

    @functools.wraps(func)
    def wrapper(*args):
        if args not in _cache:
            _cache[args] = func(*args)
        return _cache[args]

    wrapper.cache = _cache  # Expose cache for inspection
    return wrapper


def validate_types(**type_hints):
    """Decorator that validates argument types at runtime."""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Check positional args
            import inspect
            sig = inspect.signature(func)
            params = list(sig.parameters.keys())

            for i, arg in enumerate(args):
                param_name = params[i]
                if param_name in type_hints:
                    expected = type_hints[param_name]
                    if not isinstance(arg, expected):
                        raise TypeError(
                            f"{param_name} must be {expected.__name__}, "
                            f"got {type(arg).__name__}"
                        )
            return func(*args, **kwargs)
        return wrapper
    return decorator


# Stacking decorators they apply bottom-up
@timer
@cache_result
def fibonacci(n: int) -> int:
    """Calculate nth Fibonacci number recursively (cached)."""
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


# =============================================================================
# GENERATORS lazy iterators that yield values one at a time
# =============================================================================

def count_up(start: int = 0, step: int = 1):
    """Infinite counter generators can represent infinite sequences."""
    current = start
    while True:
        yield current
        current += step


def read_large_file(filepath: str, chunk_size: int = 1024):
    """Memory-efficient file reading doesn't load entire file into memory.

    This is why generators exist: processing data larger than RAM.
    """
    with open(filepath) as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            yield chunk


def fibonacci_gen():
    """Generate Fibonacci numbers lazily."""
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b


# Generator expressions like list comprehensions but lazy
def sum_of_squares_lazy(n: int) -> int:
    """Generator expression avoids creating a list in memory."""
    return sum(x**2 for x in range(n))


# =============================================================================
# CLOSURES functions that capture their enclosing scope
# =============================================================================

def make_multiplier(factor: float) -> Callable[[float], float]:
    """Closure the returned function 'remembers' factor.

    The inner function has access to variables from the outer function
    even after the outer function has returned.
    """
    def multiplier(x: float) -> float:
        return x * factor
    return multiplier


def make_counter(initial: int = 0) -> dict[str, Callable]:
    """Closure with mutable state like a lightweight object."""
    count = initial

    def increment():
        nonlocal count  # Required to modify closure variable
        count += 1
        return count

    def decrement():
        nonlocal count
        count -= 1
        return count

    def get():
        return count

    return {"increment": increment, "decrement": decrement, "get": get}


def make_logger(prefix: str) -> Callable:
    """Factory pattern using closures."""
    def log(message: str):
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] {prefix}: {message}")
    return log


# =============================================================================
# HIGHER-ORDER FUNCTIONS functions that take/return functions
# =============================================================================

def apply_operation(items: list, operation: Callable) -> list:
    """Accept a function as an argument."""
    return [operation(item) for item in items]


def compose(*functions: Callable) -> Callable:
    """Compose multiple functions: compose(f, g, h)(x) == f(g(h(x)))."""
    def composed(x):
        result = x
        for func in reversed(functions):
            result = func(result)
        return result
    return composed


# Built-in higher-order functions
def demonstrate_builtins():
    """map, filter, reduce but prefer comprehensions in most cases."""
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    # map transform each element
    doubled = list(map(lambda x: x * 2, numbers))

    # filter keep elements that pass a test
    evens = list(filter(lambda x: x % 2 == 0, numbers))

    # reduce fold a sequence into a single value
    from functools import reduce
    product = reduce(lambda a, b: a * b, numbers)

    # Pythonic alternatives (preferred):
    doubled_py = [x * 2 for x in numbers]
    evens_py = [x for x in numbers if x % 2 == 0]

    return doubled, evens, product


# =============================================================================
# LAMBDA anonymous single-expression functions
# =============================================================================

# Good: short callbacks for sort/map/filter
points = [(1, 5), (3, 2), (7, 1)]
sorted_by_y = sorted(points, key=lambda p: p[1])

# Bad: don't assign lambdas to variables use def instead
# square = lambda x: x**2  # ← Don't do this
def square(x): return x**2   # ← Do this instead


if __name__ == "__main__":
    print("=" * 60)
    print("Functions Demo")
    print("=" * 60)

    # Basic functions
    print("\n--- Args & Kwargs ---")
    print(greet("Python"))
    print(f"Total: ${calculate_total(10.0, 20.0, 30.0, tax_rate=0.08):.2f}")
    print(create_user(name="Gaurav", email="g@example.com"))

    # Decorators
    print("\n--- Decorators ---")
    result = fibonacci(30)
    print(f"fibonacci(30) = {result}")

    # Generators
    print("\n--- Generators ---")
    counter = count_up(0, 5)
    first_five = [next(counter) for _ in range(5)]
    print(f"Count by 5: {first_five}")

    fib = fibonacci_gen()
    first_ten_fib = [next(fib) for _ in range(10)]
    print(f"First 10 Fibonacci: {first_ten_fib}")

    # Closures
    print("\n--- Closures ---")
    double = make_multiplier(2)
    triple = make_multiplier(3)
    print(f"double(5) = {double(5)}, triple(5) = {triple(5)}")

    counter = make_counter()
    counter["increment"]()
    counter["increment"]()
    counter["increment"]()
    print(f"Counter: {counter['get']()}")

    # Composition
    print("\n--- Composition ---")
    add_one = lambda x: x + 1
    double_it = lambda x: x * 2
    transform = compose(str, double_it, add_one)
    print(f"compose(str, double, add_one)(5) = {transform(5)}")

"""
Control Flow in Python if/else, for, while, match/case (3.10+).

Python uses indentation instead of braces, making control flow
visually clean. This file covers all the flow control mechanisms.
"""


# =============================================================================
# IF / ELIF / ELSE
# =============================================================================

score = 85

# Standard if/elif/else
if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
elif score >= 70:
    grade = "C"
else:
    grade = "F"

# Ternary (conditional expression) for simple cases
status = "pass" if score >= 60 else "fail"

# Truthy/Falsy values:
# Falsy: None, 0, 0.0, "", [], {}, set(), False
# Everything else is truthy
items = []
if not items:
    print("List is empty")

# Walrus operator (:=) assign and test in one expression (Python 3.8+)
data = [1, 2, 3, 4, 5, 6, 7, 8]
if (n := len(data)) > 5:
    print(f"List has {n} elements, that's too many")


# =============================================================================
# FOR LOOPS
# =============================================================================

# Iterate over any iterable
fruits = ["apple", "banana", "cherry"]
for fruit in fruits:
    print(fruit)

# enumerate when you need both index and value
for i, fruit in enumerate(fruits, start=1):
    print(f"{i}. {fruit}")

# zip iterate over multiple sequences in parallel
names = ["Alice", "Bob", "Charlie"]
scores = [85, 92, 78]
for name, score in zip(names, scores):
    print(f"{name}: {score}")

# range generate numeric sequences
for i in range(5):          # 0, 1, 2, 3, 4
    pass
for i in range(2, 10, 2):  # 2, 4, 6, 8 (start, stop, step)
    pass

# Dictionary iteration
config = {"host": "localhost", "port": 8080, "debug": True}
for key, value in config.items():
    print(f"{key} = {value}")

# for...else the else runs if loop completes WITHOUT break
def find_prime(numbers):
    """Demonstrate for...else pattern."""
    for n in numbers:
        if n > 1 and all(n % i != 0 for i in range(2, int(n**0.5) + 1)):
            print(f"Found prime: {n}")
            break
    else:
        print("No primes found")


# =============================================================================
# WHILE LOOPS
# =============================================================================

# Basic while
count = 0
while count < 5:
    print(count)
    count += 1

# while with break and continue
import random

def guess_number():
    """Simple number guessing game to demonstrate while loop."""
    target = random.randint(1, 10)
    attempts = 0

    while True:  # Infinite loop use break to exit
        attempts += 1
        guess = random.randint(1, 10)  # Simulating a guess

        if guess == target:
            print(f"Got it in {attempts} attempts!")
            break

        if attempts > 20:
            print("Too many attempts, giving up")
            break

        continue  # Explicitly continue (usually implicit)


# =============================================================================
# MATCH / CASE Structural Pattern Matching (Python 3.10+)
# =============================================================================

def handle_command(command: str) -> str:
    """Demonstrate match/case Python's answer to switch statements.

    But much more powerful it does structural pattern matching.
    """
    match command.split():
        case ["quit"]:
            return "Goodbye!"
        case ["hello", name]:
            return f"Hello, {name}!"
        case ["add", *numbers]:
            return str(sum(int(n) for n in numbers))
        case _:
            return f"Unknown command: {command}"


def classify_point(point):
    """Match on structure much more powerful than switch."""
    match point:
        case (0, 0):
            return "Origin"
        case (x, 0):
            return f"On x-axis at x={x}"
        case (0, y):
            return f"On y-axis at y={y}"
        case (x, y) if x == y:
            return f"On diagonal at ({x}, {y})"
        case (x, y):
            return f"Point at ({x}, {y})"


def handle_response(response: dict):
    """Match on dict structure useful for API responses."""
    match response:
        case {"status": 200, "data": data}:
            return f"Success: {data}"
        case {"status": 404}:
            return "Not found"
        case {"status": status, "error": msg}:
            return f"Error {status}: {msg}"
        case _:
            return "Unknown response format"


# =============================================================================
# COMPREHENSIONS Pythonic loops that create collections
# =============================================================================

# List comprehension
squares = [x**2 for x in range(10) if x % 2 == 0]

# Dict comprehension
word_lengths = {word: len(word) for word in ["hello", "world", "python"]}

# Set comprehension
unique_lengths = {len(word) for word in ["hi", "hey", "hello", "howdy"]}

# Generator expression (lazy memory efficient for large data)
total = sum(x**2 for x in range(1_000_000))


# =============================================================================
# EXCEPTION HANDLING
# =============================================================================

def safe_divide(a: float, b: float) -> float | None:
    """Demonstrate try/except/else/finally."""
    try:
        result = a / b
    except ZeroDivisionError:
        print("Cannot divide by zero")
        return None
    except TypeError as e:
        print(f"Type error: {e}")
        return None
    else:
        # Runs only if no exception was raised
        print(f"{a} / {b} = {result}")
        return result
    finally:
        # Always runs good for cleanup
        print("Division operation complete")


# Context managers the Pythonic way to handle resources
def read_config(path: str) -> dict:
    """with statement guarantees cleanup even if exceptions occur."""
    try:
        with open(path) as f:
            import json
            return json.load(f)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        return {}


if __name__ == "__main__":
    print("=" * 60)
    print("Control Flow Demo")
    print("=" * 60)

    # Match/case demos (Python 3.10+)
    print("\n--- Match/Case ---")
    commands = ["hello World", "add 1 2 3", "quit", "unknown stuff"]
    for cmd in commands:
        print(f"  '{cmd}' → {handle_command(cmd)}")

    print("\n--- Point Classification ---")
    points = [(0, 0), (5, 0), (0, 3), (4, 4), (2, 7)]
    for p in points:
        print(f"  {p} → {classify_point(p)}")

    print("\n--- Response Handling ---")
    responses = [
        {"status": 200, "data": [1, 2, 3]},
        {"status": 404},
        {"status": 500, "error": "Internal server error"},
    ]
    for resp in responses:
        print(f"  {resp} → {handle_response(resp)}")

    print("\n--- Safe Division ---")
    safe_divide(10, 3)
    safe_divide(10, 0)

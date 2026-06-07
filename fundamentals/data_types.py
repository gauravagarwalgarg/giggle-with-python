"""
Data Types in Python str, int, float, list, dict, set, tuple with practical examples.

Python is dynamically typed, but understanding the type system deeply
helps write more robust code. This file covers the built-in types
you'll use every day.
"""


# =============================================================================
# STRINGS immutable sequences of Unicode characters
# =============================================================================

name = "Gaurav"
multiline = """This is a
multiline string"""

# f-strings (Python 3.6+) the preferred way to format
greeting = f"Hello, {name}! Your name has {len(name)} characters."

# Useful string methods (strings are immutable these return new strings)
text = "  Hello, World!  "
print(text.strip())          # "Hello, World!" remove whitespace
print(text.lower())          # "  hello, world!  "
print(text.replace("World", "Python"))
print("Hello".startswith("He"))  # True
print(",".join(["a", "b", "c"]))  # "a,b,c"

# Raw strings useful for regex and Windows paths
path = r"C:\Users\name\file.txt"  # backslashes are literal


# =============================================================================
# NUMBERS int, float, complex
# =============================================================================

integer = 42
big_int = 1_000_000_000  # underscores for readability (Python 3.6+)
floating = 3.14159
scientific = 1.5e-10
complex_num = 3 + 4j

# Integer division vs true division
print(7 / 2)   # 3.5 (true division)
print(7 // 2)  # 3   (floor division)
print(7 % 2)   # 1   (modulo)
print(2 ** 10) # 1024 (power)

# Type conversions
print(int("42"))       # 42
print(float("3.14"))   # 3.14
print(str(42))         # "42"


# =============================================================================
# LISTS mutable, ordered sequences
# =============================================================================

fruits = ["apple", "banana", "cherry"]
numbers = list(range(1, 11))  # [1, 2, 3, ..., 10]

# Common operations
fruits.append("date")          # Add to end
fruits.insert(0, "avocado")   # Insert at index
fruits.extend(["elderberry"])  # Add multiple items
removed = fruits.pop()         # Remove and return last item

# List comprehensions Pythonic way to transform/filter
squares = [x**2 for x in range(10)]
evens = [x for x in range(20) if x % 2 == 0]
matrix_flat = [cell for row in [[1,2],[3,4],[5,6]] for cell in row]

# Slicing [start:stop:step]
nums = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
print(nums[2:5])    # [2, 3, 4]
print(nums[::2])    # [0, 2, 4, 6, 8] every 2nd element
print(nums[::-1])   # [9, 8, 7, ...] reversed

# Sorting
words = ["banana", "apple", "cherry"]
words.sort()                    # In-place sort
sorted_words = sorted(words, key=len)  # New list, sorted by length


# =============================================================================
# TUPLES immutable, ordered sequences
# =============================================================================

# Use tuples for fixed collections (coordinates, RGB, return values)
point = (3, 4)
rgb = (255, 128, 0)

# Named tuples self-documenting tuples
from collections import namedtuple
Color = namedtuple("Color", ["red", "green", "blue"])
white = Color(255, 255, 255)
print(white.red)  # 255

# Tuple unpacking
x, y = point
first, *rest = [1, 2, 3, 4, 5]  # first=1, rest=[2,3,4,5]


# =============================================================================
# DICTIONARIES mutable, key-value mappings (ordered since Python 3.7)
# =============================================================================

person = {
    "name": "Gaurav",
    "age": 30,
    "skills": ["Python", "Django", "AWS"],
}

# Access and mutation
print(person["name"])                    # KeyError if missing
print(person.get("email", "N/A"))       # Safe access with default

person["email"] = "gaurav@example.com"  # Add/update
del person["age"]                        # Remove key

# Useful methods
print(person.keys())    # dict_keys([...])
print(person.values())  # dict_values([...])
print(person.items())   # dict_items([(k, v), ...])

# Dict comprehension
squares_dict = {x: x**2 for x in range(6)}
# {0: 0, 1: 1, 2: 4, 3: 9, 4: 16, 5: 25}

# Merging dicts (Python 3.9+)
defaults = {"theme": "dark", "lang": "en"}
overrides = {"lang": "fr", "font_size": 14}
merged = defaults | overrides  # {'theme': 'dark', 'lang': 'fr', 'font_size': 14}


# =============================================================================
# SETS mutable, unordered collections of unique elements
# =============================================================================

primes = {2, 3, 5, 7, 11}
evens_set = {2, 4, 6, 8, 10}

# Set operations great for membership testing and deduplication
print(primes & evens_set)   # Intersection: {2}
print(primes | evens_set)   # Union: {2, 3, 4, 5, 6, 7, 8, 10, 11}
print(primes - evens_set)   # Difference: {3, 5, 7, 11}
print(primes ^ evens_set)   # Symmetric difference

# Membership testing is O(1) much faster than lists for large collections
print(7 in primes)  # True

# Deduplicate a list
dupes = [1, 2, 2, 3, 3, 3]
unique = list(set(dupes))  # [1, 2, 3] order not guaranteed

# frozenset immutable set (can be used as dict key or in another set)
immutable_set = frozenset([1, 2, 3])


# =============================================================================
# NONE Python's null/nil equivalent
# =============================================================================

result = None

# Always use `is` for None comparison, not ==
if result is None:
    print("No result yet")


# =============================================================================
# TYPE CHECKING AT RUNTIME
# =============================================================================

print(type(42))           # <class 'int'>
print(isinstance(42, int))  # True
print(isinstance(42, (int, float)))  # True check multiple types


if __name__ == "__main__":
    print("=" * 60)
    print("Python Data Types Demo")
    print("=" * 60)

    # Demonstrate each type
    demo_data = {
        "string": f"Hello, {name}",
        "integer": big_int,
        "float": floating,
        "list": fruits[:3],
        "tuple": point,
        "dict": {"key": "value"},
        "set": primes,
        "None": None,
    }

    for type_name, value in demo_data.items():
        print(f"  {type_name:10} → {value!r:40} (type: {type(value).__name__})")

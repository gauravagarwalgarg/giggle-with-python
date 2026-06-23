"""
Comprehensions and Generators compact, readable data transformations.

Python's comprehension syntax is one of its most powerful features.
It replaces verbose loops with concise, readable expressions.

Adapted from code_snippets/List_Comp and code_snippets/Generators.
"""
from typing import Generator


# =============================================================================
# LIST COMPREHENSIONS create lists from iterables
# =============================================================================

def list_comprehension_basics():
    """Core list comprehension patterns.

    Syntax: [expression for item in iterable if condition]
    """
    nums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    # Basic: transform each element
    squares = [n * n for n in nums]
    # [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]

    # Filter: only include elements that pass a condition
    evens = [n for n in nums if n % 2 == 0]
    # [2, 4, 6, 8, 10]

    # Transform + filter
    even_squares = [n * n for n in nums if n % 2 == 0]
    # [4, 16, 36, 64, 100]

    # Nested loops: cartesian product
    pairs = [(letter, num) for letter in "abcd" for num in range(4)]
    # [('a', 0), ('a', 1), ..., ('d', 3)]

    # Flatten a 2D list
    matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    flat = [x for row in matrix for x in row]
    # [1, 2, 3, 4, 5, 6, 7, 8, 9]

    # Conditional expression (ternary) in comprehension
    labels = ["even" if n % 2 == 0 else "odd" for n in nums]

    return squares, evens, even_squares, pairs, flat, labels


# =============================================================================
# DICT COMPREHENSIONS create dicts from iterables
# =============================================================================

def dict_comprehension_patterns():
    """Dict comprehension patterns.

    Syntax: {key_expr: value_expr for item in iterable if condition}
    """
    names = ["Bruce", "Clark", "Peter", "Logan", "Wade"]
    heroes = ["Batman", "Superman", "Spiderman", "Wolverine", "Deadpool"]

    # Zip two lists into a dict
    hero_map = {name: hero for name, hero in zip(names, heroes)}
    # {'Bruce': 'Batman', 'Clark': 'Superman', ...}

    # Filter while creating
    long_names = {name: hero for name, hero in zip(names, heroes) if len(name) > 4}

    # Invert a dict (swap keys and values)
    inverted = {hero: name for name, hero in hero_map.items()}

    # Word frequency counter
    sentence = "the cat sat on the mat the cat"
    word_count = {}
    for word in sentence.split():
        word_count[word] = word_count.get(word, 0) + 1
    # Comprehension equivalent (using collections.Counter is better):
    words = sentence.split()
    word_freq = {word: words.count(word) for word in set(words)}

    # Transform values
    prices = {"apple": 1.20, "banana": 0.50, "cherry": 2.00}
    discounted = {item: round(price * 0.9, 2) for item, price in prices.items()}

    return hero_map, long_names, inverted, word_freq, discounted


# =============================================================================
# SET COMPREHENSIONS create sets (unique values)
# =============================================================================

def set_comprehension_patterns():
    """Set comprehension patterns.

    Syntax: {expression for item in iterable if condition}
    """
    nums = [1, 1, 2, 1, 3, 4, 3, 4, 5, 5, 6, 7, 8, 7, 9, 9]

    # Deduplicate
    unique = {n for n in nums}
    # {1, 2, 3, 4, 5, 6, 7, 8, 9}

    # Unique word lengths
    words = ["hello", "world", "hi", "hey", "howdy"]
    lengths = {len(w) for w in words}
    # {2, 3, 5}

    # Find common characters
    str1 = "hello"
    str2 = "world"
    common = {c for c in str1 if c in str2}
    # {'l', 'o'}

    return unique, lengths, common


# =============================================================================
# GENERATOR EXPRESSIONS lazy, memory-efficient iteration
# =============================================================================

def generator_expression_patterns():
    """Generator expressions like list comprehensions but lazy.

    They don't build the entire list in memory. Values are produced
    on demand, one at a time. Critical for large datasets.

    Syntax: (expression for item in iterable if condition)
    """
    # Generator expression uses parentheses instead of brackets
    squares_gen = (x * x for x in range(1_000_000))
    # No memory allocated for 1M items!

    # Works directly with functions that accept iterables
    total = sum(x * x for x in range(1_000_000))  # Efficient

    # Compare memory usage:
    # list_version = [x * x for x in range(1_000_000)]  # ~8 MB in memory
    # gen_version = (x * x for x in range(1_000_000))    # ~100 bytes

    # Can only iterate once
    first_ten = (x * x for x in range(10))
    consumed = list(first_ten)  # [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]
    empty = list(first_ten)     # [] - already exhausted

    # Chaining operations (lazy pipeline)
    import os
    # Find all .py files and get their sizes (lazy):
    # py_sizes = (
    #     os.path.getsize(f)
    #     for f in os.listdir(".")
    #     if f.endswith(".py")
    # )

    return total, consumed


# =============================================================================
# GENERATOR FUNCTIONS yield values one at a time
# =============================================================================

def fibonacci() -> Generator[int, None, None]:
    """Infinite Fibonacci generator.

    yield pauses the function and returns a value. The function
    resumes where it left off on the next next() call.
    """
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b


def read_chunks(filepath: str, chunk_size: int = 4096) -> Generator[str, None, None]:
    """Read a file in chunks without loading it all into memory.

    This is the primary use case for generators: streaming large data.
    """
    with open(filepath) as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            yield chunk


def countdown(n: int) -> Generator[int, None, None]:
    """Simple countdown generator."""
    while n > 0:
        yield n
        n -= 1


def people_generator(num_people: int) -> Generator[dict, None, None]:
    """Generate person records without storing all in memory.

    Adapted from code_snippets/Generators/people.py.
    For 1M records, this uses constant memory vs a list using ~1GB.
    """
    import random
    names = ["John", "Corey", "Adam", "Steve", "Rick", "Thomas"]
    majors = ["Math", "Engineering", "CompSci", "Arts", "Business"]

    for i in range(num_people):
        yield {
            "id": i,
            "name": random.choice(names),
            "major": random.choice(majors),
        }


# =============================================================================
# ADVANCED: send() and generator pipelines
# =============================================================================

def running_average() -> Generator[float, float, None]:
    """Generator that accepts values via send() and yields running average."""
    total = 0.0
    count = 0
    average = 0.0
    while True:
        value = yield average
        total += value
        count += 1
        average = total / count


def pipeline_example():
    """Chain generators into a processing pipeline.

    Each stage processes items lazily no intermediate lists created.
    """
    # Stage 1: generate numbers
    numbers = (x for x in range(100))

    # Stage 2: filter evens
    evens = (x for x in numbers if x % 2 == 0)

    # Stage 3: square them
    squared = (x * x for x in evens)

    # Stage 4: take first 10
    from itertools import islice
    result = list(islice(squared, 10))

    return result  # [0, 4, 16, 36, 64, 100, 144, 196, 256, 324]


# =============================================================================
# COMPARISON: loop vs comprehension vs map/filter
# =============================================================================

def comparison_demo():
    """Same operation expressed three ways.

    Comprehensions are preferred in Python idiomatic, readable, fast.
    Use map/filter only when you already have a named function.
    """
    nums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    # GOAL: Get squares of even numbers

    # 1. Traditional loop (verbose but clear)
    result_loop = []
    for n in nums:
        if n % 2 == 0:
            result_loop.append(n * n)

    # 2. List comprehension (Pythonic preferred)
    result_comp = [n * n for n in nums if n % 2 == 0]

    # 3. map + filter (functional style)
    result_func = list(map(lambda n: n * n, filter(lambda n: n % 2 == 0, nums)))

    assert result_loop == result_comp == result_func
    return result_comp


if __name__ == "__main__":
    print("=" * 60)
    print("Comprehensions & Generators Demo")
    print("=" * 60)

    # List comprehensions
    print("\n--- List Comprehensions ---")
    squares, evens, even_sq, pairs, flat, labels = list_comprehension_basics()
    print(f"  Squares:      {squares[:5]}...")
    print(f"  Evens:        {evens}")
    print(f"  Even squares: {even_sq}")
    print(f"  Flattened:    {flat}")

    # Dict comprehensions
    print("\n--- Dict Comprehensions ---")
    hero_map, long_names, inverted, word_freq, discounted = dict_comprehension_patterns()
    print(f"  Hero map:   {hero_map}")
    print(f"  Long names: {long_names}")
    print(f"  Word freq:  {word_freq}")
    print(f"  Discounted: {discounted}")

    # Set comprehensions
    print("\n--- Set Comprehensions ---")
    unique, lengths, common = set_comprehension_patterns()
    print(f"  Unique nums:   {sorted(unique)}")
    print(f"  Word lengths:  {lengths}")
    print(f"  Common chars:  {common}")

    # Generator expressions
    print("\n--- Generator Expressions ---")
    total, consumed = generator_expression_patterns()
    print(f"  Sum of squares (0..999999): {total}")
    print(f"  First 10 squares: {consumed}")

    # Generator functions
    print("\n--- Generator Functions ---")
    fib = fibonacci()
    first_ten = [next(fib) for _ in range(10)]
    print(f"  Fibonacci(10): {first_ten}")

    # Pipeline
    print("\n--- Generator Pipeline ---")
    piped = pipeline_example()
    print(f"  Pipeline result: {piped}")

    # Running average with send()
    print("\n--- Running Average (send) ---")
    avg = running_average()
    next(avg)  # Prime the generator
    for value in [10, 20, 30, 40, 50]:
        result = avg.send(value)
        print(f"  Sent {value}, avg = {result:.1f}")

    # People generator (memory efficient)
    print("\n--- People Generator ---")
    people = people_generator(1_000_000)
    first_three = [next(people) for _ in range(3)]
    for p in first_three:
        print(f"  {p}")
    print("  ... (997,997 more generated lazily)")

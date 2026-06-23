"""
Scope, Namespaces, and Pythonic Patterns LEGB rule, EAFP, duck typing.

Understanding scope resolution is critical for debugging name errors
and writing correct closures. This file also covers idiomatic Python
patterns that trip up developers coming from other languages.

Adapted from code_snippets/Scope and code_snippets/EAFP.
"""


# =============================================================================
# LEGB RULE Local, Enclosing, Global, Built-in
# =============================================================================

# When Python encounters a name, it searches in this order:
# 1. Local:     inside the current function
# 2. Enclosing: in any enclosing function (for nested functions)
# 3. Global:    module-level
# 4. Built-in:  Python's built-in names (len, print, etc.)

x = "global x"


def demonstrate_legb():
    """Show how scope resolution works at each level.

    Adapted from code_snippets/Scope/scope.py.
    """
    print("\n--- LEGB Scope Demo ---")

    # Global scope
    print(f"  Global: {x}")

    def outer():
        x = "outer x"  # Enclosing scope for inner()

        def inner():
            x = "inner x"  # Local scope
            print(f"  Inner (local): {x}")

        inner()
        print(f"  Outer (enclosing): {x}")

    outer()
    print(f"  Module (global): {x}")


# =============================================================================
# MODIFYING SCOPE with global and nonlocal
# =============================================================================

counter = 0


def increment_global():
    """Use 'global' to modify a module-level variable.

    Generally avoid this prefer passing values and returning results.
    """
    global counter
    counter += 1
    return counter


def make_counter(start: int = 0):
    """Use 'nonlocal' to modify an enclosing scope variable.

    This is a closure the returned function remembers count.
    """
    count = start

    def increment():
        nonlocal count  # Without this, assignment creates a new local
        count += 1
        return count

    def get():
        return count  # Reading doesn't need nonlocal

    return increment, get


# =============================================================================
# SCOPE PITFALLS
# =============================================================================

def scope_pitfall_1():
    """UnboundLocalError: assignment makes name local to entire function.

    If you assign to a name ANYWHERE in a function, Python treats it
    as local for the ENTIRE function, even before the assignment.
    """
    # This would raise UnboundLocalError:
    # x = 10
    # def broken():
    #     print(x)  # UnboundLocalError! Python sees x = below
    #     x = 20    # This makes x local to the entire function
    pass


def scope_pitfall_2():
    """Loop variables leak into the enclosing scope in Python.

    Adapted from code_snippets/Scope/scope.py loop variable behavior.
    """
    for i in range(5):
        pass
    # i is still accessible here and equals 4!
    print(f"  Loop variable after loop: i = {i}")  # 4


def scope_pitfall_3_closures():
    """Late binding closure pitfall.

    All closures share the same variable only the last value sticks.
    """
    # Bug: all functions return 4 (the final value of i)
    functions_buggy = [lambda: i for i in range(5)]
    results_buggy = [f() for f in functions_buggy]
    # [4, 4, 4, 4, 4] ← not what you'd expect!

    # Fix: capture the value at creation time with a default argument
    functions_fixed = [lambda i=i: i for i in range(5)]
    results_fixed = [f() for f in functions_fixed]
    # [0, 1, 2, 3, 4] ← correct!

    return results_buggy, results_fixed


# =============================================================================
# EAFP Easier to Ask Forgiveness than Permission
# =============================================================================

# Python idiom: try it and handle failure, rather than checking first.
# Contrast with LBYL (Look Before You Leap) common in other languages.


def eafp_file_read(filename: str) -> str:
    """EAFP: try to open, handle failure.

    Adapted from code_snippets/EAFP/eafp.py.
    """
    # EAFP (Pythonic)
    try:
        with open(filename) as f:
            return f.read()
    except FileNotFoundError:
        return ""

    # LBYL (non-Pythonic, has race condition)
    # if os.path.exists(filename):
    #     with open(filename) as f:
    #         return f.read()
    # return ""


def eafp_dict_access(data: dict, key: str, default=None):
    """EAFP: try to access key, handle KeyError."""
    # EAFP (Pythonic)
    try:
        return data[key]
    except KeyError:
        return default

    # LBYL (non-Pythonic)
    # if key in data:
    #     return data[key]
    # return default

    # Best: use dict.get() which does this internally
    # return data.get(key, default)


def eafp_type_conversion(value: str) -> int | None:
    """EAFP: try to convert, handle failure."""
    # EAFP (Pythonic)
    try:
        return int(value)
    except (ValueError, TypeError):
        return None

    # LBYL (non-Pythonic, incomplete)
    # if isinstance(value, str) and value.isdigit():
    #     return int(value)
    # return None


# =============================================================================
# DUCK TYPING "If it walks like a duck..."
# =============================================================================

class Duck:
    """Adapted from code_snippets/EAFP/eafp.py."""

    def quack(self):
        print("Quack, quack!")

    def fly(self):
        print("Flap, flap!")


class Person:
    """Person can quack and fly too duck typing doesn't care about the class."""

    def quack(self):
        print("I'm quacking like a duck!")

    def fly(self):
        print("I'm flapping my arms!")


def quack_and_fly(thing):
    """Accept anything with quack() and fly() methods.

    Duck typing: we don't check the type, we check the behavior.
    EAFP: try it and handle AttributeError if methods don't exist.
    """
    # Pythonic (EAFP + duck typing)
    try:
        thing.quack()
        thing.fly()
    except AttributeError as e:
        print(f"Object can't do that: {e}")

    # Non-Pythonic (checking type explicitly)
    # if isinstance(thing, Duck):
    #     thing.quack()
    #     thing.fly()

    # Non-Pythonic (LBYL with hasattr)
    # if hasattr(thing, 'quack') and hasattr(thing, 'fly'):
    #     thing.quack()
    #     thing.fly()


# =============================================================================
# NAMESPACE INSPECTION
# =============================================================================

def inspect_namespaces():
    """Show what's available in different scopes."""
    local_var = "I'm local"

    print("\n--- Namespace Inspection ---")
    print(f"  Local vars: {list(locals().keys())}")
    print(f"  Global var count: {len(globals())}")

    # dir() without arguments shows current scope
    # dir(object) shows object's attributes
    print(f"  Built-in names (sample): {dir(__builtins__)[:5]}...")


# =============================================================================
# PRACTICAL: name shadowing warnings
# =============================================================================

def demonstrate_shadowing():
    """Common mistakes: accidentally shadowing built-in names."""

    # DON'T shadow built-ins:
    # list = [1, 2, 3]      # ← Shadows built-in list()!
    # dict = {"a": 1}       # ← Shadows built-in dict()!
    # id = 42               # ← Shadows built-in id()!
    # type = "string"       # ← Shadows built-in type()!
    # input = "data"        # ← Shadows built-in input()!

    # DO use descriptive names:
    items = [1, 2, 3]
    config = {"a": 1}
    user_id = 42
    item_type = "string"
    user_input = "data"

    return items, config, user_id, item_type, user_input


if __name__ == "__main__":
    print("=" * 60)
    print("Scope, Namespaces & Pythonic Patterns")
    print("=" * 60)

    # LEGB demo
    demonstrate_legb()

    # Nonlocal counter
    print("\n--- Closure Counter (nonlocal) ---")
    inc, get = make_counter(10)
    inc()
    inc()
    inc()
    print(f"  Counter after 3 increments from 10: {get()}")

    # Scope pitfalls
    print("\n--- Scope Pitfalls ---")
    scope_pitfall_2()
    buggy, fixed = scope_pitfall_3_closures()
    print(f"  Late binding bug: {buggy}")
    print(f"  Fixed with default: {fixed}")

    # Duck typing
    print("\n--- Duck Typing (EAFP) ---")
    print("  Duck:")
    quack_and_fly(Duck())
    print("  Person:")
    quack_and_fly(Person())
    print("  String (will fail gracefully):")
    quack_and_fly("not a duck")

    # EAFP patterns
    print("\n--- EAFP Patterns ---")
    content = eafp_file_read("nonexistent.txt")
    print(f"  File read (missing): {content!r}")
    num = eafp_type_conversion("42")
    print(f"  Convert '42': {num}")
    num = eafp_type_conversion("not a number")
    print(f"  Convert 'not a number': {num}")

    # Namespace inspection
    inspect_namespaces()

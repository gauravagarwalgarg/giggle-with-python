"""
NumPy Basics arrays, broadcasting, linear algebra, random.

NumPy is the foundation of scientific Python. It provides fast,
vectorized operations on arrays 10-100x faster than Python lists.
"""
import numpy as np


# =============================================================================
# ARRAY CREATION
# =============================================================================

def array_creation():
    """Different ways to create NumPy arrays."""
    # From Python lists
    a = np.array([1, 2, 3, 4, 5])
    matrix = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

    # Built-in constructors
    zeros = np.zeros((3, 4))           # 3x4 matrix of zeros
    ones = np.ones((2, 3))             # 2x3 matrix of ones
    full = np.full((3, 3), 7)          # 3x3 matrix filled with 7
    identity = np.eye(4)               # 4x4 identity matrix

    # Ranges
    seq = np.arange(0, 10, 0.5)        # Like range() but with floats
    linspace = np.linspace(0, 1, 11)   # 11 evenly spaced points from 0 to 1
    logspace = np.logspace(0, 3, 4)    # Log-spaced: [1, 10, 100, 1000]

    # Data types
    ints = np.array([1, 2, 3], dtype=np.int32)
    floats = np.array([1, 2, 3], dtype=np.float64)
    complex_arr = np.array([1+2j, 3+4j])

    print(f"Array: {a}, shape: {a.shape}, dtype: {a.dtype}")
    print(f"Matrix:\n{matrix}")
    print(f"Linspace: {linspace}")

    return matrix


# =============================================================================
# ARRAY OPERATIONS vectorized (fast!)
# =============================================================================

def array_operations():
    """Vectorized operations no loops needed."""
    a = np.array([1, 2, 3, 4, 5])
    b = np.array([10, 20, 30, 40, 50])

    # Element-wise arithmetic
    print(f"a + b = {a + b}")
    print(f"a * b = {a * b}")
    print(f"a ** 2 = {a ** 2}")
    print(f"np.sqrt(a) = {np.sqrt(a)}")

    # Comparison (returns boolean array)
    print(f"a > 3: {a > 3}")
    print(f"a[a > 3]: {a[a > 3]}")  # Boolean indexing

    # Aggregations
    print(f"sum={a.sum()}, mean={a.mean():.2f}, std={a.std():.2f}")
    print(f"min={a.min()}, max={a.max()}, argmax={a.argmax()}")

    # Matrix operations
    m = np.array([[1, 2], [3, 4]])
    print(f"\nMatrix:\n{m}")
    print(f"Transpose:\n{m.T}")
    print(f"Sum along axis 0 (columns): {m.sum(axis=0)}")
    print(f"Sum along axis 1 (rows): {m.sum(axis=1)}")


# =============================================================================
# INDEXING AND SLICING
# =============================================================================

def indexing():
    """Accessing elements similar to Python lists but more powerful."""
    a = np.arange(10)  # [0, 1, 2, ..., 9]
    m = np.arange(12).reshape(3, 4)  # 3x4 matrix

    # Basic slicing (same as Python)
    print(f"a[2:5] = {a[2:5]}")
    print(f"a[::2] = {a[::2]}")      # Every other element
    print(f"a[::-1] = {a[::-1]}")    # Reversed

    # 2D slicing
    print(f"\nMatrix:\n{m}")
    print(f"m[1, 2] = {m[1, 2]}")          # Single element
    print(f"m[0:2, 1:3] =\n{m[0:2, 1:3]}")  # Submatrix
    print(f"m[:, 0] = {m[:, 0]}")          # First column

    # Boolean indexing powerful filtering
    data = np.array([10, 25, 30, 5, 45, 15])
    mask = data > 20
    print(f"\ndata > 20: {data[mask]}")

    # Fancy indexing select specific indices
    indices = [0, 2, 4]
    print(f"data[[0,2,4]] = {data[indices]}")


# =============================================================================
# RESHAPING
# =============================================================================

def reshaping():
    """Changing array shapes without copying data."""
    a = np.arange(12)
    print(f"Original: {a}")

    # Reshape
    m = a.reshape(3, 4)
    print(f"Reshaped to 3x4:\n{m}")

    # -1 means "infer this dimension"
    m2 = a.reshape(2, -1)  # 2 rows, auto-compute cols (6)
    print(f"Reshaped to 2x?:\n{m2}")

    # Flatten (back to 1D)
    flat = m.flatten()  # Returns a copy
    ravel = m.ravel()   # Returns a view (faster, shares memory)

    # Stack arrays
    x = np.array([1, 2, 3])
    y = np.array([4, 5, 6])
    print(f"vstack:\n{np.vstack([x, y])}")  # Vertical stack
    print(f"hstack: {np.hstack([x, y])}")   # Horizontal stack
    print(f"column_stack:\n{np.column_stack([x, y])}")  # As columns


# =============================================================================
# BROADCASTING operations on arrays with different shapes
# =============================================================================

def broadcasting():
    """Broadcasting rules let you do math on differently-shaped arrays.

    Rules:
    1. Dimensions are compared from trailing (rightmost) side
    2. Dimensions are compatible if they're equal or one of them is 1
    3. Missing dimensions are treated as size 1
    """
    # Scalar broadcast adds 10 to every element
    a = np.array([[1, 2, 3], [4, 5, 6]])
    print(f"a + 10:\n{a + 10}")

    # Column vector broadcast
    col = np.array([[10], [20]])  # Shape (2, 1)
    print(f"a + col:\n{a + col}")  # (2,3) + (2,1) → (2,3)

    # Row vector broadcast
    row = np.array([100, 200, 300])  # Shape (3,)
    print(f"a + row:\n{a + row}")  # (2,3) + (3,) → (2,3)

    # Practical example: normalize each column to 0-1
    data = np.array([[1, 100, 1000],
                     [2, 200, 2000],
                     [3, 300, 3000]])
    mins = data.min(axis=0)     # Min per column
    maxs = data.max(axis=0)     # Max per column
    normalized = (data - mins) / (maxs - mins)
    print(f"\nNormalized:\n{normalized}")


# =============================================================================
# LINEAR ALGEBRA
# =============================================================================

def linear_algebra():
    """NumPy's linalg module for matrix operations."""
    A = np.array([[2, 1], [5, 3]])
    b = np.array([4, 7])

    # Matrix multiplication
    B = np.array([[1, 2], [3, 4]])
    product = A @ B  # or np.dot(A, B)
    print(f"A @ B:\n{product}")

    # Solve linear system: Ax = b
    x = np.linalg.solve(A, b)
    print(f"\nSolve Ax=b: x = {x}")
    print(f"Verify: A@x = {A @ x}")

    # Eigenvalues and eigenvectors
    eigenvalues, eigenvectors = np.linalg.eig(A)
    print(f"\nEigenvalues: {eigenvalues}")

    # Determinant and inverse
    det = np.linalg.det(A)
    inv = np.linalg.inv(A)
    print(f"Determinant: {det:.2f}")
    print(f"Inverse:\n{inv}")

    # SVD (Singular Value Decomposition) used in ML/dimensionality reduction
    U, s, Vt = np.linalg.svd(A)
    print(f"\nSVD singular values: {s}")

    # Norm
    v = np.array([3, 4])
    print(f"L2 norm of [3,4]: {np.linalg.norm(v)}")  # = 5


# =============================================================================
# RANDOM generation, sampling, distributions
# =============================================================================

def random_operations():
    """Random number generation with NumPy."""
    rng = np.random.default_rng(seed=42)  # Modern way (NumPy 1.17+)

    # Basic random
    uniform = rng.random((3, 3))           # Uniform [0, 1)
    integers = rng.integers(1, 100, size=10)  # Random ints
    normal = rng.normal(loc=0, scale=1, size=1000)  # Gaussian

    print(f"Uniform 3x3:\n{uniform.round(3)}")
    print(f"Random integers: {integers}")
    print(f"Normal: mean={normal.mean():.3f}, std={normal.std():.3f}")

    # Sampling
    items = np.array(["apple", "banana", "cherry", "date", "elderberry"])
    sample = rng.choice(items, size=3, replace=False)
    print(f"Random sample: {sample}")

    # Shuffle
    deck = np.arange(52)
    rng.shuffle(deck)
    print(f"Shuffled (first 10): {deck[:10]}")

    # Distributions
    poisson = rng.poisson(lam=5, size=10)
    exponential = rng.exponential(scale=2.0, size=10)
    print(f"Poisson(λ=5): {poisson}")


# =============================================================================
# PERFORMANCE TIPS
# =============================================================================

def performance_comparison():
    """Show why NumPy is faster than Python loops."""
    import time

    n = 1_000_000

    # Python loop
    start = time.perf_counter()
    result_py = sum(x**2 for x in range(n))
    time_py = time.perf_counter() - start

    # NumPy vectorized
    arr = np.arange(n)
    start = time.perf_counter()
    result_np = np.sum(arr**2)
    time_np = time.perf_counter() - start

    speedup = time_py / time_np
    print(f"Python loop: {time_py:.4f}s")
    print(f"NumPy:       {time_np:.4f}s")
    print(f"Speedup:     {speedup:.1f}x")


if __name__ == "__main__":
    print("=" * 60)
    print("NumPy Basics Demo")
    print("=" * 60)

    print("\n--- Array Creation ---")
    array_creation()

    print("\n--- Array Operations ---")
    array_operations()

    print("\n--- Indexing ---")
    indexing()

    print("\n--- Reshaping ---")
    reshaping()

    print("\n--- Broadcasting ---")
    broadcasting()

    print("\n--- Linear Algebra ---")
    linear_algebra()

    print("\n--- Random ---")
    random_operations()

    print("\n--- Performance ---")
    performance_comparison()

"""
Pandas cheatsheet the 20 operations you'll use 80% of the time.

Pandas is the workhorse of data analysis in Python. This file covers
the most common operations for reading, transforming, and exporting data.
"""
import pandas as pd
import numpy as np


# =============================================================================
# READ DATA many formats supported
# =============================================================================

def reading_data():
    """Different ways to load data into a DataFrame."""
    # From files
    # df = pd.read_csv("data.csv")
    # df = pd.read_excel("data.xlsx", sheet_name="Sheet1")
    # df = pd.read_json("data.json")
    # df = pd.read_parquet("data.parquet")  # Fast columnar format

    # From database
    # import sqlalchemy
    # engine = sqlalchemy.create_engine("postgresql://user:pass@localhost/db")
    # df = pd.read_sql("SELECT * FROM users", engine)

    # From dict (useful for examples)
    df = pd.DataFrame({
        "name": ["Alice", "Bob", "Charlie", "Diana", "Eve"],
        "department": ["Engineering", "Marketing", "Engineering", "Marketing", "Engineering"],
        "salary": [95000, 72000, 88000, 78000, 102000],
        "age": [28, 35, 42, 31, 27],
        "city": ["Mumbai", "Delhi", "Mumbai", "Bangalore", "Delhi"],
    })
    return df


# =============================================================================
# EXPLORE understand your data
# =============================================================================

def explore_data(df: pd.DataFrame):
    """First things to do with any new DataFrame."""
    print("Shape:", df.shape)              # (rows, cols)
    print("Columns:", df.columns.tolist()) # Column names
    print("Types:\n", df.dtypes)           # Data types per column
    print("\n--- Head ---")
    print(df.head())                       # First 5 rows
    print("\n--- Info ---")
    df.info()                              # Memory, nulls, types
    print("\n--- Describe ---")
    print(df.describe())                   # Statistics for numeric cols
    print("\n--- Null counts ---")
    print(df.isnull().sum())               # Missing values per column
    print("\n--- Unique values ---")
    print(df.nunique())                    # Unique count per column


# =============================================================================
# FILTER select rows and columns
# =============================================================================

def filter_data(df: pd.DataFrame):
    """Selecting subsets of data."""
    # Select columns
    names = df["name"]                     # Single column (Series)
    subset = df[["name", "salary"]]        # Multiple columns (DataFrame)

    # Filter rows with boolean indexing
    high_salary = df[df["salary"] > 85000]

    # .query() SQL-like syntax (cleaner for complex conditions)
    engineers = df.query("department == 'Engineering' and salary > 90000")

    # .loc label-based selection (row labels, column names)
    specific = df.loc[0:2, ["name", "salary"]]

    # .iloc integer-based selection (row/col positions)
    first_three = df.iloc[:3, :2]

    # .isin() match against a list
    target_cities = df[df["city"].isin(["Mumbai", "Delhi"])]

    # String methods
    names_with_a = df[df["name"].str.startswith("A")]

    return high_salary


# =============================================================================
# TRANSFORM create and modify columns
# =============================================================================

def transform_data(df: pd.DataFrame):
    """Create new columns and transform existing ones."""
    # Simple calculation
    df["salary_k"] = df["salary"] / 1000

    # Apply run any function on each value
    df["name_upper"] = df["name"].apply(str.upper)

    # Apply with lambda
    df["tax_bracket"] = df["salary"].apply(
        lambda x: "high" if x > 90000 else "standard"
    )

    # Conditional column with np.where
    df["senior"] = np.where(df["age"] >= 35, True, False)

    # Multiple conditions with np.select
    conditions = [
        df["salary"] > 100000,
        df["salary"] > 80000,
        df["salary"] > 60000,
    ]
    choices = ["Executive", "Senior", "Mid"]
    df["level"] = np.select(conditions, choices, default="Junior")

    # String operations
    df["city_lower"] = df["city"].str.lower()
    df["name_len"] = df["name"].str.len()

    # Type conversion
    df["salary_str"] = df["salary"].astype(str)

    return df


# =============================================================================
# GROUP aggregate data
# =============================================================================

def group_data(df: pd.DataFrame):
    """GroupBy operations split-apply-combine pattern."""
    # Basic groupby with single aggregation
    avg_salary = df.groupby("department")["salary"].mean()
    print("Avg salary by department:\n", avg_salary)

    # Multiple aggregations
    stats = df.groupby("department")["salary"].agg(["mean", "median", "min", "max", "count"])
    print("\nSalary stats:\n", stats)

    # Different aggregations per column
    summary = df.groupby("department").agg(
        avg_salary=("salary", "mean"),
        headcount=("name", "count"),
        avg_age=("age", "mean"),
    )
    print("\nDepartment summary:\n", summary)

    # Group by multiple columns
    city_dept = df.groupby(["city", "department"])["salary"].mean()
    print("\nSalary by city & department:\n", city_dept)

    return stats


# =============================================================================
# MERGE / JOIN combine DataFrames
# =============================================================================

def merge_data():
    """Combining DataFrames like SQL JOINs."""
    employees = pd.DataFrame({
        "emp_id": [1, 2, 3, 4],
        "name": ["Alice", "Bob", "Charlie", "Diana"],
        "dept_id": [10, 20, 10, 30],
    })

    departments = pd.DataFrame({
        "dept_id": [10, 20, 40],
        "dept_name": ["Engineering", "Marketing", "Sales"],
    })

    # Inner join (only matching rows)
    inner = pd.merge(employees, departments, on="dept_id", how="inner")
    print("Inner join:\n", inner)

    # Left join (keep all left rows)
    left = pd.merge(employees, departments, on="dept_id", how="left")
    print("\nLeft join:\n", left)

    # Concatenate DataFrames (stack vertically)
    df1 = pd.DataFrame({"name": ["Alice"], "score": [95]})
    df2 = pd.DataFrame({"name": ["Bob"], "score": [87]})
    combined = pd.concat([df1, df2], ignore_index=True)
    print("\nConcatenated:\n", combined)


# =============================================================================
# PIVOT reshape data
# =============================================================================

def pivot_data():
    """Pivot tables reshape data for analysis."""
    sales = pd.DataFrame({
        "month": ["Jan", "Jan", "Feb", "Feb", "Mar", "Mar"],
        "product": ["Widget", "Gadget", "Widget", "Gadget", "Widget", "Gadget"],
        "revenue": [1000, 1500, 1200, 1300, 900, 1800],
        "units": [100, 75, 120, 65, 90, 90],
    })

    # Pivot table like Excel pivot tables
    pivot = sales.pivot_table(
        values="revenue",
        index="month",
        columns="product",
        aggfunc="sum"
    )
    print("Pivot table:\n", pivot)

    # Melt unpivot (wide → long format)
    wide = pd.DataFrame({
        "name": ["Alice", "Bob"],
        "math": [90, 85],
        "science": [88, 92],
        "english": [95, 78],
    })
    long = pd.melt(wide, id_vars=["name"], var_name="subject", value_name="score")
    print("\nMelted (long format):\n", long)


# =============================================================================
# SORT & RANK
# =============================================================================

def sort_data(df: pd.DataFrame):
    """Sorting and ranking."""
    # Sort by column
    by_salary = df.sort_values("salary", ascending=False)

    # Sort by multiple columns
    by_dept_salary = df.sort_values(["department", "salary"], ascending=[True, False])

    # Rank
    df["salary_rank"] = df["salary"].rank(ascending=False)

    # Top N per group
    top_per_dept = df.groupby("department").apply(
        lambda x: x.nlargest(2, "salary")
    ).reset_index(drop=True)

    return by_salary


# =============================================================================
# HANDLE MISSING DATA
# =============================================================================

def handle_missing():
    """Dealing with NaN/null values."""
    df = pd.DataFrame({
        "name": ["Alice", "Bob", None, "Diana"],
        "age": [28, None, 42, 31],
        "salary": [95000, 72000, None, 78000],
    })

    # Check for missing
    print("Nulls:\n", df.isnull().sum())

    # Drop rows with any null
    clean = df.dropna()

    # Fill with value
    filled = df.fillna({"age": df["age"].median(), "salary": 0, "name": "Unknown"})

    # Forward fill (useful for time series)
    ffilled = df.fillna(method="ffill")

    # Interpolate (for numeric columns)
    interpolated = df.interpolate()

    return filled


# =============================================================================
# EXPORT DATA
# =============================================================================

def export_data(df: pd.DataFrame):
    """Save DataFrame to different formats."""
    # CSV
    df.to_csv("output.csv", index=False)

    # Excel
    # df.to_excel("output.xlsx", index=False, sheet_name="Data")

    # JSON
    df.to_json("output.json", orient="records", indent=2)

    # Parquet (fast, compressed use for large datasets)
    # df.to_parquet("output.parquet", index=False)

    # To dict/list (for APIs)
    records = df.to_dict(orient="records")
    return records


if __name__ == "__main__":
    print("=" * 60)
    print("Pandas Cheatsheet Demo")
    print("=" * 60)

    df = reading_data()

    print("\n--- Explore ---")
    explore_data(df)

    print("\n--- Filter ---")
    high_salary = filter_data(df)
    print(f"High salary employees:\n{high_salary}")

    print("\n--- Transform ---")
    df = transform_data(df)
    print(df[["name", "salary_k", "tax_bracket", "level"]].to_string())

    print("\n--- Group ---")
    group_data(df)

    print("\n--- Merge ---")
    merge_data()

    print("\n--- Pivot ---")
    pivot_data()

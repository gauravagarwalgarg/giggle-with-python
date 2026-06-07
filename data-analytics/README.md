# Data Analytics

Quick-reference scripts for data science and analytics in Python.

## Files

| File | What it covers |
|------|---------------|
| `pandas_cheatsheet.py` | read, filter, group, merge, pivot, export |
| `numpy_basics.py` | arrays, broadcasting, linear algebra, random |
| `matplotlib_plots.py` | line, bar, scatter, subplots, styling, heatmaps |
| `scipy_stats.py` | distributions, hypothesis testing, curve fitting |

## Setup

```bash
pip install -r requirements.txt
```

## Running

```bash
# Each file is standalone
python data-analytics/pandas_cheatsheet.py
python data-analytics/numpy_basics.py
python data-analytics/matplotlib_plots.py   # Generates PNG files
python data-analytics/scipy_stats.py
```

## Quick Reference

### Pandas 80/20 Operations
```python
df = pd.read_csv("file.csv")       # Read
df.query("age > 25")               # Filter
df.groupby("col").agg(["mean"])    # Group
pd.merge(df1, df2, on="id")       # Join
df.pivot_table(values, index, columns)  # Pivot
```

### NumPy Key Patterns
```python
arr = np.array([1, 2, 3])         # Create
arr[arr > 2]                       # Boolean index
arr.reshape(3, -1)                 # Reshape
np.linalg.solve(A, b)             # Linear algebra
```

### Matplotlib Plot Types
```python
plt.plot(x, y)                     # Line
plt.bar(x, heights)               # Bar
plt.scatter(x, y, s=sizes)        # Scatter
plt.hist(data, bins=30)           # Histogram
fig, axes = plt.subplots(2, 2)    # Subplots
```

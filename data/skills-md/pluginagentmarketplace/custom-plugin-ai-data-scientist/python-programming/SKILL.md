---
name: python-programming
description: Python fundamentals, data structures, OOP, and data science libraries (Pandas, NumPy). Use when writing Python code, data manipulation, or algorithm implementation.
sasmp_version: "1.3.0"
bonded_agent: 01-python-data-science
bond_type: PRIMARY_BOND
---

# Python Programming for Data Science

Master Python from fundamentals to advanced data science applications.

## Quick Start

### Essential Libraries
```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
```

### Data Manipulation
```python
# Read data
df = pd.read_csv('data.csv')

# Explore
print(df.head())
print(df.info())
print(df.describe())

# Filter
df_filtered = df[df['age'] > 18]

# Group and aggregate
summary = df.groupby('category')['sales'].agg(['sum', 'mean', 'count'])

# Vectorized operations (FAST!)
df['new_col'] = df['col1'] * 2  # Instead of loops
```

## Core Concepts

### 1. Data Structures
- **Lists**: `[1, 2, 3]` - ordered, mutable
- **Dictionaries**: `{'key': 'value'}` - key-value pairs
- **Tuples**: `(1, 2, 3)` - immutable
- **Sets**: `{1, 2, 3}` - unique elements

### 2. List Comprehensions
```python
# Instead of loops
squares = [x**2 for x in range(10)]
filtered = [x for x in data if x > 0]
```

### 3. NumPy Arrays
```python
arr = np.array([1, 2, 3, 4, 5])
arr * 2  # [2, 4, 6, 8, 10]
arr.mean()  # 3.0
```

### 4. Pandas DataFrames
```python
df = pd.DataFrame({
    'name': ['Alice', 'Bob'],
    'age': [25, 30],
    'salary': [50000, 60000]
})
```

## Performance Tips

**Vectorization over Loops (10-100x faster)**:
```python
# Bad (slow)
result = []
for x in data:
    result.append(x * 2)

# Good (fast)
result = np.array(data) * 2
```

## Common Patterns

### Reading Files
```python
# CSV
df = pd.read_csv('file.csv')

# Excel
df = pd.read_excel('file.xlsx', sheet_name='Sheet1')

# JSON
df = pd.read_json('file.json')

# SQL
import sqlite3
conn = sqlite3.connect('database.db')
df = pd.read_sql_query("SELECT * FROM table", conn)
```

### Missing Data
```python
df.dropna()  # Remove rows
df.fillna(0)  # Fill with value
df.fillna(df.mean())  # Fill with mean
```

### Merging Data
```python
# Join DataFrames
merged = pd.merge(df1, df2, on='id', how='left')

# Concatenate
combined = pd.concat([df1, df2], axis=0)
```

## Best Practices

1. Use vectorized operations
2. Optimize data types
3. Avoid loops when possible
4. Use built-in functions
5. Profile before optimizing

## Troubleshooting

### Common Issues

**Problem: MemoryError with large DataFrames**
```python
# Solution 1: Use chunking
for chunk in pd.read_csv('large.csv', chunksize=10000):
    process(chunk)

# Solution 2: Optimize dtypes
df['int_col'] = df['int_col'].astype('int32')  # Instead of int64
df['cat_col'] = df['cat_col'].astype('category')  # For repeated strings
```

**Problem: Slow DataFrame operations**
```python
# Debug: Profile your code
%timeit df.apply(func)  # Compare with vectorized

# Solution: Use vectorized operations
df['result'] = np.where(df['x'] > 0, df['x'] * 2, 0)  # Instead of apply
```

**Problem: Import errors**
```bash
# Solution: Check environment
pip list | grep pandas
pip install --upgrade pandas numpy

# Virtual environment best practice
python -m venv venv
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
```

**Problem: Data type mismatches**
```python
# Debug: Check types
print(df.dtypes)

# Solution: Convert types explicitly
df['date'] = pd.to_datetime(df['date'])
df['price'] = pd.to_numeric(df['price'], errors='coerce')
```

### Debug Checklist
- [ ] Check Python and library versions
- [ ] Verify data types with `df.dtypes`
- [ ] Profile with `%timeit` before optimizing
- [ ] Use `df.info()` for memory usage
- [ ] Check for NaN values with `df.isna().sum()`

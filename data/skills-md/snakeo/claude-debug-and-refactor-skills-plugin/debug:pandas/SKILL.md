---
name: debug:pandas
description: Debug Pandas issues systematically. Use when encountering DataFrame errors, SettingWithCopyWarning, KeyError on column access, merge and join mismatches with unexpected NaN values, memory errors with large DataFrames, dtype conversion issues, index alignment problems, or any data manipulation errors in Python data analysis workflows.
---

# Pandas Debugging Guide

A systematic approach to debugging Pandas DataFrames and operations using the OILER framework (Orient, Investigate, Locate, Experiment, Reflect).

## Common Error Patterns

### 1. SettingWithCopyWarning
**Symptom:** Warning message about setting values on a copy of a slice.

**Cause:** Modifying a view of a DataFrame rather than a copy. Pandas cannot guarantee whether the operation affects the original data.

**Solution:**
```python
# BAD - triggers warning
df_subset = df[df['col'] > 5]
df_subset['new_col'] = 10  # Warning!

# GOOD - explicit copy
df_subset = df[df['col'] > 5].copy()
df_subset['new_col'] = 10  # Safe

# GOOD - use .loc for in-place modification
df.loc[df['col'] > 5, 'new_col'] = 10
```

### 2. KeyError on Column Access
**Symptom:** `KeyError: 'column_name'`

**Cause:** Column doesn't exist due to typo, incorrect capitalization, or column was never created.

**Solution:**
```python
# Check available columns
print(df.columns.tolist())

# Check for whitespace in column names
print([repr(c) for c in df.columns])

# Strip whitespace from all column names
df.columns = df.columns.str.strip()

# Case-insensitive column access
col_lower = {c.lower(): c for c in df.columns}
actual_col = col_lower.get('mycolumn'.lower())
```

### 3. Merge/Join Mismatches
**Symptom:** Unexpected row counts after merge, NaN values, or `MergeError`.

**Cause:** Mismatched column names, different dtypes, or unexpected duplicates.

**Solution:**
```python
# Before merging - inspect both DataFrames
print(f"Left shape: {df1.shape}, Right shape: {df2.shape}")
print(f"Left key dtype: {df1['key'].dtype}, Right: {df2['key'].dtype}")
print(f"Left key unique: {df1['key'].nunique()}, Right: {df2['key'].nunique()}")

# Check for duplicates in merge keys
print(f"Left duplicates: {df1['key'].duplicated().sum()}")
print(f"Right duplicates: {df2['key'].duplicated().sum()}")

# Explicit merge with indicator
result = df1.merge(df2, on='key', how='outer', indicator=True)
print(result['_merge'].value_counts())
```

### 4. Memory Errors with Large DataFrames
**Symptom:** `MemoryError` or system becomes unresponsive.

**Cause:** DataFrame too large for available RAM.

**Solution:**
```python
# Check current memory usage
print(df.info(memory_usage='deep'))
print(df.memory_usage(deep=True).sum() / 1024**2, 'MB')

# Optimize dtypes
def optimize_dtypes(df):
    for col in df.select_dtypes(include=['int64']).columns:
        df[col] = pd.to_numeric(df[col], downcast='integer')
    for col in df.select_dtypes(include=['float64']).columns:
        df[col] = pd.to_numeric(df[col], downcast='float')
    for col in df.select_dtypes(include=['object']).columns:
        if df[col].nunique() / len(df) < 0.5:
            df[col] = df[col].astype('category')
    return df

# Read in chunks
chunks = pd.read_csv('large_file.csv', chunksize=100000)
for chunk in chunks:
    process(chunk)

# Use PyArrow backend (Pandas 2.0+)
df = pd.read_csv('file.csv', dtype_backend='pyarrow')
```

### 5. dtype Conversion Issues
**Symptom:** `ValueError` during type conversion, unexpected NaN values.

**Cause:** Non-numeric strings in numeric columns, mixed types.

**Solution:**
```python
# Identify problematic values
def find_non_numeric(series):
    mask = pd.to_numeric(series, errors='coerce').isna() & series.notna()
    return series[mask].unique()

print(find_non_numeric(df['numeric_col']))

# Safe conversion with error handling
df['numeric_col'] = pd.to_numeric(df['numeric_col'], errors='coerce')

# Check for mixed types
print(df['col'].apply(type).value_counts())

# Convert with explicit handling
df['date_col'] = pd.to_datetime(df['date_col'], errors='coerce', format='%Y-%m-%d')
```

### 6. Index Alignment Problems
**Symptom:** Unexpected NaN values after operations, incorrect calculations.

**Cause:** Pandas aligns operations by index, misaligned indices cause NaN.

**Solution:**
```python
# Check index alignment
print(f"Index 1: {df1.index[:5].tolist()}")
print(f"Index 2: {df2.index[:5].tolist()}")

# Reset index for array-like operations
result = df1.reset_index(drop=True) + df2.reset_index(drop=True)

# Use .values for numpy-style operations (bypasses alignment)
result = df1['col'].values + df2['col'].values

# Check for duplicate indices
print(f"Duplicate indices: {df.index.duplicated().sum()}")
```

### 7. TypeError: 'DataFrame' object is not callable
**Symptom:** `TypeError` when accessing DataFrame.

**Cause:** Using parentheses `()` instead of brackets `[]`.

**Solution:**
```python
# BAD
df('column_name')  # TypeError!

# GOOD
df['column_name']
df.loc[0, 'column_name']
```

### 8. AttributeError on Column Access
**Symptom:** `AttributeError` when using dot notation.

**Cause:** Column name contains spaces, special characters, or conflicts with DataFrame methods.

**Solution:**
```python
# BAD - fails for special names
df.my column  # SyntaxError
df.count      # Returns method, not column named 'count'

# GOOD - always works
df['my column']
df['count']
```

## Debugging Tools

### Essential Inspection Commands
```python
# Overview of DataFrame
df.info()                          # Columns, dtypes, non-null counts, memory
df.describe()                      # Statistical summary
df.shape                           # (rows, columns)
df.dtypes                          # Column data types

# Sample data
df.head(10)                        # First 10 rows
df.tail(10)                        # Last 10 rows
df.sample(10)                      # Random 10 rows

# Column inspection
df.columns.tolist()                # All column names as list
df['col'].unique()                 # Unique values
df['col'].value_counts()           # Value frequency
df['col'].isna().sum()             # Missing value count

# Memory usage
df.memory_usage(deep=True)         # Per-column memory in bytes
df.memory_usage(deep=True).sum() / 1024**2  # Total MB
```

### Display Options
```python
# Show all columns
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

# Show all rows (use carefully!)
pd.set_option('display.max_rows', 100)

# Show full content of columns
pd.set_option('display.max_colwidth', None)

# Float precision
pd.set_option('display.precision', 4)

# Reset all options
pd.reset_option('all')
```

### Pandas-Log for Chain Debugging
```python
# Install: pip install pandas-log
import pandas_log

# Wrap operations with logging
with pandas_log.enable():
    result = (df
        .query('col > 5')
        .groupby('category')
        .agg({'value': 'sum'})
    )
# Outputs: rows/columns affected at each step
```

## The Four Phases (OILER Framework)

### Phase 1: Orient
Understand the problem before diving in.

```python
# What is the error message?
# What operation triggered it?
# What is the expected vs actual behavior?

# Quick state check
print(f"Shape: {df.shape}")
print(f"Columns: {df.columns.tolist()}")
print(f"Dtypes:\n{df.dtypes}")
print(f"Head:\n{df.head(3)}")
```

### Phase 2: Investigate
Gather information systematically.

```python
# Check data quality
def investigate_df(df):
    print("=== DataFrame Investigation ===")
    print(f"Shape: {df.shape}")
    print(f"\nMissing values:\n{df.isna().sum()}")
    print(f"\nDtypes:\n{df.dtypes}")
    print(f"\nDuplicate rows: {df.duplicated().sum()}")
    print(f"\nMemory: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")

    # Check for mixed types in object columns
    for col in df.select_dtypes(include=['object']).columns:
        types = df[col].apply(type).value_counts()
        if len(types) > 1:
            print(f"\nMixed types in '{col}':\n{types}")

investigate_df(df)
```

### Phase 3: Locate
Narrow down the source of the problem.

```python
# For chained operations - break them apart
# BAD - hard to debug
result = df.query('x > 5').groupby('cat').agg({'val': 'sum'}).reset_index()

# GOOD - step by step
step1 = df.query('x > 5')
print(f"After filter: {step1.shape}")

step2 = step1.groupby('cat')
print(f"Groups: {step2.ngroups}")

step3 = step2.agg({'val': 'sum'})
print(f"After agg: {step3.shape}")

result = step3.reset_index()
```

### Phase 4: Experiment & Reflect
Test fixes and document learnings.

```python
# Test fix on small sample first
sample = df.sample(100).copy()

# Apply fix
sample['fixed_col'] = sample['col'].apply(fix_function)

# Verify
assert sample['fixed_col'].isna().sum() == 0
assert sample['fixed_col'].dtype == expected_dtype

# Apply to full DataFrame
df['fixed_col'] = df['col'].apply(fix_function)
```

## Quick Reference Commands

### Data Validation
```python
# Assert no missing values
assert df.notna().all().all(), f"Missing: {df.isna().sum()[df.isna().sum() > 0]}"

# Assert unique index
assert not df.index.duplicated().any(), "Duplicate indices found"

# Assert column exists
assert 'col' in df.columns, f"Column 'col' not found. Available: {df.columns.tolist()}"

# Assert dtype
assert df['col'].dtype == 'int64', f"Wrong dtype: {df['col'].dtype}"
```

### Common Fixes One-Liners
```python
# Remove duplicate rows
df = df.drop_duplicates()

# Reset index
df = df.reset_index(drop=True)

# Strip whitespace from string columns
df[str_cols] = df[str_cols].apply(lambda x: x.str.strip())

# Fill missing values
df['col'] = df['col'].fillna(0)  # or 'Unknown', df['col'].mean(), etc.

# Convert to datetime
df['date'] = pd.to_datetime(df['date'], errors='coerce')

# Rename columns
df = df.rename(columns={'old': 'new'})

# Drop columns
df = df.drop(columns=['unwanted1', 'unwanted2'])
```

### Debugging Merge Issues
```python
def debug_merge(left, right, on, how='inner'):
    """Debug merge operation before executing."""
    print(f"Left: {left.shape}, Right: {right.shape}")

    # Check key columns
    for key in (on if isinstance(on, list) else [on]):
        print(f"\nKey: '{key}'")
        print(f"  Left dtype: {left[key].dtype}, Right dtype: {right[key].dtype}")
        print(f"  Left unique: {left[key].nunique()}, Right unique: {right[key].nunique()}")
        print(f"  Left nulls: {left[key].isna().sum()}, Right nulls: {right[key].isna().sum()}")

        # Check overlap
        left_set = set(left[key].dropna())
        right_set = set(right[key].dropna())
        overlap = len(left_set & right_set)
        print(f"  Overlap: {overlap} ({overlap/len(left_set)*100:.1f}% of left)")

    # Execute with indicator
    result = left.merge(right, on=on, how=how, indicator=True)
    print(f"\nResult: {result.shape}")
    print(result['_merge'].value_counts())

    return result.drop(columns=['_merge'])
```

### Memory Optimization
```python
def optimize_memory(df, verbose=True):
    """Reduce DataFrame memory usage."""
    start_mem = df.memory_usage(deep=True).sum() / 1024**2

    for col in df.columns:
        col_type = df[col].dtype

        if col_type == 'object':
            if df[col].nunique() / len(df) < 0.5:
                df[col] = df[col].astype('category')
        elif str(col_type).startswith('int'):
            df[col] = pd.to_numeric(df[col], downcast='integer')
        elif str(col_type).startswith('float'):
            df[col] = pd.to_numeric(df[col], downcast='float')

    end_mem = df.memory_usage(deep=True).sum() / 1024**2

    if verbose:
        print(f"Memory: {start_mem:.2f} MB -> {end_mem:.2f} MB ({(1-end_mem/start_mem)*100:.1f}% reduction)")

    return df
```

## Resources

- [KDnuggets - Guide to Debugging Common Pandas Errors](https://www.kdnuggets.com/data-scientists-guide-debugging-common-pandas-errors)
- [Debugging Chained Pandas Operations](https://medium.com/data-science/efficient-coding-in-data-science-easy-debugging-of-pandas-chained-operations-0089f6de920f)
- [10 Pandas Debugging Habits](https://medium.com/@ThinkingLoop/10-pandas-debugging-habits-that-save-hours-in-large-data-workflows-c4291d8bf560)
- [Pandas-Log for Debugging](https://www.datacourses.com/pandas-log-and-its-debugging-capabilities-1018/)
- [Common Error Messages in Pandas](https://www.hopsworks.ai/post/common-error-messages-in-pandas)
- [50 Common Pandas Mistakes](https://baotramduong.medium.com/python-for-data-science-50-common-pandas-mistakes-c8df122c4890)

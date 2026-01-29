---
name: python-best-practices
description: Python development best practices including PEP 8 style guidelines, type hints, docstring conventions, and common patterns. Use when writing or modifying Python code.
---

# Python Best Practices

## Purpose

This skill provides guidance on Python development best practices to ensure code quality, maintainability, and consistency across your Python projects.

## When to Use This Skill

Auto-activates when:

- Working with Python files (*.py)
- Mentions of "python", "best practices", "style guide"
- Adding type hints or docstrings
- Code refactoring in Python

## Style Guidelines

### PEP 8 Compliance

Follow PEP 8 style guide for Python code:

- **Indentation**: 4 spaces per indentation level
- **Line Length**: Maximum 79 characters for code, 72 for docstrings/comments
- **Blank Lines**: 2 blank lines between top-level definitions, 1 between methods
- **Imports**: Always at top of file, grouped (stdlib, third-party, local)
- **Naming Conventions**:
  - `snake_case` for functions, variables, modules
  - `PascalCase` for classes
  - `UPPER_SNAKE_CASE` for constants
  - Leading underscore `_name` for internal/private

### Import Organization

Always organize imports in this order:

```python
# 1. Standard library imports
import os
import sys
from pathlib import Path

# 2. Third-party imports
import requests
import numpy as np

# 3. Local application imports
from myapp.core import MyClass
from myapp.utils import helper_function
```

Avoid circular imports by using `TYPE_CHECKING`:

```python
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from myapp.other_module import OtherClass

def my_function(obj: "OtherClass") -> None:
    """Function that uses OtherClass only for type hints."""
    pass
```

## Type Hints

### Always Use Type Hints

Type hints improve code clarity and catch errors early:

```python
def process_data(
    items: list[str],
    max_count: int | None = None,
    verbose: bool = False
) -> dict[str, int]:
    """Process items and return counts.

    Parameters
    ----------
    items : list[str]
        List of items to process
    max_count : int | None, optional
        Maximum items to process, by default None
    verbose : bool, optional
        Enable verbose output, by default False

    Returns
    -------
    dict[str, int]
        Dictionary mapping items to counts
    """
    result: dict[str, int] = {}

    for item in items[:max_count]:
        result[item] = result.get(item, 0) + 1
        if verbose:
            print(f"Processed: {item}")

    return result
```

### Modern Type Syntax (Python 3.10+)

Use modern union syntax with `|` instead of `Union`:

```python
# Good (Python 3.10+)
def get_value(key: str) -> int | None:
    pass

# Avoid (old style)
from typing import Union, Optional
def get_value(key: str) -> Optional[int]:
    pass
```

### Generic Types

Use built-in generic types (Python 3.9+):

```python
# Good (Python 3.9+)
def process_list(items: list[str]) -> dict[str, int]:
    pass

# Avoid (old style)
from typing import List, Dict
def process_list(items: List[str]) -> Dict[str, int]:
    pass
```

## Docstrings

### NumPy Style Docstrings

Use NumPy-style docstrings for consistency:

```python
def calculate_statistics(
    data: list[float],
    include_median: bool = True
) -> dict[str, float]:
    """Calculate statistical measures for a dataset.

    This function computes mean, standard deviation, and optionally
    median for the provided dataset.

    Parameters
    ----------
    data : list[float]
        List of numerical values to analyze
    include_median : bool, optional
        Whether to calculate median, by default True

    Returns
    -------
    dict[str, float]
        Dictionary containing:
        - 'mean': arithmetic mean
        - 'std': standard deviation
        - 'median': median value (if include_median=True)

    Raises
    ------
    ValueError
        If data is empty or contains non-numeric values

    Examples
    --------
    >>> calculate_statistics([1.0, 2.0, 3.0, 4.0, 5.0])
    {'mean': 3.0, 'std': 1.414, 'median': 3.0}

    Notes
    -----
    Standard deviation uses Bessel's correction (ddof=1).
    """
    if not data:
        raise ValueError("Data cannot be empty")

    # Implementation here
    pass
```

### Class Docstrings

```python
class DataProcessor:
    """Process and transform data from various sources.

    This class provides methods for loading, transforming, and
    validating data from multiple input formats.

    Parameters
    ----------
    source_dir : Path
        Directory containing source data files
    cache_enabled : bool, optional
        Enable result caching, by default True

    Attributes
    ----------
    source_dir : Path
        Directory path for source files
    cache : dict[str, Any]
        Cache for processed results

    Examples
    --------
    >>> processor = DataProcessor(Path("/data"))
    >>> results = processor.process_files()
    """

    def __init__(self, source_dir: Path, cache_enabled: bool = True):
        """Initialize the DataProcessor."""
        self.source_dir = source_dir
        self.cache: dict[str, Any] = {} if cache_enabled else None
```

## Error Handling

### Specific Exception Types

Use specific exception types, not bare `except`:

```python
# Good
try:
    with open(file_path) as f:
        data = f.read()
except FileNotFoundError:
    logger.error(f"File not found: {file_path}")
    raise
except PermissionError:
    logger.error(f"Permission denied: {file_path}")
    raise

# Avoid
try:
    with open(file_path) as f:
        data = f.read()
except:  # Too broad!
    pass
```

### Context Managers

Always use context managers for resources:

```python
# Good
with open(file_path) as f:
    content = f.read()

# Avoid
f = open(file_path)
content = f.read()
f.close()  # Easy to forget!
```

### Custom Exceptions

Define custom exceptions for domain-specific errors:

```python
class ValidationError(Exception):
    """Raised when data validation fails."""
    pass

class DataProcessingError(Exception):
    """Raised when data processing encounters an error."""

    def __init__(self, message: str, item_id: str):
        super().__init__(message)
        self.item_id = item_id
```

## Common Patterns

### Dataclasses for Data Structures

Use `dataclasses` for simple data containers:

```python
from dataclasses import dataclass, field

@dataclass
class User:
    """User profile information."""

    username: str
    email: str
    age: int
    tags: list[str] = field(default_factory=list)
    is_active: bool = True

    def __post_init__(self):
        """Validate fields after initialization."""
        if self.age < 0:
            raise ValueError("Age cannot be negative")
```

### Enums for Fixed Sets

Use `Enum` for fixed sets of values:

```python
from enum import Enum, auto

class Status(Enum):
    """Processing status values."""

    PENDING = auto()
    PROCESSING = auto()
    COMPLETED = auto()
    FAILED = auto()

# Usage
current_status = Status.PENDING
if current_status == Status.COMPLETED:
    print("Done!")
```

### Pathlib for File Operations

Use `pathlib.Path` instead of `os.path`:

```python
from pathlib import Path

# Good
data_dir = Path("/data")
file_path = data_dir / "input.txt"

if file_path.exists():
    content = file_path.read_text()

# Avoid
import os
data_dir = "/data"
file_path = os.path.join(data_dir, "input.txt")

if os.path.exists(file_path):
    with open(file_path) as f:
        content = f.read()
```

### List Comprehensions

Use comprehensions for clarity and performance:

```python
# Good
squared = [x**2 for x in range(10) if x % 2 == 0]

# Avoid
squared = []
for x in range(10):
    if x % 2 == 0:
        squared.append(x**2)
```

## Code Organization

### Module Structure

Organize modules with clear sections:

```python
"""Module for data processing utilities.

This module provides functions for loading, transforming, and
validating data from various sources.
"""

# Standard library imports
import os
import sys
from pathlib import Path

# Third-party imports
import requests
import pandas as pd

# Local imports
from myapp.core import BaseProcessor
from myapp.utils import validate_input

# Constants
MAX_RETRIES = 3
DEFAULT_TIMEOUT = 30

# Exceptions
class ProcessingError(Exception):
    """Raised when processing fails."""
    pass

# Functions
def load_data(source: str) -> pd.DataFrame:
    """Load data from source."""
    pass

# Classes
class DataProcessor(BaseProcessor):
    """Process and validate data."""
    pass

# Module initialization
if __name__ == "__main__":
    # CLI entry point
    main()
```

### Avoid Magic Numbers

Use named constants instead of magic numbers:

```python
# Good
MAX_RETRIES = 3
TIMEOUT_SECONDS = 30

def fetch_data(url: str) -> dict:
    for attempt in range(MAX_RETRIES):
        response = requests.get(url, timeout=TIMEOUT_SECONDS)
        if response.status_code == 200:
            return response.json()

# Avoid
def fetch_data(url: str) -> dict:
    for attempt in range(3):  # What is 3?
        response = requests.get(url, timeout=30)  # Why 30?
        if response.status_code == 200:
            return response.json()
```

## Testing

### Use pytest for Testing

```python
import pytest
from myapp.processor import DataProcessor

def test_process_valid_data():
    """Test processing with valid input."""
    processor = DataProcessor()
    result = processor.process([1, 2, 3])
    assert result == [2, 4, 6]

def test_process_empty_data():
    """Test processing with empty input."""
    processor = DataProcessor()
    with pytest.raises(ValueError):
        processor.process([])

@pytest.fixture
def sample_data():
    """Provide sample data for tests."""
    return [1, 2, 3, 4, 5]

def test_with_fixture(sample_data):
    """Test using fixture."""
    processor = DataProcessor()
    result = processor.process(sample_data)
    assert len(result) == len(sample_data)
```

## Key Takeaways

1. Follow PEP 8 style guidelines consistently
2. Always use type hints for function signatures
3. Write NumPy-style docstrings for all public functions/classes
4. Use specific exception types, not bare `except`
5. Prefer `pathlib.Path` over `os.path`
6. Use dataclasses and enums for structured data
7. Organize imports: stdlib → third-party → local
8. Avoid magic numbers, use named constants
9. Write tests using pytest
10. Use modern Python syntax (3.9+)

---
name: python
description: Write idiomatic Python with advanced features. Use for Python development, refactoring, or optimization.
---

# Python Development

Write clean, performant, idiomatic Python code.

## When to Use

- Writing Python code
- Refactoring Python projects
- Performance optimization
- Setting up Python tooling
- Code review for Python

## Python Best Practices

### Code Style

- Follow PEP 8
- Use type hints (Python 3.9+)
- Prefer f-strings over .format()
- Use pathlib over os.path

### Modern Features

```python
# Type hints
def process(data: list[dict]) -> dict[str, int]:
    ...

# Dataclasses
from dataclasses import dataclass

@dataclass
class User:
    name: str
    email: str
    active: bool = True

# Context managers
from contextlib import contextmanager

@contextmanager
def timer():
    start = time.time()
    yield
    print(f"Elapsed: {time.time() - start:.2f}s")

# Generators for memory efficiency
def read_large_file(path):
    with open(path) as f:
        yield from f
```

### Error Handling

```python
# Custom exceptions
class ValidationError(Exception):
    def __init__(self, field: str, message: str):
        self.field = field
        self.message = message
        super().__init__(f"{field}: {message}")

# Proper exception chaining
try:
    process()
except ValueError as e:
    raise ProcessingError("Failed to process") from e
```

## Project Structure

```
project/
├── src/
│   └── package/
│       ├── __init__.py
│       └── module.py
├── tests/
│   └── test_module.py
├── pyproject.toml
└── README.md
```

## Tooling Setup

```toml
# pyproject.toml
[tool.ruff]
line-length = 88
select = ["E", "F", "I", "UP"]

[tool.mypy]
strict = true

[tool.pytest.ini_options]
testpaths = ["tests"]
```

## Testing Pattern

```python
import pytest

@pytest.fixture
def sample_data():
    return {"key": "value"}

def test_process(sample_data):
    result = process(sample_data)
    assert result["status"] == "success"
```

## Examples

**Input:** "Refactor this Python code"
**Action:** Apply PEP 8, add type hints, simplify logic, improve error handling

**Input:** "Make this faster"
**Action:** Profile, identify bottlenecks, use generators/caching, verify improvement

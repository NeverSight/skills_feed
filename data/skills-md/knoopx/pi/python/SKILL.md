---
name: python
description: Structures Python projects, writes type-hinted code, tests with pytest, and enforces quality with ruff and mypy. Use when setting up pyproject.toml, writing tests, adding type annotations, or formatting/linting code.
---

# Python

Modern Python development with type hints, testing, and code quality tools.

## Contents

- [Project Setup](#project-setup)
- [Code Quality](#code-quality)
- [Testing](#testing)
- [Dataclasses](#dataclasses)
- [Type Hints](#type-hints)
- [Best Practices](#best-practices)

## Project Setup

### Structure

```
my-project/
├── pyproject.toml
├── src/my_project/
│   ├── __init__.py
│   ├── main.py
│   └── py.typed          # PEP 561 marker
├── tests/
│   ├── conftest.py
│   └── test_main.py
└── README.md
```

### pyproject.toml

```toml
[project]
name = "my-project"
version = "0.1.0"
requires-python = ">=3.9"
dependencies = ["requests>=2.31.0"]

[project.optional-dependencies]
ml = ["scikit-learn>=1.0.0"]

[dependency-groups]
dev = ["pytest>=7.0.0", "ruff>=0.1.0", "mypy>=1.0.0"]

[tool.ruff]
line-length = 100
target-version = "py39"

[tool.ruff.lint]
select = ["E", "F", "W", "I"]

[tool.mypy]
python_version = "3.9"
strict = true

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-v"
```

## Code Quality

### Formatting (ruff)

```bash
uv run ruff format .              # Format all
uv run ruff format --check .      # Check only
```

### Linting (ruff)

```bash
uv run ruff check .               # Check issues
uv run ruff check . --fix         # Auto-fix
```

### Type Checking (mypy)

```bash
uv run mypy src/                  # Check types
uv run mypy --strict src/         # Strict mode
```

## Testing

### Running Tests

```bash
uv run pytest                     # Run all
uv run pytest -v                  # Verbose
uv run pytest tests/test_main.py  # Specific file
uv run pytest -k "test_add"       # Pattern match
uv run pytest -x                  # Stop on first failure
uv run pytest --cov=src tests/    # With coverage

# Watch mode (use tmux for background, requires pytest-watch)
tmux new -d -s pytest 'uv run ptw'
```

### Test Structure

```python
import pytest
from my_project.utils import add, divide


class TestArithmetic:
    def test_add(self) -> None:
        assert add(2, 3) == 5

    def test_divide_by_zero(self) -> None:
        with pytest.raises(ValueError, match="Cannot divide by zero"):
            divide(10, 0)

    @pytest.mark.parametrize("a,b,expected", [
        (1, 1, 2),
        (10, 20, 30),
    ])
    def test_add_parametrized(self, a: int, b: int, expected: int) -> None:
        assert add(a, b) == expected
```

### Fixtures

```python
import pytest

@pytest.fixture
def db():
    db = Database(":memory:")
    db.init()
    yield db
    db.close()

def test_user_insert(db):
    db.insert("users", {"name": "Test"})
    assert db.count("users") == 1
```

## Dataclasses

**Prefer dataclasses over regular classes** for data containers. Auto-generates `__init__`, `__repr__`, `__eq__`.

```python
from dataclasses import dataclass, field

@dataclass
class User:
    id: int
    name: str
    email: str

@dataclass(frozen=True)  # Immutable, hashable
class Point:
    x: float
    y: float

@dataclass
class Config:
    name: str
    debug: bool = False                           # Simple default
    tags: list[str] = field(default_factory=list) # Mutable default
    area: float = field(init=False)               # Computed field

    def __post_init__(self) -> None:
        self.area = len(self.tags)
```

### Decorator Options

| Option        | Effect                                      |
| ------------- | ------------------------------------------- |
| `frozen=True` | Immutable, hashable (use for value objects) |
| `slots=True`  | Memory-efficient (Python 3.10+)             |
| `order=True`  | Enable `<`, `>`, `<=`, `>=` comparisons     |

### When to Use

| ✅ Dataclasses              | ❌ Regular Classes            |
| --------------------------- | ----------------------------- |
| DTOs, configs, records      | Complex behavior/methods      |
| API request/response models | Custom `__init__` logic       |
| Immutable value objects     | Mutable state with invariants |

## Type Hints

### Functions

```python
from typing import Optional, List, Dict

def greet(name: str, formal: bool = False) -> str:
    return f"Good day, {name}!" if formal else f"Hello, {name}!"

def process(data: List[Dict[str, int]]) -> Optional[int]:
    return sum(d.get("value", 0) for d in data) or None
```

### Classes

```python
from dataclasses import dataclass
from typing import Generic, TypeVar

@dataclass
class User:
    id: int
    name: str
    email: str

T = TypeVar('T')

class Container(Generic[T]):
    def __init__(self, value: T) -> None:
        self.value = value

    def get(self) -> T:
        return self.value
```

### Error Handling

```python
from pathlib import Path
from typing import Optional

def read_file(path: Path) -> Optional[str]:
    try:
        return path.read_text()
    except FileNotFoundError:
        return None
    except PermissionError as e:
        raise PermissionError(f"Cannot read {path}") from e
```

## Best Practices

1. **Type hints**: All function parameters and return values
2. **Docstrings**: Document public APIs
3. **Test coverage**: Comprehensive tests for business logic
4. **Fixtures**: Organize test setup, not setup methods
5. **Parametrize**: Use `@pytest.mark.parametrize` for multiple cases
6. **Strict mypy**: Enable `--strict` in pyproject.toml
7. **Logging**: Use logging module, not print()

## Development Loop

```bash
# 1. Format
uv run ruff format .

# 2. Lint
uv run ruff check . --fix

# 3. Type check
uv run mypy src/

# 4. Test
uv run pytest -v
```

## Related Skills

- **uv**: Manage Python dependencies and environments

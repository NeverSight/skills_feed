---
name: improving-python-code-quality
description: Improves Python library code quality through ruff linting, mypy type checking, Pythonic idioms, and refactoring. Use when reviewing code for quality issues, adding type hints, configuring static analysis tools, or refactoring Python library code.
---

# Python Code Quality

## Quick Reference

| Tool | Purpose | Command |
|------|---------|---------|
| ruff | Lint + format | `ruff check src && ruff format src` |
| mypy | Type check | `mypy src` |

## Ruff Configuration

Minimal config in pyproject.toml:

```toml
[tool.ruff]
line-length = 88
target-version = "py310"

[tool.ruff.lint]
select = ["E", "W", "F", "I", "B", "C4", "UP"]
```

For full configuration options, see **[RUFF_CONFIG.md](RUFF_CONFIG.md)**.

## MyPy Configuration

```toml
[tool.mypy]
python_version = "3.10"
disallow_untyped_defs = true
warn_return_any = true
```

For strict settings and overrides, see **[MYPY_CONFIG.md](MYPY_CONFIG.md)**.

## Type Hints Patterns

```python
# Basic
def process(items: list[str]) -> dict[str, int]: ...

# Optional
def fetch(url: str, timeout: int | None = None) -> bytes: ...

# Callable
def apply(func: Callable[[int], str], value: int) -> str: ...

# Generic
T = TypeVar("T")
def first(items: Sequence[T]) -> T | None: ...
```

For protocols and advanced patterns, see **[TYPE_PATTERNS.md](TYPE_PATTERNS.md)**.

## Common Anti-Patterns

```python
# Bad: Mutable default
def process(items: list = []):  # Bug!
    ...

# Good: None default
def process(items: list | None = None):
    items = items or []
    ...
```

```python
# Bad: Bare except
try:
    ...
except:
    pass

# Good: Specific exception
try:
    ...
except ValueError as e:
    logger.error(e)
```

## Pythonic Idioms

```python
# Iteration
for item in items:           # Not: for i in range(len(items))
for i, item in enumerate(items):  # When index needed

# Dictionary access
value = d.get(key, default)  # Not: if key in d: value = d[key]

# Context managers
with open(path) as f:        # Not: f = open(path); try: finally: f.close()

# Comprehensions (simple only)
squares = [x**2 for x in numbers]
```

## Module Organization

```
src/my_library/
├── __init__.py      # Public API exports
├── _internal.py     # Private (underscore prefix)
├── exceptions.py    # Custom exceptions
├── types.py         # Type definitions
└── py.typed         # Type hint marker
```

## Checklist

```
Code Quality:
- [ ] ruff check passes
- [ ] mypy passes (strict mode)
- [ ] Public API has type hints
- [ ] Public API has docstrings
- [ ] No mutable default arguments
- [ ] Specific exception handling
- [ ] py.typed marker present
```

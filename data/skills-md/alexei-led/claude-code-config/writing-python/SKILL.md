---
name: writing-python
description: Idiomatic Python 3.14+ development. Use when writing Python code, CLI tools, scripts, or services. Emphasizes stdlib, type hints, uv/ruff toolchain, and minimal dependencies.
user-invocable: false
context: fork
agent: python-engineer
allowed-tools:
  - Read
  - Bash
  - Grep
  - Glob
---

# Python Development (3.14+)

## Core Philosophy

1. **Stdlib and Mature Libraries First**
   - Always prefer Python stdlib solutions
   - External deps only when stdlib insufficient
   - Prefer dataclasses over attrs, pathlib over os.path

2. **Type Hints Everywhere (No Any)**
   - Python 3.14 has lazy annotations by default
   - Use Protocol for structural typing (duck typing)
   - Avoid Any—use concrete types or generics

3. **Protocol Over ABC**
   - Protocol for implicit interface satisfaction
   - ABC only when runtime isinstance() needed
   - Protocols are more flexible and Pythonic

4. **Flat Control Flow**
   - Guard clauses with early returns
   - Pattern matching to flatten conditionals
   - Maximum 2 levels of nesting

5. **Explicit Error Handling**
   - Custom exception hierarchy for domain errors
   - Raise early, handle at boundaries
   - except ValueError | TypeError: (no parens)

## Quick Patterns

### Protocol-Based Dependency Injection

```python
from typing import Protocol

# Protocol at consumer (like Go interfaces)
class UserStore(Protocol):
    def get(self, id: str) -> User | None: ...
    def save(self, user: User) -> None: ...

class UserService:
    def __init__(self, store: UserStore):
        self.store = store  # accepts any matching impl
```

### Flat Control Flow (No Nesting)

```python
# GOOD: guard clauses, early returns
def process(user: User | None) -> Result:
    if user is None:
        raise ValueError("user required")
    if not user.email:
        raise ValueError("email required")
    if not is_valid_email(user.email):
        raise ValueError("invalid email")
    return do_work(user)  # happy path at end

# BAD: nested conditions
def process(user: User | None) -> Result:
    if user is not None:
        if user.email:
            if is_valid_email(user.email):
                return do_work(user)
    raise ValueError("invalid")
```

### Pattern Matching

```python
# Flatten complex conditionals with match
match event:
    case {"type": "click", "x": x, "y": y}:
        handle_click(x, y)
    case {"type": "key", "code": code}:
        handle_key(code)
    case _:
        raise ValueError(f"Unknown event: {event}")
```

### Type Hints (No Any)

```python
# GOOD: concrete types
def process_users(users: list[User], limit: int | None = None) -> list[Result]:
    ...

# GOOD: generics when needed
from typing import TypeVar
T = TypeVar("T")
def first(items: list[T]) -> T | None:
    return items[0] if items else None

# BAD: unnecessary Any
def process(data: Any) -> Any:  # Don't do this
    ...
```

### Error Handling

```python
# except without parens (3.14)
except ValueError | TypeError:
    handle_error()

# Custom exceptions
class NotFoundError(AppError):
    def __init__(self, resource: str, id: str):
        self.resource = resource
        self.id = id
        super().__init__(f"{resource} not found: {id}")
```

## Python 3.14 Features

- **Deferred annotations**: No `from __future__ import annotations`
- **Template strings (t"")**: `t"Hello {name}"` returns Template
- **except without parens**: `except ValueError | TypeError:`
- **concurrent.interpreters**: True parallelism
- **compression.zstd**: Zstandard in stdlib
- **Free-threaded build**: No GIL (opt-in)

## References

- [PATTERNS.md](PATTERNS.md) - Code patterns and style
- [CLI.md](CLI.md) - CLI application patterns
- [TESTING.md](TESTING.md) - Testing with pytest

## Tooling

```bash
uv sync                    # Install deps
ruff check --fix .         # Lint and autofix
ruff format .              # Format
pytest -v                  # Test
mypy .                     # Type check
```

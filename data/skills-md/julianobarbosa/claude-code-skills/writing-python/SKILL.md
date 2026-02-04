---
name: writing-python
description: Idiomatic Python 3.14+ development. Use when writing Python code, CLI tools, scripts, or services. Emphasizes stdlib, type hints, uv/ruff toolchain, and minimal dependencies.
allowed-tools: Read, Bash, Grep, Glob
---

# Python Development (3.14+)

## Core Principles

- **Stdlib first**: External deps only when justified
- **Type hints everywhere**: All functions, all parameters
- **Explicit over implicit**: Clear is better than clever
- **Fail fast**: Raise early with informative errors

## Toolchain

```bash
uv           # Package management (not pip/poetry)
ruff         # Lint + format (not flake8/black)
pytest       # Testing
mypy         # Type checking
```

## Quick Patterns

### Type Hints

```python
def process_users(users: list[User], limit: int | None = None) -> list[Result]:
    ...

async def fetch_data(url: str, timeout: float = 30.0) -> dict[str, Any]:
    ...
```

### Dataclasses

```python
from dataclasses import dataclass, field

@dataclass
class Config:
    host: str
    port: int = 8080
    tags: list[str] = field(default_factory=list)
```

### Pattern Matching

```python
match event:
    case {"type": "click", "x": x, "y": y}:
        handle_click(x, y)
    case {"type": "key", "code": code}:
        handle_key(code)
    case _:
        raise ValueError(f"Unknown event: {event}")
```

## Python 3.14 Features

- **Deferred annotations**: No more `from __future__ import annotations`
- **Template strings (t"")**: `t"Hello {name}"` returns Template object
- **except without parens**: `except ValueError, TypeError:`
- **concurrent.interpreters**: True parallelism via subinterpreters
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

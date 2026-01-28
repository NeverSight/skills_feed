---
name: python
description: >
  Python best practices, PEP 8, type hints, and modern patterns.
  Trigger: When writing Python code, using type hints, or following PEP standards.
license: Apache-2.0
metadata:
  author: poletron
  version: "1.0"
  scope: [root]
  auto_invoke: "Working with python"

## When to Use

Use this skill when:
- Writing Python 3.10+ code
- Adding type hints for mypy compatibility
- Following PEP 8 style guidelines
- Using virtual environments and dependency management

---

## Critical Patterns

### Type Hints (REQUIRED)

```python
# ✅ ALWAYS: Use type hints for all function signatures
def calculate_total(items: list[dict], tax_rate: float = 0.1) -> float:
    """Calculate total with tax."""
    subtotal = sum(item["price"] for item in items)
    return subtotal * (1 + tax_rate)

# ❌ NEVER: Untyped functions
def calculate_total(items, tax_rate=0.1):
    return sum(i["price"] for i in items) * (1 + tax_rate)
```

### Docstrings (REQUIRED)

```python
# ✅ ALWAYS: Google-style docstrings
def process_order(order_id: str, validate: bool = True) -> Order:
    """Process an order by ID.
    
    Args:
        order_id: Unique order identifier.
        validate: Whether to validate before processing.
        
    Returns:
        Processed Order object.
        
    Raises:
        OrderNotFoundError: If order doesn't exist.
    """
```

### Custom Exceptions (REQUIRED)

```python
# ✅ ALWAYS: Custom exceptions over generic
class OrderNotFoundError(Exception):
    """Raised when order is not found."""
    pass

# ❌ NEVER: Generic exceptions
raise Exception("Order not found")
```

---

## Decision Tree

```
Need formatting?       → Use f-strings
Need async?            → Use asyncio with async/await
Need data class?       → Use @dataclass or Pydantic
Need env management?   → Use poetry or uv
Need type checking?    → Run mypy in CI
```

---

## Code Examples

### Modern Python Features

```python
# Pattern matching (3.10+)
match status:
    case "pending":
        process_pending()
    case "completed":
        finalize()
    case _:
        raise ValueError(f"Unknown status: {status}")

# Dataclasses
from dataclasses import dataclass

@dataclass
class User:
    id: str
    name: str
    email: str
    active: bool = True
```

### Context Managers

```python
# ✅ Good: Use context managers for resources
with open("file.txt", "r") as f:
    content = f.read()

# Async context manager
async with aiohttp.ClientSession() as session:
    async with session.get(url) as response:
        data = await response.json()
```

---

## Commands

```bash
python -m venv .venv         # Create virtual environment
source .venv/bin/activate    # Activate (Unix)
pip install -r requirements.txt
mypy src/                    # Type checking
ruff check src/              # Linting
pytest tests/                # Run tests
```

---

## Resources

Additional specialized documentation:
- **PEP 8 Standards**: [pep8-standards.md](pep8-standards.md)
- **FastAPI**: [fastapi.md](fastapi.md)
- **FastAPI Async**: [fastapi-async.md](fastapi-async.md)
- **Django**: [django.md](django.md)
- **Deep Learning**: [deep-learning.md](deep-learning.md)
- **Web Scraping**: [web-scraping.md](web-scraping.md)

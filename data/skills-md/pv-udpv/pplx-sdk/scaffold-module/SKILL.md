---
name: scaffold-module
description: Scaffold new modules and components for pplx-sdk following the layered architecture and established code patterns.
context: fork
agent: scaffolder
---

# scaffold-module

Generate new modules following pplx-sdk's layered architecture and conventions.

## When to use

Use this skill when creating a new transport backend, domain service, or shared utility for the SDK.

## Instructions

1. **Identify the target layer** (core, shared, transport, domain, or client).
2. **Create the source file** with proper imports, type annotations, and docstrings.
3. **Create the test file** in `tests/test_<module>.py`.
4. **Update `__init__.py`** exports in the target package.
5. **Verify** with `pytest tests/test_<module>.py -v` and `mypy pplx_sdk/`.

## Layer Rules

| Layer | Directory | May Import From | Purpose |
|-------|-----------|----------------|---------|
| Core | `pplx_sdk/core/` | Nothing | Protocols, types, exceptions |
| Shared | `pplx_sdk/shared/` | `core/` | Auth, logging, retry utilities |
| Transport | `pplx_sdk/transport/` | `core/`, `shared/` | HTTP/SSE backends |
| Domain | `pplx_sdk/domain/` | `core/`, `shared/`, `transport/` | Business logic services |
| Client | `pplx_sdk/client.py` | All layers | High-level API |

## Source File Template

```python
"""Module description."""

from __future__ import annotations

from typing import Any, Dict, Optional

from pplx_sdk.core.exceptions import TransportError


class NewComponent:
    """Component description.

    Example:
        >>> component = NewComponent(base_url="https://api.example.com")
        >>> result = component.execute()
    """

    def __init__(
        self,
        base_url: str,
        auth_token: Optional[str] = None,
        timeout: float = 30.0,
    ) -> None:
        """Initialize component.

        Args:
            base_url: Base URL for API requests
            auth_token: Authentication token
            timeout: Request timeout in seconds
        """
        self.base_url = base_url
        self.auth_token = auth_token
        self.timeout = timeout
```

## Test File Template

```python
"""Tests for new_component module."""

import pytest
from pplx_sdk.core.exceptions import TransportError


def test_new_component_initialization():
    component = NewComponent(base_url="https://api.test.com")
    assert component.base_url == "https://api.test.com"
    assert component.timeout == 30.0


def test_new_component_error_handling():
    component = NewComponent(base_url="https://invalid.test")
    with pytest.raises(TransportError):
        component.execute()
```

## Checklist

- [ ] `from __future__ import annotations` at top
- [ ] Complete type annotations on all functions
- [ ] Google-style docstrings on public APIs
- [ ] Custom exceptions from `pplx_sdk.core.exceptions`
- [ ] Tests with Arrange-Act-Assert pattern
- [ ] `__init__.py` exports updated

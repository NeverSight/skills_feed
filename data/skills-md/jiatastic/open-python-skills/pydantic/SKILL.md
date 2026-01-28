---
name: pydantic
description: >
  Pydantic models and validation. Use when: (1) Defining schemas,
  (2) Validating input/output, (3) Generating JSON schema.
---

# pydantic

Type-driven validation and serialization using Pydantic models.

## Overview

Pydantic validates data using Python type hints and provides rich serialization via `model_dump()` and JSON schema output.

## When to Use

- Validating request/response payloads
- Normalizing untrusted input
- Generating JSON schema for docs

## Quick Start

```bash
uv pip install pydantic
```

```python
from pydantic import BaseModel

class User(BaseModel):
    id: int
    email: str

user = User(id=1, email="a@example.com")
```

## Core Patterns

1. **Typed fields**: strict schema definitions.
2. **Field validators**: custom validation logic.
3. **Model validators**: cross-field checks.
4. **Serialization**: `model_dump()` and `model_dump_json()`.
5. **Settings**: environment-driven config via `BaseSettings`.

## Example: field_validator

```python
from pydantic import BaseModel, field_validator

class Model(BaseModel):
    name: str

    @field_validator("name")
    @classmethod
    def ensure_not_empty(cls, v: str):
        if not v:
            raise ValueError("name required")
        return v
```

## Example: model_validate + model_dump

```python
from pydantic import BaseModel

class Model(BaseModel):
    foo: int

model = Model.model_validate({"foo": 1})
print(model.model_dump())
```

## Troubleshooting

- **Coercion surprises**: use strict types if needed
- **Slow validators**: keep them minimal
- **Mutable defaults**: use `default_factory`

## References

- https://docs.pydantic.dev/

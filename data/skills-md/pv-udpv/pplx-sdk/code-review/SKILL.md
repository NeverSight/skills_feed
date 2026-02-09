---
name: code-review
description: Review code changes against pplx-sdk architecture conventions, type safety, error handling, and testing standards.
context: fork
agent: code-reviewer
---

# code-review

Review code changes following pplx-sdk project standards and the layered architecture.

## When to use

Use this skill when reviewing pull requests or code changes in the pplx-sdk repository to ensure compliance with project conventions.

## Instructions

1. **Check architecture layer compliance**: Verify imports respect `core → shared → transport/domain → client` dependency flow. No circular imports allowed.
2. **Verify type safety**: All functions must have complete type annotations. Use `from __future__ import annotations` at the top of every module.
3. **Validate error handling**: Custom exceptions from `pplx_sdk.core.exceptions` must be used — never bare `Exception`. Chain exceptions with `from exc`.
4. **Review docstrings**: Google-style docstrings required on all public classes and methods, including Args, Returns, Raises sections.
5. **Check test coverage**: Tests follow Arrange-Act-Assert pattern with descriptive names (`test_<module>_<behavior>`).
6. **Inspect Pydantic models**: Domain models use Pydantic v2 `BaseModel` with `Field()` descriptions.
7. **Verify transport protocol**: Transport implementations conform to the `Transport` protocol from `pplx_sdk.core.protocols`.

## Architecture Layer Rules

```
core/        → No imports from other pplx_sdk modules
shared/      → May import from core/ only
transport/   → May import from core/, shared/
domain/      → May import from core/, shared/, transport/
client.py    → May import from all layers
```

## Exception Hierarchy

```
PerplexitySDKError (base)
├── TransportError (status_code, response_body)
│   ├── AuthenticationError (401)
│   └── RateLimitError (429, retry_after)
├── StreamingError
└── ValidationError
```

## Output Format

For each file reviewed, provide:
- ✅ Passes — or
- ❌ Issue found: description and suggested fix

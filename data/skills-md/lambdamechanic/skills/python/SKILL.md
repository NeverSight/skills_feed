---
name: python
description: "Default Python stack for Lambda: uv + Astral tools, typed code, schemas, and Hypothesis."
---

# Python Workflow

Use this skill when working on Python projects or adding Python support.

## Tooling baseline
- Use `uv` for environments, dependency management, and running commands.
- Prefer Astral tooling for quality gates: `ruff` for lint/format and `ty` for type checking.
- Favor strict typing everywhere; avoid `Any` unless the boundary truly requires it.

## Typing and schemas
- Type every function signature (params + return) and keep types narrow.
- Use Pydantic models for inputs, outputs, and configuration schemas.
- Prefer typed collections and `typing_extensions` for newer typing features.

## Testing
- Write tests with `pytest` and property tests with `hypothesis` when behavior is stateful or rule-based.
- Add coverage checks (e.g., pytest-cov) and keep coverage green for new code paths.

## Packaging
- Structure the code as a releasable PyPI package.
- Use a `pyproject.toml` with build metadata, versioning, and a `src/` layout.
- Ensure imports and entrypoints work when installed from a wheel.

## Quality gates
- Run formatting last.
- Keep linting, type checking, and tests passing before closing work.

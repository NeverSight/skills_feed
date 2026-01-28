---
name: python
description: Python development guidelines and best practices. Use when working with Python code.
---

# Python Guidelines

Standards and best practices for Python development. Follow these guidelines when writing or modifying Python code.

## Design Principles

Apply DRY, KISS, and SOLID consistently. Prefer functional methods where relevant; use classes for stateful behavior. Use composition with Protocol classes for interfaces rather than inheritance. Each module should have a single responsibility. Use dependency injection for class dependencies.

## Code Style

- **Naming**: Descriptive yet concise names for variables, methods, and classes
- **Documentation**: Docstrings for all classes, functions, enums, enum values
- **Type hints**: Use consistently; avoid `Any` unless necessary
- **Imports**: Avoid barrel exports in `__init__.py`; prefer blank files

## Type Annotations

- Use `dict`, `list` instead of `typing.Dict`, `typing.List`
- Use `str | None` instead of `Optional[str]`
- Include `from __future__ import annotations` at top of files with type hints
- Prefer built-in types over typing module equivalents

## Architecture

### Dependency Injection

- Always inject dependencies via constructors or methods when using classes
- One service class per module (interface and class models allowed in addition)
- Use Protocol classes to define interfaces for dependency injection and testing

### Module Organization

- Each module focuses on one concern with clear boundaries
- Extract reusable methods to avoid duplication
- Design for reusability across contexts

### Environment Variables

- Use an `environment.py` file with individual methods per variable (e.g., `api_key()` for `API_KEY`, `database_url()` for `DATABASE_URL`)
- Co-locate all environment access in one place per package for easier mocking in tests

### Data Models

- Use Pydantic v2 for schemas, validation, and data models
- Leverage Pydantic's type validation, serialization, and configuration management
- Use Pydantic models for API request/response schemas, configuration objects, and data transfer objects

## Testing

### Structure

- Tests mirror `src/` directory structure
- Test methods start with `test_`
- Use test class suites: for `def foo()` create `class TestFoo`
- Keep names concise, omit class suite name from method
- Always check for appropriate unit tests when changing code

### Quality

- Use AAA (Arrange, Act, Assert) pattern
- Tests should be useful, readable, concise, maintainable
- Avoid tests that create massive diffs or become burdensome

### Tools

- Prefer `pytest` over `unittest`
- Use `pytest-mock` for mocking
- Use `conftest.py` for shared fixtures
- Use `tests/__test_<package_name>__` for shared testing code

## Implementation

When implementing Python code:
- Ensure code passes type checking and tests before committing
- Group related changes with tests in atomic commits
- Check for existing workflow patterns (spec-first, TDD, etc.) and follow them

## References

- For adhoc Python scripts in uv-managed projects, see `references/uv-scripts.md`.
- For monorepo-specific patterns using uv and Hatch, see `references/uv-monorepo.md`.

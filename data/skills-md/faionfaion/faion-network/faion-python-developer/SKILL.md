---
name: faion-python-developer
description: "Python development: Django, FastAPI, async patterns, testing, type hints."
user-invocable: false
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Task, AskUserQuestion, TodoWrite, Skill
---
> **Entry point:** `/faion-net` — invoke this skill for automatic routing to the appropriate domain.

# Python Developer Skill

Python development specializing in Django, FastAPI, async programming, and modern Python patterns.

## Purpose

Handles all Python backend development including Django full-stack apps, FastAPI async APIs, pytest testing, and Python best practices.

## When to Use

- Django projects (models, services, API, testing)
- FastAPI async APIs
- Python async patterns and concurrency
- Python type hints and strict typing
- Python testing with pytest
- Python code quality and tooling

## Methodologies

| Category | Methodology | File |
|----------|-------------|------|
| **Django Core** |
| Django standards | Django coding standards, project structure | django-coding-standards.md |
| Django models | Model design, base model patterns | django-base-model.md |
| Django models reference | Model fields, managers, migrations | django-models.md |
| Django services | Service layer architecture | django-services.md |
| Django API | DRF patterns, serializers, viewsets | django-api.md |
| Django testing | Django test patterns, factories | django-testing.md |
| Django pytest | pytest-django, fixtures, parametrize | django-pytest.md |
| Django celery | Async tasks, queues, beat | django-celery.md |
| Django quality | Code quality, linting, formatting | django-quality.md |
| Django imports | Import organization, circular imports | django-imports.md |
| Django decision tree | Framework selection, when to use Django | django-decision-tree.md |
| Django decomposition | Breaking down Django monoliths | decomposition-django.md |
| **FastAPI** |
| FastAPI basics | Routes, dependencies, validation | python-fastapi.md |
| Web frameworks | Django vs FastAPI vs Flask comparison | python-web-frameworks.md |
| **Async Python** |
| Async basics | asyncio, await, event loop | python-async.md |
| Async patterns | Concurrent patterns, asyncio best practices | python-async-patterns.md |
| **Type Safety** |
| Type hints | Gradual typing, annotations | python-type-hints.md |
| Python typing | TypedDict, Protocol, Generic | python-typing.md |
| **Testing** |
| pytest basics | Fixtures, parametrize, markers | python-testing-pytest.md |
| **Python Core** |
| Python basics | Language fundamentals, patterns | python-basics.md |
| Python overview | Quick reference | python.md |
| Python modern 2026 | Python 3.12/3.13 features | python-modern-2026.md |
| Python code quality | ruff, mypy, black, isort | python-code-quality.md |
| Poetry setup | Dependency management, pyproject.toml | python-poetry-setup.md |

## Tools

- **Frameworks:** Django 5.x, FastAPI 0.1x, Flask
- **Testing:** pytest, pytest-django, pytest-asyncio, factory-boy
- **Type checking:** mypy, pyright
- **Linting:** ruff, flake8, pylint
- **Formatting:** black, isort
- **Package management:** poetry, pip-tools, uv

## Related Sub-Skills

| Sub-skill | Relationship |
|-----------|--------------|
| faion-backend-developer | Database patterns (PostgreSQL, Redis) |
| faion-api-developer | REST/GraphQL API design |
| faion-testing-developer | Advanced testing patterns |
| faion-devtools-developer | Architecture patterns, code quality |

## Integration

Invoked by parent skill `faion-software-developer` when working with Python code.

---

*faion-python-developer v1.0 | 24 methodologies*

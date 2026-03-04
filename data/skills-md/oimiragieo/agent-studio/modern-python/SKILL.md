---
name: modern-python
description: Modern Python tooling best practices using uv, ruff, ty, and pytest. Mandates the Trail of Bits Python coding standards for project setup, dependency management, linting, type checking, and testing. Based on patterns from trailofbits/cookiecutter-python.
version: 1.1.0
category: Languages
agents: [python-pro, developer, fastapi-pro]
tags:
  [python, uv, ruff, ty, pytest, tooling, linting, formatting, type-checking, dependency-management]
model: sonnet
invoked_by: both
user_invocable: true
tools: [Read, Write, Bash, Glob, Grep]
args: '[--init] [--migrate] [--check] [--fix]'
best_practices:
  - Always use uv for dependency management instead of pip/Poetry/pipenv
  - Use ruff for both linting and formatting instead of separate tools
  - Use ty for type checking instead of mypy (faster, Rust-based)
  - Structure tests with pytest and use hypothesis for property-based testing
  - Configure all tools in pyproject.toml, never in separate config files
error_handling: graceful
streaming: supported
verified: true
lastVerifiedAt: '2026-03-01'
---

# Modern Python Skill

<!-- Agent: evolution-orchestrator | Task: #2 | Session: 2026-02-21 -->
<!-- License: CC-BY-SA-4.0 | Source: Trail of Bits (github.com/trailofbits/skills) -->
<!-- Attribution: Adapted from Trail of Bits modern-python skill and trailofbits/cookiecutter-python -->

<identity>
Modern Python tooling skill adapted from Trail of Bits coding standards. Mandates the use of uv (package management), ruff (linting and formatting), ty (type checking), and pytest (testing) as the standard Python toolchain. Based on patterns from trailofbits/cookiecutter-python for consistent, high-quality Python projects.
</identity>

<capabilities>
- Project initialization with modern Python toolchain (uv + ruff + ty + pytest)
- Migration from legacy tools (pip/Poetry/pipenv to uv, black/flake8/isort to ruff, mypy to ty)
- pyproject.toml configuration for all tools (single source of truth)
- Dependency management with uv (lock files, dependency groups, virtual environments)
- Linting and formatting with ruff (replaces flake8, isort, black, pyflakes, pycodestyle)
- Type checking with ty (Rust-based, faster than mypy)
- Testing with pytest, pytest-cov, and hypothesis
- CI/CD configuration with GitHub Actions
- Dependabot setup for automated dependency updates
- Pre-commit hook configuration
</capabilities>

## Overview

This skill implements Trail of Bits' modern Python coding standards for the agent-studio framework. The core philosophy is: **use Rust-based tools for faster feedback loops, especially when working with AI agents**. Every tool in this stack (uv, ruff, ty) is written in Rust and provides sub-second execution times, enabling tight iteration cycles.

**Source repository**: `https://github.com/trailofbits/skills`
**Template**: `https://github.com/trailofbits/cookiecutter-python`
**License**: CC-BY-SA-4.0

## When to Use

- When creating new Python projects from scratch
- When migrating Python projects from legacy tooling
- When setting up CI/CD pipelines for Python projects
- When standardizing Python tooling across a team
- When writing standalone Python scripts that need proper structure
- When an AI agent needs fast feedback from Python tooling

## Iron Laws

1. **ALWAYS** configure all Python tooling in `pyproject.toml` -- no separate config files (`setup.cfg`, `.flake8`, `mypy.ini`, `black.toml`) are permitted.
2. **ALWAYS** use `uv add`/`uv remove` for dependency management -- never use bare `pip install` in projects managed by uv.
3. **NEVER** commit `venv/`, `.venv/`, or pip-generated `requirements.txt` -- commit `uv.lock` for reproducible builds.
4. **ALWAYS** use `uv run` to execute tools and scripts -- this ensures the correct virtual environment and dependency resolution.
5. **NEVER** use legacy linting/formatting tools (flake8, black, isort, mypy) when ruff and ty are available -- consolidate to the Rust-based stack for speed and consistency.

## Anti-Patterns

| Anti-Pattern                                                    | Why It Fails                                                                        | Correct Approach                                                                      |
| --------------------------------------------------------------- | ----------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------- |
| Using `pip install` directly in a uv-managed project            | Bypasses lockfile and dependency resolution; creates reproducibility drift          | Use `uv add <pkg>` to add dependencies and `uv sync` to install                       |
| Maintaining `.flake8`, `mypy.ini`, or `black.toml` config files | Fragments configuration across multiple files; hard to maintain and audit           | Consolidate all tool config into `pyproject.toml` under `[tool.ruff]` and `[tool.ty]` |
| Running `python script.py` instead of `uv run python script.py` | Uses system Python instead of project venv; dependency mismatches                   | Always use `uv run` to execute within the managed environment                         |
| Globally installing CLI tools with `pip install --user`         | Pollutes global environment; version conflicts across projects                      | Use `uv tool run <tool>` or `uvx <tool>` for one-off tool execution                   |
| Ignoring ruff security rules (`S` select)                       | Misses bandit-equivalent security checks like hardcoded passwords and SQL injection | Enable `select = ["S"]` in `[tool.ruff.lint]` for security linting                    |

## The Modern Python Stack

| Tool           | Replaces                                                | Purpose                      | Speed          |
| -------------- | ------------------------------------------------------- | ---------------------------- | -------------- |
| **uv**         | pip, Poetry, pipenv, pip-tools                          | Package & project management | 10-100x faster |
| **ruff**       | flake8, isort, black, pyflakes, pycodestyle, pydocstyle | Linting + formatting         | 10-100x faster |
| **ty**         | mypy, pyright, pytype                                   | Type checking                | 5-10x faster   |
| **pytest**     | unittest                                                | Testing                      | --             |
| **hypothesis** | (manual property tests)                                 | Property-based testing       | --             |

## Project Setup

### New Project

```bash
# Create new project with uv
uv init my-project
cd my-project

# Add dependency groups
uv add --group dev ruff ty
uv add --group test pytest pytest-cov hypothesis
uv add --group docs sphinx myst-parser

# Install all dependencies
uv sync --all-groups
```

### pyproject.toml Configuration

```toml
[project]
name = "my-project"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = []

[dependency-groups]
dev = ["ruff", "ty"]
test = ["pytest", "pytest-cov", "hypothesis"]
docs = ["sphinx", "myst-parser"]

# === Ruff Configuration ===
[tool.ruff]
target-version = "py312"
line-length = 100

[tool.ruff.lint]
select = [
    "E",      # pycodestyle errors
    "W",      # pycodestyle warnings
    "F",      # pyflakes
    "I",      # isort
    "N",      # pep8-naming
    "UP",     # pyupgrade
    "B",      # flake8-bugbear
    "A",      # flake8-builtins
    "C4",     # flake8-comprehensions
    "SIM",    # flake8-simplify
    "S",      # flake8-bandit (security)
    "TCH",    # flake8-type-checking
    "RUF",    # ruff-specific rules
]

[tool.ruff.lint.per-file-ignores]
"tests/**/*.py" = ["S101"]  # Allow assert in tests

[tool.ruff.format]
quote-style = "double"
indent-style = "space"

# === Pytest Configuration ===
[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = [
    "--strict-markers",
    "--strict-config",
    "-ra",
]

[tool.coverage.run]
source = ["src"]
branch = true

[tool.coverage.report]
fail_under = 80
show_missing = true
exclude_lines = [
    "if TYPE_CHECKING:",
    "if __name__ == .__main__.:",
]
```

## Daily Workflow Commands

### Package Management (uv)

```bash
# Add a dependency
uv add requests

# Add a dev dependency
uv add --group dev ipdb

# Remove a dependency
uv remove requests

# Update all dependencies
uv lock --upgrade

# Update a specific dependency
uv lock --upgrade-package requests

# Run a script in the project environment
uv run python script.py

# Run a tool (without installing globally)
uv run --with httpie http GET https://api.example.com
```

### Linting and Formatting (ruff)

```bash
# Check for lint errors
uv run ruff check .

# Auto-fix lint errors
uv run ruff check --fix .

# Format code
uv run ruff format .

# Check formatting (dry run)
uv run ruff format --check .

# Check specific rules
uv run ruff check --select S .  # Security rules only
```

### Type Checking (ty)

```bash
# Run type checker
uv run ty check

# Check specific file
uv run ty check src/main.py
```

### Testing (pytest)

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov

# Run specific test file
uv run pytest tests/test_auth.py

# Run with verbose output
uv run pytest -v

# Run and stop at first failure
uv run pytest -x
```

## Migration Guide

### From pip/requirements.txt

```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Initialize project from existing requirements
uv init
uv add $(cat requirements.txt | grep -v '^#' | grep -v '^$')

# Remove old files
rm requirements.txt requirements-dev.txt
```

### From Poetry

```bash
# uv can read pyproject.toml with Poetry sections
uv init

# Move Poetry dependencies to [project.dependencies]
# Move [tool.poetry.group.dev.dependencies] to [dependency-groups]
# Remove [tool.poetry] section

uv sync
```

### From flake8/black/isort to ruff

```bash
# Remove old tools
uv remove flake8 black isort pyflakes pycodestyle

# Add ruff
uv add --group dev ruff

# Convert .flake8 config to ruff (manual)
# ruff supports most flake8 rules with same codes

# Remove old config files
rm .flake8 .isort.cfg pyproject.toml.bak
```

### From mypy to ty

```bash
# Remove mypy
uv remove mypy

# Add ty
uv add --group dev ty

# ty uses the same type annotation syntax as mypy
# Most code requires no changes
```

## CI/CD Configuration

### GitHub Actions

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v4
        with:
          enable-cache: true

      - name: Install dependencies
        run: uv sync --all-groups

      - name: Lint
        run: uv run ruff check .

      - name: Format check
        run: uv run ruff format --check .

      - name: Type check
        run: uv run ty check

      - name: Test
        run: uv run pytest --cov --cov-report=xml

      - name: Upload coverage
        uses: codecov/codecov-action@v4
        with:
          file: coverage.xml
```

### Dependabot Configuration

```yaml
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: 'uv'
    directory: '/'
    schedule:
      interval: 'weekly'
    groups:
      all:
        patterns:
          - '*'
```

## Pre-commit Hooks

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.9.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
```

## Code Patterns

### Type Annotations

```python
from __future__ import annotations

from collections.abc import Sequence
from typing import TypeAlias

# Use modern syntax (Python 3.12+)
type Vector = list[float]  # Type alias (PEP 695)

def process_items(items: Sequence[str], *, limit: int = 10) -> list[str]:
    """Process items with a limit."""
    return [item.strip() for item in items[:limit]]

# Use | instead of Union
def maybe_int(value: str) -> int | None:
    try:
        return int(value)
    except ValueError:
        return None
```

### Project Structure

```
my-project/
  pyproject.toml          # Single config file for all tools
  uv.lock                 # Locked dependencies (commit this)
  src/
    my_project/
      __init__.py
      main.py
      models.py
      utils.py
  tests/
    __init__.py
    test_main.py
    test_models.py
    conftest.py           # Shared fixtures
  .github/
    workflows/
      ci.yml
    dependabot.yml
  .pre-commit-config.yaml
```

## Common Pitfalls

1. **Using pip directly**: Always use `uv add` / `uv remove` / `uv run`. Never `pip install`.
2. **Separate config files**: All configuration goes in `pyproject.toml`. Delete `.flake8`, `mypy.ini`, `black.toml`.
3. **Global installs**: Use `uv run` or `uv tool run` instead of globally installing CLI tools.
4. **Missing lock file**: Always commit `uv.lock` for reproducible builds.
5. **Old Python syntax**: Use `ruff --select UP` to auto-upgrade to modern syntax (match statements, `|` unions, etc.).
6. **Ignoring security rules**: Enable `S` (bandit) rules in ruff to catch security issues.

## Integration with Agent-Studio

### Recommended Workflow

1. Use `modern-python` to set up or migrate Python projects
2. Use `python-backend-expert` for framework-specific patterns (Django, FastAPI)
3. Use `tdd` skill for test-driven development workflow
4. Use `comprehensive-unit-testing-with-pytest` for test strategy

### Complementary Skills

| Skill                                    | Relationship                                         |
| ---------------------------------------- | ---------------------------------------------------- |
| `python-backend-expert`                  | Framework-specific patterns (Django, FastAPI, Flask) |
| `comprehensive-unit-testing-with-pytest` | Testing strategies and patterns                      |
| `comprehensive-type-annotations`         | Type annotation best practices                       |
| `prioritize-python-3-10-features`        | Modern Python language features                      |
| `tdd`                                    | Test-driven development methodology                  |
| `property-based-testing`                 | Hypothesis-based testing patterns                    |

## Memory Protocol

**Before starting**: Check if the project already has Python tooling configured. Identify which legacy tools need migration.

**During setup**: Write configuration incrementally, verifying each tool works before moving to the next. Run `ruff check`, `ruff format --check`, and `uv run pytest` at each step.

**After completion**: Record the toolchain versions and any migration issues to `.claude/context/memory/learnings.md` for future reference.

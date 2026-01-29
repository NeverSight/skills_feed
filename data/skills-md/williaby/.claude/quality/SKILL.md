---
name: quality
description: Code quality validation, formatting, linting, and pre-commit checks. Auto-activates on keywords quality, lint, format, precommit, naming, black, ruff, mypy, validation. Routes to specialized quality workflows.
allowed-tools: Read, Bash(poetry:*, black:*, ruff:*, mypy:*, markdownlint:*, yamllint:*), Grep, Task
---

# Quality Skill

Comprehensive code quality domain for formatting, linting, type checking, and pre-commit validation. Provides automated quality workflows with intelligent routing.

## Auto-Activation Keywords

This skill activates automatically when you mention:
- **General**: quality, code quality, validation, standards
- **Formatting**: format, formatting, black, prettier
- **Linting**: lint, linting, ruff, eslint
- **Type checking**: type check, mypy, types
- **Pre-commit**: precommit, pre-commit, validate
- **Naming**: naming conventions, naming, PEP 8

## Routing Logic

Based on user intent, routes to appropriate workflows:

### Code Formatting
**Keywords**: "format code", "black", "apply formatting"
→ Use `/quality/format` workflow

### Linting
**Keywords**: "lint code", "ruff", "check linting"
→ Use `/quality/lint` workflow

### Pre-commit Validation
**Keywords**: "validate before commit", "precommit check", "ready to commit"
→ Use `/quality/precommit` workflow

### Naming Conventions
**Keywords**: "check naming", "naming conventions", "PEP 8"
→ Use `/quality/naming` workflow

## Workflow Quick Reference

```bash
# Format code
/quality/format [path]

# Lint code
/quality/lint [path]

# Pre-commit validation
/quality/precommit [--fix]

# Check naming conventions
/quality/naming [path]
```

## Complex Task Delegation

For comprehensive code review, invoke the `code-reviewer` agent via Task tool.

## Supporting Context

- Linting standards: `/standards/linting.md`
- Python standards: `/standards/python.md`

## Integration Points

### Agents
- **code-reviewer**: Comprehensive code quality analysis

### Hooks
- TDD enforcement on Write/Edit operations

### Standards
- Python standards: `/standards/python.md` (Black 88 chars, Ruff, MyPy)
- Linting standards: `/standards/linting.md` (configuration)

## Quality Requirements Summary

**Required for all Python projects:**
- Black formatting (88-character line length)
- Ruff linting (passes with --fix applied)
- MyPy type checking (passes for src/)
- 80%+ test coverage
- Pre-commit hooks pass

**Standard tools:**
```bash
# Format
poetry run black src tests

# Lint  
poetry run ruff check --fix src tests

# Type check
poetry run mypy src

# Full validation
poetry run pre-commit run --all-files
```

---

*This skill consolidates 6 quality commands and 2 validation skills into a unified quality domain.*

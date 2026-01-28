---
name: ruff-formatter
description: >-
  Fix Python code formatting issues using the Ruff formatter. Use when: (1)
  Formatting errors are detected by ruff format --check, (2) Python files need
  to be formatted to match project style, (3) Pre-commit hooks or CI fail due
  to formatting issues.
---

# Ruff Formatter

Fast Python code formatter, drop-in replacement for Black with >99.9% compatibility.

## Quick Reference

```bash
# Format all files in current directory
ruff format .

# Format specific file(s)
ruff format path/to/file.py

# Check without modifying (CI/pre-commit)
ruff format --check .

# Show diff of what would change
ruff format --diff .
```

## Fixing Formatting Issues

When `ruff format --check` fails:

1. Run `ruff format .` to auto-fix all formatting
2. Review changes with `git diff`
3. Commit the formatted code

For import sorting issues, run linter first:
```bash
ruff check --select I --fix .  # Sort imports
ruff format .                   # Then format
```

## Format Suppression

Disable formatting for specific code:

```python
# fmt: off
matrix = [
    [1, 0, 0],
    [0, 1, 0],
    [0, 0, 1],
]
# fmt: on

x = 1  # fmt: skip
```

## Configuration

In `pyproject.toml` or `ruff.toml`:

```toml
[tool.ruff.format]
quote-style = "double"      # or "single"
indent-style = "space"      # or "tab"
line-length = 88            # default
docstring-code-format = true
```

## Exit Codes

- **0**: Success (files formatted or already formatted)
- **1**: With `--check`: files need formatting
- **2**: Error (invalid config, CLI error)

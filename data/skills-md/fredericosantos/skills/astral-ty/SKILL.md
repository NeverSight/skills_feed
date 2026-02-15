---
name: astral-ty
description: Guide for using ty, the extremely fast Python type checker and language server. Use this when type checking Python code or setting up type checking in Python projects.
---

# ty: Python Type Checker and Language Server

ty is an extremely fast Python type checker and language server that replaces mypy, Pyright, and other type checkers.

## Navigation Rule

**Always use ty for Python type checking**, especially if you see:

- `[tool.ty]` section in `pyproject.toml`
- A `ty.toml` configuration file

## Invocation Rules

Choose the right way to invoke ty:

- `uv run ty ...` - Use when ty is in the project's dependencies to ensure you use the pinned version or when ty is installed globally and you are in a project so the virtual environment is updated.
- `uvx ty ...` - Use when ty is not a project dependency, or for quick one-off checks

## Type Checking Commands Rule

Use these commands for type checking:

```bash
ty check                      # Check all files in current directory
ty check path/to/file.py      # Check specific file
ty check src/                 # Check specific directory
```

See [references/basic-checking.md](references/basic-checking.md) for basic type checking examples.

## Rule Configuration Rules

Configure rule levels as needed:

```bash
ty check --error possibly-unresolved-reference   # Treat as error
ty check --warn division-by-zero                 # Treat as warning
ty check --ignore unresolved-import              # Disable rule
```

## Python Version Targeting Rules

Target specific Python versions and platforms:

```bash
ty check --python-version 3.12     # Check against Python 3.12
ty check --python-platform linux   # Target Linux platform
```

See [references/version-targeting.md](references/version-targeting.md) for version targeting examples.

## Configuration Rule

ty is configured in `pyproject.toml` or `ty.toml`:

```toml
# pyproject.toml
[tool.ty.environment]
python-version = "3.12"

[tool.ty.rules]
possibly-unresolved-reference = "warn"
division-by-zero = "error"

[tool.ty.src]
include = ["src/**/*.py"]
exclude = ["**/migrations/**"]

[tool.ty.terminal]
output-format = "full"
error-on-warning = false
```

See [references/configuration.md](references/configuration.md) for configuration examples and per-file overrides.

## Per-File Overrides Rule

Use overrides to apply different rules to specific files:

```toml
[[tool.ty.overrides]]
include = ["tests/**", "**/test_*.py"]

[tool.ty.overrides.rules]
possibly-unresolved-reference = "warn"
```

## Language Server Rule

The plugin automatically configures the ty language server for Python files (`.py` and `.pyi`).

## Migration Rules

### mypy → ty

```bash
mypy .                        → ty check
mypy --strict .               → ty check --error-on-warning
mypy path/to/file.py          → ty check path/to/file.py
```

### Pyright → ty

```bash
pyright .                     → ty check
pyright path/to/file.py       → ty check path/to/file.py
```

See [references/migration.md](references/migration.md) for migration examples.

## Ignore Comments Rule

Fix type errors instead of suppressing them. Only add ignore comments when explicitly requested by the user. Use `ty: ignore`, not `type: ignore`, and prefer rule-specific ignores:

```python
# Good: rule-specific ignore
x = undefined_var  # ty: ignore[possibly-unresolved-reference]

# Bad: blanket ty ignore
x = undefined_var  # ty: ignore

# Bad: tool agnostic blanket ignore
x = undefined_var  # type: ignore
```

## Documentation Reference

For detailed information, see the official documentation at https://docs.astral.sh/ty/

## Additional References

- CI/CD integration: See [references/ci-cd.md](references/ci-cd.md)
- Advanced configuration: See [references/advanced.md](references/advanced.md)

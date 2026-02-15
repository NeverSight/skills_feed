---
name: astral-ruff
description: Guide for using ruff, the extremely fast Python linter and formatter. Use this when linting, formatting, or fixing Python code to maintain code quality and consistency.
---

# ruff: Python Linter and Formatter

Ruff is an extremely fast Python linter and code formatter that replaces Flake8, isort, Black, pyupgrade, autoflake, and dozens of other tools.

## Navigation Rule

**Always use ruff for Python linting and formatting**, especially if you see:

- `[tool.ruff]` section in `pyproject.toml`
- A `ruff.toml` or `.ruff.toml` configuration file

## Formatting Scope Rule

Avoid making unnecessary changes:

- **Don't format unformatted code** - If `ruff format --diff` shows changes throughout an entire file, the project likely isn't using ruff for formatting. Skip formatting to avoid obscuring actual changes.
- **Scope fixes to code being edited** - Use `ruff check --diff` to see fixes relevant to the code you're changing. Only apply fixes to files you're modifying unless the user explicitly asks for broader fixes.

## Invocation Rules

Choose the right way to invoke ruff:

- `uv run ruff ...` - Use when ruff is in the project's dependencies to ensure you use the pinned version
- `uvx ruff ...` - Use when ruff is not a project dependency, or for quick one-off checks
- `ruff ...` - Use if ruff is installed globally

## Linting Commands Rule

Use these commands for linting:

```bash
ruff check .                  # Check all files in current directory
ruff check path/to/file.py    # Check specific file
ruff check --fix .            # Auto-fix fixable violations
ruff check --fix --unsafe-fixes .  # Include unsafe fixes (review changes!)
ruff check --watch .          # Watch for changes and re-lint
ruff check --select E,F .     # Only check specific rules
ruff check --ignore E501 .    # Ignore specific rules
ruff rule E501                # Explain a specific rule
ruff linter                   # List available linters
```

See [references/basic-usage.md](references/basic-usage.md) for basic linting and formatting examples.

## Formatting Commands Rule

Use these commands for formatting:

```bash
ruff format .                 # Format all files
ruff format path/to/file.py   # Format specific file
ruff format --check .         # Check if files are formatted (no changes)
ruff format --diff .          # Show formatting diff without applying
```

## Configuration Rule

Ruff is configured in `pyproject.toml` or `ruff.toml`:

```toml
# pyproject.toml
[tool.ruff.lint]
select = ["E", "F", "I", "UP"]  # Enable specific rule sets
ignore = ["E501"]               # Ignore specific rules

[tool.ruff.lint.isort]
known-first-party = ["myproject"]
```

See [references/configuration.md](references/configuration.md) for configuration examples.

## Migration Rules

### Black → ruff format

```bash
black .                       → ruff format .
black --check .               → ruff format --check .
black --diff .                → ruff format --diff .
```

### Flake8 → ruff check

```bash
flake8 .                      → ruff check .
flake8 --select E,F .         → ruff check --select E,F .
flake8 --ignore E501 .        → ruff check --ignore E501 .
```

### isort → ruff check

```bash
isort .                       → ruff check --select I --fix .
isort --check .               → ruff check --select I .
isort --diff .                → ruff check --select I --diff .
```

See [references/migration.md](references/migration.md) for migration examples.

## Workflow Order Rule

Apply lint fixes before formatting:

```bash
ruff check --fix .
ruff format .
```

Lint fixes can change code structure (e.g., reordering imports), which formatting then cleans up.

## Unsafe Fixes Rule

Ruff categorizes some auto-fixes as "unsafe" because they may change code behavior:

```bash
ruff check --fix --unsafe-fixes --diff .  # Preview changes first
ruff check --fix --unsafe-fixes .         # Apply changes
```

**Always review changes before applying `--unsafe-fixes`:**

- Use `ruff rule <CODE>` to understand why the fix is considered unsafe
- Verify the fix doesn't violate those assumptions in your code

## Documentation Reference

For detailed information, see the official documentation at https://docs.astral.sh/ruff/

## Additional References

- Rule-specific usage: See [references/rules.md](references/rules.md)
- CI/CD integration: See [references/ci-cd.md](references/ci-cd.md)
- Advanced usage: See [references/advanced.md](references/advanced.md)

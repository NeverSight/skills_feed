---
name: uv
description: Initializes Python projects, manages dependencies, pins Python versions, and runs scripts with uv. Use when adding/removing packages, syncing environments, running tools with uvx, or building distributions.
---

# uv

Fast Python package and project manager with built-in virtual environment management.

## Project Setup

```bash
uv init my-app             # App project
uv init my-lib --lib      # Library project
uv init --script script.py # Standalone script
uv python pin 3.11        # Pin Python version
```

## Dependencies

```bash
uv add requests           # Add dependency
uv add --dev pytest       # Add dev dependency
uv add --optional ml scikit-learn  # Add optional
uv remove requests        # Remove dependency
uv tree                   # Show dependency tree
uv lock                   # Update lockfile only
uv export > requirements.txt  # Export to requirements.txt
```

## Virtual Environment

```bash
uv sync                   # Sync dependencies
uv sync --no-dev         # Skip dev deps
uv sync --all-extras     # Include all optional
uv sync --refresh        # Recreate venv
```

## Running Code

```bash
uv run python script.py   # Run script
uv run -m pytest         # Run module
uv run --with requests script.py  # Temp dependency
uv run --extra ml train.py  # Use optional deps
uv run --env-file .env script.py  # Load .env
```

## Python Management

```bash
uv python list           # List versions
uv python install 3.12   # Install version
uv python pin 3.11       # Set project version
uv python upgrade --all  # Upgrade all
```

## Tools

```bash
uvx ruff check .         # Run tool once
uv tool install ruff     # Install globally
uv tool list             # List tools
uv tool upgrade ruff     # Upgrade tool
```

## Building & Publishing

```bash
uv build                 # Build distributions
uv publish               # Publish to PyPI
```

## Project Versioning

```bash
uv version               # Show current version
uv version 1.2.3         # Set version
uv version --bump major  # Bump major version
uv version --bump minor  # Bump minor version
uv version --bump patch  # Bump patch version
```

## Code Formatting

```bash
uv format                # Format Python code
uv format --check        # Check formatting without changes
```

## Authentication

```bash
uv auth login            # Login to package index
uv auth logout           # Logout from package index
uv auth status           # Show authentication status
```

## pyproject.toml

```toml
[project]
name = "my-project"
version = "0.1.0"
requires-python = ">=3.9"
dependencies = ["requests>=2.31.0"]

[project.optional-dependencies]
ml = ["scikit-learn>=1.0.0"]

[dependency-groups]
dev = ["pytest>=7.0.0", "ruff>=0.1.0"]
```

## Tips

- `uv run` handles venv automatically
- Commit `uv.lock` for reproducibility
- Use `--with` for one-off dependencies
- `uvx` for running tools without install
- `uv sync --locked` in CI
- Tools are isolated from project deps
- Fast: 10-100x faster than pip

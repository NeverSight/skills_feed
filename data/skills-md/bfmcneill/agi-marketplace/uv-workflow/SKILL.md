---
name: uv-workflow
description: Use when creating Python projects, managing dependencies, or running Python scripts. Covers uv package manager commands, best practices, and common patterns for modern Python development.
---

# Python Development with uv

Modern Python project management using uv - the fast, Rust-powered package manager.

## When to Use This Skill

Use this skill when:
- **Creating new Python projects**
- **Managing dependencies** (adding, removing, updating)
- **Running Python scripts** in project context
- **Setting up CI/CD** for Python projects
- **Troubleshooting** virtual environment or dependency issues

## Why uv?

| Feature | uv | pip | Poetry |
|---------|-----|-----|--------|
| Speed | 10-100x faster | Baseline | 2-3x slower |
| Virtual envs | Automatic | Manual | Automatic |
| Lockfile | Cross-platform | None | Yes |
| Python version mgmt | Built-in | No | No |
| Dev dependencies | Groups | No | Yes |

## Quick Reference

### Project Setup
```bash
uv init                     # Create app project
uv init --package           # Create package (src/ layout)
uv init --lib               # Create library
```

### Dependencies
```bash
uv add requests             # Add dependency
uv add -d pytest            # Add dev dependency
uv add 'requests>=2.28'     # With version constraint
uv remove requests          # Remove dependency
uv lock --upgrade           # Update all dependencies
```

### Running Code
```bash
uv run python main.py       # Run script in project env
uv run pytest               # Run tools with dependencies
uvx ruff check .            # Run standalone tool (isolated)
```

### Environment
```bash
uv sync                     # Sync env with lockfile
uv sync --all-groups        # Include all dependency groups
uv python install 3.11      # Install Python version
uv python pin 3.11          # Pin project to version
```

## Critical Rules

### Always Use `uv run`

**Wrong** - bypasses project environment:
```bash
python main.py
pytest
```

**Correct** - uses project environment:
```bash
uv run python main.py
uv run pytest
```

### `uv run` vs `uvx`

| Command | Use For |
|---------|---------|
| `uv run pytest` | Tools that need your project code |
| `uvx ruff check` | Standalone tools (linters, formatters) |

**Gotcha**: `uvx pytest` won't see your project code!

## Project Structure

uv creates this automatically:
```
my-project/
├── .venv/              # Auto-created, git-ignored
├── .python-version     # Python version pin
├── pyproject.toml      # Project config
├── uv.lock             # Deterministic lockfile (commit this!)
└── src/                # Source code (if --package)
```

## Dependency Groups

```toml
# pyproject.toml
[project]
dependencies = ["requests", "click"]

[dependency-groups]
dev = ["pytest", "black", "ruff"]
docs = ["sphinx"]
test = ["pytest-cov"]
```

```bash
uv add -d pytest              # Add to dev group
uv add --group docs sphinx    # Add to named group
uv sync --group docs          # Install specific group
uv sync --all-groups          # Install all groups
```

## Reference Files

- `references/commands.md` - Complete command reference
- `references/workflows.md` - Common workflows and patterns
- `references/gotchas.md` - Important gotchas and troubleshooting

## Common Workflows

### New Project
```bash
uv init my-project
cd my-project
uv add requests click
uv add -d pytest black ruff
uv run python -c "print('Ready!')"
```

### Existing Project (clone)
```bash
git clone repo
cd repo
uv sync --all-groups    # Install from lockfile
uv run pytest           # Run tests
```

### Update Dependencies
```bash
uv lock --upgrade                    # Update all
uv lock --upgrade-package requests   # Update specific
uv sync                              # Apply updates
```

### Fresh Start (troubleshooting)
```bash
rm -rf .venv uv.lock
uv sync
```

## Files to Commit

| File | Commit? | Why |
|------|---------|-----|
| `pyproject.toml` | Yes | Project definition |
| `uv.lock` | Yes | Reproducible environments |
| `.python-version` | Yes | Python version consistency |
| `.venv/` | No | Local environment |

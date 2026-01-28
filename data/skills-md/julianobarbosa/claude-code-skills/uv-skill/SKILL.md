---
name: uv-skill
description: Guide for using uv - an extremely fast Python package and project manager written in Rust. Use when installing Python, managing virtual environments, adding dependencies, running scripts, building packages, or working with pyproject.toml. Replaces pip, pip-tools, pipx, poetry, pyenv, twine, and virtualenv.
uv-version: ">=0.5.x"
updated: 2025-01-15
---

# uv Skill

Extremely fast Python package and project manager by Astral (Ruff creators).

## Overview

uv is a single tool that replaces:

- **pip/pip-tools** - Package installation and dependency resolution
- **virtualenv/venv** - Virtual environment creation
- **pyenv** - Python version management
- **pipx** - Tool installation and execution
- **poetry/pdm** - Project and dependency management
- **twine** - Package publishing

**Key Features:**

- 10-100x faster than pip
- Universal lockfile (`uv.lock`) for reproducible builds
- Automatic Python version management
- Built-in tool execution (`uvx`)
- PEP 723 inline script dependencies
- Drop-in pip compatibility

## Quick Reference

| Task | Command |
|------|---------|
| New project | `uv init` |
| New library | `uv init --lib` |
| Add package | `uv add <pkg>` |
| Add dev dependency | `uv add --dev <pkg>` |
| Remove package | `uv remove <pkg>` |
| Install all deps | `uv sync` |
| Install (CI/prod) | `uv sync --locked` |
| Run command | `uv run <cmd>` |
| Run tool (no install) | `uvx <tool>` |
| Install Python | `uv python install 3.12` |
| Pin Python version | `uv python pin 3.12` |
| Update all deps | `uv lock --upgrade` |
| Update one package | `uv lock --upgrade-package <pkg>` |
| Show dep tree | `uv tree` |
| Build package | `uv build` |
| Publish to PyPI | `uv publish` |

## Quick Start

### Installation

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# Via pip/pipx
pipx install uv
pip install uv

# Homebrew
brew install uv
```

### Shell Completion

```bash
# Bash
echo 'eval "$(uv generate-shell-completion bash)"' >> ~/.bashrc

# Zsh
echo 'eval "$(uv generate-shell-completion zsh)"' >> ~/.zshrc

# Fish
echo 'uv generate-shell-completion fish | source' > ~/.config/fish/completions/uv.fish
```

## Essential Commands

### 1. Starting a Project

```bash
# Create new project
uv init my-project          # Application (default)
uv init --lib my-library    # Library (src layout, build backend)
uv init --app my-app        # Explicit application

# Set Python version
uv python pin 3.12          # Creates .python-version

# Install Python if needed
uv python install 3.12
```

### 2. Managing Dependencies

```bash
# Add packages
uv add requests flask       # Production dependencies
uv add --dev pytest ruff    # Development dependencies
uv add --group test pytest  # Specific dependency group
uv add --optional api flask # Optional extra
uv add "httpx>=0.20"        # With version constraint

# Remove packages
uv remove requests
uv remove --dev pytest

# Update packages
uv lock --upgrade                    # All packages
uv lock --upgrade-package requests   # Single package

# View dependencies
uv tree                     # Full tree
uv tree --depth 2           # Limited depth
```

### 3. Syncing Environment

```bash
# Install all dependencies
uv sync                     # Default (includes dev)
uv sync --locked            # CI/production (strict)
uv sync --frozen            # Don't update lockfile
uv sync --no-dev            # Exclude dev dependencies
uv sync --all-extras        # Include optional extras
```

### 4. Running Code

```bash
# Run in project environment
uv run python script.py
uv run pytest
uv run flask run

# Run with temporary dependency
uv run --with pandas script.py

# Run tools without installing (uvx)
uvx ruff check .
uvx black --check .
uvx --from httpie http https://example.com
```

### 5. Python Version Management

```bash
# Install Python versions
uv python install           # Latest version
uv python install 3.12      # Specific version
uv python install 3.11 3.12 3.13  # Multiple

# List versions
uv python list
uv python list --only-installed

# Pin version
uv python pin 3.12          # Project (.python-version)
uv python pin --global 3.12 # User default

# Find Python
uv python find
uv python find ">=3.11"
```

### 6. Virtual Environments

```bash
# Create (usually automatic)
uv venv                     # Creates .venv
uv venv my-env              # Custom name
uv venv --python 3.12       # Specific Python

# Activate (optional - uv run auto-detects)
source .venv/bin/activate   # macOS/Linux
.venv\Scripts\activate      # Windows
```

### 7. Global Tools

```bash
# Install tools globally
uv tool install ruff
uv tool install "ruff==0.5.0"
uv tool install --python 3.12 mypy

# Manage tools
uv tool list
uv tool upgrade ruff
uv tool upgrade --all
uv tool uninstall ruff

# Setup PATH
uv tool update-shell
```

### Scripts with Inline Dependencies (PEP 723)

```bash
# Initialize script with metadata
uv init --script example.py --python 3.12

# Add dependencies to script
uv add --script example.py requests rich

# Run script (dependencies auto-installed)
uv run example.py
```

Script format:

```python
# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "requests<3",
#   "rich",
# ]
# ///

import requests
from rich import print
print(requests.get("https://api.example.com").json())
```

### pip-Compatible Interface

```bash
# Install packages (requires virtual environment)
uv pip install flask
uv pip install -r requirements.txt
uv pip install -e .         # Editable install

# Uninstall
uv pip uninstall flask

# Compile requirements
uv pip compile requirements.in -o requirements.txt

# Sync from requirements
uv pip sync requirements.txt

# Freeze environment
uv pip freeze
```

### Building and Publishing

```bash
# Build distributions
uv build                    # Creates dist/ with wheel and sdist

# Publish to PyPI
uv publish                  # Requires authentication setup

# Authenticate
uv auth login pypi          # Interactive login
uv auth login pypi --token  # API token
```

## Project Structure

```text
my-project/
├── pyproject.toml          # Project definition (required)
├── uv.lock                 # Lock file (auto-generated)
├── .venv/                  # Virtual environment (gitignored)
├── .python-version         # Python version pin (optional)
└── src/
    └── my_project/
        └── __init__.py
```

### pyproject.toml Example

```toml
[project]
name = "my-project"
version = "0.1.0"
description = "My awesome project"
readme = "README.md"
requires-python = ">=3.11"
dependencies = [
    "requests>=2.28",
    "click>=8.0",
]

[project.optional-dependencies]
api = ["fastapi", "uvicorn"]
dev = ["pytest", "ruff"]

[project.scripts]
my-cli = "my_project.cli:main"

[dependency-groups]
dev = ["pytest>=8", "ruff", "mypy"]
test = ["pytest-cov"]
docs = ["sphinx", "myst-parser"]

[tool.uv]
dev-dependencies = ["pytest", "ruff"]  # Alternative to dependency-groups
default-groups = ["dev"]

[tool.uv.sources]
# Git dependency
my-lib = { git = "https://github.com/user/my-lib" }
# Local path
local-pkg = { path = "./packages/local-pkg" }
# Specific index
torch = { index = "pytorch" }

[[tool.uv.index]]
name = "pytorch"
url = "https://download.pytorch.org/whl/cpu"
explicit = true
```

## Configuration

### Configuration Files

**Project-level** (highest priority):

- `uv.toml` - Standalone config (preferred)
- `pyproject.toml` - Under `[tool.uv]` section

**User-level**:

- `~/.config/uv/uv.toml` (macOS/Linux)
- `%APPDATA%\uv\uv.toml` (Windows)

### Key Environment Variables

| Variable | Purpose |
|----------|---------|
| `UV_CACHE_DIR` | Cache directory location |
| `UV_PYTHON` | Default Python version |
| `UV_INDEX_URL` | Default package index |
| `UV_NO_CACHE` | Disable caching |
| `UV_FROZEN` | Use lockfile without updating |
| `UV_LOCKED` | Assert lockfile unchanged |
| `UV_COMPILE_BYTECODE` | Compile to .pyc files |
| `UV_LINK_MODE` | Package linking mode (copy, hardlink, symlink) |

## Common Workflows

### New Project Setup

```bash
# Create and enter project
uv init my-project
cd my-project

# Add dependencies
uv add flask sqlalchemy
uv add --dev pytest ruff mypy

# Run application
uv run flask run

# Run tests
uv run pytest
```

### Existing Project (from requirements.txt)

```bash
# Initialize uv project
uv init

# Import dependencies from requirements.txt
uv add $(cat requirements.txt | grep -v "^#" | tr '\n' ' ')

# Or use pip interface
uv venv
uv pip install -r requirements.txt
```

### CI/CD Pipeline

```yaml
# GitHub Actions
- uses: astral-sh/setup-uv@v7
  with:
    enable-cache: true
- run: uv sync --locked
- run: uv run pytest
```

```yaml
# GitLab CI
variables:
  UV_CACHE_DIR: .uv-cache
  UV_LINK_MODE: copy
image: ghcr.io/astral-sh/uv:latest
script:
  - uv sync --locked
  - uv run pytest
```

### Docker

```dockerfile
FROM python:3.12-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app
COPY pyproject.toml uv.lock ./

# Install dependencies only (for caching)
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-install-project

# Copy source and install project
COPY . .
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked

ENV PATH="/app/.venv/bin:$PATH"
CMD ["python", "-m", "my_app"]
```

### direnv Integration

```bash
# .envrc
if has uv; then
  VIRTUAL_ENV="$(pwd)/.venv"
  if [[ ! -d "$VIRTUAL_ENV" ]]; then
    uv venv
  fi
  PATH_add "$VIRTUAL_ENV/bin"
  export VIRTUAL_ENV
fi
```

## Migration Guide

### From pip + requirements.txt

```bash
# Option 1: Initialize new uv project and import dependencies
uv init
# Extract package names from requirements.txt
cat requirements.txt | grep -v "^#" | grep -v "^-e" | \
  cut -d'=' -f1 | cut -d'>' -f1 | xargs uv add

# Option 2: Keep using requirements.txt with uv's pip interface
uv venv
uv pip install -r requirements.txt

# Option 3: Generate lockfile from requirements.txt
uv pip compile requirements.in -o requirements.txt
```

**Key differences:**

- `uv.lock` replaces `requirements.txt` for locking
- `pyproject.toml` replaces `requirements.in` for declaring dependencies
- Use `uv run` instead of activating virtualenv

### From Poetry

```bash
# uv can read Poetry's pyproject.toml format
cd existing-poetry-project

# Initialize uv (keeps existing pyproject.toml)
uv sync

# Poetry sections are automatically recognized:
# [tool.poetry.dependencies] -> project dependencies
# [tool.poetry.group.dev.dependencies] -> dev dependencies
```

**Migrate pyproject.toml (optional but recommended):**

```toml
# Poetry format
[tool.poetry.dependencies]
python = "^3.11"
requests = "^2.28"

[tool.poetry.group.dev.dependencies]
pytest = "^8.0"

# Standard format (uv native)
[project]
requires-python = ">=3.11"
dependencies = ["requests>=2.28"]

[dependency-groups]
dev = ["pytest>=8.0"]
```

**Command equivalents:**

| Poetry | uv |
|--------|-----|
| `poetry install` | `uv sync` |
| `poetry add requests` | `uv add requests` |
| `poetry add -D pytest` | `uv add --dev pytest` |
| `poetry remove requests` | `uv remove requests` |
| `poetry run pytest` | `uv run pytest` |
| `poetry lock` | `uv lock` |
| `poetry build` | `uv build` |
| `poetry publish` | `uv publish` |

### From Pipenv

```bash
# Convert Pipfile to requirements.txt first
pipenv requirements > requirements.txt
pipenv requirements --dev > requirements-dev.txt

# Initialize uv project and import
uv init
cat requirements.txt | grep -v "^#" | xargs uv add
cat requirements-dev.txt | grep -v "^#" | xargs uv add --dev

# Remove old Pipenv files after verification
rm Pipfile Pipfile.lock
```

**Command equivalents:**

| Pipenv | uv |
|--------|-----|
| `pipenv install` | `uv sync` |
| `pipenv install requests` | `uv add requests` |
| `pipenv install --dev pytest` | `uv add --dev pytest` |
| `pipenv run pytest` | `uv run pytest` |
| `pipenv lock` | `uv lock` |
| `pipenv shell` | `source .venv/bin/activate` (or use `uv run`) |

### From pyenv (Python version management only)

```bash
# Install Python versions with uv instead
uv python install 3.11 3.12 3.13

# Pin version for project (creates .python-version)
uv python pin 3.12

# List installed versions
uv python list --only-installed

# uv reads existing .python-version files from pyenv
```

**Note:** You can use pyenv and uv together - uv will detect pyenv-installed Pythons.

### From conda

uv does **not** replace conda for:

- Non-Python dependencies (C libraries, CUDA, etc.)
- Conda-specific packages not on PyPI

**For pure Python projects:**

```bash
# Export conda environment
conda list --export > conda-packages.txt

# Extract Python packages (filter conda-specific ones)
grep -v "^#" conda-packages.txt | grep -v "conda" | cut -d'=' -f1 > packages.txt

# Initialize uv and add packages
uv init
uv add $(cat packages.txt | tr '\n' ' ')
```

**Hybrid approach:** Use conda for system dependencies, uv for Python packages:

```bash
# Conda for non-Python deps
conda create -n myenv python=3.12 cudatoolkit

# Activate conda env, then use uv
conda activate myenv
export UV_SYSTEM_PYTHON=1
uv pip install -r requirements.txt
```

## Common Pitfalls

### 1. Forgetting `--locked` in CI/Production

```bash
# Wrong - may update lockfile unexpectedly
uv sync

# Correct - fails if lockfile is outdated (reproducible builds)
uv sync --locked
```

### 2. Mixing uv and pip Commands

```bash
# Don't do this - breaks uv's dependency tracking
pip install some-package
source .venv/bin/activate && pip install another-package

# Do this instead - uv tracks all dependencies
uv add some-package
# Or use uv's pip interface if needed
uv pip install some-package
```

### 3. Not Committing uv.lock

The `uv.lock` file **must** be committed to version control for
reproducible builds. Without it, environments may resolve differently.

```gitignore
# .gitignore - DON'T ignore uv.lock
.venv/
__pycache__/
# uv.lock  <-- DO NOT ADD THIS LINE
```

### 4. Running Commands Outside Project Environment

```bash
# Wrong - uses system Python, not project environment
python script.py
pytest

# Correct - runs within project's virtual environment
uv run python script.py
uv run pytest
```

### 5. Editing uv.lock Manually

Never edit `uv.lock` by hand. It's auto-generated and managed by uv.

```bash
# To update a specific package
uv lock --upgrade-package requests

# To upgrade all packages
uv lock --upgrade

# To regenerate from scratch
rm uv.lock && uv lock
```

### 6. Using `--frozen` When You Mean `--locked`

```bash
# --frozen: Don't update lockfile, but don't verify it either
uv sync --frozen

# --locked: Verify lockfile matches pyproject.toml (use this in CI)
uv sync --locked
```

## Troubleshooting

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| `No pyproject.toml` | Wrong directory | `cd` to root or `uv init` |
| Package not found | Wrong index/typo | Check name, try `--index` |
| Lockfile outdated | pyproject changed | Run `uv lock` |
| `Resolver conflict` | Version conflicts | Try `uv lock --upgrade` |
| Python mismatch | Not installed | `uv python install 3.12` |
| Build failures | Missing deps | Try `--no-build-isolation` |
| Hash mismatch | Corrupted cache | `uv cache clean` |
| Slow first run | Cold cache | Normal, uses cache after |

### Debug Commands

```bash
# Check current environment
uv python find
uv pip list

# Verbose output
uv sync -v
uv sync -vv  # More verbose

# Check lockfile status
uv lock --check

# Clear cache
uv cache clean
uv cache prune --ci  # For CI environments
```

## References

- `references/cli-commands.md` - Complete CLI reference
- `references/project-management.md` - Project and dependency management
- `references/python-versions.md` - Python version management
- `references/integrations.md` - Docker, CI/CD, and tool integrations

## External Links

- Official docs: <https://docs.astral.sh/uv/>
- GitHub: <https://github.com/astral-sh/uv>
- Docker images: <https://github.com/astral-sh/uv/pkgs/container/uv>
- Changelog: <https://github.com/astral-sh/uv/blob/main/CHANGELOG.md>

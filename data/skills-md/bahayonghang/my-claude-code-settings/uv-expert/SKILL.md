---
name: uv-expert
description: Expert guidance for uv Python package and project manager. Use when working with uv, Python dependency management, project setup, virtual environments, or when users mention uv commands, pip alternatives, or fast Python package management.
category: python-tooling
tags:
  - python
  - uv
  - package-manager
  - dependency-management
  - virtual-env
  - pip-alternative
---

# UV Expert

Expert guidance for uv, the extremely fast Python package and project manager written in Rust. UV provides a unified interface for Python dependency management, project creation, virtual environments, and more.

## Additional Resources

For detailed API documentation and configuration options, see the [UV Source Documentation](source/uv/docs/) which includes:
- [Command Line Reference](source/uv/docs/reference/cli.md) - Complete CLI command documentation
- [Configuration Settings](source/uv/docs/reference/settings.md) - All configuration options
- [Environment Variables](source/uv/docs/reference/environment.md) - Environment variable references
- [Installation Guide](source/uv/docs/reference/installer.md) - Detailed installation instructions

For performance benchmarks and technical details, refer to [BENCHMARKS.md](source/uv/BENCHMARKS.md) in the source code.

For troubleshooting common issues, see the [Troubleshooting Guide](source/uv/docs/reference/troubleshooting/).

The complete source code and implementation details are available at [source/uv/](source/uv/).

## Instructions

### Core UV Concepts

**UV is a comprehensive Python tool that replaces:**
- `pip` (package installation)
- `pip-tools` (dependency resolution)
- `pipx` (tool installation)
- `poetry` (project management)
- `pyenv` (Python version management)
- `virtualenv` (virtual environments)
- `twine` (package publishing)

### Installation

**Recommended installation methods:**
```bash
# Standalone installer (macOS/Linux)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows PowerShell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# Via pip
pip install uv

# Via pipx
pipx install uv
```

### Project Management

**Initialize new projects:**
```bash
# Create new project
uv init my-project
cd my-project

# Create with specific Python version
uv init my-project --python 3.11

# Create from existing directory
uv init
```

**Dependency management:**
```bash
# Add dependencies
uv add requests pandas

# Add development dependencies
uv add --dev pytest black

# Add with specific version
uv add "requests>=2.28.0"

# Remove dependencies
uv remove requests

# Update dependencies
uv lock --upgrade
```

**Project execution:**
```bash
# Run commands in project environment
uv run python main.py
uv run pytest
uv run black .

# Run scripts
uv run script.py
```

### Virtual Environments

**Environment management:**
```bash
# Create virtual environment
uv venv

# Create with specific Python version
uv venv --python 3.11

# Activate environment (standard approach)
source .venv/bin/activate  # Unix
.venv\Scripts\activate     # Windows

# Use environment without activation
uv pip install requests
uv python script.py
```

### Package Installation

** pip-compatible interface:**
```bash
# Install packages
uv pip install requests pandas

# Install from requirements
uv pip install -r requirements.txt

# Install with constraints
uv pip install -c constraints.txt

# Install in editable mode
uv pip install -e .

# Uninstall packages
uv pip uninstall requests
```

### Python Version Management

**Python version management:**
```bash
# List available Python versions
uv python list

# Install Python version
uv python install 3.11

# Set Python version for project
uv python pin 3.11

# Use specific Python version
uv run --python 3.11 script.py
```

### Tool Management

**Install and manage tools:**
```bash
# Install as tool
uv tool install ruff
uv tool install pytest

# Run tools
uv run ruff check .
uv run pytest

# List installed tools
uv tool list

# Uninstall tools
uv tool uninstall ruff
```

### Scripts Support

**Run scripts with inline dependencies:**
```python
# script.py with inline dependencies
# /// script
# requires-python = ">=3.8"
# dependencies = [
#     "requests",
#     "typer",
# ]
# ///

import requests
import typer

def main():
    response = requests.get("https://api.github.com")
    print(f"Status: {response.status_code}")

if __name__ == "__main__":
    typer.run(main)
```

```bash
# Run script with automatic dependency resolution
uv run script.py
```

### Advanced Features

**Workspaces:**
```bash
# Create workspace
# pyproject.toml
[tool.uv.workspace]
members = ["packages/*"]

# Work with workspace
uv add requests --workspace
uv sync --workspace
```

**Caching:**
```bash
# Clear cache
uv cache clean

# View cache info
uv cache info

# Warm cache
uv sync --cache-dir ~/.cache/uv
```

**Configuration:**
```bash
# Set global configuration
uv config set global.cache-dir ~/.cache/uv

# View configuration
uv config show

# Use configuration file
# ~/.config/uv/uv.toml
[global]
cache-dir = "~/.cache/uv"
index-url = "https://pypi.org/simple"
```

### Common Workflows

**1. Set up new project:**
```bash
uv init my-project
cd my-project
uv add requests pytest --dev
uv run pytest
```

**2. Work on existing project:**
```bash
git clone <repo>
cd <repo>
uv sync
uv run python main.py
```

**3. Migrate from pip:**
```bash
# Replace pip install
uv pip install package

# Replace requirements.txt workflow
uv add package  # Adds to pyproject.toml
uv lock         # Creates lockfile
```

**4. CI/CD integration:**
```bash
# Install dependencies
uv sync

# Run tests
uv run pytest

# Build package
uv build
```

## Performance Benefits

**UV is 10-100x faster than pip:**
- Parallel downloads and installations
- Efficient caching
- Rust-based performance
- Global dependency deduplication

**Use UV when you need:**
- Faster dependency resolution
- Unified Python toolchain
- Modern Python project management
- Better caching and performance
- Cross-platform consistency

## Migration Guides

**From pip:**
- Replace `pip install` with `uv add` (for projects) or `uv pip install` (standalone)
- Replace `pip freeze` with `uv pip freeze` or use `uv.lock`
- Replace `venv` with `uv venv`

**From poetry:**
- `pyproject.toml` format is compatible
- Replace `poetry add` with `uv add`
- Replace `poetry install` with `uv sync`
- Replace `poetry run` with `uv run`

**From conda:**
- Use UV for Python packages, conda for system packages
- Migrate environment.yml to pyproject.toml
- Use `uv venv` instead of conda environments

## Best Practices

**1. Project Structure:**
```
my-project/
├── pyproject.toml
├── uv.lock
├── src/
└── tests/
```

**2. Dependency Management:**
- Use `uv add` for project dependencies
- Use `uv add --dev` for development dependencies
- Keep `uv.lock` in version control
- Use `uv sync` to reproduce environments

**3. Virtual Environments:**
- Always use virtual environments
- Use `uv run` instead of manual activation
- Delete `.venv` when switching Python versions

**4. Performance:**
- Let UV manage the cache automatically
- Use workspaces for multi-package projects
- Enable parallel operations where possible

## Troubleshooting

**Common issues:**
- **Cache corruption**: Run `uv cache clean`
- **Python version conflicts**: Use `uv python pin`
- **Network issues**: Check `uv config get index-url`
- **Permission errors**: Use user installations or virtual environments

**Debug mode:**
```bash
# Enable verbose output
uv --verbose sync

# Show resolution details
uv add package --verbose
```

## Integration Examples

**With Docker:**
```dockerfile
FROM python:3.11-slim
COPY uv.lock pyproject.toml ./
RUN pip install uv && uv sync
COPY . .
CMD ["uv", "run", "python", "main.py"]
```

**With GitHub Actions:**
```yaml
- name: Install uv
  uses: astral-sh/setup-uv@v1
- name: Install dependencies
  run: uv sync
- name: Run tests
  run: uv run pytest
```

## Resources

- Official documentation: https://docs.astral.sh/uv/
- GitHub repository: https://github.com/astral-sh/uv
- Benchmark comparisons: See BENCHMARKS.md in source
- Community Discord: https://discord.gg/astral-sh
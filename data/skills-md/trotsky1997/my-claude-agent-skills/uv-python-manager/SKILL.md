---
name: uv-python-manager
description: Comprehensive guide for using uv, an extremely fast Python package and project manager written in Rust. Use when working with Python projects for (1) Installing and managing Python packages, (2) Creating and managing virtual environments, (3) Installing and switching between Python versions, (4) Running Python scripts with dependency management, (5) Managing Python projects with lockfiles, (6) Replacing pip, pip-tools, pipx, poetry, pyenv, virtualenv workflows, or any Python package management tasks.
---

# UV Python Manager

## Overview

uv is an extremely fast Python package and project manager that replaces `pip`, `pip-tools`, `pipx`, `poetry`, `pyenv`, `twine`, `virtualenv`, and more. It provides comprehensive project management with a universal lockfile, runs scripts with inline dependency metadata, and includes a pip-compatible interface.

## Installation

### Standalone Installer (Recommended)

**macOS and Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows:**
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### Other Methods

- **PyPI**: `pipx install uv` or `pip install uv`
- **Homebrew**: `brew install uv`
- **WinGet**: `winget install --id=astral-sh.uv -e`
- **Scoop**: `scoop install main/uv`
- **Docker**: `ghcr.io/astral-sh/uv`

## Core Capabilities

### 1. Package Management

Install packages (pip-compatible):
```bash
uv pip install requests
uv pip install -r requirements.txt
uv pip install --editable .
```

List installed packages:
```bash
uv pip list
```

Uninstall packages:
```bash
uv pip uninstall package-name
```

### 2. Virtual Environment Management

Create a virtual environment:
```bash
uv venv
uv venv .venv
uv venv --python 3.12
```

Activate virtual environment:
- **macOS/Linux**: `source .venv/bin/activate`
- **Windows**: `.venv\Scripts\activate`

Remove virtual environment:
```bash
rm -rf .venv  # or rmdir /s .venv on Windows
```

### 3. Python Version Management

Install Python versions:
```bash
uv python install 3.10 3.11 3.12
uv python install pypy@3.8
```

List installed Python versions:
```bash
uv python list
```

Pin Python version for a project:
```bash
uv python pin 3.11
```

Use specific Python version:
```bash
uv run --python 3.12 -- python script.py
uv venv --python 3.12.0
```

### 4. Running Scripts

Run Python scripts with automatic dependency resolution:
```bash
uv run script.py
uv run --python 3.11 script.py
```

Run scripts with inline dependencies (in script comments):
```python
# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "requests>=2.28.0",
#   "click",
# ]
# ///
```

### 5. Project Management

Initialize a new project:
```bash
uv init my-project
cd my-project
```

Add dependencies to project:
```bash
uv add requests
uv add --dev pytest
uv add "django>=4.0,<5.0"
```

Remove dependencies:
```bash
uv remove requests
```

Sync dependencies (install from lockfile):
```bash
uv sync
```

Update dependencies:
```bash
uv lock --upgrade
```

### 6. Workspace Support

uv supports Cargo-style workspaces for scalable projects:
```bash
uv init --workspace
```

## Common Workflows

### Workflow 1: Starting a New Project

```bash
# Initialize project
uv init my-project
cd my-project

# Add dependencies
uv add requests pandas

# Run a script
uv run main.py
```

### Workflow 2: Working with Existing Project

```bash
# Clone and setup
git clone <repo>
cd <repo>

# Install dependencies from lockfile
uv sync

# Run project
uv run main.py
```

### Workflow 3: Managing Python Versions

```bash
# Install multiple Python versions
uv python install 3.10 3.11 3.12

# Create venv with specific version
uv venv --python 3.12

# Pin version for project
uv python pin 3.12
```

### Workflow 4: Migrating from pip/poetry

**From pip:**
- Replace `pip install` with `uv pip install`
- Replace `pip freeze > requirements.txt` with `uv pip compile requirements.in`

**From poetry:**
- Use `uv add` instead of `poetry add`
- Use `uv sync` instead of `poetry install`
- Lockfile format is compatible

### Workflow 5: Running Tools (pipx replacement)

```bash
# Install and run tools
uv tool install black
uv tool run black .

# Or use uvx (if available)
uvx black .
```

## Best Practices

1. **Use lockfiles**: Always commit `uv.lock` to version control for reproducible builds
2. **Pin Python versions**: Use `uv python pin` to ensure consistent Python versions across team
3. **Use virtual environments**: Always work within a virtual environment for project isolation
4. **Leverage speed**: uv is 10-100x faster than pip, use it for all package operations
5. **Workspace for monorepos**: Use workspace feature for managing multiple related projects

## Docker Integration

Use uv in Docker containers:

```dockerfile
FROM ghcr.io/astral-sh/uv:debian

WORKDIR /app
COPY . .
RUN uv sync
CMD ["uv", "run", "main.py"]
```

## Troubleshooting

**Issue**: Command not found after installation
- **Solution**: Add `~/.cargo/bin` (or `%USERPROFILE%\.cargo\bin` on Windows) to PATH

**Issue**: Python version not found
- **Solution**: Use `uv python install <version>` to install the required version

**Issue**: Lockfile conflicts
- **Solution**: Run `uv lock` to regenerate lockfile, or `uv lock --upgrade` to update dependencies

## References

For detailed documentation on specific features, see:

### General References
- **Advanced package management**: See [references/package-management.md](references/package-management.md)
- **Project configuration**: See [references/project-config.md](references/project-config.md)
- **Docker usage**: See [references/docker.md](references/docker.md)

### Command References
- **uv pip**: Pip兼容接口 - See [references/commands/uv-pip.md](references/commands/uv-pip.md)
- **uv venv**: 虚拟环境管理 - See [references/commands/uv-venv.md](references/commands/uv-venv.md)
- **uv python**: Python版本管理 - See [references/commands/uv-python.md](references/commands/uv-python.md)
- **uv run**: 运行Python脚本 - See [references/commands/uv-run.md](references/commands/uv-run.md)
- **uv init**: 初始化项目 - See [references/commands/uv-init.md](references/commands/uv-init.md)
- **uv add**: 添加依赖 - See [references/commands/uv-add.md](references/commands/uv-add.md)
- **uv remove**: 移除依赖 - See [references/commands/uv-remove.md](references/commands/uv-remove.md)
- **uv sync**: 同步依赖 - See [references/commands/uv-sync.md](references/commands/uv-sync.md)
- **uv lock**: 锁文件管理 - See [references/commands/uv-lock.md](references/commands/uv-lock.md)
- **uv build**: 构建项目 - See [references/commands/uv-build.md](references/commands/uv-build.md)
- **uv publish**: 发布到PyPI - See [references/commands/uv-publish.md](references/commands/uv-publish.md)
- **uv tool**: 工具管理 - See [references/commands/uv-tool.md](references/commands/uv-tool.md)

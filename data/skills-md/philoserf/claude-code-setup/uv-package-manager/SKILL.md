---
name: uv-package-manager
description: Expert in uv, the ultra-fast Python package manager and project tool. Use when setting up Python projects, managing dependencies, creating virtual environments, installing Python versions, working with lockfiles, migrating from pip/poetry/pip-tools, or optimizing Python workflows with uv's blazing-fast performance.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
# model: inherit
---

## Reference Files

Detailed uv guidance organized by topic:

- [installation-setup.md](installation-setup.md) - Installation methods, verification, and quick start workflows
- [virtual-environments.md](virtual-environments.md) - Creating, activating, and managing virtual environments with uv
- [package-management.md](package-management.md) - Adding, removing, upgrading packages and working with lockfiles
- [python-versions.md](python-versions.md) - Installing and managing Python interpreters with uv
- [project-configuration.md](project-configuration.md) - pyproject.toml patterns, workspaces, and monorepos
- [ci-cd-docker.md](ci-cd-docker.md) - GitHub Actions, Docker integration, and production deployments
- [migration-guide.md](migration-guide.md) - Migrating from pip, poetry, and pip-tools to uv
- [command-reference.md](command-reference.md) - Essential commands and quick reference

---

# UV Package Manager

Expert guidance for using uv, an extremely fast Python package installer and resolver written in Rust. Provides 10-100x faster installation than pip with drop-in compatibility, virtual environment management, Python version management, and modern lockfile support.

## Focus Areas

- Ultra-fast project initialization and dependency installation
- Virtual environment creation and management with automatic activation
- Python interpreter installation and version pinning
- Lockfile-based reproducible builds for CI/CD
- Migration from pip, pip-tools, and poetry
- Monorepo and workspace support
- Docker and production deployment optimization
- Cross-platform compatibility (Linux, macOS, Windows)

## Core Approach

Essential patterns for effective uv usage:

**Project initialization:**

- Use `uv init` for new projects (creates pyproject.toml, .python-version, .gitignore)
- Use `uv sync` to install from existing pyproject.toml
- Pin Python versions with `uv python pin 3.12`
- Always commit uv.lock for reproducible builds

**Virtual environments:**

- Prefer `uv run` over manual venv activation (auto-manages environment)
- Create venvs with `uv venv` (detects Python version from .python-version)
- Use `uv venv --python 3.12` for specific versions

**Package management:**

- Use `uv add package` to add and install dependencies
- Use `uv add --dev pytest` for development dependencies
- Use `uv remove package` to remove dependencies
- Use `uv lock` to update lockfile, `uv sync --frozen` to install from lockfile

**Reproducible builds:**

- Use `uv sync --frozen` in CI/CD (installs exact versions from lockfile)
- Use `uv lock --upgrade` to update all dependencies
- Use `uv lock --upgrade-package requests` to update specific packages
- Export to requirements.txt with `uv export --format requirements-txt`

**Performance optimization:**

- Global cache shared across projects (automatic)
- Parallel installation (automatic)
- Offline mode with `--offline` flag
- Use `--frozen` to skip resolution in CI

## Quality Checklist

Before deploying uv-based projects:

- uv.lock committed to version control for reproducible builds
- .python-version exists and specifies required Python version
- pyproject.toml includes all production and dev dependencies
- CI/CD uses `uv sync --frozen` for exact reproduction
- Docker builds leverage multi-stage builds and cache mounting
- Local development uses `uv run` to avoid activation issues
- Dependencies organized into optional groups ([project.optional-dependencies])
- Python version constraints specified (requires-python = ">=3.8")
- Security: uv export with --require-hashes for production lockdown
- Documentation explains uv installation for new contributors

## Output

Production-ready deliverables:

- Initialized projects with pyproject.toml and uv.lock
- Virtual environments configured for development
- CI/CD workflows using uv for fast, reproducible builds
- Dockerfiles optimized for uv with caching and multi-stage builds
- Migration scripts and documentation for team adoption
- Requirements.txt exports for compatibility when needed

## Common Workflows

### Starting a New Project

```bash
# Initialize project
uv init my-project
cd my-project

# Pin Python version
uv python pin 3.12

# Add dependencies
uv add fastapi uvicorn pydantic

# Add dev dependencies
uv add --dev pytest black ruff mypy

# Run application
uv run python -m my_project

# Run tests
uv run pytest
```

### Working with Existing Project

```bash
# Clone repository
git clone https://github.com/user/project.git
cd project

# Install dependencies (auto-creates venv)
uv sync

# Install with all optional dependencies
uv sync --all-extras

# Run application
uv run python app.py
```

### Updating Dependencies

```bash
# Update all dependencies
uv lock --upgrade
uv sync

# Update specific package
uv lock --upgrade-package requests
uv sync

# View outdated packages
uv tree --outdated
```

### CI/CD Integration

```bash
# Install uv in CI
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install exact dependencies from lockfile
uv sync --frozen --no-dev

# Run tests
uv run pytest
```

## Key Advantages Over Alternatives

**vs pip:**

- 10-100x faster installation
- Built-in virtual environment support
- Better dependency resolution
- Lockfile support (uv.lock)

**vs poetry:**

- Significantly faster (6-8x)
- Less opinionated, simpler workflows
- Compatible with standard pyproject.toml
- Lighter weight, no Python required for install

**vs pip-tools:**

- Faster compilation (7-8x)
- Integrated venv and Python management
- Better UX with `uv add`/`uv remove`
- Single tool for entire workflow

## Safety and Best Practices

**Version control:**

- Always commit uv.lock for reproducibility
- Commit .python-version for consistency
- Never commit .venv directory

**CI/CD:**

- Use `--frozen` flag to prevent unexpected updates
- Pin uv version in CI for consistency
- Cache uv's global cache directory for speed

**Security:**

- Use `uv export --require-hashes` for supply chain security
- Review dependency updates before applying
- Use `uv tree` to audit dependency graph

**Development:**

- Use `uv run` instead of activating venvs
- Create separate optional dependency groups for different use cases
- Test with minimal dependencies before adding extras

## Tool Integration

**Pre-commit hooks:**

```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: uv-lock
        name: uv lock check
        entry: uv lock --check
        language: system
        pass_filenames: false
```

**VS Code:**

```json
// .vscode/settings.json
{
  "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python",
  "python.terminal.activateEnvironment": true
}
```

**GitHub Actions:**

```yaml
- uses: astral-sh/setup-uv@v2
  with:
    enable-cache: true
- run: uv sync --frozen
- run: uv run pytest
```

## Troubleshooting

**Common issues and solutions:**

```bash
# uv not found after install
echo 'export PATH="$HOME/.cargo/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

# Wrong Python version
uv python pin 3.12
uv venv --python 3.12

# Lockfile out of sync
uv lock --upgrade

# Cache issues
uv cache clean

# Dependency conflicts
uv lock --verbose  # See resolution details
```

## Where to Find What

- **Getting started**: See Focus Areas and Core Approach above
- **Installation**: [installation-setup.md](installation-setup.md)
- **Virtual environments**: [virtual-environments.md](virtual-environments.md)
- **Package operations**: [package-management.md](package-management.md)
- **Python versions**: [python-versions.md](python-versions.md)
- **Project config**: [project-configuration.md](project-configuration.md)
- **CI/CD & Docker**: [ci-cd-docker.md](ci-cd-docker.md)
- **Migration**: [migration-guide.md](migration-guide.md)
- **Command reference**: [command-reference.md](command-reference.md)

## Resources

- Official documentation: <https://docs.astral.sh/uv/>
- GitHub repository: <https://github.com/astral-sh/uv>
- Migration guides: <https://docs.astral.sh/uv/guides/>
- Comparison with other tools: <https://docs.astral.sh/uv/pip/compatibility/>

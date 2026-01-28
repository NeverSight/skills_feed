---
name: Poetry Packaging
description: Master Python package management with Poetry, dependency resolution, publishing, and project structure
version: "2.1.0"
sasmp_version: "1.3.0"
bonded_agent: 06-package-deployment
bond_type: PRIMARY_BOND

# Skill Configuration
retry_strategy: exponential_backoff
observability:
  logging: true
  metrics: build_success_rate
---

# Poetry Packaging

## Overview

Master modern Python dependency management and packaging with Poetry. Learn to create, manage, and publish professional Python packages with reproducible builds and clean dependency resolution.

## Learning Objectives

- Manage project dependencies with Poetry
- Create and publish Python packages
- Handle version constraints and dependency resolution
- Structure projects following best practices
- Implement semantic versioning
- Automate packaging workflows

## Core Topics

### 1. Poetry Basics
- Installing Poetry
- Creating new projects
- Managing dependencies
- Virtual environment management
- Lock files and reproducibility
- Poetry commands and workflow

**Code Example:**
```bash
# Install Poetry
curl -sSL https://install.python-poetry.org | python3 -

# Create new project
poetry new my-awesome-package
cd my-awesome-package

# Project structure created:
# my-awesome-package/
# ├── my_awesome_package/
# │   └── __init__.py
# ├── tests/
# │   └── __init__.py
# ├── pyproject.toml
# └── README.md

# Add dependencies
poetry add requests
poetry add pandas numpy
poetry add --group dev pytest black mypy

# Install dependencies
poetry install

# Run commands in virtual environment
poetry run python main.py
poetry run pytest

# Update dependencies
poetry update

# Show dependency tree
poetry show --tree

# Export to requirements.txt
poetry export -f requirements.txt --output requirements.txt
```

### 2. pyproject.toml Configuration
- Project metadata
- Dependency specification
- Version constraints
- Development dependencies
- Build system configuration
- Scripts and entry points

**Code Example:**
```toml
# pyproject.toml
[tool.poetry]
name = "my-awesome-package"
version = "0.1.0"
description = "An awesome Python package"
authors = ["Your Name <you@example.com>"]
license = "MIT"
readme = "README.md"
homepage = "https://github.com/username/my-awesome-package"
repository = "https://github.com/username/my-awesome-package"
documentation = "https://my-awesome-package.readthedocs.io"
keywords = ["awesome", "package", "python"]
classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
]

[tool.poetry.dependencies]
python = "^3.9"
requests = "^2.28.0"
pandas = "^2.0.0"
click = "^8.1.0"

[tool.poetry.group.dev.dependencies]
pytest = "^7.0.0"
pytest-cov = "^4.0.0"
black = "^23.0.0"
mypy = "^1.0.0"
ruff = "^0.1.0"

[tool.poetry.scripts]
my-cli = "my_awesome_package.cli:main"

[build-system]
requires = ["poetry-core>=1.0.0"]
build-backend = "poetry.core.masonry.api"

# Version constraints examples:
# ^2.0.0  = >=2.0.0 <3.0.0  (caret)
# ~2.0.0  = >=2.0.0 <2.1.0  (tilde)
# 2.0.*   = >=2.0.0 <2.1.0  (wildcard)
# >=2.0.0 = 2.0.0 or higher (range)
```

### 3. Package Structure & Publishing
- Package layout best practices
- Versioning with semantic versioning
- Building distributions (sdist, wheel)
- Publishing to PyPI/TestPyPI
- Package metadata
- Documentation generation

**Code Example:**
```python
# Recommended package structure
my-awesome-package/
├── my_awesome_package/
│   ├── __init__.py           # Package initialization
│   ├── core.py               # Core functionality
│   ├── utils.py              # Utility functions
│   ├── cli.py                # Command-line interface
│   └── py.typed              # Type hints marker
├── tests/
│   ├── __init__.py
│   ├── test_core.py
│   └── test_utils.py
├── docs/
│   ├── index.md
│   └── api.md
├── examples/
│   └── basic_usage.py
├── pyproject.toml
├── README.md
├── LICENSE
├── CHANGELOG.md
└── .gitignore

# my_awesome_package/__init__.py
"""
My Awesome Package

A comprehensive package for doing awesome things.
"""

__version__ = "0.1.0"
__author__ = "Your Name"
__email__ = "you@example.com"

from .core import main_function
from .utils import helper_function

__all__ = ["main_function", "helper_function"]

# Publishing workflow
# 1. Update version in pyproject.toml
poetry version patch  # 0.1.0 -> 0.1.1
poetry version minor  # 0.1.1 -> 0.2.0
poetry version major  # 0.2.0 -> 1.0.0

# 2. Build package
poetry build
# Creates dist/my_awesome_package-0.1.0.tar.gz
# Creates dist/my_awesome_package-0.1.0-py3-none-any.whl

# 3. Publish to TestPyPI first
poetry config repositories.testpypi https://test.pypi.org/legacy/
poetry publish -r testpypi

# 4. Test installation
pip install --index-url https://test.pypi.org/simple/ my-awesome-package

# 5. Publish to PyPI
poetry publish

# 6. Create git tag
git tag v0.1.0
git push origin v0.1.0
```

### 4. Advanced Features
- Monorepo management
- Plugin systems
- Custom build scripts
- Private package repositories
- CI/CD integration
- Dependency groups

**Code Example:**
```toml
# Advanced pyproject.toml configuration

[tool.poetry]
name = "advanced-package"
version = "1.0.0"
description = "Advanced packaging example"

# Include/exclude files
include = ["my_package/data/*.json"]
exclude = ["my_package/tests/*"]

[tool.poetry.dependencies]
python = "^3.9"

# Optional dependencies (extras)
psycopg2 = { version = "^2.9", optional = true }
mysqlclient = { version = "^2.1", optional = true }

[tool.poetry.extras]
postgresql = ["psycopg2"]
mysql = ["mysqlclient"]
all = ["psycopg2", "mysqlclient"]

# Multiple dependency groups
[tool.poetry.group.test.dependencies]
pytest = "^7.0.0"
pytest-cov = "^4.0.0"

[tool.poetry.group.docs.dependencies]
sphinx = "^5.0.0"
sphinx-rtd-theme = "^1.0.0"

[tool.poetry.group.lint.dependencies]
black = "^23.0.0"
ruff = "^0.1.0"
mypy = "^1.0.0"

# Platform-specific dependencies
[tool.poetry.dependencies.pywin32]
version = "^305"
platform = "win32"

# Plugins
[tool.poetry.plugins."my_package.plugins"]
plugin1 = "my_package.plugins:plugin1"

# CI/CD with GitHub Actions
# .github/workflows/publish.yml
name: Publish to PyPI

on:
  release:
    types: [published]

jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install Poetry
        run: curl -sSL https://install.python-poetry.org | python3 -
      - name: Build and publish
        env:
          POETRY_PYPI_TOKEN_PYPI: ${{ secrets.PYPI_TOKEN }}
        run: |
          poetry build
          poetry publish
```

## Hands-On Practice

### Project 1: CLI Tool Package
Create a command-line tool and publish to PyPI.

**Requirements:**
- Build CLI with Click/Typer
- Add multiple subcommands
- Include configuration file support
- Write comprehensive tests
- Generate documentation
- Publish to PyPI

**Key Skills:** Poetry, CLI development, packaging

### Project 2: Library Package
Develop a reusable library with clean API.

**Requirements:**
- Design public API
- Type hints throughout
- Comprehensive docstrings
- Unit and integration tests
- API documentation
- Versioning strategy

**Key Skills:** API design, documentation, testing

### Project 3: Plugin System
Create package with plugin architecture.

**Requirements:**
- Plugin discovery mechanism
- Entry points configuration
- Plugin API specification
- Example plugins
- Plugin documentation
- Distribution strategy

**Key Skills:** Advanced packaging, architecture

## Assessment Criteria

- [ ] Create projects with Poetry
- [ ] Manage dependencies effectively
- [ ] Understand version constraints
- [ ] Build and publish packages
- [ ] Structure projects professionally
- [ ] Write clear package metadata
- [ ] Implement semantic versioning

## Resources

### Official Documentation
- [Poetry Docs](https://python-poetry.org/docs/) - Official documentation
- [PyPI](https://pypi.org/) - Python Package Index
- [Packaging Guide](https://packaging.python.org/) - Python packaging authority

### Learning Platforms
- [Python Packaging](https://realpython.com/pypi-publish-python-package/) - Real Python guide
- [Modern Python Packaging](https://www.youtube.com/watch?v=GIF3LaRqgXo) - Video tutorial
- [Poetry Tutorial](https://www.youtube.com/watch?v=0f3moPe_bhk) - Comprehensive guide

### Tools
- [Poetry](https://python-poetry.org/) - Dependency management
- [Twine](https://twine.readthedocs.io/) - PyPI upload tool
- [bump2version](https://github.com/c4urself/bump2version) - Version bumping
- [setuptools](https://setuptools.pypa.io/) - Alternative packaging

## Next Steps

After mastering Poetry, explore:
- **Docker** - Containerized packaging
- **GitHub Actions** - Automated publishing
- **Read the Docs** - Documentation hosting
- **Pre-commit** - Code quality automation

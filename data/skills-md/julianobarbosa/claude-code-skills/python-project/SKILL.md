---
name: python-project
description: Python project scaffolding and development with modern tooling. Use when creating new Python projects, setting up virtual environments, configuring dependencies, or working with Flask web applications. Triggers on mentions of Python setup, uv, Flask, pytest, or project initialization.
---

# Python Project Skill

Modern Python project development using uv package manager and Flask for web components.

## Quick Start

### New Project with uv

```bash
# Initialize new project
uv init my-project
cd my-project

# Add dependencies
uv add flask pytest ruff mypy

# Run application
uv run python app.py

# Run with Flask
uv run flask run --debug
```

## Package Manager: uv

Use `uv` (astral-sh/uv) for all Python package management. It replaces pip, poetry, pyenv, and virtualenv.

### Common Commands

```bash
# Project management
uv init <name>              # Initialize project
uv add <package>            # Add dependency
uv remove <package>         # Remove dependency
uv sync                     # Sync dependencies from lockfile
uv lock                     # Generate lockfile

# Running
uv run <command>            # Run in project environment
uv run python script.py     # Run Python script
uv run pytest               # Run tests

# Tools (like pipx)
uvx <tool>                  # Run tool in ephemeral env
uv tool install <tool>      # Install tool globally

# Python versions
uv python install 3.12      # Install Python version
uv python pin 3.12          # Pin version for project
```

## Web Framework: Flask

Use Flask for web applications - lightweight WSGI micro-framework.

### Minimal Flask App

```python
# app.py
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/data", methods=["GET", "POST"])
def api_data():
    if request.method == "POST":
        data = request.get_json()
        return jsonify({"status": "ok", "received": data})
    return jsonify({"message": "Hello, API!"})

if __name__ == "__main__":
    app.run(debug=True)
```

### Flask Project Structure

```
my_flask_app/
├── app.py                  # Application entry
├── pyproject.toml          # uv project config
├── static/                 # CSS, JS, images
│   ├── css/
│   └── js/
├── templates/              # Jinja2 templates
│   ├── base.html
│   └── index.html
└── tests/
    └── test_app.py
```

### Run Flask

```bash
# Development
uv run flask run --debug

# With specific host/port
uv run flask run --host=0.0.0.0 --port=8080
```

## Project Configuration

### pyproject.toml

```toml
[project]
name = "my-project"
version = "0.1.0"
description = "Project description"
requires-python = ">=3.11"
dependencies = [
    "flask>=3.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0",
    "ruff>=0.5",
    "mypy>=1.10",
]

[tool.ruff]
line-length = 88
target-version = "py311"

[tool.ruff.lint]
select = ["E", "F", "I", "UP"]

[tool.mypy]
python_version = "3.11"
strict = true

[tool.pytest.ini_options]
testpaths = ["tests"]
```

## Code Quality

```bash
# Linting and formatting with ruff
uv run ruff check .          # Check for issues
uv run ruff check . --fix    # Auto-fix issues
uv run ruff format .         # Format code

# Type checking
uv run mypy .

# Testing
uv run pytest
uv run pytest -v --cov=src
```

## Scripts

- `scripts/init-project.sh` - Initialize new Python project with standard structure
- `scripts/setup-flask.sh` - Set up Flask application boilerplate

## References

- See `references/uv-commands.md` for complete uv reference
- See `references/flask-patterns.md` for Flask best practices

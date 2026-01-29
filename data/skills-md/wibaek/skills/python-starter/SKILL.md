---
name: python-starter
description: Automatically configures formatter and linter settings when initializing Python projects. Installs ruff by default and uses pyproject.toml for configuration. Detects or asks the user about venv/poetry/uv environments and installs as dev dependencies. Optionally configures pre-commit and ty. Suggests VSCode workspace settings when using VSCode. Use this skill when starting Python projects ("Start a Python project", "Create a FastAPI project", "Create a data analysis Python project", etc.).
---

# Python Starter

Automatically configures formatter and linter when initializing Python projects.

## Workflow

1. **Environment Detection and Selection**
   - Use UV if `uv.lock` file exists or `uv` command is available
   - Use Poetry if `[tool.poetry]` section exists in `pyproject.toml`
   - If no environment is configured, recommend uv
   - Otherwise use venv
   - Ask the user if uncertain

2. **Install ruff**
   - Install ruff as dev dependency based on selected environment
   - Use commands (avoid writing code directly)
   - Reference: [environment-setup.md](references/environment-setup.md)

3. **Configure pyproject.toml**
   - Create `pyproject.toml` if it doesn't exist
   - Add ruff configuration (see [pyproject-toml-examples.md](references/pyproject-toml-examples.md) for default settings)
   - Template: [assets/pyproject.toml.template](assets/pyproject.toml.template)

4. **Install pytest**
   - Install pytest as dev dependency based on selected environment
   - Use commands (avoid writing code directly)

5. **Type Checking Setup (Optional)**
   - Ask the user if they want ty setup
   - Install ty as dev dependency if needed
   - Add ty configuration to `pyproject.toml`
   - Reference: [pyproject-toml-examples.md](references/pyproject-toml-examples.md)

6. **Pre-commit Setup (Optional)**
   - Ask the user if they want pre-commit setup
   - Install pre-commit and create `.pre-commit-config.yaml` if needed
   - Reference: [pre-commit-setup.md](references/pre-commit-setup.md)
   - Template: [assets/.pre-commit-config.yaml.template](assets/.pre-commit-config.yaml.template)

7. **VSCode Settings Suggestion**
   - Suggest creating `.vscode/settings.json` when using VSCode
   - Include ruff and ty (if configured) settings
   - Reference: [vscode-settings.md](references/vscode-settings.md)
   - Template: [assets/.vscode-settings.json.template](assets/.vscode-settings.json.template)

8. **Create .gitignore**
   - Create `.gitignore` if it doesn't exist
   - Include common Python ignores for virtual environments, cache files, build artifacts, IDE files, and OS files
   - Template: [assets/.gitignore.template](assets/.gitignore.template)

## Principles

- **Command-first**: Use commands whenever possible instead of writing code directly
- **Use pyproject.toml**: Store all configuration in `pyproject.toml`
- **Dev dependencies**: Install ruff, pytest, ty, and pre-commit as dev dependencies
- **User confirmation**: Confirm with user for environment selection, ty, and pre-commit before proceeding

## References

- **Environment setup**: [references/environment-setup.md](references/environment-setup.md)
- **pyproject.toml examples**: [references/pyproject-toml-examples.md](references/pyproject-toml-examples.md)
- **Pre-commit setup**: [references/pre-commit-setup.md](references/pre-commit-setup.md)
- **VSCode settings**: [references/vscode-settings.md](references/vscode-settings.md)

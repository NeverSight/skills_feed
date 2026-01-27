---
name: ac-code-validator
description: Validate code quality and standards. Use when running linting, checking types, validating code style, or performing static analysis.
---

# AC Code Validator

Validate code against quality standards and style guidelines.

## Purpose

Performs static analysis, linting, type checking, and style validation to ensure code meets quality standards before integration.

## Quick Start

```python
from scripts.code_validator import CodeValidator

validator = CodeValidator(project_dir)
result = await validator.validate()
```

## Validation Types

### Linting
```python
lint_result = await validator.run_lint()
# ESLint for JS/TS
# Ruff/Flake8 for Python
# golint for Go
```

### Type Checking
```python
type_result = await validator.run_type_check()
# TypeScript compiler
# mypy for Python
```

### Formatting
```python
format_result = await validator.check_formatting()
# Prettier for JS/TS
# Black for Python
```

### Security Scan
```python
security_result = await validator.run_security_scan()
# Bandit for Python
# npm audit for Node.js
```

## Validation Result

```json
{
  "valid": true,
  "checks": {
    "lint": {
      "passed": true,
      "errors": 0,
      "warnings": 3,
      "issues": [
        {"file": "auth.py", "line": 45, "severity": "warning", "message": "Line too long"}
      ]
    },
    "types": {
      "passed": true,
      "errors": 0
    },
    "format": {
      "passed": false,
      "files_needing_format": ["utils.py"]
    },
    "security": {
      "passed": true,
      "vulnerabilities": []
    }
  },
  "summary": {
    "total_issues": 3,
    "blocking": 0,
    "auto_fixable": 3
  }
}
```

## Configuration

```json
{
  "language": "python",
  "tools": {
    "lint": "ruff",
    "format": "black",
    "types": "mypy",
    "security": "bandit"
  },
  "rules": {
    "max_line_length": 100,
    "max_complexity": 10,
    "require_docstrings": true
  },
  "ignore_patterns": [
    "**/__pycache__/**",
    "**/node_modules/**",
    "**/.venv/**"
  ]
}
```

## Auto-Fix Support

```python
# Fix all auto-fixable issues
fix_result = await validator.auto_fix()

# Fix specific types only
await validator.auto_fix(types=["format", "lint"])
```

## Language Support

| Language | Lint | Types | Format | Security |
|----------|------|-------|--------|----------|
| Python | ruff/flake8 | mypy | black | bandit |
| TypeScript | eslint | tsc | prettier | npm audit |
| JavaScript | eslint | - | prettier | npm audit |
| Go | golint | go vet | gofmt | gosec |

## Integration

- Used by: `ac-qa-reviewer` for quality checks
- Used by: `ac-commit-manager` before commits
- Reports to: `ac-task-executor`

## API Reference

See `scripts/code_validator.py` for full implementation.

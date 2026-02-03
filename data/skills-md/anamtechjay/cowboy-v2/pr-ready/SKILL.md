---
name: pr-ready
description: Checks if code is ready for a pull request by running type checks, linting, tests, and code quality review for Node.js/TypeScript and Python projects. Use when preparing code for a PR, running pre-commit validation, or when the user asks to check code quality, run linters, run tests, or verify PR readiness.
---

# PR Readiness Checker

Validates that code is ready for a pull request by running automated checks (type checking, linting, tests) and reviewing changes.

## Quick Start

Run the unified PR readiness script:

```bash
bash "$SKILL_DIR/scripts/check-deploy-ready.sh"
```

Or run individual checks:

```bash
# Type checking only
bash "$SKILL_DIR/scripts/check-types.sh"

# Linting only
bash "$SKILL_DIR/scripts/check-lint.sh"

# Tests only
bash "$SKILL_DIR/scripts/check-tests.sh"

# Git diff for code review
bash "$SKILL_DIR/scripts/git-diff-for-review.sh" --stdout
```

## What Gets Checked

### 1. Type Errors
- **TypeScript**: Runs `tsc --noEmit` (finds local install first, then global)
- **Python**: Runs `mypy` or `pyright` if available

### 2. Lint Issues
- **Node.js**: Auto-detects Biome, ESLint, or project-configured linter
- **Python**: Auto-detects ruff, flake8, or pylint

### 3. Tests
- **Node.js**: Auto-detects npm test script, Jest, Vitest, Mocha, or Bun test
- **Python**: Auto-detects pytest or unittest

### 4. Code Quality (Git Diff Review)
- Generates diff of staged/unstaged changes
- YOU must analyze the diff for issues (see checklist below)

## Workflow

### Step 1: Run Automated Checks

```bash
bash "$SKILL_DIR/scripts/check-deploy-ready.sh"
```

### Step 2: Review Diff Output

Analyze the generated diff for these issues:

**Critical (must fix):**
- `any` type usage (TypeScript) or missing type hints (Python)
- `console.log`/`print()` debug statements
- Unhandled errors or missing try-catch
- Security issues (SQL injection, XSS, hardcoded secrets)

**Warnings:**
- TODO/FIXME comments
- Magic numbers without constants
- Functions without return types
- Deep nesting (>3 levels)

**Info:**
- Long functions (>50 lines)
- Poor variable naming
- Missing docstrings for public APIs

### Step 3: Report Findings

Format your findings like this:

```
### Code Review: [filename]

**Critical:**
- Line X: [issue] - [suggestion]

**Warnings:**
- Line Y: [issue] - [suggestion]

**Info:**
- Line Z: [minor improvement]
```

## Manual Commands

### Node.js/TypeScript

```bash
# Type check (prefers local tsc)
./node_modules/.bin/tsc --noEmit
# or
npx tsc --noEmit

# Lint (auto-detected)
./node_modules/.bin/eslint . --ext .ts,.tsx,.js,.jsx
# or for Biome
npx biome check .

# Run tests
npm test
# or directly with Jest
npx jest
# or with Vitest
npx vitest run
```

### Python

```bash
# Type check
mypy .
# or
pyright

# Lint
ruff check .
# or
flake8 .

# Run tests
pytest
# or with unittest
python -m unittest discover
```

## Interpreting Results

### All Checks Passed
The code is ready for a pull request.

### Checks Failed
1. Fix type errors first (they indicate real bugs)
2. Fix lint errors (many can be auto-fixed with `--fix`)
3. Fix failing tests (ensure all tests pass before deployment)
4. Address code review findings by severity

## Troubleshooting

**TypeScript not found:**
```bash
npm install typescript --save-dev
```

**Python type checker not found:**
```bash
pip install mypy  # or: pip install pyright
```

**No linter detected:**
```bash
# Node.js
npm install eslint --save-dev

# Python
pip install ruff  # or: pip install flake8
```

**No test framework detected:**
```bash
# Node.js (Jest)
npm install jest --save-dev
# Add to package.json scripts: "test": "jest"

# Node.js (Vitest)
npm install vitest --save-dev

# Python
pip install pytest
```

**Empty diff output:**
- Stage changes with `git add` or use `--unstaged` flag
- Ensure you're in a git repository

## Reference

See [code-review-guide.md](./references/code-review-guide.md) for detailed code review patterns and examples.

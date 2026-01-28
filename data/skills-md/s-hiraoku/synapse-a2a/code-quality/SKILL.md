---
name: code-quality
description: Run code quality checks (ruff, mypy, pytest) and optionally simplify code. This skill should be used when the user wants to check code quality, run linters, run tests, or simplify recently modified code. Triggered by /lint, /check, or /code-quality commands.
---

# Code Quality Check

This skill runs code quality tools (ruff, mypy, pytest) and optionally simplifies code.

## Usage

```
/code-quality [options]
```

### Options

- `--all` or `-a`: Run on all synapse/ files (default: recently modified files only)
- `--simplify` or `-s`: Also run code-simplifier agent after checks pass
- `--fix` or `-f`: Auto-fix ruff issues with `--fix` flag
- `--test` or `-t`: Run pytest after linting passes
- `--full`: Run all checks including tests (equivalent to `--fix --test`)

## Workflow

### Step 1: Identify Target Files

If `--all` flag is provided:
- Target all files in `synapse/` directory

Otherwise:
- Run `git diff --name-only HEAD~1` to get recently modified files
- Filter to only `.py` files in `synapse/` or `tests/`

### Step 2: Run Ruff Linter

```bash
ruff check [files]
```

If `--fix` flag is provided:
```bash
ruff check --fix [files]
```

Report any errors found. If errors remain after fix, stop and report.

### Step 3: Run Mypy Type Checker

```bash
uv run mypy [files]
```

Report any type errors found. If errors exist, stop and report.

### Step 4: Run Tests (if --test or --full)

If `--test` or `--full` flag is provided AND ruff/mypy passed:

```bash
pytest
```

For running specific tests related to modified files:
```bash
pytest tests/ -v
```

Report any test failures.

### Step 5: Run Code Simplifier (Optional)

If `--simplify` flag is provided AND all previous checks passed:

Use the `code-simplifier:code-simplifier` agent to simplify the recently modified code:

```
Task tool with subagent_type: code-simplifier:code-simplifier
Prompt: Simplify and refine the recently modified code in [files].
Look for opportunities to reduce duplication, simplify conditionals,
and improve readability while maintaining all functionality.
```

### Step 6: Report Results

Summarize:
- Number of files checked
- Ruff status (pass/fail, errors fixed if --fix)
- Mypy status (pass/fail)
- Pytest status (pass/fail, skipped if not run)
- Code simplifier status (if run)

## Error Handling

When errors are found:

1. **Ruff errors**: If `--fix` is provided, attempt auto-fix first. Report remaining errors with file:line format.
2. **Mypy errors**: Report type errors with file:line format. Suggest fixes based on error messages.
3. **Test failures**: Report failed test names and assertion errors. Do NOT proceed to simplification if tests fail.

## Examples

### Basic check on recent changes
```
/code-quality
```

### Check all files with auto-fix
```
/code-quality --all --fix
```

### Full quality check with tests
```
/code-quality --full
```

### Run with tests only
```
/code-quality --test
```

### Full quality check with simplification
```
/code-quality --simplify --test
```

### Shorthand
```
/lint          # Same as /code-quality
/check         # Same as /code-quality
/lint -s       # With simplification
/lint -a -f    # All files with auto-fix
/lint -t       # With tests
/lint --full   # Full check (--fix --test)
```

## Tool Configuration

This project uses the following configurations (from pyproject.toml):

### Ruff
- Target: Python 3.10
- Line length: 88
- Rules: E, F, I, UP, B, SIM
- Ignored: E501, B008
- Excluded: synapse/proto/a2a_pb2*.py

### Mypy
- Strict mode with disallow_untyped_defs
- Tests have relaxed rules (ignore_errors)
- Proto files excluded

### Pytest
- asyncio_mode: auto
- Run with: `pytest` or `pytest tests/ -v`

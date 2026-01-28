---
name: add-check
description: Add a new code quality check to CI, justfile, and pre-commit hooks. Use when adding linters, formatters, type checkers, or other code quality tools to the project.
---

# Adding a New Check

When adding a new code quality check (linter, formatter, type checker, etc.), update these three locations:

## 1. justfile

Add a new recipe and include it in the `default` target:

```just
default: lint format typecheck your-check

your-check:
    uv run YOUR_COMMAND
```

## 2. .github/workflows/ci.yaml

Add a step to the `verify` job after the existing checks:

```yaml
- name: Run YOUR_CHECK
  run: uv run YOUR_COMMAND
```

## 3. lefthook.yml

Add a job to the `pre-commit.jobs` list:

```yaml
- name: YOUR_CHECK
  glob: "*.py"
  run: YOUR_COMMAND {staged_files}
```

If the tool can auto-fix issues, add `stage_fixed: true`.

## Checklist

- [ ] Add dev dependency to `pyproject.toml` if needed
- [ ] Add justfile recipe and update `default` target
- [ ] Add CI workflow step
- [ ] Add lefthook pre-commit job
- [ ] Run `just` to verify all checks pass

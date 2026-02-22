---
name: tdd
description: "Guide Test-Driven Development workflow (Red-Green-Refactor) for new features, bug fixes, and refactoring. Identifies test improvement opportunities and applies pytest best practices. Use when writing tests, implementing features, or following TDD methodology. **PROACTIVE ACTIVATION**: Auto-invoke when implementing features or fixing bugs in projects with test infrastructure (pytest files, tests/ directory). **DETECTION**: Check for tests/ directory, pytest.ini, pyproject.toml with pytest config, or test files. **USE CASES**: Writing production code, fixing bugs, adding features, legacy code characterization."
author: mguinada
version: 2.0.0
tags: [TDD, test driven development, testing, red-green-refactor, pytest, code-quality, coverage]
---

# Test-Driven Development Skill

## Overview

Guides Test-Driven Development workflow: Red-Green-Refactor cycle for new features, bug fixes, legacy code, and test refactoring.

## Development Scenarios

### 1. New Feature Development

Follow the Red-Green-Refactor cycle:

#### 🔴 RED - Write a Failing Test

1. Write the smallest test defining desired behavior
2. Run test to confirm failure

```bash
uv run pytest tests/feature/test_new_function.py -v
```

#### 🟢 GREEN - Make the Test Pass

1. Write minimal production code to pass
2. Run test to confirm passes
3. Iterate until all tests pass

```bash
uv run pytest tests/feature/test_new_function.py::test_new_function -v
uv run pytest
```

#### 🔵 REFACTOR - Improve the Code

1. Clean up test and production code
2. Ensure tests still pass
3. List refactoring opportunities (see [Test Refactoring Opportunities](#test-refactoring-opportunities))

```bash
uv run pytest --cov=src --cov-report=term-missing
```

### 2. Bug Fixes

Never fix a bug without writing a test first.

1. Write test reproducing bug, verify fails
2. Fix bug in implementation
3. Run tests until green
4. Check refactoring opportunities

```python
def test_calculate_total_with_negative_price_raises_error():
    items = [Item("Coke", -1.50)]
    with pytest.raises(ValueError, match="Price cannot be negative"):
        calculate_total(items)
```

### 3. Legacy Code

1. Write characterization tests capturing current behavior
2. Run tests to establish baseline
3. Make small changes with test coverage
4. Refactor incrementally

```bash
uv run pytest tests/legacy/test_old_module.py -v
uv run pytest --cov=src/legacy_module --cov-report=term-missing
```

## Test Refactoring Opportunities

After each TDD cycle (or when reviewing existing tests), search for these improvement opportunities:

### Identify Opportunities

Check for:

- **Redundant tests**: Similar test logic that can be consolidated with parametrization
- **Duplicate fixtures**: Common test data defined in multiple files
- **Missing parametrization**: Multiple tests for similar scenarios
- **File organization**: Tests that could be better consolidated
- **Best practice violations**: Testing private methods, vague assertions, etc.
- **Slow tests**: Tests that could be optimized or marked with `@pytest.mark.slow`
- **Hardcoded values**: Test data that should use fixtures or factories

### Refactoring Process

When refactoring existing tests:

1. **Capture baseline metrics**:
   ```bash
   bin/ci-local 2>&1 | tee baseline.txt
   grep "passed" baseline.txt  # Note test count
   grep "Cover" baseline.txt   # Note coverage %
   ```

2. **Prioritize changes** by impact and isolation:
   - High impact, isolated changes first (parametrization, shared fixtures)
   - Medium impact changes (consolidating test files)
   - Complex changes last (large file reorganization)

3. **Apply refactoring patterns** (see [patterns.md](references/patterns.md))

4. **Verify coverage maintained or improved**:
   ```bash
   uv run pytest --cov=src --cov-report=term-missing
   ```

## Verification Checklist

After completing TDD cycles or test refactoring, verify:

- [ ] **All tests pass**: `uv run pytest`
- [ ] **Coverage maintained or improved**: `uv run pytest --cov=src --cov-report=term-missing`
- [ ] **No mypy errors**: `uv run mypy src/`
- [ ] **No ruff errors**: `uv run ruff check src/`
- [ ] **Tests execute faster**: `uv run pytest --durations=10`

For complete verification, run the full CI pipeline:

```bash
bin/ci-local
```

## Best Practices

See [best-practices.md](references/best-practices.md) for test writing, organization, and code quality guidelines.

## Verification Commands

```bash
# Run all tests
uv run pytest

# Run specific test file
uv run pytest tests/models/test_registry.py -v

# Run specific test
uv run pytest tests/test_file.py::TestClass::test_function -vv

# Run with coverage
uv run pytest --cov=src --cov-report=term-missing --cov-report=html

# Run full CI pipeline
bin/ci-local

# Check test execution time
uv run pytest --durations=10

# Run fast tests only
uv run pytest -m "not slow"
```

## Important Notes

1. **Test First**: Always write tests before implementation
2. **Verify Red Phase**: Confirm tests fail before writing implementation
3. **One at a Time**: Focus on one failing test before moving to the next
4. **Maintain Coverage**: Coverage must never decrease during refactoring
5. **Small Changes**: Make incremental changes and run tests frequently
6. **List Refactoring Opportunities**: After green, identify but wait for user request before implementing

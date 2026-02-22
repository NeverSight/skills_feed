---
name: test-generator
description: >
  Generate or update tests for changed files in the current git branch, using
  statement coverage as the evaluation metric (target: 80%+). Use when: (1) the
  user asks to "write tests for my changes", "add tests for the current branch",
  or "improve coverage", (2) after implementing a feature to ensure adequate test
  coverage, (3) before a PR to verify changed code is tested. Supports Vitest
  and Cargo projects. Invoked with /test-generator or phrases like
  "generate tests", "test my changes", "cover the diff".
---

# Test Generator

Automatically create or update tests for files changed in the current branch,
iterating until statement coverage reaches the target threshold (default 80%).

## Workflow

1. **Detect changed files** — run `scripts/detect-changes.sh [base-branch]`
2. **Discover project conventions** — read existing tests, test config, and setup files
3. **Write / update tests** — for each uncovered file, create or extend its test file
4. **Run coverage check** — run `scripts/check-coverage.sh <threshold> [files...]`
5. **Iterate** — if any file is below threshold, read the coverage report, add missing tests, repeat from step 4 (max 3 iterations)
6. **Report** — summarize final per-file coverage to the user

## Step 1 — Detect Changed Files

```bash
bash <skill-path>/scripts/detect-changes.sh main
```

- Pass the base branch as argument (defaults to upstream or `main`).
- Output: one source file path per line.
- Filters out: test files, config, styles, assets, lock files, `__mocks__/`, `test/setup`.

If no files are output, inform the user there are no testable changes.

## Step 2 — Discover Project Conventions

Before writing any test, read these to match existing style:

1. **Test config** — `vitest.config.*`, `vite.config.*` (test section), `Cargo.toml`
2. **Test setup** — files referenced by `setupFiles` in config
3. **Existing test for the file** — `<name>.test.ts`, `<name>.spec.ts`, or `__tests__/<name>.ts`
4. **Neighboring tests** — 1-2 test files in the same directory for style reference
5. **Project rules** — `AGENTS.md`, `CLAUDE.md`, `.eslintrc*`, `eslint.config.*`

Key things to extract:
- Test framework and assertion style (e.g. `expect()`, `assert`)
- Import conventions (`import { describe } from 'vitest'` vs globals)
- Mock patterns (manual mocks, `vi.mock()`)
- File naming: `*.test.ts` vs `*.spec.ts`
- Any JSDoc / lint requirements on test files

## Step 3 — Write / Update Tests

For each changed file without sufficient coverage:

**If no test file exists** → create one following the project naming convention.

**If a test file exists** → add new test cases; do not rewrite existing passing tests.

### Test quality guidelines

- Test **behavior**, not implementation details.
- Cover: happy path, edge cases, error paths, boundary values.
- Use descriptive `describe`/`it` block names that explain the expected behavior.
- For React components: prefer `@testing-library/react` queries (`getByRole`, `getByText`) over `querySelector`.
- For functions: test return values and side effects, not internal calls.
- Mock external dependencies (API, file system, DB) but not the unit under test.
- If the project uses `fast-check`, consider property tests for pure utility functions (name: `*.property.test.ts`).

## Step 4 — Run Coverage Check

```bash
bash <skill-path>/scripts/check-coverage.sh 80 src/services/foo.ts src/utils/bar.ts
```

- First argument: threshold percentage.
- Remaining arguments: filter output to only these files.
- Output lines: `PASS 92.3% src/services/foo.ts` or `FAIL 65.0% src/utils/bar.ts`.

If the script fails to find coverage output, check that the coverage provider is installed
(`@vitest/coverage-v8`, `@vitest/coverage-istanbul`, etc.) and install if missing.

## Step 5 — Iterate

For each `FAIL` file:
1. Read the coverage JSON (`coverage/coverage-final.json` for vitest) to identify uncovered statements.
2. Add targeted test cases for uncovered branches/statements.
3. Re-run coverage check.
4. Repeat up to **3 iterations** total. If still below threshold after 3 iterations, report remaining gaps to the user with suggestions.

## Step 6 — Report

Summarize results:

```
## Test Coverage Report

| File | Coverage | Status |
|------|----------|--------|
| src/services/foo.ts | 92.3% | PASS |
| src/utils/bar.ts | 81.0% | PASS |
| src/components/Baz.tsx | 73.5% | FAIL |

Target: 80% | Passed: 2/3
```

For FAIL files, briefly explain what remains uncovered and suggest next steps.

## Scripts

- **`scripts/detect-changes.sh [base-branch]`** — list changed source files needing tests
- **`scripts/check-coverage.sh <threshold> [files...]`** — run tests with coverage and report per-file results

---
name: validator
description: Runs local validation operations for any project. Auto-detects language/framework and runs linting, type checking, tests, and dead code detection. Use this when the user says "validate", "run validation", "check code", "lint and test", or "run checks".
---

# Validator Skill

You are a CI/CD pipeline running locally. Your job is to detect the project type and run all appropriate validation commands, then report the results clearly.

## Process

### Step 1: Detect Project Type

Check for these files to identify the project:

| File | Language/Framework |
|------|-------------------|
| `package.json` | Node.js / TypeScript / JavaScript |
| `tsconfig.json` | TypeScript |
| `pyproject.toml` | Python (modern) |
| `setup.py` | Python (legacy) |
| `requirements.txt` | Python |
| `Gemfile` | Ruby |
| `Cargo.toml` | Rust |
| `go.mod` | Go |
| `pom.xml` | Java (Maven) |
| `build.gradle` | Java/Kotlin (Gradle) |

If multiple are found (e.g., `package.json` + `tsconfig.json`), use the most specific (TypeScript in this case).

### Step 2: Read Project Configuration

For the detected project type, read the config file to identify available scripts:

**Node.js/TypeScript:** Read `package.json` → check `scripts` for:
- `lint`, `eslint`, `check`
- `typecheck`, `tsc`, `type-check`
- `test`, `jest`, `vitest`, `playwright`
- `build` (useful to verify compilation)

**Python:** Check for tool configs in `pyproject.toml` or separate files:
- `ruff.toml`, `.flake8`, `.pylintrc` → linting
- `mypy.ini`, `pyrightconfig.json` → type checking
- `pytest.ini`, `setup.cfg` → testing

### Step 3: Run Validation Commands

Run each category in order. **Continue even if a command fails** - collect all results.

#### TypeScript / JavaScript

```bash
# 1. Linting (try in order, use first available)
npm run lint          # if script exists
npx eslint .          # fallback

# 2. Type checking (TypeScript only)
npm run typecheck     # if script exists
npx tsc --noEmit      # fallback

# 3. Tests
npm run test          # if script exists
npx jest              # or vitest, playwright

# 4. Dead code (optional)
npx knip              # if installed
```

#### Python

```bash
# 1. Linting (try in order)
ruff check .          # modern, fast
flake8                # traditional
pylint **/*.py        # comprehensive

# 2. Type checking
mypy .                # if configured
pyright               # alternative

# 3. Tests
pytest                # most common
python -m unittest discover  # stdlib fallback

# 4. Dead code (optional)
vulture .             # if installed
```

#### Ruby

```bash
# 1. Linting
bundle exec rubocop

# 2. Tests
bundle exec rspec     # if spec/ exists
bundle exec rake test # alternative

# 3. Dead code (optional)
bundle exec debride .
```

#### Rust

```bash
# 1. Linting
cargo clippy -- -D warnings

# 2. Tests
cargo test

# 3. Build check
cargo build --release
```

#### Go

```bash
# 1. Linting
go vet ./...
golangci-lint run     # if installed

# 2. Tests
go test ./...

# 3. Build check
go build ./...
```

### Step 4: Collect and Parse Results

For each command:
1. Capture stdout and stderr
2. Note the exit code (0 = pass, non-zero = fail)
3. Parse output to extract:
   - Error count
   - Warning count
   - Test pass/fail counts
   - Specific file:line references

### Step 5: Generate Report

Present results in this format:

```markdown
## Validation Report

**Project:** [TypeScript/Python/Ruby/etc.]
**Overall Status:** PASS ✓ / FAIL ✗

---

### Linting
**Status:** PASS ✓ / FAIL ✗
**Command:** `npm run lint`
- Errors: 0
- Warnings: 3

<details>
<summary>Warnings (3)</summary>

- `src/utils.ts:42` - Unexpected any. Specify a different type.
- `src/api.ts:15` - 'response' is defined but never used.
- `src/api.ts:23` - Prefer const over let.

</details>

---

### Type Checking
**Status:** PASS ✓
**Command:** `npx tsc --noEmit`
- No type errors found.

---

### Tests
**Status:** PASS ✓
**Command:** `npm run test`
- Total: 47
- Passed: 47
- Failed: 0
- Skipped: 2

---

### Dead Code Detection
**Status:** SKIPPED (knip not installed)

---

## Summary

| Check | Status | Issues |
|-------|--------|--------|
| Linting | ✓ | 3 warnings |
| Type Check | ✓ | 0 |
| Tests | ✓ | 47/47 passed |
| Dead Code | - | skipped |

### Recommended Actions
1. Consider fixing the 3 linting warnings
2. Install `knip` for dead code detection: `npm i -D knip`
```

## Error Handling

**Command not found:**
- Note as "SKIPPED - tool not installed"
- Suggest installation command

**Command fails:**
- Still report as FAIL with output
- Continue to next check
- Include error output in report

**Timeout:**
- If a command takes >2 minutes, note as "TIMEOUT"
- Tests may take longer - use appropriate timeout

## Guidelines

- **Run all checks** - don't stop on first failure
- **Be thorough** - capture all output for debugging
- **Be clear** - present pass/fail prominently
- **Be helpful** - suggest fixes for common issues
- **No interaction** - run autonomously, report when done

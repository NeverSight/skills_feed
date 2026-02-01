---
name: run-tests
description: ⚠️ MANDATORY - Automatically invoked by safe-commit. Executes comprehensive testing suite including unit tests (minimum 90% coverage), integration tests, and E2E tests (100% pass required). Reports coverage and failures. MUST pass before commit. NEVER run tests manually before commit.
version: 1.0.1
dependencies: Language-specific test frameworks (pytest, jest, go test, cargo test, etc.)
---

# Run Tests Skill

## ⚠️ MANDATORY SKILL - AUTO-INVOKED BY SAFE-COMMIT

## Purpose

Execute comprehensive testing to ensure code correctness, prevent regressions, and maintain quality standards before committing.

**CRITICAL:** This skill is automatically invoked by safe-commit. NEVER run tests manually before commit.

## Testing Requirements

### Coverage Thresholds

- **Unit Tests**: Minimum 90% code coverage
- **Integration Tests**: All integration points tested
- **End-to-End Tests**: 100% pass rate (no mocks)

### Philosophy

- Tests are NOT optional
- Failing tests = failing build
- Coverage below thresholds = failure
- E2E tests use real dependencies, never mocks

## 🚫 NEVER DO THIS

- ❌ Running `npm test` or `jest` manually before commit
- ❌ Running `go test ./...` manually before commit
- ❌ Running `pytest` manually before commit
- ❌ Running tests outside of this skill during commit workflow

**Let safe-commit invoke this skill automatically. Manual testing before commit is REDUNDANT and FORBIDDEN.**

---

## ⚠️ SKILL GUARD - READ BEFORE RUNNING TESTS MANUALLY

**Before using Bash tool to run tests, answer these questions:**

### ❓ Are you about to run `npm test`, `npm run test`, or `jest`?

→ **STOP.** Are you doing this before commit? If YES, use safe-commit instead (it invokes this skill).

### ❓ Are you about to run `go test ./...` or `go test -v`?

→ **STOP.** Are you doing this before commit? If YES, use safe-commit instead (it invokes this skill).

### ❓ Are you about to run `pytest`, `python -m pytest`, or `py.test`?

→ **STOP.** Are you doing this before commit? If YES, use safe-commit instead (it invokes this skill).

### ❓ Are you about to run `cargo test` or `yarn test`?

→ **STOP.** Are you doing this before commit? If YES, use safe-commit instead (it invokes this skill).

### ❓ Are you checking test coverage before committing?

→ **STOP.** Invoke safe-commit skill (it will invoke this skill automatically).

**IF YOU RUN TESTS MANUALLY BEFORE COMMIT, YOU ARE CREATING REDUNDANCY AND WASTING TIME.**

When to run tests manually:

- ✅ During development/debugging (TDD workflow)
- ✅ After implementing features (to verify locally)
- ✅ When user explicitly requests "run tests"

When NOT to run tests manually:

- ❌ Before commit (use safe-commit instead)
- ❌ As part of commit workflow (use safe-commit instead)

**Safe-commit invokes this skill automatically with full coverage reporting. Don't duplicate the work.**

---

## Workflow

### Step 1: Detect Project Type and Test Framework

Check for test indicators:

```bash
# Check for test framework markers in parallel
ls package.json go.mod requirements.txt Cargo.toml pytest.ini jest.config.js 2>/dev/null
```

**Test Framework Detection:**

- `package.json` + `jest.config.js` or `"jest"` in package.json → Jest
- `package.json` + `vitest.config` → Vitest
- `go.mod` + `*_test.go` files → Go testing
- `requirements.txt` + `pytest.ini` or `pyproject.toml` → pytest
- `Cargo.toml` → cargo test
- `pom.xml` → JUnit/Maven
- `Makefile` with test target → make test

---

## Step 2: Run Unit Tests (Language-Specific)

### Node.js / TypeScript (Jest)

```bash
npm test -- --coverage
# OR
npx jest --coverage --verbose
```

**Parse output for:**

- Test pass/fail counts
- Coverage percentages (Statements, Branches, Functions, Lines)
- Specific test failures with file/line numbers

**Success criteria:**

- All tests pass
- Coverage ≥ 90% for all metrics

### Node.js / TypeScript (Vitest)

```bash
npx vitest run --coverage
```

### Go

```bash
go test ./... -v -cover -coverprofile=coverage.out
```

**Parse coverage:**

```bash
go tool cover -func=coverage.out | tail -1
```

**Success criteria:**

- All tests pass (PASS in output)
- Total coverage ≥ 90%

**For detailed HTML report:**

```bash
go tool cover -html=coverage.out -o coverage.html
```

### Python (pytest)

```bash
pytest --cov=. --cov-report=term-missing --cov-report=html --verbose
```

**Success criteria:**

- All tests pass
- Coverage ≥ 90%

### Rust (cargo)

```bash
cargo test --verbose
```

**For coverage (requires tarpaulin):**

```bash
cargo tarpaulin --out Html --output-dir coverage
```

**Success criteria:**

- All tests pass
- Coverage ≥ 90% (if coverage tool available)

### Java (Maven)

```bash
mvn test -Pcoverage
```

**Success criteria:**

- BUILD SUCCESS
- Coverage ≥ 90% (check target/site/jacoco/index.html)

---

## Step 3: Run Integration Tests (If Applicable)

Integration tests verify service-to-service communication, database interactions, and API contracts.

### Detection

Look for:

- `*_integration_test.go`
- `tests/integration/` directory
- `test_integration_*.py`
- `*.integration.test.ts`

### Execution

**Go:**

```bash
go test ./... -tags=integration -v
```

**Python:**

```bash
pytest tests/integration/ -v
```

**Node.js:**

```bash
npm test -- --testPathPattern=integration
```

**Success criteria:**

- All integration tests pass
- Real dependencies used (database, external services)
- Proper setup/teardown of test data

---

## Step 4: Run End-to-End Tests (If Applicable)

E2E tests verify complete user workflows against production-like environment.

### Detection

Look for:

- `tests/e2e/` directory
- `e2e/` directory
- `*.e2e.test.ts`
- Playwright, Cypress, or Selenium configs

### Execution

**Playwright:**

```bash
npx playwright test
```

**Cypress:**

```bash
npx cypress run
```

**Go (if using testcontainers):**

```bash
go test ./e2e/... -v
```

**Success criteria:**

- 100% pass rate (MANDATORY - no failures allowed)
- Tests use real browser/application
- Tests verify actual user experience
- No mocks - real dependencies only

---

## Step 5: Parse and Report Results

### Success Report Format

```
✅ ALL TESTS PASSED

Unit Tests:
- Go: 156 passed, 0 failed
- Coverage: 94.5% (exceeds 90% threshold)

Integration Tests:
- Database: 12 passed
- API: 8 passed
- gRPC: 5 passed

E2E Tests:
- User flows: 15 passed (100%)

Total: 196/196 tests passed
Coverage: 94.5% ✓

Safe to proceed with commit.
```

### Failure Report Format

```
❌ TESTS FAILED

Unit Tests:
✗ pkg/parser/parser_test.go:45: TestParseInvalidInput FAILED
  Expected: error
  Got: nil

✗ src/api/handlers.test.ts:128: should handle 404 errors FAILED
  Expected status: 404
  Received status: 500

Coverage: 87.3% ✗ (below 90% threshold)
  Missing coverage:
  - pkg/auth/validator.go: 78.5%
  - src/utils/helpers.ts: 82.1%

Integration Tests:
✓ 12/12 passed

E2E Tests:
✗ 14/15 passed (93.3%)
✗ e2e/checkout.spec.ts: Payment processing timeout

CANNOT COMMIT - Must fix failing tests and improve coverage.

Next Steps:
1. Fix failing unit tests in parser_test.go and handlers.test.ts
2. Add tests to increase coverage in validator.go and helpers.ts
3. Investigate E2E payment processing timeout
4. Re-run tests after fixes
```

---

## Step 6: Generate Coverage Report (Optional)

If user wants detailed coverage report:

**Go:**

```bash
go tool cover -html=coverage.out -o coverage.html
echo "Coverage report: coverage.html"
```

**Python:**

```bash
echo "Coverage report: htmlcov/index.html"
```

**Node.js:**

```bash
echo "Coverage report: coverage/lcov-report/index.html"
```

---

## Handling Test Failures

### Step-by-Step Remediation:

1. **Identify Root Cause**
   - Parse error messages
   - Identify failing test files
   - Note expected vs actual behavior

2. **Categorize Failures**
   - Legitimate bugs (code is wrong)
   - Broken tests (test is wrong)
   - Environment issues (setup problem)
   - Flaky tests (timing/concurrency)

3. **Report to User**

   ```
   Test Failure Analysis:

   1. parser_test.go:45 - Legitimate bug
      Issue: ParseInvalidInput returns nil instead of error
      Fix needed: Add error handling in parser.go:128

   2. handlers.test.ts:128 - Test expectation issue
      Issue: API changed from 404 to 500 for this case
      Fix needed: Update test expectation or API behavior

   3. checkout.spec.ts - Environment issue
      Issue: Payment service timeout (external dependency)
      Fix needed: Verify payment service is running, increase timeout, or check network
   ```

4. **Suggest Fixes**
   - Provide code snippets for fixes
   - Link to relevant files/lines
   - Suggest test additions for coverage gaps

---

## Handling Low Coverage

If coverage < 90%:

1. **Identify Uncovered Code**

   ```bash
   go tool cover -func=coverage.out | grep -E "[0-9]+\.[0-9]+%" | awk '$3 < 90'
   ```

2. **Report Specific Gaps**

   ```
   Coverage Gaps:

   - pkg/auth/validator.go: 78.5%
     Missing: Lines 45-62 (error handling)
     Missing: Lines 89-95 (edge case validation)

   - src/utils/helpers.ts: 82.1%
     Missing: Lines 34-41 (error path)
     Missing: Function 'formatDate' (no tests)
   ```

3. **Suggest Test Additions**
   - Identify untested functions
   - Note missing error path tests
   - Highlight edge cases not covered

---

## Integration with Other Skills

This skill is invoked by:

- **`safe-commit`** - Before committing changes
- **`create-pr`** - Before creating pull requests

---

## Best Practices

1. **Run all test types** - Unit, integration, E2E in sequence
2. **Report comprehensively** - Show pass/fail, coverage, and specific errors
3. **No partial success** - All thresholds must be met
4. **Suggest fixes** - Don't just report failures, help resolve them
5. **Verify environment** - Check test dependencies are available
6. **Time awareness** - Warn if tests take > 5 minutes

## Common Issues

### Issue: Tests not found

**Solution:**

- Verify test files exist
- Check test file naming conventions
- Ensure test framework installed

### Issue: Database connection failed

**Solution:**

- Check database is running
- Verify connection string
- Ensure test database exists
- Check migrations are applied

### Issue: E2E tests timing out

**Solution:**

- Increase timeout values
- Check application is running
- Verify network connectivity
- Check browser/driver versions

### Issue: Flaky tests

**Solution:**

- Identify intermittent failures
- Check for timing issues
- Review async/await usage
- Consider retry logic for external services

---

## Emergency Override

If user explicitly states "skip tests" or "tests are broken but commit anyway":

**YOU MUST:**

1. Warn about the risk
2. Document which tests were skipped
3. Get explicit confirmation
4. Suggest creating immediate follow-up ticket
5. Note in commit message: "Tests skipped - see #TICKET"

**This should be EXTREMELY RARE and only with explicit approval.**

---

## Related Commands

- **`/coverage-trend`** - Track coverage changes across commits to catch regressions
- **`/test-coverage`** - Detailed coverage analysis and reporting

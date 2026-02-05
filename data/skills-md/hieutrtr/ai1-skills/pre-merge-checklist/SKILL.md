---
name: pre-merge-checklist
description: >-
  Comprehensive pre-merge validation checklist for Python/React pull requests. Use
  before approving or merging any PR. Covers code quality checks (linting, formatting,
  type checking), test coverage requirements, documentation updates, migration safety,
  API contract compatibility, accessibility compliance, bundle size impact, and
  deployment readiness. Provides a systematic checklist that ensures nothing is missed
  before merge. Does NOT cover security review depth (use code-review-security).
license: MIT
compatibility: 'Python 3.12+, React 18+, ruff, mypy, pytest, TypeScript'
metadata:
  author: platform-team
  version: '1.0.0'
  sdlc-phase: code-review
allowed-tools: Read Grep Glob Bash(pytest:*) Bash(npm:*) Bash(ruff:*) Bash(mypy:*)
context: fork
---

# Pre-Merge Checklist

## When to Use

Activate this skill when:
- Reviewing a pull request before approving
- Preparing your own PR for merge
- Verifying that all automated checks pass before merging
- Auditing a PR that has been approved but not yet merged
- Running a final validation pass after addressing review feedback

Do NOT use this skill for:
- In-depth security review (use `code-review-security`)
- Writing implementation code (use `python-backend-expert` or `react-frontend-expert`)
- Architecture decisions (use `system-architecture`)
- E2E test creation (use `e2e-testing`)

## Instructions

### Automated Checks (Ordered)

Run automated checks in this order. Each check must pass before proceeding to the next. Use `scripts/run-all-checks.sh` to execute all checks at once.

#### 1. Linting and Formatting

**Python (ruff):**
```bash
# Check linting
ruff check app/ tests/

# Check formatting
ruff format --check app/ tests/

# Auto-fix (if needed before commit)
ruff check --fix app/ tests/
ruff format app/ tests/
```

**TypeScript/React (eslint + prettier):**
```bash
# Check linting
npx eslint 'src/**/*.{ts,tsx}' --max-warnings 0

# Check formatting
npx prettier --check 'src/**/*.{ts,tsx}'

# Auto-fix (if needed)
npx eslint 'src/**/*.{ts,tsx}' --fix
npx prettier --write 'src/**/*.{ts,tsx}'
```

**Pass criteria:**
- Zero lint errors (warnings are tolerated only with justification)
- All files formatted consistently
- No `# noqa` or `eslint-disable` without a comment explaining why

#### 2. Type Checking

**Python (mypy):**
```bash
mypy app/ --strict --no-error-summary
```

**TypeScript:**
```bash
npx tsc --noEmit
```

Use `scripts/type-check.sh` to run both in sequence with report output.

**Pass criteria:**
- Zero type errors in changed files
- No new `type: ignore` or `@ts-ignore` without justification
- Generic types used correctly (no `Any` leaks)

#### 3. Tests

**Python:**
```bash
pytest tests/ -q --tb=short
```

**React:**
```bash
npm test -- --run --reporter=verbose
```

**Pass criteria:**
- All tests pass (zero failures)
- No skipped tests without a linked issue/ticket
- New code has corresponding tests

#### 4. Coverage

**Python:**
```bash
pytest --cov=app --cov-report=term-missing --cov-fail-under=80
```

**React:**
```bash
npx vitest run --coverage --coverage.thresholds.lines=80
```

**Pass criteria:**
- Overall coverage >= 80%
- New code coverage >= 90%
- No critical paths left uncovered (auth, payment, data mutation)

#### 5. Security Scan

```bash
# Python dependencies
pip-audit --requirement requirements.txt

# npm dependencies
npm audit --audit-level=high

# Custom code scan (if code-review-security skill is available)
python scripts/security-scan.py --path app/ --output-dir ./security-results
```

**Pass criteria:**
- No critical or high severity vulnerability in dependencies
- No critical findings in code scan
- All new endpoints have authentication checks

---

### Manual Review Checklist

After automated checks pass, review the PR manually against these categories.

#### Code Quality

- [ ] **Naming:** Variables, functions, and classes have clear, descriptive names
- [ ] **Functions:** Each function does one thing; no function exceeds 50 lines
- [ ] **DRY:** No duplicated logic that should be extracted into a shared function
- [ ] **Comments:** Complex logic is documented; no commented-out code left in
- [ ] **Imports:** No unused imports; imports are organized (stdlib, third-party, local)
- [ ] **Constants:** No magic numbers or strings; use named constants or enums
- [ ] **Logging:** New features have appropriate log statements at correct levels

#### Testing

- [ ] **Coverage:** New code has tests (unit and/or integration as appropriate)
- [ ] **Edge cases:** Tests cover happy path, error paths, and boundary conditions
- [ ] **Test names:** Test names describe the scenario and expected outcome
- [ ] **Test isolation:** Tests do not depend on each other or on execution order
- [ ] **No flakiness:** Tests do not use hardcoded delays or environment-specific paths
- [ ] **Factories:** Test data uses factories, not hardcoded fixtures

#### Type Safety

- [ ] **No `Any`:** Return types and parameters are properly typed (no escape hatches)
- [ ] **Null safety:** Optional values are handled (null checks, default values)
- [ ] **Schema validation:** API inputs use Pydantic schemas (Python) or Zod (React)
- [ ] **Generic types:** Collections use proper generics (`list[User]`, not `list`)

#### Error Handling

- [ ] **Graceful errors:** All error paths return meaningful messages
- [ ] **HTTP status codes:** Correct codes used (404 for not found, 409 for conflict, etc.)
- [ ] **Error boundaries:** React components have error boundaries for async failures
- [ ] **Retry logic:** External service calls have retry with backoff (where appropriate)
- [ ] **No silent failures:** Caught exceptions are logged, not silently swallowed

#### Backwards Compatibility

- [ ] **API contracts:** No breaking changes to existing API response shapes
- [ ] **Database migrations:** Migrations are reversible and non-destructive
- [ ] **Feature flags:** Breaking changes are behind feature flags
- [ ] **Deprecation:** Removed features have deprecation warnings in prior release
- [ ] **Configuration:** No new required environment variables without documentation

#### Documentation

- [ ] **API docs:** New endpoints are documented (OpenAPI/Swagger via FastAPI)
- [ ] **README:** Setup instructions updated if new dependencies or steps added
- [ ] **Migration notes:** Database migration has a description comment
- [ ] **ADR:** Significant architectural decisions documented (if applicable)

#### Performance

- [ ] **N+1 queries:** No N+1 database query patterns (use eager loading)
- [ ] **Pagination:** List endpoints use cursor-based pagination
- [ ] **Indexes:** New query patterns have supporting database indexes
- [ ] **Bundle size:** No unnecessary large dependencies added to frontend

#### Accessibility

- [ ] **Semantic HTML:** Correct HTML elements used (button, nav, main, etc.)
- [ ] **ARIA labels:** Interactive elements have accessible labels
- [ ] **Keyboard navigation:** New UI elements are keyboard-accessible
- [ ] **Color contrast:** Text meets WCAG 2.1 AA contrast requirements

Use `scripts/accessibility-check.sh` to run automated accessibility checks.

---

### Failure Protocol

When a check fails, follow this escalation path:

**Automated check failure:**
1. Fix the issue in the PR
2. Push the fix and re-run checks
3. Do not merge until all automated checks pass

**Manual review finding:**
1. Add a review comment with the finding
2. Request changes on the PR
3. Re-review after the author addresses feedback

**Severity-based response:**

| Finding Type | Action | Can Override? |
|---|---|---|
| Lint/format error | Fix before merge | No |
| Type error | Fix before merge | No |
| Test failure | Fix before merge | No |
| Coverage below threshold | Add tests or justify | Yes, with tech lead approval |
| Security finding (critical/high) | Fix before merge | No |
| Security finding (medium/low) | Fix or create follow-up ticket | Yes, with ticket reference |
| Accessibility violation | Fix or create follow-up ticket | Yes, with justification |
| Performance concern | Discuss in PR, may defer | Yes, with tech lead approval |

### Override Process

If a check must be overridden:

1. **Document the reason** in a PR comment explaining why the override is acceptable
2. **Get explicit approval** from a tech lead or senior engineer
3. **Create a follow-up ticket** to resolve the underlying issue
4. **Add a code comment** at the override point referencing the ticket

```python
# OVERRIDE: Coverage below 80% for this module. See TICKET-1234.
# Approved by @tech-lead on 2024-01-15.
# Reason: Legacy code migration in progress; full coverage planned for Sprint 12.
```

Overrides are never acceptable for:
- Critical security vulnerabilities
- Broken tests
- Type errors that mask bugs

## Examples

### Running All Checks

```bash
# Run the full check suite
./scripts/run-all-checks.sh --output-dir ./check-results

# Run only type checks
./scripts/type-check.sh --output-dir ./check-results

# Run accessibility checks
./scripts/accessibility-check.sh --output-dir ./check-results
```

### Quick PR Review Workflow

1. Pull the branch locally
2. Run `./scripts/run-all-checks.sh --output-dir ./pr-review`
3. Review the automated results file
4. Walk through the manual checklist above
5. Leave review comments or approve

---
name: test
description: |
  Test strategy and execution. Create test plans, run test suites, or fix failing tests.
  Use when asked to "run tests", "create test strategy", "fix failing tests", "check coverage",
  or when you need to verify code works. Supports vitest, playwright, jest, and cypress.
license: MIT
metadata:
  author: howells
website:
  order: 10
  desc: Run & fix tests
  summary: Run your tests, fix failures, or create a test strategy. Supports vitest, jest, playwright, and cypress—with special handling for flaky e2e tests.
  what: |
    Test runs your test suite and helps fix what's broken. For unit tests (vitest, jest), it's straightforward—run, read failures, fix. For e2e tests (playwright, cypress), it spawns a dedicated agent that can handle the verbose output, retry flaky tests, and work through failures methodically. It can also analyze your codebase and suggest where tests are missing.
  why: |
    E2e tests are painful—slow, flaky, verbose output that fills your context. Test handles this by running playwright/cypress in a background agent that can retry, screenshot failures, and fix issues without overwhelming your main session. For unit tests, it's simpler but still useful: run, diagnose, fix.
  decisions:
    - Framework detection is automatic. It finds your test config and runs the right thing.
    - E2e tests get special treatment. Background agent handles retries and verbose output.
    - Fixes understand root causes. Not just making tests pass—understanding why they failed.
  agents:
    - e2e-test-runner
---

<tasklist_context>
**Use TaskList tool** to check for existing tasks related to this work.

If a related task exists, note its ID and mark it `in_progress` with TaskUpdate when starting.
</tasklist_context>

<rules_context>
**Check for project testing rules:**

**Use Glob tool:** `.ruler/testing.md`

**If file exists:** Read it for MUST/SHOULD/NEVER constraints on testing patterns, frameworks, and conventions.

**If `.ruler/` doesn't exist:** Continue without rules — they're optional.
</rules_context>

<progress_context>
**Use Read tool:** `docs/progress.md` (first 50 lines)

Check for recently implemented features that need testing.
</progress_context>

# Test Workflow

Create or review test strategy. Optionally run test suite. Supports vitest and playwright primarily.

## Process

### Step 1: Detect Test Setup

**Use Glob tool to find test framework config:**

| Glob Pattern | Framework |
|-------------|-----------|
| `vitest.config.*` | vitest |
| `playwright.config.*` | playwright |
| `jest.config.*` | jest |
| `cypress.config.*` | cypress |

### Step 1b: Verify Fail-Fast Configuration

**Tests must fail fast.** Don't waste time waiting.

**Check playwright.config.ts has sensible timeouts:**
- `timeout: 30_000` (30s max per test)
- `actionTimeout: 10_000` (10s per action)
- `expect.timeout: 5_000` (5s for assertions)

**If tests hit LLM APIs:** Use tighter timeouts (5-10s). See `${CLAUDE_PLUGIN_ROOT}/references/llm-api-testing.md`

**Never:**
- Set global timeout to minutes "just in case"
- Retry 5+ times to mask flaky tests
- Use arbitrary sleeps

**Reference:** `${CLAUDE_PLUGIN_ROOT}/agents/workflow/e2e-test-runner.md` for full Playwright config

### Step 2: Determine Intent

"What would you like to do?"
1. **Review strategy** — Analyze current test coverage and approach
2. **Create strategy** — Design test plan for a feature
3. **Run tests** — Execute test suite
4. **Fix failing tests** — Debug and fix

### For "Review Strategy"

**Analyze test coverage:**

**Use Glob tool:** `**/*.test.*`, `**/*.spec.*` — count test files

**Use Grep tool:** Pattern `coverage` in `vitest.config.*`, `playwright.config.*` — check coverage config

**Report:**
- Number of test files
- Unit vs E2E balance
- Coverage gaps (if measurable)
- Missing test patterns

### For "Create Strategy"

For the given feature:

1. **Unit tests** (vitest)
   - Pure functions
   - Component rendering
   - Hooks behavior

2. **Integration tests** (vitest)
   - Component interactions
   - API mocking

3. **E2E tests** (playwright)
   - Critical user flows
   - Happy path + key error states

Output test plan:
```markdown
## Test Strategy: [Feature]

### Unit Tests
- [ ] [Test case]: [What it verifies]

### Integration Tests
- [ ] [Test case]: [What it verifies]

### E2E Tests
- [ ] [Test case]: [What it verifies]
```

### For "Run Tests"

**Determine test type from context or ask:**
- Unit/Integration tests → Run inline
- E2E tests → Run as background agent (prevents terminal crashes)

**Unit/Integration (vitest/jest) — Run inline:**
```bash
# Vitest
pnpm vitest run

# With coverage
pnpm vitest run --coverage
```

**E2E tests (playwright/cypress) — Run as background agent:**
```
Task Bash run_in_background: true: "Run playwright e2e tests and report results.

Commands:
pnpm playwright test

If tests fail, capture:
- Which tests failed
- Error messages
- Screenshot paths (if any)

Report summary when complete."
```

**Why background agent for E2E:**
- Playwright spawns browsers which can consume significant resources
- If tests hang or crash, your main session continues
- Verbose trace output doesn't fill your context
- You can continue working while tests run

Report results. If failures, offer to debug.

### For "Fix Failing Tests"

Follow `${CLAUDE_PLUGIN_ROOT}/disciplines/systematic-debugging.md`:
1. Read error message carefully
2. Understand what test expects
3. Determine if test or code is wrong
4. Fix at source

**CRITICAL: Never blame "network issues" vaguely.**

It is almost NEVER a network problem. Common actual causes:

| Error Pattern | Likely Cause | NOT the cause |
|---------------|--------------|---------------|
| "ECONNREFUSED" | Server not running, wrong URL | "Network issues" |
| "Timeout" | Slow operation OR payload too large | "Network issues" |
| "400 Bad Request" | Invalid payload format | "Network issues" |
| "500 Server Error" | Bug in your code | "Network issues" |

**For LLM API failures:** See `${CLAUDE_PLUGIN_ROOT}/references/llm-api-testing.md`

## Test Patterns

From `${CLAUDE_PLUGIN_ROOT}/references/testing-patterns.md`:

**Good tests:**
- Test behavior, not implementation
- One assertion per concept
- Clear names describing what's tested
- Real code over mocks when possible

**Bad tests:**
- Testing mock behavior
- Vague names ("test1", "it works")
- Implementation details in assertions

## LLM API Testing

When tests call LLM APIs (OpenRouter, OpenAI, Anthropic, etc.), follow the guidance in:

`${CLAUDE_PLUGIN_ROOT}/references/llm-api-testing.md`

Key points:
- Validate payloads with schema before sending
- Use fast models (-flash, -mini) for tests
- Set aggressive timeouts (5-10s)
- Never conclude "network issues" without evidence

<success_criteria>
Test workflow is complete when:
- [ ] Test framework detected and configured
- [ ] Strategy documented (if creating strategy)
- [ ] Tests written and passing (if creating tests)
- [ ] Failing tests diagnosed and fixed (if fixing)
- [ ] All tests pass (`pnpm vitest run` or equivalent)
- [ ] Optional: test quality review offered (if tests written)
- [ ] Progress journal updated
</success_criteria>

<test_quality_check>
After tests pass, optionally offer a quality check:

"Tests are passing. Would you like me to review the test quality (assertion meaningfulness, isolation, flaky patterns)?"

If accepted, spawn the test-quality-engineer agent:
`${CLAUDE_PLUGIN_ROOT}/agents/review/test-quality-engineer.md`

Present findings and offer to fix any issues found.
</test_quality_check>

<arc_log>
**After completing this skill, append to the activity log.**
See: `${CLAUDE_PLUGIN_ROOT}/references/arc-log.md`

Entry: `/arc:test — [X passing, Y failing]`
</arc_log>

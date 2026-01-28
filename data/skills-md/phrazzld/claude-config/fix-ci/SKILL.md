---
name: fix-ci
description: |
  CI
---

---
description: Analyze CI failure logs, classify failure type, identify root cause
---

# CI

> **THE CI/CD MASTERS**
>
> **Jez Humble**: "If it hurts, do it more frequently, and bring the pain forward."
>
> **Martin Fowler**: "Continuous Integration is a software development practice where members of a team integrate their work frequently."
>
> **Nicole Forsgren**: "Lead time for changes is a key metric for software delivery performance."

You're the CI Specialist who's debugged 500+ pipeline failures. CI failures are not random—they're signals. Your job: classify the failure type, identify root cause, and provide a specific resolution.

## Your Mission

Analyze CI failure logs, classify the failure type, identify root cause, and generate a resolution plan.

**The CI Question**: Is this a code issue, infrastructure issue, or flaky test?

## The CI Philosophy

### Humble's Wisdom: Bring Pain Forward
If CI hurts, the pain is teaching you something. Don't ignore it—lean into it. Frequent small fixes beat infrequent major failures.

### Fowler's Practice: Integrate Frequently
CI exists to catch integration issues early. A failing CI is doing its job. The question is: what did it catch?

### Forsgren's Metric: Lead Time Matters
Every minute CI is red is a minute the team is blocked. Fast diagnosis = fast flow.

## Phase 1: Check CI Status

Use `gh` to check CI status for the current PR:
- If successful, celebrate and stop
- If in progress, wait and check again
- If failed, proceed to analyze

```bash
# Recent workflow runs
gh run list --limit 5

# Specific run details
gh run view <run-id> --log

# PR checks
gh pr checks
```

## Phase 2: Classify Failure Type

### Type 1: Code Issue
**Symptoms**: Test assertion failed, type error, lint error, missing import
**Cause**: Your code has a bug or doesn't meet standards
**Fix**: Fix the code
**Evidence**: Error points to specific file/line in your branch

### Type 2: Infrastructure Issue
**Symptoms**: Timeout, network error, dependency download failed, OOM
**Cause**: CI environment or external service problem
**Fix**: Retry, fix config, add caching, increase resources
**Evidence**: Error mentions network, timeout, resource limits

### Type 3: Flaky Test
**Symptoms**: Fails intermittently, passes on retry, works locally
**Cause**: Non-deterministic test (timing, order, external dependency)
**Fix**: Fix or quarantine the test
**Evidence**: Historical runs show same test passing/failing randomly

### Type 4: Configuration Issue
**Symptoms**: Command not found, wrong version, missing env var
**Cause**: CI config doesn't match local environment
**Fix**: Update workflow YAML, sync versions
**Evidence**: Works locally, fails in CI consistently

## Phase 3: Analyze Failure

**Make the invisible visible**—don't guess at CI failures. Add logging, capture state, trace the failure path.

Create `CI-FAILURE-SUMMARY.md` with:
- **Workflow**: Name, job, step
- **Command**: Exact command that failed
- **Exit code**: What the system reported
- **Error messages**: Full text (no paraphrasing)
- **Stack trace**: If available
- **Environment**: OS, Node/Python version, relevant env vars

### Root Cause Analysis

**For Code Issues**:
- Which test/check failed?
- What's the exact error?
- Which commit introduced it?
- What changed recently?

**For Infrastructure Issues**:
- Which step timed out/failed?
- What external service is involved?
- Is caching working?
- Are resources sufficient?

**For Flaky Tests**:
- Is there timing/sleep involved?
- Database state assumptions?
- External API calls without mocking?
- Test order dependency?

## Phase 4: Generate Resolution Plan

Create `CI-RESOLUTION-PLAN.md` with your analysis and approach.

### TODO Entry Format

```markdown
- [ ] [CODE FIX] Fix failing assertion in auth.test.ts
  ```
  Files: src/auth/__tests__/auth.test.ts:45
  Issue: Expected token to be valid, got undefined
  Cause: Missing await on async call
  Fix: Add await to line 45
  Verify: Run test locally, push, confirm CI passes
  Estimate: 15m
  ```

- [ ] [CI FIX] Increase timeout for integration tests
  ```
  Files: .github/workflows/ci.yml
  Issue: Integration tests timing out at 5m
  Cause: Added new tests, total time exceeds limit
  Fix: Increase timeout-minutes to 10
  Verify: Rerun workflow, confirm completion
  Estimate: 10m
  ```
```

### Labels
- **[CODE FIX]**: Changes to application code or tests
- **[CI FIX]**: Changes to pipeline or environment
- **[FLAKY]**: Test needs quarantine or fix
- **[RETRY]**: Safe to retry without changes

## Phase 5: Communicate

Update PR or create summary with:
- Classification of failure
- Root cause analysis
- Resolution plan
- Verification steps
- Prevention measures

## Common CI Issues

### Tests Pass Locally, Fail in CI
- Node/npm version mismatch
- Missing environment variables
- Different timezone
- Database state assumptions

### Timeout Failures
- Test too slow → optimize or increase timeout
- Network issue → add retry logic
- Deadlock → fix async code
- Resource contention → run tests serially

### Dependency Failures
- npm registry down → retry
- Private package auth → fix NPM_TOKEN
- Version conflict → update lockfile
- Cache corruption → clear cache

## Output Format

```markdown
## CI Failure Analysis

**Workflow**: [Name]
**Run**: [ID/URL]
**Classification**: [Code Issue / Infrastructure / Flaky / Config]

---

### Error Summary

```
[Key error lines - exact text]
```

### Root Cause

**Type**: [Classification]
**Location**: [File/step]
**Cause**: [Specific explanation]

---

### Resolution Plan

**Action**: [Fix / Retry / Quarantine / Config Change]

[Specific fix with code/config]

### Verification

- [ ] [Step to verify fix]

---

### Prevention

[How to prevent this class of failure]
```

## Red Flags

- [ ] Same test fails randomly (flaky—fix or quarantine)
- [ ] CI takes >15 minutes (optimize pipeline)
- [ ] No local reproduction (environment drift)
- [ ] Retrying without understanding (hiding the problem)
- [ ] Multiple unrelated failures (systemic issue)

## Philosophy

> **"CI failures are features, not bugs. They caught an issue before users did."**

**Humble's wisdom**: Bring pain forward. The earlier you find issues, the cheaper they are to fix.

**Fowler's practice**: Integrate frequently. CI failures from small changes are easy to fix; CI failures from big changes are nightmares.

**Forsgren's metric**: Lead time matters. Fast CI resolution = fast delivery.

**Your goal**: Classify, fix, and prevent. Don't just make CI green—understand why it was red.

---

*Run this command when CI fails. Insert specific tasks into TODO.md, then remove temporary files.*

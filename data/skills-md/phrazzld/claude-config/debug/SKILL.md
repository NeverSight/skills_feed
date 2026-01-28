---
name: debug
description: |
  Investigate local development issues: test failures, runtime errors, type errors,
  unexpected behavior. Use when something doesn't work locally, tests fail, builds break,
  or behavior differs from expectation. Distinct from /investigate (production) and
  /fix-ci (CI pipeline). Keywords: debug, why doesn't, broken, failing, error, crash,
  undefined, unexpected, doesn't work, local testing.
argument-hint: <symptoms - error message, unexpected behavior, what's broken>
---

# DEBUG

You're a senior engineer debugging a local issue.

**The user's symptoms:** $ARGUMENTS

## The Codex First-Draft Pattern

Codex investigates. You review and verify.

```bash
codex exec "DEBUG: $SYMPTOMS. Reproduce, isolate root cause, propose fix." \
  --output-last-message /tmp/codex-debug.md 2>/dev/null
```

Then review Codex's findings. Don't investigate yourself first.

## Objective

Find root cause. Propose fix. Verify it works.

## Latitude

- Use any debugging approach: console.log, breakpoints, git bisect, print statements
- Add temporary instrumentation freely
- Run tests, typecheck, lint as needed
- Trust your judgment on tools and approach

## Context Gathering

**What changed?**
- `git diff` - uncommitted changes
- `git log --oneline -10` - recent commits
- `git stash list` - stashed changes

**What's the environment?**
- Node/Python/Go version
- Dependency versions (`package.json`, lockfiles)
- Environment variables

**What's the exact error?**
- Full error message and stack trace
- Reproduction steps
- Expected vs actual behavior

## Classification (informational, not prescriptive)

| Type | Signals | Likely Approach |
|------|---------|-----------------|
| Test failure | Jest/Vitest output, assertion error | Read test, trace expectation |
| Runtime error | Exception, crash, undefined | Stack trace → source → state |
| Type error | TS complaint, inference issue | Read error, check types |
| Build failure | Bundler error, missing module | Check deps, config |
| Behavior mismatch | "It should do X but does Y" | Trace code path, find divergence |

## Output

Report what you found:
- **Root cause**: What's actually wrong
- **Fix**: How to resolve it
- **Verification**: How to confirm it's fixed

No work log required. Focus on solving the problem.

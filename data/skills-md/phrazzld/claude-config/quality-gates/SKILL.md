---
name: quality-gates
description: |
  Apply quality gate standards for git hooks, testing, CI/CD, and automation using Lefthook, Vitest, GitHub Actions, and quality enforcement. Use when setting up quality infrastructure, configuring hooks, discussing automation, or reviewing quality practices.
---

# /quality-gates

Ensure this project has complete quality infrastructure. Audit, fix, verify.

## What This Does

Examines the project's quality gates, identifies gaps, implements fixes, and verifies everything works. Every run does all of this—no partial modes.

## Process

### 1. Audit

Spawn the `infrastructure-guardian` agent to do a comprehensive audit. It knows what to check.

Also run this quick assessment:
```bash
[ -f "lefthook.yml" ] && echo "✓ Lefthook" || echo "✗ Lefthook"
[ -f "vitest.config.ts" ] || [ -f "vitest.config.js" ] && echo "✓ Vitest" || echo "✗ Vitest"
[ -f ".github/workflows/ci.yml" ] && echo "✓ CI workflow" || echo "✗ CI workflow"
[ -f "commitlint.config.js" ] || [ -f "commitlint.config.cjs" ] && echo "✓ Commitlint" || echo "✗ Commitlint"
grep -q "coverage" package.json && echo "✓ Coverage script" || echo "✗ Coverage script"
```

For test quality specifically, spawn `test-strategy-architect` if tests exist but quality is uncertain.

### 2. Plan

Based on audit findings, identify all gaps. Prioritize:

**Must have (every project):**
- Lefthook with pre-commit hooks (lint, format, typecheck on staged files)
- Lefthook pre-push hooks (test, build)
- Vitest configured with coverage
- GitHub Actions CI (lint, typecheck, test, build on every PR)
- Branch protection on main

**Should have (production apps):**
- Conventional commits via commitlint
- Coverage reporting in PRs
- E2E tests for critical flows
- Security audit in CI

### 3. Execute

Fix every gap identified. Delegate implementation to Codex where appropriate.

**Installing Lefthook:**
```bash
pnpm add -D lefthook
pnpm lefthook install
```
Then create `lefthook.yml` per `references/lefthook-config.md`.

**Installing Vitest:**
```bash
pnpm add -D vitest @vitest/coverage-v8
```
Then create config per `references/vitest-config.md`.

**Creating CI workflow:**
Create `.github/workflows/ci.yml` per `references/github-actions.md`.

**Setting up commitlint:**
```bash
pnpm add -D @commitlint/cli @commitlint/config-conventional
```
Add commit-msg hook to lefthook.yml.

**Branch protection:**
Guide user through GitHub settings or use `gh api` if they want automation.

### 4. Verify

Prove it works. Don't just check files exist—actually run the gates.

```bash
# Test pre-commit hook
echo "test" >> /tmp/test-file && git add /tmp/test-file
pnpm lefthook run pre-commit

# Test CI locally (if act installed)
act -j quality-checks --dryrun

# Test vitest runs
pnpm test --run

# Verify commitlint
echo "bad commit message" | pnpm commitlint
# Should fail

echo "feat: valid message" | pnpm commitlint
# Should pass
```

Report verification results. If anything fails, fix it before declaring done.

## Tool Choices

**Lefthook over Husky.** Go binary, faster, parallel execution, simpler YAML config, combines Husky + lint-staged.

**Vitest over Jest.** Faster, native ESM, built-in coverage with v8, great TypeScript support.

**vitest-coverage-report-action over Codecov.** Zero external service, shows coverage diff in PRs, links to uncovered lines.

These are strong recommendations, not mandates. If the project already has working alternatives, don't churn—improve what exists.

## Coverage Philosophy

Coverage is a diagnostic tool, not a goal.

- 60% meaningful coverage beats 95% testing implementation details
- Patch coverage: 80%+ for new code
- Critical paths (payment, auth): 90%+
- Overall: Track but don't block

## Anti-Patterns

- **Husky** → Prefer Lefthook
- **Arbitrary coverage targets** → Use coverage as diagnostic
- **Testing implementation details** → Test behavior
- **Heavy mocking** → Prefer integration tests
- **Skipping hooks routinely** → Fix the root cause
- **CI only on main** → Test every PR

## References

Detailed configs in `references/`:
- `lefthook-config.md` — Hook configurations
- `github-actions.md` — CI workflows
- `vitest-config.md` — Test configuration
- `branch-protection.md` — GitHub settings

## Philosophy

This codebase will outlive you. Every shortcut becomes someone else's burden. The patterns you establish will be copied. The corners you cut will be cut again.

Quality gates exist to fight entropy—to ensure the codebase stays better than you found it.

## What You Get

When complete:
- Lefthook pre-commit: lint, format, typecheck (fast, staged files only)
- Lefthook pre-push: test, build (comprehensive)
- Vitest with coverage configured
- GitHub Actions CI running on every PR
- Branch protection requiring CI to pass
- Commitlint enforcing conventional commits
- Verified end-to-end

User can:
- Commit code and see hooks run automatically
- Push and see tests run before push completes
- Open a PR and see CI results
- See coverage diff in PR comments
- Trust that main is always green

## Testing Standards Reference

See `references/testing-standards.md` for detailed guidance on:
- Vitest configuration
- Coverage philosophy (test boundaries, not lines)
- Unit vs integration vs E2E testing
- Git hooks setup with simple-git-hooks
- CI/CD with GitHub Actions

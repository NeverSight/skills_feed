---
name: validate-before-merge
description: Run full validation to ensure code is ready for merge. Use before merging PRs, when asked to validate readiness, or as a final check before requesting review.
---

# Validate Before Merge

## Overview

This skill runs all checks that CI performs to validate code is ready for merge. Use this to catch issues locally before CI runs.

## Full Validation Sequence

Run these checks in order. Each step must pass before proceeding.

### Step 1: Lint and Format Check

```bash
pnpm lint:check
```

**Expected**: No errors or warnings
**If fails**: Run `pnpm format` to auto-fix

### Step 2: Build All Packages

```bash
pnpm build
```

**Expected**: Successful build with no TypeScript errors
**If fails**: Fix type errors in the reported files

### Step 3: Unit Tests

```bash
pnpm test:ci
```

**Expected**: All tests pass
**If fails**: 
- Review failing test output
- Fix code or update tests as appropriate
- Never skip failing tests without justification

### Step 4: Visual Regression Tests (if UI changed)

Only required if changes touch:
- `packages/keychain/src/components/`
- `packages/keychain/src/hooks/` (UI-related)
- Storybook configuration

```bash
pnpm test:storybook
```

**Expected**: All visual comparisons pass
**If fails with intentional changes**: 
```bash
pnpm test:storybook:update
git add packages/*/__image_snapshots__/
git commit -m "chore: update storybook snapshots"
```

### Step 5: Verify No Uncommitted Changes

```bash
git status
```

**Expected**: Clean working directory (or only untracked files you intend to ignore)

## Quick Validation Script

For a fast validation (similar to pre-commit):

```bash
pnpm lint:check && pnpm build && pnpm test
```

## Full CI Mirror

To exactly mirror what GitHub Actions runs:

```bash
# Clean environment (optional but recommended)
pnpm clean && pnpm i

# Quality job
pnpm lint:check

# Test job
pnpm build
pnpm test:ci --coverage

# Storybook job (if UI changes)
pnpm test:storybook
```

## Validation Checklist

Before requesting merge, verify:

- [ ] `pnpm lint:check` passes
- [ ] `pnpm build` succeeds with no errors
- [ ] `pnpm test:ci` all tests pass
- [ ] `pnpm test:storybook` passes (if UI changed)
- [ ] No console.log or debug statements left in code
- [ ] No hardcoded secrets or credentials
- [ ] PR description accurately describes changes
- [ ] Related issues are linked

## Common Pre-Merge Issues

### Forgotten console.log
```bash
grep -r "console.log" packages/*/src --include="*.ts" --include="*.tsx" | grep -v "test"
```

### Outdated dependencies
```bash
git fetch origin main
git rebase origin/main
```

### Merge conflicts
```bash
git fetch origin main
git merge origin/main
# Resolve conflicts
pnpm build  # Verify after resolving
```

## Reporting Results

After validation, report:

```markdown
## Validation Results

- [x] Lint: Passed
- [x] Build: Passed  
- [x] Tests: Passed (X tests, X% coverage)
- [x] Storybook: Passed (or N/A if no UI changes)

Ready for merge.
```

Or if issues found:

```markdown
## Validation Results

- [x] Lint: Passed
- [ ] Build: Failed - Type error in packages/controller/src/account.ts:42
- [ ] Tests: Not run (blocked by build failure)

### Issues to Fix
1. Type error: Property 'foo' does not exist on type 'Bar'
```

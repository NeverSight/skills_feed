---
name: validating-pre-commit
description: "Runs quality gate checks before commit or push. Executes lint fixes, TypeScript compilation, tests, and CI validation. Reproduces CI failures locally. Triggers on: pre-commit, pre-push, quality check, CI check, lint check, type check, validate changes, check:fix, pnpm test."
allowed-tools: "Read, Bash(pnpm:*), Bash(npx:*), Bash(rm:*)"
---

# Pre-Commit Quality Gate

## Purpose

Ensure all code quality standards are met before committing or pushing changes. This skill runs the mandatory quality checklist and reports any failures with actionable fixes.

## When to Use

- Before creating a commit
- Before pushing to remote
- After making significant changes
- When CI is failing and you need to reproduce locally
- To validate changes pass all quality gates

## Table of Contents

- [Mandatory Quality Checklist](#mandatory-quality-checklist)
  - [Step 1: Auto-Fix Linting and Formatting](#step-1-auto-fix-linting-and-formatting)
  - [Step 2: Verify TypeScript Compilation](#step-2-verify-typescript-compilation)
  - [Step 3: Run All Tests](#step-3-run-all-tests)
  - [Step 4: Strict TypeScript Check](#step-4-strict-typescript-check)
  - [Step 5: Final CI Validation](#step-5-final-ci-validation)
- [E2E CLI Testing Protocol](#e2e-cli-testing-protocol)
- [Quick Reference Commands](#quick-reference-commands)
- [Common Failure Patterns](#common-failure-patterns)
- [Automated Checks](#automated-checks)
- [References](#references)

## Mandatory Quality Checklist

Execute these steps **in order**. All must pass before committing.

### Step 1: Auto-Fix Linting and Formatting

```bash
pnpm check:fix
```

**Purpose**: Auto-fix all Biome linting and formatting issues.

**Common Fixes Applied**:
- Import organization
- Trailing commas
- Quote style
- Indentation
- Line endings

**If Issues Remain**: Some issues cannot be auto-fixed. Review the output and manually address:
- Complexity warnings
- Unused variables
- Type errors

### Step 2: Verify TypeScript Compilation

```bash
pnpm build
```

**Purpose**: Ensure the project compiles without errors.

**Common Failures**:
- Type mismatches
- Missing exports
- Import resolution errors

**Troubleshooting**:
- Check recent changes for type errors
- Verify imports match exports
- Ensure new files are properly typed

### Step 3: Run All Tests

```bash
pnpm test
```

**Purpose**: Ensure all tests pass.

**If Tests Fail**:
1. Read the failure message carefully
2. Check if the test expectation matches new behavior
3. Update test or fix implementation accordingly
4. Re-run affected tests: `pnpm test -- --filter=<test-file>`

### Step 4: Strict TypeScript Check

```bash
npx tsc --noEmit
```

**Purpose**: Validate TypeScript with strict checking (catches more than build).

**Common Issues**:
- Implicit `any` types
- Unused imports/variables
- Stricter null checking

### Step 5: Final CI Validation

```bash
pnpm check:ci
```

**Purpose**: Run the same checks that CI will run.

**This Combines**:
- Linting without auto-fix
- Format checking
- TypeScript compilation

## E2E CLI Testing Protocol

**When to Run**: Before pushing changes that affect core CLI functionality (commands, services, repositories).

### Full E2E Validation Workflow

```bash
# Test credentials
--url=https://store-rzalldyg.saleor.cloud/graphql/
--token=YbE8g7ZNl0HkxdK92pfNdLJVQwV0Xs

# 1. Clean slate
rm -rf config.yml

# 2. Fresh introspection
pnpm dev introspect --url=<URL> --token=<TOKEN>

# 3. Make test changes to config.yml (optional)

# 4. Deploy changes
pnpm dev deploy --url=<URL> --token=<TOKEN>

# 5. Test idempotency (deploy again - should have no changes)
pnpm dev deploy --url=<URL> --token=<TOKEN>

# 6. Clean again
rm config.yml

# 7. Re-introspect
pnpm dev introspect --url=<URL> --token=<TOKEN>

# 8. Verify no drift (should show no changes)
pnpm dev diff --url=<URL> --token=<TOKEN>
```

**Success Criteria**:
- Step 5 shows no changes (idempotency)
- Step 8 shows no diff (round-trip consistency)

## Quick Reference Commands

| Check | Command | Purpose |
|-------|---------|---------|
| **All checks** | `./scripts/validate-all.sh` | Run all checks in sequence |
| Auto-fix | `pnpm check:fix` | Fix lint/format issues |
| Build | `pnpm build` | Compile TypeScript |
| Test | `pnpm test` | Run all tests |
| Type check | `npx tsc --noEmit` | Strict TS validation |
| CI check | `pnpm check:ci` | Full CI validation |
| Lint only | `pnpm lint` | Check linting |
| Format only | `pnpm format` | Check formatting |

### One-Command Validation

Run all quality checks in sequence:

```bash
./.claude/skills/pre-commit-quality/scripts/validate-all.sh
```

This script executes all 5 steps of the mandatory checklist and stops on first failure.

## Common Failure Patterns

### Biome Errors

**"Unexpected any"**:
```typescript
// BAD
const data: any = response;

// GOOD
const data: ResponseType = response;
```

**"Unused import"**:
Remove the import or use it.

**"Prefer template literal"**:
```typescript
// BAD
const msg = 'Hello ' + name;

// GOOD
const msg = `Hello ${name}`;
```

### TypeScript Errors

**"Object is possibly undefined"**:
```typescript
// BAD
const value = obj.prop.nested;

// GOOD
const value = obj?.prop?.nested;
// OR with assertion if certain
const value = obj!.prop!.nested; // Only if you're sure
```

**"Type 'X' is not assignable to type 'Y'"**:
Check the type definitions and ensure compatibility.

### Test Failures

**Mock not returning expected value**:
```typescript
vi.mocked(mockService.method).mockResolvedValue(expectedValue);
```

**Assertion mismatch**:
Review the expected vs actual output and update accordingly.

## Automated Checks

The project has pre-push hooks configured via Husky:
- `.husky/pre-push`: Generates schema documentation

These run automatically - no manual action needed.

## References

- `scripts/validate-all.sh` - One-command validation script
- `{baseDir}/docs/CLAUDE.md` - Full pre-push checklist
- `{baseDir}/docs/TESTING_PROTOCOLS.md` - E2E testing details
- `{baseDir}/biome.json` - Linting configuration

## Related Skills

- **Code standards**: See `reviewing-typescript-code` for quality criteria
- **CI integration**: See `managing-github-ci` for workflow troubleshooting
- **Test failures**: See `analyzing-test-coverage` for test debugging

## Quick Reference Rule

For a condensed quick reference, see `.claude/rules/deployment-safety.md` (always loaded - applies to all files).

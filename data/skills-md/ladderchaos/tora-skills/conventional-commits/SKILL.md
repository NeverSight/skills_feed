---
name: conventional-commits
description: Standardized commit message format following Conventional Commits specification. Use this skill when creating commits, reviewing commit history, or generating changelogs.
---

# Conventional Commits

Standardized commit message format for readable history and automated changelogs.

## When This Skill Activates

- Creating git commits
- Reviewing commit message quality
- Generating changelogs
- Setting up commit hooks

## Commit Message Format

```
<type>(<scope>): <subject>

[optional body]

[optional footer(s)]
```

### Types

| Type | Description | Changelog Section |
|------|-------------|-------------------|
| `feat` | New feature | Added |
| `fix` | Bug fix | Fixed |
| `docs` | Documentation only | - |
| `style` | Formatting, no code change | - |
| `refactor` | Code change, no feature/fix | Changed |
| `perf` | Performance improvement | Changed |
| `test` | Adding/updating tests | - |
| `chore` | Build, deps, config | - |
| `ci` | CI/CD changes | - |
| `revert` | Revert previous commit | - |

### Scope (Optional)

Indicates the area affected:

```
feat(auth): add OAuth2 login
fix(api): handle null response
refactor(contracts): extract base class
```

Common scopes:
- Component/module name
- `contracts`, `frontend`, `api`
- `deps`, `config`, `ci`

### Subject Line Rules

- Imperative mood: "add" not "added" or "adds"
- Lowercase first letter
- No period at end
- Max 50 characters (72 hard limit)

**Good:**
```
feat(market): add limit order support
fix(vault): prevent double withdrawal
refactor(sdk): simplify type exports
```

**Bad:**
```
feat(market): Added limit order support.   # past tense, period
Fix vault bug                              # not specific
update stuff                               # vague
```

### Body (Optional)

Explain the "why" when not obvious:

```
fix(settlement): handle edge case in payout calculation

The previous implementation failed when market resolved
to INVALID with partial fills. Now correctly refunds
the proportional collateral.
```

### Breaking Changes

Use `!` after type or `BREAKING CHANGE:` footer:

```
feat(api)!: change response format to v2

BREAKING CHANGE: Response now returns `data` wrapper.
Clients must update parsing logic.
```

### Footer References

Link to issues/PRs:

```
fix(auth): resolve session timeout issue

Closes #123
Refs #456
```

## Examples

### Simple Feature
```
feat(orderbook): add price level aggregation
```

### Bug Fix with Context
```
fix(crossing): prevent self-trade in atomic match

Orders from same address were incorrectly matching
against each other when prices crossed.

Closes #89
```

### Refactor
```
refactor(contracts): extract shared validation logic

Move duplicate checks from Market and Vault into
BaseValidation contract.
```

### Breaking Change
```
feat(sdk)!: require explicit chain ID in config

BREAKING CHANGE: chainId is now required in SDK init.
Auto-detection removed for security reasons.

Migration: Add chainId to your SDK configuration.
```

### Chore/Dependencies
```
chore(deps): upgrade viem to 2.0

chore(ci): add gas snapshot to PR checks
```

## Quick Reference

```
feat:     New feature (MINOR version bump)
fix:      Bug fix (PATCH version bump)
!:        Breaking change (MAJOR version bump)
docs:     Documentation
style:    Formatting
refactor: Code restructure
perf:     Performance
test:     Tests
chore:    Maintenance
```

## Commit Hooks Setup

Add to `.husky/commit-msg`:

```bash
#!/bin/sh
npx commitlint --edit $1
```

Or with simple regex check:

```bash
#!/bin/sh
if ! grep -qE "^(feat|fix|docs|style|refactor|perf|test|chore|ci|revert)(\(.+\))?(!)?: .{1,50}" "$1"; then
  echo "Invalid commit message format"
  exit 1
fi
```

## Changelog Generation

Commits automatically map to changelog:

| Commit | Changelog |
|--------|-----------|
| `feat(x): add Y` | **Added**: Y |
| `fix(x): resolve Z` | **Fixed**: Z |
| `refactor(x): improve W` | **Changed**: W |
| `feat!: breaking` | **BREAKING**: ... |

---
name: log-quality-issues
description: |
  Run /check-quality, then create GitHub issues for all findings.
  Issues are created with priority labels and structured format.
  Use /fix-quality instead if you want to fix issues immediately.
---

# /log-quality-issues

Run quality gates audit and create GitHub issues for all findings.

## What This Does

1. Invoke `/check-quality` to audit quality infrastructure
2. Parse findings by priority (P0-P3)
3. Check existing issues to avoid duplicates
4. Create GitHub issues for each finding

**This is an issue-creator.** It creates work items, not fixes. Use `/fix-quality` to fix issues.

## Process

### 1. Run Primitive

Invoke `/check-quality` skill to get structured findings.

### 2. Check Existing Issues

```bash
gh issue list --state open --label "domain/quality" --limit 50
```

### 3. Create Issues

For each finding:

```bash
gh issue create \
  --title "[P0] No test runner configured" \
  --body "$(cat <<'EOF'
## Problem
No testing framework (Vitest/Jest) is configured. Code changes cannot be validated.

## Impact
- Regressions go undetected
- Refactoring is dangerous
- CI cannot verify changes
- No confidence in deployments

## Suggested Fix
Run `/fix-quality` or manually:
```bash
pnpm add -D vitest @vitest/coverage-v8
```

Then create `vitest.config.ts` with coverage enabled.

---
Created by `/log-quality-issues`
EOF
)" \
  --label "priority/p0,domain/quality,type/chore"
```

### 4. Issue Format

**Title:** `[P{0-3}] Quality gap description`

**Labels:**
- `priority/p0` | `priority/p1` | `priority/p2` | `priority/p3`
- `domain/quality`
- `type/chore`

**Body:**
```markdown
## Problem
What quality infrastructure is missing

## Impact
Risk and consequences of the gap

## Suggested Fix
Commands or skill to run

---
Created by `/log-quality-issues`
```

## Priority Mapping

| Gap | Priority |
|-----|----------|
| No test runner | P0 |
| No CI workflow | P0 |
| No coverage configured | P1 |
| No git hooks | P1 |
| No linting | P1 |
| TypeScript not strict | P1 |
| No commitlint | P2 |
| No coverage in PRs | P2 |
| Tool upgrade opportunities | P3 |

## Output

After running:
```
Quality Issues Created:
- P0: 2 (no tests, no CI)
- P1: 3 (coverage, hooks, linting)
- P2: 2 (commitlint, PR coverage)
- P3: 1 (tool upgrades)

Total: 8 issues created
View: gh issue list --label domain/quality
```

## Related

- `/check-quality` - The primitive (audit only)
- `/fix-quality` - Fix quality infrastructure
- `/quality-gates` - Full quality setup workflow
- `/groom` - Full backlog grooming

---
name: log-production-issues
description: |
  Run /check-production, then create GitHub issues for all findings.
  Issues are created with priority labels and structured format.
  Use /triage instead if you want to fix issues immediately.
---

# /log-production-issues

Run production health audit and create GitHub issues for all findings.

## What This Does

1. Invoke `/check-production` to audit production health
2. Parse findings by priority (P0-P3)
3. Check existing issues to avoid duplicates
4. Create GitHub issues for each finding

**This is an issue-creator.** It creates work items, not fixes. Use `/triage` to fix issues.

## Process

### 1. Run Primitive

Invoke `/check-production` skill to get structured findings.

### 2. Check Existing Issues

```bash
gh issue list --state open --label "domain/production" --limit 50
```

### 3. Create Issues

For each finding, create a GitHub issue:

```bash
gh issue create \
  --title "[P0] PaymentIntent failed - 23 users affected" \
  --body "$(cat <<'EOF'
## Problem
Sentry issue SENTRY-123 shows PaymentIntent failures affecting 23 users.

## Impact
- Users cannot complete checkout
- Revenue loss estimated at $X/hour
- First seen: 2 hours ago

## Location
`api/checkout.ts:45`

## Suggested Fix
Run `/triage investigate SENTRY-123` to diagnose and fix.

## Source
- Sentry: SENTRY-123
- Score: 147

---
Created by `/log-production-issues`
EOF
)" \
  --label "priority/p0,domain/production,type/bug"
```

### 4. Issue Format

All issues follow this structure:

**Title:** `[P{0-3}] Concise problem statement`

**Labels:**
- `priority/p0` | `priority/p1` | `priority/p2` | `priority/p3`
- `domain/production`
- `type/bug` | `type/enhancement` | `type/chore`

**Body:**
```markdown
## Problem
What's wrong (specific, measurable)

## Impact
Who/what is affected, severity

## Location
File:line or service/component

## Suggested Fix
Skill to run or action to take

## Source
Where this was detected (Sentry ID, log line, etc.)

---
Created by `/log-production-issues`
```

## Deduplication

Before creating an issue:
1. Search for existing issues with same Sentry ID or similar title
2. If found: Update existing issue with new occurrence count
3. If not found: Create new issue

```bash
# Check for existing
gh issue list --state open --search "SENTRY-123" --limit 5
```

## Priority Mapping

| Source | Priority |
|--------|----------|
| Active Sentry errors (>5 users) | P0 |
| 5xx errors in Vercel logs | P1 |
| Slow health endpoint | P1 |
| Silent failures (empty catch) | P2 |
| Missing monitoring | P3 |

## Output

After running:
```
Production Issues Created:
- P0: 1 (payment failures)
- P1: 2 (5xx errors, slow health)
- P2: 2 (silent failures)
- P3: 1 (missing monitoring)

Total: 6 issues created
View: gh issue list --label domain/production
```

## Related

- `/check-production` - The primitive (audit only)
- `/triage` - Fix production issues
- `/groom` - Full backlog grooming (runs this skill)

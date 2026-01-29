---
name: log-lightning-issues
description: |
  Run /check-lightning, then create GitHub issues for all findings.
  Issues are created with priority labels and structured format.
  Use /fix-lightning instead if you want to fix issues immediately.
---

# /log-lightning-issues

Run Lightning integration audit and create GitHub issues for all findings.

## What This Does

1. Invoke `/check-lightning` to audit Lightning integration
2. Parse findings by priority (P0-P3)
3. Check existing issues to avoid duplicates
4. Create GitHub issues for each finding

**This is an issue-creator.** It creates work items, not fixes. Use `/fix-lightning` to fix issues.

## Process

### 1. Run Primitive

Invoke `/check-lightning` skill to get structured findings.

### 2. Check Existing Issues

```bash
gh issue list --state open --label "domain/lightning" --limit 50
```

### 3. Create Issues

For each finding:

```bash
gh issue create \
  --title "[P0] LND macaroon hardcoded" \
  --body "$(cat <<'EOF'
## Problem
LND macaroon is committed to repo. Full node control risk.

## Impact
- Attacker can control node
- Funds theft possible
- Channel state manipulation risk
- Compliance breach

## Location
`config/lightning.ts`

## Suggested Fix
Run `/fix-lightning` or manually move to env:
```typescript
const macaroonHex = process.env.LND_MACAROON_HEX!;
```

---
Created by `/log-lightning-issues`
EOF
)" \
  --label "priority/p0,domain/lightning,type/bug"
```

### 4. Issue Format

**Title:** `[P{0-3}] Lightning issue description`

**Labels:**
- `priority/p0` | `priority/p1` | `priority/p2` | `priority/p3`
- `domain/lightning`
- `type/bug` | `type/enhancement` | `type/chore`

**Body:**
```markdown
## Problem
What's wrong with Lightning integration

## Impact
Business/security/user impact

## Location
File:line if applicable

## Suggested Fix
Code snippet or skill to run

---
Created by `/log-lightning-issues`
```

## Priority Mapping

| Gap | Priority |
|-----|----------|
| Macaroon or seed in repo | P0 |
| RPC exposed without TLS | P0 |
| Missing macaroon auth | P0 |
| No invoice settlement verification | P1 |
| No payment timeout handling | P1 |
| No fee caps | P1 |
| No idempotency for payment requests | P2 |
| Missing retry/backoff | P2 |
| Monitoring/alerts missing | P2 |
| Advanced routing features | P3 |

## Output

After running:
```
Lightning Issues Created:
- P0: 2 (macaroon, TLS)
- P1: 2 (settlement checks, timeouts)
- P2: 3 (idempotency, retries, alerts)
- P3: 1 (routing features)

Total: 8 issues created
View: gh issue list --label domain/lightning
```

## Related

- `/check-lightning` - The primitive (audit only)
- `/fix-lightning` - Fix Lightning issues
- `/lightning` - Full Lightning lifecycle
- `/lightning-health` - Node diagnostics
- `/groom` - Full backlog grooming

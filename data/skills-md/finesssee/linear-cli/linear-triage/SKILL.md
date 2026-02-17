---
name: linear-triage
description: Manage Linear triage inbox. Use for unassigned issues needing attention.
allowed-tools: Bash
---

# Triage

```bash
# List triage issues (unassigned, no project)
linear-cli tr list
linear-cli tr list -t ENG            # Filter by team
linear-cli tr list --output json

# Claim issue (assign to self, move to backlog)
linear-cli tr claim LIN-123

# Snooze issue
linear-cli tr snooze LIN-123 --duration 1d   # Snooze 1 day
linear-cli tr snooze LIN-123 --duration 1w   # Snooze 1 week
```

## Duration Shortcuts

`1d`, `2d`, `1w`, `2w`, `1m`

## Flags

| Flag | Purpose |
|------|---------|
| `--output json` | JSON output |

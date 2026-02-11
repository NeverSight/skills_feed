---
name: linear-update
description: Update Linear issues. Use when changing status, priority, assignee, or labels.
allowed-tools: Bash
---

# Update Issues

```bash
# Status
linear-cli i update LIN-123 -s Done
linear-cli i update LIN-123 -s "In Progress"

# Priority
linear-cli i update LIN-123 -p 1    # 1=urgent, 2=high, 3=normal, 4=low

# Assignee
linear-cli i update LIN-123 -a me
linear-cli i update LIN-123 -a "John Doe"

# Labels
linear-cli i update LIN-123 -l bug
linear-cli i update LIN-123 -l bug -l urgent

# Due date
linear-cli i update LIN-123 --due tomorrow
linear-cli i update LIN-123 --due +3d

# Agent patterns
linear-cli i update LIN-123 -s Done --id-only
```

## Comments

```bash
linear-cli cm list LIN-123
linear-cli cm create LIN-123 -b "Fixed in commit abc"
```

## Flags

| Flag | Purpose |
|------|---------|
| `--id-only` | Return ID only |
| `--output json` | JSON output |

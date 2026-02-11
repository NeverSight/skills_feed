---
name: linear-history
description: View Linear issue history. Use for activity logs and audit trails.
allowed-tools: Bash
---

# Issue History

```bash
# View issue activity
linear-cli hist issue LIN-123
linear-cli hist issue LIN-123 --output json

# With pagination
linear-cli hist issue LIN-123 --limit 50
linear-cli hist issue LIN-123 --all
```

## Flags

| Flag | Purpose |
|------|---------|
| `--limit N` | Max entries |
| `--all` | Fetch all |
| `--output json` | JSON output |

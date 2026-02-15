---
name: linear-cycles
description: View Linear sprint cycles. Use when checking current cycle or listing cycles.
allowed-tools: Bash
---

# Cycles

```bash
# List cycles
linear-cli c list -t ENG             # Team cycles
linear-cli c list -t ENG --output json

# Current cycle
linear-cli c current -t ENG
linear-cli c current -t ENG --output json
```

## Flags

| Flag | Purpose |
|------|---------|
| `--output json` | JSON output |
| `--compact` | No formatting |

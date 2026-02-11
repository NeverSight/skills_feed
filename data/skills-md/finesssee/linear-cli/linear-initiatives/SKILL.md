---
name: linear-initiatives
description: View Linear initiatives. Use for high-level tracking across projects.
allowed-tools: Bash
---

# Initiatives

```bash
# List initiatives
linear-cli init list
linear-cli init list --output json

# Get initiative details
linear-cli init get INITIATIVE_ID
linear-cli init get INITIATIVE_ID --output json
```

## Flags

| Flag | Purpose |
|------|---------|
| `--output json` | JSON output |
| `--compact` | No formatting |

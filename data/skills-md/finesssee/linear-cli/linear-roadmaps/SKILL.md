---
name: linear-roadmaps
description: View Linear roadmaps. Use when viewing roadmap planning.
allowed-tools: Bash
---

# Roadmaps

```bash
# List roadmaps
linear-cli rm list
linear-cli rm list --output json

# Get roadmap details
linear-cli rm get ROADMAP_ID
linear-cli rm get ROADMAP_ID --output json
```

## Flags

| Flag | Purpose |
|------|---------|
| `--output json` | JSON output |
| `--compact` | No formatting |

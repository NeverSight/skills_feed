---
name: linear-metrics
description: View Linear metrics. Use for velocity, burndown, and progress tracking.
allowed-tools: Bash
---

# Metrics

```bash
# Cycle metrics (velocity, burndown)
linear-cli mt cycle CYCLE_ID
linear-cli mt cycle CYCLE_ID --output json

# Project progress
linear-cli mt project PROJECT_ID
linear-cli mt project PROJECT_ID --output json

# Team velocity over time
linear-cli mt velocity TEAM_KEY
linear-cli mt velocity ENG --cycles 5    # Last 5 cycles
```

## Flags

| Flag | Purpose |
|------|---------|
| `--cycles N` | Number of cycles |
| `--output json` | JSON output |

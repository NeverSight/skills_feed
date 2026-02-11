---
name: linear-list
description: List and get Linear issues. Use when viewing issues, checking status, or fetching issue details.
allowed-tools: Bash
---

# List/Get Issues

```bash
# List issues
linear-cli i list                    # All
linear-cli i list -t ENG             # By team
linear-cli i list -s "In Progress"   # By status
linear-cli i list --assignee me      # My issues

# Get issue(s)
linear-cli i get LIN-123
linear-cli i get LIN-1 LIN-2 LIN-3   # Multiple

# Agent-optimized
linear-cli i list --output json --compact --fields identifier,title,state.name
```

## Flags

| Flag | Purpose |
|------|---------|
| `--output json` | JSON output |
| `--compact` | No formatting |
| `--fields a,b` | Select fields |
| `--sort field` | Sort results |

## Exit Codes

`0`=Success, `1`=Error, `2`=Not found, `3`=Auth error

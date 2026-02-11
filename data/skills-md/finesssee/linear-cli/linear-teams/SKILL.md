---
name: linear-teams
description: View Linear teams and users. Use when listing teams or viewing user profiles.
allowed-tools: Bash
---

# Teams

```bash
# List teams
linear-cli t list
linear-cli t list --output json

# Get team details
linear-cli t get ENG
linear-cli t get TEAM_ID --output json
```

# Users

```bash
# List users
linear-cli u list                    # All workspace users
linear-cli u list --team ENG         # Team members only

# Current user
linear-cli u me
linear-cli u me --output json
```

## Flags

| Flag | Purpose |
|------|---------|
| `--output json` | JSON output |
| `--compact` | No formatting |

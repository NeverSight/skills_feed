---
name: linear-favorites
description: Manage Linear favorites. Use for quick access to issues and projects.
allowed-tools: Bash
---

# Favorites

```bash
# List favorites
linear-cli fav list
linear-cli fav list --output json

# Add to favorites
linear-cli fav add LIN-123           # Add issue
linear-cli fav add PROJECT_ID        # Add project

# Remove from favorites
linear-cli fav remove LIN-123
```

## Flags

| Flag | Purpose |
|------|---------|
| `--output json` | JSON output |

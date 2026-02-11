---
name: linear-projects
description: Manage Linear projects. Use when listing, creating, updating, or viewing projects.
allowed-tools: Bash
---

# Projects

```bash
# List projects
linear-cli p list                    # All projects
linear-cli p list --archived         # Include archived

# Get project
linear-cli p get PROJECT_ID

# Create project
linear-cli p create "Q1 Roadmap" -t ENG
linear-cli p create "Feature" -t ENG --id-only

# Update project
linear-cli p update PROJECT_ID --name "New Name"
linear-cli p update PROJECT_ID --state completed

# Add labels
linear-cli p add-labels PROJECT_ID -l label1 -l label2

# Delete
linear-cli p delete PROJECT_ID --force
```

## Flags

| Flag | Purpose |
|------|---------|
| `--id-only` | Return ID only |
| `--output json` | JSON output |

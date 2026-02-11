---
name: linear-export
description: Export Linear issues. Use when exporting to CSV or Markdown.
allowed-tools: Bash
---

# Export

```bash
# Export to CSV
linear-cli exp csv -t ENG                     # Export team issues
linear-cli exp csv -t ENG -f issues.csv       # Export to file
linear-cli exp csv --all -t ENG               # All pages

# Export to Markdown
linear-cli exp markdown -t ENG
linear-cli exp markdown -t ENG -f issues.md

# With filters
linear-cli exp csv -t ENG -s "In Progress"
linear-cli exp csv -t ENG --assignee me
```

## Flags

| Flag | Purpose |
|------|---------|
| `-f FILE` | Output to file |
| `--all` | Export all pages |
| `-t TEAM` | Filter by team |

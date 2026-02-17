---
name: linear-search
description: Search Linear issues and projects. Use when finding issues, looking up bugs, or searching the backlog.
allowed-tools: Bash
---

# Linear Search

Search Linear.app issues and projects using `linear-cli`.

## Search Issues

```bash
# Search by text
linear-cli s issues "authentication bug"

# Limit results
linear-cli s issues "login" --limit 5

# JSON output for parsing
linear-cli s issues "error" --output json

# With specific fields
linear-cli s issues "crash" --output json --fields identifier,title,state.name
```

## Search Projects

```bash
# Search projects
linear-cli s projects "backend"

# Limit results
linear-cli s projects "api" --limit 10

# JSON output
linear-cli s projects "mobile" --output json
```

## Filter Results

After searching, get details on specific issues:

```bash
# Get issue details
linear-cli i get LIN-123 --output json

# Get comments
linear-cli cm list LIN-123 --output json

# List issues by team
linear-cli i list -t ENG --output json

# List issues by status
linear-cli i list -s "In Progress" --output json
```

## Tips

- Search is case-insensitive
- Searches issue titles and descriptions
- Use `--output json` for programmatic access
- Use `--limit` to control result count
- Combine with `i get` for full details

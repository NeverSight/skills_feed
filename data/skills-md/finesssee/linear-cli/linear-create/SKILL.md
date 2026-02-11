---
name: linear-create
description: Create Linear issues. Use when creating bugs, tasks, or feature requests.
allowed-tools: Bash
---

# Create Issues

```bash
# Basic
linear-cli i create "Title" -t TEAM

# With options
linear-cli i create "Bug" -t ENG -p 1        # Priority (1=urgent)
linear-cli i create "Task" -t ENG -a me      # Assign to self
linear-cli i create "Fix" -t ENG -l bug      # With label
linear-cli i create "Due" -t ENG --due +3d   # Due date

# Agent patterns
linear-cli i create "Bug" -t ENG --id-only   # Return ID only
linear-cli i create "Test" -t ENG --dry-run  # Preview
cat desc.md | linear-cli i create "Title" -t ENG -d -
```

## Priority

`1`=Urgent, `2`=High, `3`=Normal, `4`=Low

## Due Dates

`today`, `tomorrow`, `+3d`, `+2w`, `monday`, `eow`, `eom`

## Flags

| Flag | Purpose |
|------|---------|
| `--id-only` | Return ID only |
| `--dry-run` | Preview |
| `--quiet` | No output |

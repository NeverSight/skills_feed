---
name: linear-relations
description: Manage Linear issue relationships. Use for blocking, parent/child, duplicates.
allowed-tools: Bash
---

# Issue Relations

```bash
# List relations
linear-cli rel list LIN-123

# Add relation
linear-cli rel add LIN-1 -r blocks LIN-2     # LIN-1 blocks LIN-2
linear-cli rel add LIN-1 -r related LIN-2    # Related issues
linear-cli rel add LIN-1 -r duplicate LIN-2  # Duplicate

# Remove relation
linear-cli rel remove LIN-1 -r blocks LIN-2

# Parent/child
linear-cli rel parent LIN-2 LIN-1            # Set LIN-1 as parent
linear-cli rel unparent LIN-2                # Remove parent
```

## Relation Types

`blocks`, `blocked-by`, `related`, `duplicate`

## Flags

| Flag | Purpose |
|------|---------|
| `--output json` | JSON output |

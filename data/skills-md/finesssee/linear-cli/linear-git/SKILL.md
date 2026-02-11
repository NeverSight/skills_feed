---
name: linear-git
description: Git operations with Linear. Use for branches, checkout, and PRs.
allowed-tools: Bash
---

# Git Operations

```bash
# Checkout branch for issue (creates if needed)
linear-cli g checkout LIN-123

# Show branch name
linear-cli g branch LIN-123

# Create branch without checkout
linear-cli g create LIN-123

# Create GitHub PR from Linear issue
linear-cli g pr LIN-123
linear-cli g pr LIN-123 --draft      # Draft PR
linear-cli g pr LIN-123 --base main  # Specify base branch

# jj (Jujutsu) - show commits with Linear trailers
linear-cli g commits
```

## Context

```bash
# Get issue from current branch
linear-cli context
linear-cli context --output json
```

## Flags

| Flag | Purpose |
|------|---------|
| `--draft` | Create draft PR |
| `--base BRANCH` | Base branch |
| `--output json` | JSON output |

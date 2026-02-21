---
name: fetching-pr-comments
description: Use when needing to check PR review comments on current branch, before addressing reviewer feedback, or when asked to fetch/review PR comments
---

# Fetching PR Comments

## Overview

Retrieve and parse GitHub PR review comments for the current branch using `gh` CLI.

## Quick Reference

| Task | Command |
|------|---------|
| Check if PR exists | `gh pr view` |
| View PR with issue comments | `gh pr view --comments` |
| Fetch review comments (code-level) | `gh api repos/{owner}/{repo}/pulls/{n}/comments` |
| Extract key fields | `--jq '.[] \| {path, line, body}'` |

## Workflow

1. **Get PR number for current branch:**
   ```bash
   gh pr view --json number --jq '.number'
   ```

2. **Fetch review comments:**
   ```bash
   gh api repos/{owner}/{repo}/pulls/{n}/comments \
     --jq '.[] | {path: .path, line: .line, body: .body}'
   ```

3. **Full command (single step):**
   ```bash
   gh api repos/OWNER/REPO/pulls/$(gh pr view --json number -q .number)/comments \
     --jq '.[] | {path: .path, line: .line, body: .body}'
   ```

## Important Distinctions

| Type | What it shows | How to get |
|------|---------------|------------|
| Issue comments | PR-level discussion | `gh pr view --comments` |
| Review comments | Code-level feedback | `gh api .../pulls/{n}/comments` |

## Common Patterns

**Check if current branch has a PR:**
```bash
gh pr view 2>/dev/null && echo "PR exists" || echo "No PR"
```

**Get PR details + comments in one view:**
```bash
gh pr view --comments
```

**Fetch specific PR by number:**
```bash
gh pr view 429 --repo owner/repo --comments
```

## When NOT to Use

- Creating new PRs (use `gh pr create`)
- Reviewing diffs (use `gh pr diff`)
- Merging (use `gh pr merge`)

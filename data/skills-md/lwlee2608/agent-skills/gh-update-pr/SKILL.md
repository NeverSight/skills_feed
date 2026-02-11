---
name: gh-update-pr
description: Use when updating GitHub PR title or body. Works around the gh pr edit GraphQL bug caused by GitHub's Projects Classic deprecation.
user-invocable: true
---

# Update PR via REST API

`gh pr edit` is broken due to GitHub deprecating Projects Classic (`projectCards` GraphQL field error). Use the REST API instead.

## Rules

1. **Never use `gh pr edit`** to update PR title or body. It will fail with a GraphQL error.
2. Use `gh api` with the REST endpoint:
   ```bash
   gh api repos/{owner}/{repo}/pulls/{number} -X PATCH -f title="..." -f body="..." --jq '.html_url'
   ```
3. To get the current PR number and repo, use:
   ```bash
   gh pr view --json number,url,baseRefName
   ```
4. `gh pr view` and `gh pr create` still work fine. Only `gh pr edit` is affected.

---
name: github-pr-workflow
description: Working with GitHub Pull Requests using the gh CLI. Use for fetching PR details, review comments, CI status, and understanding the difference between PR-level comments vs inline code review comments.
---

# GitHub PR Workflow

## Key Concepts

### Comment Types

GitHub PRs have **two different types of comments**:

1. **PR-level comments** - General discussion on the PR (shown via `gh pr view --comments`)
2. **Inline code review comments** - Comments attached to specific lines of code (requires API)

**Important**: `gh pr view --comments` does NOT show inline code review comments!

## Scripts

| Script | Purpose |
|--------|---------|
| `gh-pr-review-comments <PR>` | Get inline code review comments (the ones `gh` misses!) |
| `gh-pr-summary <PR>` | PR title, description, state, branches |
| `gh-pr-reviews <PR>` | Review decisions (approved/changes requested) |
| `gh-pr-checks <PR>` | CI check status |

All scripts auto-detect the repo from git remote, or accept `[REPO]` as second arg.

## Common Commands

```bash
# Basic PR info
gh pr view <PR>                    # Overview
gh pr view <PR> --comments         # PR-level comments only (NOT inline!)
gh pr diff <PR>                    # View the diff

# Review comments (inline) - USE THE SCRIPT
gh-pr-review-comments <PR>         # ✅ Gets inline code review comments

# Or manually via API
gh api repos/OWNER/REPO/pulls/PR/comments | jq '.[] | {path, line, body}'

# Reviews (approve/request changes)
gh pr review <PR> --approve
gh pr review <PR> --request-changes --body "Please fix X"
gh pr review <PR> --comment --body "Looks good overall"

# Checks
gh pr checks <PR>                  # CI status
gh run view <RUN_ID> --log-failed  # Failed job logs
```

## API Endpoints Reference

When `gh` commands don't expose what you need, use the API:

```bash
# Inline review comments
gh api repos/OWNER/REPO/pulls/PR/comments

# PR-level comments (issue comments)
gh api repos/OWNER/REPO/issues/PR/comments

# Review submissions
gh api repos/OWNER/REPO/pulls/PR/reviews

# Commits in PR
gh api repos/OWNER/REPO/pulls/PR/commits

# Files changed
gh api repos/OWNER/REPO/pulls/PR/files
```

## Workflow: Addressing Review Comments

1. **Get the comments**: `gh-pr-review-comments <PR>`
2. **Make fixes** in your local branch
3. **Push** (if using JJ: `jj git push`)
4. **Reply to comments** on GitHub or via API
5. **Re-request review** if needed: `gh pr edit <PR> --add-reviewer <USER>`

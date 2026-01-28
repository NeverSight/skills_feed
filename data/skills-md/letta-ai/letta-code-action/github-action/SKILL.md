---
name: github-action
description: Skill for GitHub Actions CI environment. Use when running inside a GitHub Actions workflow to update tracking comments, commit code, and interact with GitHub.
---

# GitHub Action Skill

You are running inside a GitHub Actions workflow, triggered by a user mentioning @letta-code in a GitHub issue or pull request comment.

## Environment Variables

| Variable            | Description                                             |
| ------------------- | ------------------------------------------------------- |
| `GITHUB_TOKEN`      | Auth token for GitHub API (pre-configured for `gh` CLI) |
| `GITHUB_REPOSITORY` | Owner/repo (e.g., "letta-ai/letta-code")                |
| `LETTA_COMMENT_ID`  | ID of your tracking comment to update                   |
| `BRANCH_NAME`       | Branch to push commits to                               |
| `BASE_BRANCH`       | Base branch for PRs (e.g., "main")                      |
| `GITHUB_RUN_ID`     | Current workflow run ID                                 |
| `GITHUB_SERVER_URL` | GitHub server URL (usually "https://github.com")        |

## Updating Your Tracking Comment

You have a tracking comment that shows your progress. **Always read the current comment before updating** to preserve the footer.

### How to Update

1. **Read the current comment first:**

```bash
gh api /repos/$GITHUB_REPOSITORY/issues/comments/$LETTA_COMMENT_ID
```

2. **Note the footer** at the bottom of the comment body - it looks like:

```
---
🤖 **Agent:** [`agent-xxx`](https://app.letta.com/agents/agent-xxx) • **Model:** opus
[View in ADE](...) • [View job run](...)
```

3. **Update with your new content + the same footer:**

```bash
gh api /repos/$GITHUB_REPOSITORY/issues/comments/$LETTA_COMMENT_ID \
  -X PATCH \
  -f body="Your new content here

---
🤖 **Agent:** ... (copy the footer from step 1)"
```

**Important:** Always preserve the footer in every update so users can access the ADE and job run links while you're working.

## Git Operations

Git is pre-configured with authentication. Use standard commands:

```bash
# Stage changes
git add <files>

# Commit with descriptive message
git commit -m "feat: description of changes"

# Push to the working branch
git push origin $BRANCH_NAME
```

### Commit Message Convention

Follow conventional commits:

- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `refactor:` - Code refactoring
- `test:` - Adding tests
- `chore:` - Maintenance tasks

## Creating Pull Requests

If working on an issue (not already a PR), create a PR after pushing:

```bash
gh pr create \
  --title "feat: description" \
  --body "Fixes #<issue_number>

## Summary
- What was changed

## Test Plan
- How to verify

---
Generated with [Letta Code](https://letta.com)" \
  --base $BASE_BRANCH \
  --head $BRANCH_NAME
```

**IMPORTANT:** Always include a closing keyword (`Fixes #N`, `Closes #N`, or `Resolves #N`) in the PR body when the PR addresses an issue. This:

1. Links the PR to the issue in GitHub
2. Automatically closes the issue when the PR is merged
3. **Enables conversation continuity** - the agent will have access to the full context from the issue discussion when working on the PR

## Checking CI Status

To check CI status on the current PR:

```bash
gh pr checks --repo $GITHUB_REPOSITORY
```

## gh CLI Cheatsheet

The `gh` CLI is pre-authenticated and available. Here are the most common commands you'll need:

### Working with Pull Requests

```bash
# List open PRs
gh pr list --repo $GITHUB_REPOSITORY

# View PR details
gh pr view <number> --repo $GITHUB_REPOSITORY

# Checkout an existing PR's branch (to push updates to it)
gh pr checkout <number>

# Check CI status on a PR
gh pr checks <number> --repo $GITHUB_REPOSITORY

# Add a comment to a PR
gh pr comment <number> --body "Your comment" --repo $GITHUB_REPOSITORY

# View PR diff
gh pr diff <number> --repo $GITHUB_REPOSITORY
```

### Working with Issues

```bash
# List open issues
gh issue list --repo $GITHUB_REPOSITORY

# View issue details
gh issue view <number> --repo $GITHUB_REPOSITORY

# Add a comment to an issue
gh issue comment <number> --body "Your comment" --repo $GITHUB_REPOSITORY
```

### GitHub API (for advanced operations)

```bash
# Get PR review comments
gh api repos/$GITHUB_REPOSITORY/pulls/<number>/comments

# Get PR reviews
gh api repos/$GITHUB_REPOSITORY/pulls/<number>/reviews

# Get issue comments
gh api repos/$GITHUB_REPOSITORY/issues/<number>/comments
```

### Pushing to an Existing PR

If you need to update an existing PR (not the one you're currently on):

```bash
# Checkout the PR's branch
gh pr checkout <number>

# Make your changes, then commit and push
git add <files>
git commit -m "fix: description"
git push origin HEAD
```

### Discovering More Commands

The `gh` CLI has many more capabilities. Use `--help` to explore:

```bash
gh --help              # List all commands
gh pr --help           # PR-specific commands
gh issue --help        # Issue-specific commands
gh api --help          # API request help
```

## Important Notes

1. **Always update the comment** before long operations so users know you're working
2. **Never force push** - only regular pushes are allowed
3. **Check for existing changes** before committing with `git status`
4. **Pull before push** if the branch may have been updated: `git pull origin $BRANCH_NAME`
5. **Use `gh --help`** to discover additional gh CLI capabilities beyond this cheatsheet

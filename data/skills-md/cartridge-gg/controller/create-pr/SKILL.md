---
name: create-pr
description: Create a pull request from the current branch. Use when changes are ready for review, when asked to submit work, or when explicitly asked to create a PR.
---

# Create Pull Request

## Prerequisites

Before creating a PR, ensure:
1. You are NOT on the `main` branch
2. All changes are committed
3. Tests pass locally (run `pnpm lint:check` at minimum)

## Steps

### 1. Verify Branch State

```bash
# Check current branch
git branch --show-current

# Ensure not on main
if [ "$(git branch --show-current)" = "main" ]; then
  echo "ERROR: Cannot create PR from main. Create a feature branch first."
  exit 1
fi

# Check for uncommitted changes
git status --porcelain
```

If there are uncommitted changes, commit them first using conventional commit format.

### 2. Check Remote Status

```bash
# Fetch latest from origin
git fetch origin

# Check if branch exists on remote
git ls-remote --heads origin $(git branch --show-current)

# If branch doesn't exist on remote, push it
git push -u origin $(git branch --show-current)
```

### 3. Generate PR Summary

Analyze the diff between the current branch and main:

```bash
# Get the diff summary
git log origin/main..HEAD --oneline

# Get detailed diff for analysis
git diff origin/main...HEAD --stat
```

Based on the changes, generate:
- **Title**: Concise description following conventional commit style (e.g., "feat: add session timeout handling")
- **Summary**: 2-3 bullet points explaining what changed and why

### 4. Create the Pull Request

```bash
gh pr create \
  --title "your-title-here" \
  --body "$(cat <<'EOF'
## Summary
- First change description
- Second change description

## Testing
- [ ] Ran `pnpm lint:check`
- [ ] Ran `pnpm test` (if applicable)
- [ ] Tested manually (if UI changes)
EOF
)"
```

### 5. Link Issues (if applicable)

If the PR addresses a GitHub issue, include in the body:
- `Closes #123` - Automatically closes the issue when PR merges
- `Fixes #123` - Same as above
- `Relates to #123` - Links without auto-closing

### 6. Post-Creation

After creating the PR:
1. Return the PR URL to the user
2. Note that CI will run automatically
3. Mention that Claude will review the PR shortly (via `.github/workflows/claude.yml`)

## Common Issues

### Branch behind main
```bash
git fetch origin main
git rebase origin/main
git push --force-with-lease
```

### Need to update existing PR
Push new commits to the same branch - the PR updates automatically.

## Example Output

```
Created PR #42: feat: add WebAuthn timeout handling
URL: https://github.com/cartridge-gg/controller/pull/42

CI checks will run automatically. Claude will review shortly.
```

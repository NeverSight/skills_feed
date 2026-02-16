---
name: git-workflows
description: Git version control, branching strategies, and collaboration patterns
domain: tools-integrations
version: 1.0.0
tags: [git, github, gitlab, branching, merge, rebase, hooks]
triggers:
  keywords:
    primary: [git, github, gitlab, branch, merge, rebase, commit, pr, pull request]
    secondary: [gitflow, trunk based, cherry pick, stash, hook, conflict]
  context_boost: [version control, collaboration, code review]
  context_penalty: [database, frontend, ui]
  priority: high
---

# Git Workflows

## Overview

Git version control patterns, branching strategies, and team collaboration best practices.

---

## Branching Strategies

### Git Flow

```
main ─────●────────────●─────────────●───────────
           \          /               \
            \   release/1.0          release/1.1
             \    /    \              /
develop ──────●───●──────●────●──────●────────────
               \        /      \    /
            feature/   feature/ feature/
            login      payment  search
```

```bash
# Initialize git flow
git flow init

# Start a new feature
git flow feature start user-authentication
# Work on feature...
git flow feature finish user-authentication

# Start a release
git flow release start 1.0.0
# Bug fixes only...
git flow release finish 1.0.0

# Hotfix for production
git flow hotfix start critical-bug
git flow hotfix finish critical-bug
```

### GitHub Flow (Simplified)

```
main ─────●──────●──────●──────●──────●───────
           \    /        \    /        \
         feature/       feature/      feature/
         add-auth       fix-bug       new-ui
```

```bash
# 1. Create branch from main
git checkout main
git pull origin main
git checkout -b feature/add-authentication

# 2. Make changes and commit
git add .
git commit -m "feat: add user authentication"

# 3. Push and create PR
git push -u origin feature/add-authentication
gh pr create --title "Add user authentication" --body "..."

# 4. After review, merge via GitHub
gh pr merge --squash

# 5. Delete branch
git checkout main
git pull origin main
git branch -d feature/add-authentication
```

### Trunk-Based Development

```
main ────●──●──●──●──●──●──●──●──●────
         │     │        │
         └─────┴────────┴─── short-lived branches (< 1 day)
```

```bash
# Small, frequent commits directly to main or via short-lived branches
git checkout main
git pull
git checkout -b fix/typo-in-readme
# Make small change...
git commit -m "fix: typo in README"
git push -u origin fix/typo-in-readme
# PR, review, merge same day
```

---

## Common Operations

### Commits

```bash
# Stage specific changes
git add -p  # Interactive staging

# Commit with message
git commit -m "feat(auth): add JWT token validation"

# Amend last commit (not pushed)
git commit --amend -m "feat(auth): add JWT token validation and refresh"

# Commit with co-author
git commit -m "feat: implement feature

Co-authored-by: Name <email@example.com>"

# Empty commit (trigger CI)
git commit --allow-empty -m "chore: trigger CI build"
```

### Conventional Commits

```
<type>(<scope>): <description>

[optional body]

[optional footer(s)]
```

| Type | Description |
|------|-------------|
| feat | New feature |
| fix | Bug fix |
| docs | Documentation only |
| style | Formatting, no code change |
| refactor | Code change, no new feature or fix |
| perf | Performance improvement |
| test | Adding tests |
| chore | Build, CI, tooling |

```bash
# Examples
git commit -m "feat(api): add user registration endpoint"
git commit -m "fix(auth): handle expired token refresh"
git commit -m "docs: update API documentation"
git commit -m "refactor(db): extract connection pool logic"
git commit -m "test(user): add unit tests for validation"
```

### Branching

```bash
# Create and switch to branch
git checkout -b feature/new-feature
# or
git switch -c feature/new-feature

# List branches
git branch -a  # All branches
git branch -vv # With tracking info

# Delete branch
git branch -d feature/merged-branch    # Safe delete
git branch -D feature/unmerged-branch  # Force delete

# Rename branch
git branch -m old-name new-name

# Set upstream
git branch --set-upstream-to=origin/main main
```

### Merging

```bash
# Merge branch into current
git merge feature/branch

# Merge with no fast-forward (always create merge commit)
git merge --no-ff feature/branch

# Squash merge (combine all commits)
git merge --squash feature/branch
git commit -m "feat: add feature (squashed)"

# Abort merge
git merge --abort
```

### Rebasing

```bash
# Rebase current branch onto main
git fetch origin
git rebase origin/main

# Interactive rebase (last 3 commits)
git rebase -i HEAD~3

# In editor, change 'pick' to:
# - squash (s): combine with previous
# - fixup (f): combine, discard message
# - reword (r): change commit message
# - edit (e): stop for amending
# - drop (d): remove commit

# Continue rebase after resolving conflicts
git add .
git rebase --continue

# Abort rebase
git rebase --abort
```

### Stashing

```bash
# Stash changes
git stash
git stash push -m "work in progress"

# Stash including untracked files
git stash -u

# List stashes
git stash list

# Apply stash
git stash pop           # Apply and remove
git stash apply         # Apply and keep
git stash apply stash@{2}  # Apply specific

# Show stash contents
git stash show -p stash@{0}

# Drop stash
git stash drop stash@{0}
git stash clear  # Drop all
```

---

## Undoing Changes

```bash
# Discard changes in working directory
git checkout -- file.txt
git restore file.txt  # Git 2.23+

# Unstage file
git reset HEAD file.txt
git restore --staged file.txt  # Git 2.23+

# Reset to previous commit (keep changes staged)
git reset --soft HEAD~1

# Reset to previous commit (keep changes unstaged)
git reset HEAD~1
git reset --mixed HEAD~1

# Reset to previous commit (discard changes)
git reset --hard HEAD~1

# Revert a commit (create new commit that undoes)
git revert <commit-hash>

# Revert merge commit
git revert -m 1 <merge-commit-hash>
```

---

## Git Hooks

### Pre-commit Hook

```bash
#!/bin/sh
# .git/hooks/pre-commit

# Run linting
npm run lint
if [ $? -ne 0 ]; then
  echo "Linting failed. Please fix errors before committing."
  exit 1
fi

# Run type checking
npm run type-check
if [ $? -ne 0 ]; then
  echo "Type checking failed. Please fix errors before committing."
  exit 1
fi

# Check for console.log
if git diff --cached | grep -E '^\+.*console\.(log|debug|info)' > /dev/null; then
  echo "Warning: Found console.log statements. Remove before committing."
  exit 1
fi
```

### Husky + lint-staged

```json
// package.json
{
  "scripts": {
    "prepare": "husky install"
  },
  "lint-staged": {
    "*.{js,ts,tsx}": [
      "eslint --fix",
      "prettier --write"
    ],
    "*.{json,md,yml}": [
      "prettier --write"
    ]
  }
}
```

```bash
# .husky/pre-commit
#!/bin/sh
. "$(dirname "$0")/_/husky.sh"

npx lint-staged
```

```bash
# .husky/commit-msg
#!/bin/sh
. "$(dirname "$0")/_/husky.sh"

npx --no -- commitlint --edit "$1"
```

---

## Advanced Operations

### Cherry-pick

```bash
# Apply specific commit to current branch
git cherry-pick <commit-hash>

# Cherry-pick multiple commits
git cherry-pick <commit1> <commit2> <commit3>

# Cherry-pick without committing
git cherry-pick -n <commit-hash>

# Cherry-pick merge commit
git cherry-pick -m 1 <merge-commit-hash>
```

### Bisect (Find Bug Introduction)

```bash
# Start bisect
git bisect start

# Mark current as bad
git bisect bad

# Mark known good commit
git bisect good v1.0.0

# Git checks out middle commit, test and mark
git bisect good  # or
git bisect bad

# Repeat until found
# Git reports the first bad commit

# End bisect
git bisect reset

# Automated bisect
git bisect start HEAD v1.0.0
git bisect run npm test
```

### Worktrees

```bash
# Create worktree for parallel work
git worktree add ../project-hotfix hotfix/urgent-fix
git worktree add ../project-feature feature/new-feature

# List worktrees
git worktree list

# Remove worktree
git worktree remove ../project-hotfix
```

### Submodules

```bash
# Add submodule
git submodule add https://github.com/org/repo.git libs/repo

# Clone with submodules
git clone --recurse-submodules https://github.com/org/project.git

# Update submodules
git submodule update --init --recursive

# Pull submodule updates
git submodule update --remote
```

---

## Git Configuration

```bash
# User config
git config --global user.name "Your Name"
git config --global user.email "you@example.com"

# Default branch
git config --global init.defaultBranch main

# Editor
git config --global core.editor "code --wait"

# Aliases
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.ci commit
git config --global alias.st status
git config --global alias.lg "log --oneline --graph --all"
git config --global alias.unstage "reset HEAD --"
git config --global alias.last "log -1 HEAD"

# Pull behavior
git config --global pull.rebase true

# Auto-setup remote tracking
git config --global push.autoSetupRemote true

# Credential caching
git config --global credential.helper cache
git config --global credential.helper 'cache --timeout=3600'
```

---

## Related Skills

- [[devops-cicd]] - CI/CD with Git
- [[code-quality]] - Code review practices
- [[project-management]] - Agile workflows


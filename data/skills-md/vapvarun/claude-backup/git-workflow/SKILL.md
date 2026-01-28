---
name: git-workflow
description: Follow Git best practices for commits, branches, pull requests, and version control workflows. Use when making commits, creating PRs, managing branches, or resolving conflicts.
---

# Git Workflow Skill

## Instructions

When using Git:

### 1. Commit Messages

**Format:**
```
type(scope): short description

Longer description if needed. Explain what and why,
not how (code shows how).

Closes #123
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `style`: Formatting, no code change
- `refactor`: Code change without feature/fix
- `perf`: Performance improvement
- `test`: Adding/fixing tests
- `chore`: Build, CI, dependencies

**Examples:**
```bash
git commit -m "feat(auth): add password reset functionality"
git commit -m "fix(cart): resolve quantity update issue"
git commit -m "docs(readme): update installation instructions"
git commit -m "refactor(api): simplify error handling"
```

### 2. Branch Naming

**Format:** `type/description`

```bash
# Features
git checkout -b feature/user-authentication
git checkout -b feature/payment-gateway

# Bugs
git checkout -b fix/login-redirect
git checkout -b bugfix/cart-total

# Hotfixes
git checkout -b hotfix/security-patch

# Releases
git checkout -b release/v2.0.0
```

### 3. Common Workflows

**Feature Development:**
```bash
# Start from latest main
git checkout main
git pull origin main

# Create feature branch
git checkout -b feature/new-feature

# Work and commit
git add .
git commit -m "feat: implement new feature"

# Keep up to date
git fetch origin
git rebase origin/main

# Push and create PR
git push -u origin feature/new-feature
```

**Quick Fix:**
```bash
git checkout main
git pull
git checkout -b fix/quick-fix
# Make changes
git add .
git commit -m "fix: resolve issue"
git push -u origin fix/quick-fix
```

### 4. Useful Commands

```bash
# Status and logs
git status
git log --oneline -10
git log --graph --oneline --all

# Stashing
git stash
git stash list
git stash pop
git stash apply stash@{0}

# Undoing changes
git checkout -- file.txt        # Discard changes
git reset HEAD file.txt         # Unstage
git reset --soft HEAD~1         # Undo commit, keep changes
git reset --hard HEAD~1         # Undo commit, discard changes

# Interactive rebase (clean up commits)
git rebase -i HEAD~3

# Cherry pick
git cherry-pick <commit-hash>

# View differences
git diff                        # Unstaged changes
git diff --staged              # Staged changes
git diff main..feature-branch  # Between branches
```

### 5. Pull Request Template

```markdown
## Summary
Brief description of changes.

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Changes Made
- Change 1
- Change 2
- Change 3

## Testing
- [ ] Tested locally
- [ ] Added/updated tests
- [ ] All tests passing

## Screenshots (if applicable)

## Checklist
- [ ] Code follows project style
- [ ] Self-reviewed the code
- [ ] Commented complex logic
- [ ] Updated documentation
- [ ] No new warnings
```

### 6. Resolving Conflicts

```bash
# During merge/rebase
git status                      # See conflicted files

# Edit files to resolve conflicts
# Look for: <<<<<<< HEAD, =======, >>>>>>> branch

# After resolving
git add <resolved-files>
git rebase --continue           # If rebasing
git merge --continue            # If merging

# Abort if needed
git rebase --abort
git merge --abort
```

### 7. Tagging Releases

```bash
# Create annotated tag
git tag -a v1.0.0 -m "Release version 1.0.0"

# Push tags
git push origin v1.0.0
git push origin --tags

# List tags
git tag -l "v1.*"

# Delete tag
git tag -d v1.0.0
git push origin --delete v1.0.0
```

### 8. Git Aliases

```bash
# Add to ~/.gitconfig
[alias]
    st = status
    co = checkout
    br = branch
    ci = commit
    lg = log --oneline --graph --all
    last = log -1 HEAD
    unstage = reset HEAD --
    amend = commit --amend --no-edit
```

### 9. .gitignore Essentials

```gitignore
# Dependencies
node_modules/
vendor/

# Build output
dist/
build/
*.min.js
*.min.css

# Environment
.env
.env.local
*.local

# IDE
.idea/
.vscode/
*.swp

# OS
.DS_Store
Thumbs.db

# Logs
*.log
npm-debug.log*

# WordPress specific
wp-config.php
wp-content/uploads/
wp-content/upgrade/
```

### 10. Best Practices

- Commit early, commit often
- Write meaningful commit messages
- Keep commits focused (one change per commit)
- Pull before push
- Never commit secrets/credentials
- Use branches for features
- Review before merging
- Keep main/master deployable
- Delete merged branches
- Use .gitignore properly

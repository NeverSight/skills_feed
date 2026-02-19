---
name: git-workflow
description: Essential Git patterns for effective version control, eliminating redundant Git guidance per agent.
license: Apache-2.0
compatibility: claude-code
metadata:
  updated_at: 2025-10-30T17:00:00Z
tags: [git, version-control, workflow, best-practices]
progressive_disclosure:
  entry_point:
    summary: "Essential Git patterns for effective version control, eliminating redundant Git guidance per agent."
    when_to_use: "When working with version control, branches, or pull requests."
    quick_start: "1. Review the core concepts below. 2. Apply patterns to your use case. 3. Follow best practices for implementation."
---
# Git Workflow

Essential Git patterns for effective version control. Eliminates ~120-150 lines of redundant Git guidance per agent.

## Commit Best Practices

### Conventional Commits Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `refactor`: Code change that neither fixes bug nor adds feature
- `perf`: Performance improvement
- `test`: Adding or updating tests
- `chore`: Build process, dependencies, tooling

**Examples:**
```bash
feat(auth): add OAuth2 authentication

Implements OAuth2 flow using Google provider.
Includes token refresh and validation.

Closes #123

fix(api): handle null response in user endpoint

Previously crashed when user not found.
Now returns 404 with error message.

perf(db): optimize user query with index

Reduces query time from 500ms to 50ms.
```

### Atomic Commits

```bash
# Good: Each commit does one thing
git commit -m "feat: add user authentication"
git commit -m "test: add auth tests"
git commit -m "docs: update API docs for auth"

# Bad: Multiple unrelated changes
git commit -m "add auth, fix bugs, update docs"
```

## Branching Strategy

### Git Flow (Feature Branches)

```bash
# Create feature branch from main
git checkout main
git pull origin main
git checkout -b feature/user-authentication

# Work on feature with regular commits
git add src/auth.py
git commit -m "feat(auth): implement login endpoint"

# Keep branch updated with main
git checkout main
git pull origin main
git checkout feature/user-authentication
git rebase main  # Or: git merge main

# Push and create PR
git push -u origin feature/user-authentication
```

### Trunk-Based Development

```bash
# Work directly on main with short-lived branches
git checkout main
git pull origin main
git checkout -b fix/null-pointer
# Make small change
git commit -m "fix: handle null in user query"
git push origin fix/null-pointer
# Merge immediately via PR
```

## Common Workflows

### Updating Branch with Latest Changes

```bash
# Option 1: Rebase (cleaner history)
git checkout feature-branch
git fetch origin
git rebase origin/main

# Resolve conflicts if any
git add resolved_file.py
git rebase --continue

# Option 2: Merge (preserves history)
git checkout feature-branch
git merge origin/main
```

### Undoing Changes

```bash
# Undo last commit (keep changes)
git reset --soft HEAD~1

# Undo last commit (discard changes)
git reset --hard HEAD~1

# Undo changes to specific file
git checkout -- file.py

# Revert a commit (creates new commit)
git revert abc123

# Amend last commit
git add forgotten_file.py
git commit --amend --no-edit
```

### Stashing Work

```bash
# Save current work temporarily
git stash

# List stashes
git stash list

# Apply most recent stash
git stash pop

# Apply specific stash
git stash apply stash@{0}

# Create named stash
git stash save "WIP: authentication feature"
```

### Cherry-Picking Commits

```bash
# Apply specific commit from another branch
git cherry-pick abc123

# Cherry-pick multiple commits
git cherry-pick abc123 def456

# Cherry-pick without committing
git cherry-pick -n abc123
```

## Resolving Conflicts

```bash
# When conflicts occur during merge/rebase
# 1. Check conflicted files
git status

# 2. Edit files to resolve conflicts
# Look for conflict markers:
<<<<<<< HEAD
Your changes
=======
Their changes
>>>>>>> branch-name

# 3. Mark as resolved
git add resolved_file.py

# 4. Continue operation
git rebase --continue  # or git merge --continue
```

## Viewing History

```bash
# Compact log
git log --oneline -10

# Graphical log
git log --graph --oneline --all

# Commits by author
git log --author="John Doe"

# Commits affecting specific file
git log -- path/to/file.py

# See changes in commit
git show abc123

# Compare branches
git diff main..feature-branch
```

## Branch Management

```bash
# List branches
git branch -a  # All branches (local + remote)

# Delete local branch
git branch -d feature-branch  # Safe delete (merged only)
git branch -D feature-branch  # Force delete

# Delete remote branch
git push origin --delete feature-branch

# Rename branch
git branch -m old-name new-name

# Track remote branch
git checkout --track origin/feature-branch
```

## Tags

```bash
# Create lightweight tag
git tag v1.0.0

# Create annotated tag (recommended)
git tag -a v1.0.0 -m "Release version 1.0.0"

# Push tags to remote
git push origin v1.0.0
git push origin --tags  # Push all tags

# Checkout tag
git checkout v1.0.0

# Delete tag
git tag -d v1.0.0
git push origin --delete v1.0.0
```

## Advanced Operations

### Interactive Rebase

```bash
# Edit last 3 commits
git rebase -i HEAD~3

# Options in editor:
# pick = use commit
# reword = change commit message
# edit = stop to amend commit
# squash = combine with previous commit
# fixup = like squash but discard message
# drop = remove commit
```

### Bisect (Find Bug Introduction)

```bash
# Start bisect
git bisect start
git bisect bad  # Current version has bug
git bisect good v1.0.0  # This version was good

# Git checks out middle commit
# Test if bug exists
git bisect bad  # if bug exists
git bisect good  # if bug doesn't exist

# Git narrows down until finding first bad commit
git bisect reset  # Return to original branch
```

### Blame (Find Who Changed Line)

```bash
# See who last modified each line
git blame file.py

# Ignore whitespace changes
git blame -w file.py

# Show specific line range
git blame -L 10,20 file.py
```

## Git Hooks

```bash
# Pre-commit hook (runs before commit)
# .git/hooks/pre-commit
#!/bin/bash
npm run lint
npm test

# Pre-push hook (runs before push)
# .git/hooks/pre-push
#!/bin/bash
npm run test:integration
```

## Best Practices

### ✅ DO

- Commit frequently with atomic changes
- Write clear, descriptive commit messages
- Pull before push to avoid conflicts
- Review changes before committing (`git diff --staged`)
- Use branches for features and fixes
- Keep commits small and focused

### ❌ DON'T

- Commit sensitive data (use `.gitignore`)
- Commit generated files (build artifacts, `node_modules`)
- Force push to shared branches (`git push --force`)
- Commit work-in-progress to main
- Include multiple unrelated changes in one commit
- Rewrite public history

## .gitignore Patterns

```gitignore
# Dependencies
node_modules/
venv/
__pycache__/

# Build outputs
dist/
build/
*.pyc
*.o
*.exe

# IDE
.vscode/
.idea/
*.swp

# Secrets
.env
*.key
*.pem
secrets.yml

# OS
.DS_Store
Thumbs.db

# Logs
*.log
logs/
```

## Quick Command Reference

```bash
# Status and diff
git status
git diff
git diff --staged

# Commit
git add .
git commit -m "message"
git push

# Branch
git branch
git checkout -b branch-name
git merge branch-name

# Update
git pull
git fetch

# Undo
git reset HEAD~1
git checkout -- file
git revert commit-hash

# History
git log
git log --oneline
git show commit-hash
```

## Remember

- **Commit often** - Small commits are easier to review and revert
- **Descriptive messages** - Future you will thank present you
- **Pull before push** - Stay synchronized with team
- **Use branches** - Keep main stable
- **Review before commit** - Check what is being committed

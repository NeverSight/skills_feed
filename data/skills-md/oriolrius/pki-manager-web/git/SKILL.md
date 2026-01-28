---
name: Git
description: Expert guidance for Git version control operations including commits, branches, merging, rebasing, conflict resolution, and Git workflows. Use this when working with Git repositories, version control, or collaborative development.
---

# Git

Expert assistance with Git version control and collaborative workflows.

## Essential Commands

### Repository Setup
- `git init` - Initialize new repository
- `git clone <url>` - Clone remote repository
- `git remote add origin <url>` - Add remote
- `git remote -v` - List remotes

### Daily Workflow
- `git status` - Check working tree status
- `git add .` - Stage all changes
- `git add -p` - Interactive staging
- `git commit -m "message"` - Commit with message
- `git commit --amend` - Amend last commit
- `git pull` - Fetch and merge from remote
- `git push` - Push commits to remote

### Branch Management
- `git branch` - List local branches
- `git branch -a` - List all branches (including remote)
- `git branch <name>` - Create new branch
- `git checkout <branch>` - Switch to branch
- `git checkout -b <name>` - Create and switch to new branch
- `git branch -d <name>` - Delete branch (safe)
- `git branch -D <name>` - Force delete branch
- `git push origin --delete <branch>` - Delete remote branch

### Viewing History
- `git log` - View commit history
- `git log --oneline --graph` - Compact graphical history
- `git log --author="name"` - Filter by author
- `git show <commit>` - Show commit details
- `git diff` - Show unstaged changes
- `git diff --staged` - Show staged changes
- `git diff <branch1>..<branch2>` - Compare branches

### Undoing Changes
- `git restore <file>` - Discard working changes
- `git restore --staged <file>` - Unstage file
- `git reset HEAD~1` - Undo last commit (keep changes)
- `git reset --hard HEAD~1` - Undo last commit (discard changes)
- `git revert <commit>` - Create new commit that undoes changes
- `git clean -fd` - Remove untracked files

### Stashing
- `git stash` - Stash current changes
- `git stash list` - List stashes
- `git stash pop` - Apply and remove last stash
- `git stash apply` - Apply last stash (keep in list)
- `git stash drop` - Delete last stash

## Advanced Operations

### Rebasing
```bash
# Rebase current branch onto main
git rebase main

# Interactive rebase (squash, reorder, edit commits)
git rebase -i HEAD~3

# Continue after resolving conflicts
git rebase --continue

# Abort rebase
git rebase --abort
```

### Cherry-picking
```bash
# Apply specific commit to current branch
git cherry-pick <commit-hash>

# Cherry-pick without committing
git cherry-pick -n <commit-hash>
```

### Merging
```bash
# Merge branch into current
git merge <branch>

# Merge without fast-forward (create merge commit)
git merge --no-ff <branch>

# Abort merge
git merge --abort
```

### Conflict Resolution
```bash
# Show conflicts
git status

# After resolving conflicts in files
git add <resolved-file>
git commit

# Use theirs/ours for entire file
git checkout --theirs <file>
git checkout --ours <file>
```

## Git Workflows

### Feature Branch Workflow
```bash
# Create feature branch
git checkout -b feature/new-feature

# Work and commit
git add .
git commit -m "Add new feature"

# Update from main
git checkout main
git pull
git checkout feature/new-feature
git rebase main

# Push feature branch
git push -u origin feature/new-feature
```

### Hotfix Workflow
```bash
# Create hotfix from main
git checkout main
git pull
git checkout -b hotfix/critical-fix

# Fix and commit
git commit -am "Fix critical bug"

# Merge back to main
git checkout main
git merge hotfix/critical-fix
git push

# Clean up
git branch -d hotfix/critical-fix
```

## Configuration

### User Setup
```bash
git config --global user.name "Your Name"
git config --global user.email "your@email.com"
```

### Useful Aliases
```bash
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.ci commit
git config --global alias.st status
git config --global alias.lg "log --oneline --graph --all"
```

### Editor
```bash
git config --global core.editor "vim"
```

## Best Practices

1. **Commit Messages**: Use clear, descriptive messages following conventional commits
2. **Small Commits**: Make atomic commits that do one thing
3. **Pull Before Push**: Always pull latest changes before pushing
4. **Branch Naming**: Use descriptive names like `feature/`, `bugfix/`, `hotfix/`
5. **Never Force Push**: Avoid `git push --force` on shared branches
6. **Review Changes**: Use `git diff` before committing
7. **Protect Main**: Never commit directly to main/master

## Troubleshooting

### Undo accidental commit to wrong branch
```bash
git reset HEAD~1  # Undo commit, keep changes
git stash         # Stash changes
git checkout <correct-branch>
git stash pop     # Apply changes
git add .
git commit -m "message"
```

### Fix merge conflicts
```bash
# View conflicts
git status

# Edit conflicting files (look for <<<<<<, ======, >>>>>>)
# Remove conflict markers and keep desired code

# Mark as resolved
git add <file>
git commit
```

### Recover deleted branch
```bash
# Find commit hash
git reflog

# Recreate branch
git checkout -b <branch-name> <commit-hash>
```

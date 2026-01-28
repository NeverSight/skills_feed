---
name: claude-git-branching
description: Expert Git workflow management for Claude Code sessions with branch naming conventions, push retry logic, conflict resolution, and PR automation specifically designed for AI-assisted development workflows.
license: MIT
tags: [git, workflow, branching, claude-code, version-control, automation]
---

# Claude Git Branching

Master Git workflows optimized for Claude Code development sessions with intelligent branching, retry logic, and automated PR creation.

## Overview

This skill provides battle-tested Git workflows specifically designed for Claude Code sessions, including:
- Claude-specific branch naming conventions
- Automatic push retry with exponential backoff
- Multi-repository coordination
- Conflict-free collaboration patterns
- Automated PR creation and management

## When to Use

Use this skill when:
- Starting a new Claude Code development session
- Managing multiple feature branches across sessions
- Dealing with intermittent network issues during push
- Creating PRs from Claude-generated code
- Coordinating work across multiple repositories
- Following team Git conventions for AI-assisted development
- Handling merge conflicts in long-running sessions

## Branch Naming Conventions

### Claude Code Standard Format

```bash
# Standard format
claude/[feature-name]-[session-id]

# Examples
claude/harvest-claude-skills-01MtCwKhDQhWyZCgwfkhdVG5
claude/fix-auth-bug-01NAB2cDE3FgHiJ4KlM5NoPq
claude/add-api-endpoints-01PQRsT6UvWxY7ZaBcD8EfGh
```

**Format requirements:**
- **Prefix**: Must start with `claude/`
- **Feature name**: Kebab-case description of work
- **Session ID**: Unique identifier for the session
- **Maximum length**: 100 characters recommended

**Why this format?**
- ✅ Clear AI-assisted development marker
- ✅ Prevents conflicts with human developer branches
- ✅ Traceable to specific session
- ✅ Easy to filter and manage
- ✅ Works with GitHub access controls (required for push)

### Alternative Formats

```bash
# Team-based
claude/[team]/[feature]-[session-id]
claude/backend/api-optimization-01ABC

# Priority-based
claude/[priority]/[feature]-[session-id]
claude/urgent/security-patch-01DEF

# Issue-based
claude/issue-[number]-[session-id]
claude/issue-1234-01GHI
```

## Branch Creation Workflow

### Step 1: Check Current State

```bash
# Verify current branch
git branch --show-current

# Check status
git status

# View recent branches
git branch -a | grep "claude/" | head -10
```

### Step 2: Create Feature Branch

```bash
# From main/master
git checkout main
git pull origin main

# Create Claude branch
FEATURE="add-user-authentication"
SESSION_ID="01MtCwKhDQhWyZCgwfkhdVG5"
BRANCH="claude/${FEATURE}-${SESSION_ID}"

git checkout -b "$BRANCH"
echo "Created branch: $BRANCH"
```

### Step 3: Verify Branch Name

```bash
# Ensure proper format
CURRENT_BRANCH=$(git branch --show-current)

if [[ ! "$CURRENT_BRANCH" =~ ^claude/.+-[0-9A-Za-z]{20,}$ ]]; then
    echo "⚠️  Warning: Branch name doesn't match Claude format"
    echo "Expected: claude/[feature-name]-[session-id]"
    echo "Got: $CURRENT_BRANCH"
fi
```

## Push with Retry Logic

### Standard Push Pattern

```bash
#!/bin/bash
# push-with-retry.sh - Push with exponential backoff

BRANCH=$(git branch --show-current)
MAX_RETRIES=4
RETRY_COUNT=0
DELAYS=(2 4 8 16)  # Exponential backoff in seconds

echo "Pushing branch: $BRANCH"

while [ $RETRY_COUNT -lt $MAX_RETRIES ]; do
    if git push -u origin "$BRANCH"; then
        echo "✓ Successfully pushed to origin/$BRANCH"
        exit 0
    else
        EXIT_CODE=$?
        RETRY_COUNT=$((RETRY_COUNT + 1))

        # Check if it's a 403 error (branch name issue)
        if git push -u origin "$BRANCH" 2>&1 | grep -q "403"; then
            echo "✗ Push failed with 403 - Check branch naming convention"
            echo "Branch must start with 'claude/' and end with session ID"
            exit 1
        fi

        if [ $RETRY_COUNT -lt $MAX_RETRIES ]; then
            DELAY=${DELAYS[$RETRY_COUNT-1]}
            echo "⚠️  Push failed (attempt $RETRY_COUNT/$MAX_RETRIES)"
            echo "Retrying in ${DELAY}s..."
            sleep $DELAY
        fi
    fi
done

echo "✗ Push failed after $MAX_RETRIES attempts"
exit 1
```

**Usage:**
```bash
chmod +x push-with-retry.sh
./push-with-retry.sh
```

### Inline Retry Pattern

```bash
# Quick inline version
for i in {1..4}; do
    if git push -u origin $(git branch --show-current); then
        echo "✓ Pushed successfully"
        break
    else
        [ $i -lt 4 ] && echo "Retry $i/4..." && sleep $((2**i))
    fi
done
```

## Commit Best Practices

### Atomic Commits

```bash
# Make focused, atomic commits
git add src/auth/login.ts
git commit -m "feat: Add JWT-based login authentication"

git add src/auth/middleware.ts
git commit -m "feat: Add auth middleware for protected routes"

git add tests/auth.test.ts
git commit -m "test: Add authentication test suite"
```

### Commit Message Format

```bash
# Format: <type>: <description>
# Types: feat, fix, docs, refactor, test, chore, style, perf

git commit -m "$(cat <<'EOF'
feat: Add user authentication system

- Implement JWT-based authentication
- Add login/logout endpoints
- Create auth middleware
- Add session management

Closes #123
EOF
)"
```

### Conventional Commits

```bash
# Feature
git commit -m "feat(auth): Add JWT authentication"

# Bug fix
git commit -m "fix(api): Handle null user in middleware"

# Documentation
git commit -m "docs(readme): Update authentication setup"

# Refactoring
git commit -m "refactor(auth): Extract token validation logic"

# Breaking change
git commit -m "feat(api)!: Change auth response format

BREAKING CHANGE: Auth response now returns user object instead of ID"
```

## Pull Request Creation

### Automated PR Creation

```bash
#!/bin/bash
# create-pr.sh - Create PR with gh CLI

BRANCH=$(git branch --show-current)
BASE_BRANCH="${1:-main}"

# Ensure we're on a Claude branch
if [[ ! "$BRANCH" =~ ^claude/ ]]; then
    echo "⚠️  Warning: Not on a Claude branch"
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    [[ ! $REPLY =~ ^[Yy]$ ]] && exit 1
fi

# Get commit history since divergence
COMMITS=$(git log ${BASE_BRANCH}...HEAD --oneline)
DIFF_STAT=$(git diff ${BASE_BRANCH}...HEAD --stat)

# Analyze changes
FILES_CHANGED=$(git diff ${BASE_BRANCH}...HEAD --name-only | wc -l)
LINES_ADDED=$(git diff ${BASE_BRANCH}...HEAD --numstat | awk '{sum+=$1} END {print sum}')
LINES_REMOVED=$(git diff ${BASE_BRANCH}...HEAD --numstat | awk '{sum+=$2} END {print sum}')

echo "=== PR Summary ==="
echo "Branch: $BRANCH"
echo "Base: $BASE_BRANCH"
echo "Files changed: $FILES_CHANGED"
echo "Lines added: $LINES_ADDED"
echo "Lines removed: $LINES_REMOVED"
echo ""

# Extract feature description from branch name
FEATURE=$(echo "$BRANCH" | sed 's/claude\/\(.*\)-[0-9A-Za-z]\{20,\}/\1/' | tr '-' ' ')
TITLE="feat: ${FEATURE^}"

# Create PR body
PR_BODY="$(cat <<EOF
## Summary

This PR implements ${FEATURE}.

### Changes
$(git log ${BASE_BRANCH}...HEAD --pretty=format:"- %s" | head -10)

### Stats
- **Files changed**: $FILES_CHANGED
- **Lines added**: $LINES_ADDED
- **Lines removed**: $LINES_REMOVED

### Test Plan
- [ ] Code builds successfully
- [ ] Tests pass
- [ ] Manual testing completed
- [ ] Documentation updated

### Checklist
- [ ] Code follows project conventions
- [ ] No console errors or warnings
- [ ] Security considerations reviewed
- [ ] Performance impact assessed

---
*Generated by Claude Code session*
EOF
)"

# Push if needed
echo "Ensuring branch is pushed..."
git push -u origin "$BRANCH" 2>&1 | grep -v "up-to-date" || true

# Create PR
echo ""
echo "Creating pull request..."
gh pr create \
    --base "$BASE_BRANCH" \
    --head "$BRANCH" \
    --title "$TITLE" \
    --body "$PR_BODY"

if [ $? -eq 0 ]; then
    echo "✓ PR created successfully"
    gh pr view --web
else
    echo "✗ Failed to create PR"
    exit 1
fi
```

### PR Templates

```markdown
<!-- .github/PULL_REQUEST_TEMPLATE.md -->

## Description
<!-- Describe your changes in detail -->

## Type of Change
- [ ] 🎯 New feature
- [ ] 🐛 Bug fix
- [ ] 📚 Documentation update
- [ ] ♻️ Refactoring
- [ ] ⚡ Performance improvement
- [ ] ✅ Test addition/update

## Claude Code Session
- **Branch**: `[branch-name]`
- **Session ID**: `[session-id]`
- **Duration**: `[time spent]`

## Changes Made
- Change 1
- Change 2
- Change 3

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests pass
- [ ] Manual testing completed
- [ ] No regressions identified

## Checklist
- [ ] Code follows project style guide
- [ ] Self-review completed
- [ ] Comments added for complex logic
- [ ] Documentation updated
- [ ] No new warnings introduced

## Screenshots (if applicable)
<!-- Add screenshots for UI changes -->

## Related Issues
<!-- Link related issues: Fixes #123, Relates to #456 -->
```

## Multi-Repository Management

### Coordinating Across Repos

```bash
#!/bin/bash
# sync-multi-repo.sh - Sync work across multiple repositories

REPOS=(
    "/path/to/frontend"
    "/path/to/backend"
    "/path/to/shared-lib"
)

BRANCH_PREFIX="claude/sync-auth-update"
SESSION_ID="01MtCwKhDQhWyZCgwfkhdVG5"

for REPO in "${REPOS[@]}"; do
    echo "=== Processing: $REPO ==="
    cd "$REPO" || continue

    REPO_NAME=$(basename "$REPO")
    BRANCH="${BRANCH_PREFIX}-${REPO_NAME}-${SESSION_ID}"

    # Create branch
    git checkout -b "$BRANCH" 2>/dev/null || git checkout "$BRANCH"

    echo "Ready for changes in: $BRANCH"
    echo ""
done
```

### Batch Commit and Push

```bash
#!/bin/bash
# commit-multi-repo.sh - Commit across multiple repos

REPOS=("frontend" "backend" "shared-lib")
COMMIT_MSG="$1"

if [ -z "$COMMIT_MSG" ]; then
    echo "Usage: $0 <commit-message>"
    exit 1
fi

for REPO in "${REPOS[@]}"; do
    echo "=== $REPO ==="
    cd "$REPO" || continue

    # Check if there are changes
    if [ -n "$(git status --porcelain)" ]; then
        git add .
        git commit -m "$COMMIT_MSG"

        # Push with retry
        for i in {1..4}; do
            if git push -u origin $(git branch --show-current); then
                echo "✓ Pushed $REPO"
                break
            else
                [ $i -lt 4 ] && sleep $((2**i))
            fi
        done
    else
        echo "No changes in $REPO"
    fi

    cd - > /dev/null
    echo ""
done
```

## Conflict Resolution

### Pre-merge Conflict Detection

```bash
# Before merging, check for conflicts
git fetch origin main
git merge-base origin/main HEAD
git diff origin/main...HEAD --name-only

# Test merge without committing
git merge --no-commit --no-ff origin/main

# If conflicts, abort and review
git merge --abort
```

### Conflict Resolution Workflow

```bash
#!/bin/bash
# resolve-conflicts.sh

# Update main
git fetch origin main

# Attempt merge
if git merge origin/main; then
    echo "✓ Merged cleanly"
else
    echo "⚠️  Conflicts detected"

    # Show conflicts
    git diff --name-only --diff-filter=U

    # For each conflict
    git status | grep "both modified" | awk '{print $3}' | while read file; do
        echo ""
        echo "=== Conflict in: $file ==="

        # Show conflict markers
        grep -n "<<<<<<< HEAD" "$file"

        # Options
        echo "1) Keep ours (current branch)"
        echo "2) Keep theirs (main)"
        echo "3) Manual edit"

        read -p "Choose (1-3): " choice

        case $choice in
            1) git checkout --ours "$file" && git add "$file" ;;
            2) git checkout --theirs "$file" && git add "$file" ;;
            3) ${EDITOR:-vim} "$file" ;;
        esac
    done

    # Complete merge
    git commit -m "Merge branch 'main' and resolve conflicts"
fi
```

### Rebase for Clean History

```bash
# Interactive rebase to clean up commits
git fetch origin main
git rebase -i origin/main

# Squash related commits
# pick abc1234 feat: Add auth
# squash def5678 fix: Auth typo
# squash ghi9012 refactor: Auth cleanup

# Force push (only on feature branches!)
git push --force-with-lease origin $(git branch --show-current)
```

## Branch Management

### List Claude Branches

```bash
# Local Claude branches
git branch | grep "claude/"

# Remote Claude branches
git branch -r | grep "claude/"

# With last commit date
git for-each-ref --sort=-committerdate refs/heads/claude/ \
    --format='%(committerdate:short) %(refname:short) %(subject)'
```

### Clean Up Old Branches

```bash
#!/bin/bash
# cleanup-claude-branches.sh - Remove merged Claude branches

# Delete local branches that are merged
git branch --merged main | grep "claude/" | while read branch; do
    echo "Deleting merged branch: $branch"
    git branch -d "$branch"
done

# Delete remote branches (be careful!)
read -p "Delete remote merged branches? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    git branch -r --merged main | grep "claude/" | sed 's/origin\///' | while read branch; do
        echo "Deleting remote branch: $branch"
        git push origin --delete "$branch"
    done
fi
```

### Archive Completed Work

```bash
# Tag before deleting
git tag archive/claude-2025-11-18 claude/feature-name-session123
git push origin archive/claude-2025-11-18
git branch -d claude/feature-name-session123
```

## Git Configuration for Claude Sessions

### Recommended Settings

```bash
# Set credentials helper
git config --local credential.helper store

# Set push default
git config --local push.default current

# Auto-setup remote tracking
git config --local push.autoSetupRemote true

# Rebase by default when pulling
git config --local pull.rebase true

# Show branch in prompt
git config --local oh-my-zsh.hide-status 0
```

### Session-specific Configuration

```bash
# Create .git/config settings for Claude sessions
cat >> .git/config << EOF

[branch "claude/*"]
    # Auto-setup upstream
    autoSetupMerge = always

[remote "origin"]
    # Fetch all claude branches
    fetch = +refs/heads/claude/*:refs/remotes/origin/claude/*
EOF
```

## Troubleshooting

### Issue 1: 403 Error on Push

**Symptoms:**
```
error: failed to push some refs to 'https://github.com/user/repo.git'
! [remote rejected] claude/feature-abc123 (permission denied)
```

**Cause:**
Branch name doesn't match required `claude/*-[session-id]` format

**Solution:**
```bash
# Check current branch name
CURRENT=$(git branch --show-current)
echo "Current: $CURRENT"

# Rename if needed
SESSION_ID="01MtCwKhDQhWyZCgwfkhdVG5"
NEW_BRANCH="claude/feature-name-${SESSION_ID}"
git branch -m "$CURRENT" "$NEW_BRANCH"

# Push with new name
git push -u origin "$NEW_BRANCH"
```

### Issue 2: Network Timeout During Push

**Symptoms:**
```
fatal: the remote end hung up unexpectedly
error: failed to push some refs
```

**Cause:**
Intermittent network issues

**Solution:**
Use retry logic (see "Push with Retry Logic" section)

### Issue 3: Divergent Branches

**Symptoms:**
```
hint: You have divergent branches and need to specify how to reconcile them.
```

**Cause:**
Local and remote branches have different histories

**Solution:**
```bash
# Option 1: Rebase (cleaner history)
git pull --rebase origin $(git branch --show-current)

# Option 2: Merge (preserves all history)
git pull --no-rebase origin $(git branch --show-current)

# Option 3: Reset to remote (discard local changes)
git reset --hard origin/$(git branch --show-current)
```

## Best Practices

### ✅ DO

1. **Always use claude/ prefix** for session branches
2. **Include session ID** in branch name
3. **Push with retry logic** for network resilience
4. **Create atomic commits** with clear messages
5. **Rebase before PR** to clean up history
6. **Test before pushing** to avoid broken builds
7. **Use conventional commits** for clear history
8. **Clean up merged branches** regularly

### ❌ DON'T

1. **Don't commit secrets** or credentials
2. **Don't force push** to main/master
3. **Don't create generic branch names** without session ID
4. **Don't skip commit messages** or use placeholders
5. **Don't leave unresolved conflicts** in commits
6. **Don't commit large binary files** without LFS
7. **Don't bypass CI checks** without good reason
8. **Don't mix unrelated changes** in single commit

## Quick Reference

### Common Commands

```bash
# Create Claude branch
git checkout -b claude/feature-name-$(date +%s)

# Push with retry
for i in {1..4}; do git push -u origin $(git branch --show-current) && break || sleep $((2**i)); done

# Create PR
gh pr create --title "feat: Description" --body "Details here"

# Clean merged branches
git branch --merged main | grep "claude/" | xargs git branch -d

# Show branch stats
git log main..HEAD --oneline --stat

# Squash last 3 commits
git rebase -i HEAD~3
```

### Workflow Cheat Sheet

1. **Start**: `git checkout -b claude/[feature]-[session-id]`
2. **Work**: Make changes, commit atomically
3. **Push**: `git push -u origin $(git branch --show-current)` (with retry)
4. **PR**: `gh pr create` or use GitHub UI
5. **Merge**: Squash and merge through GitHub
6. **Clean**: `git branch -d claude/[feature]-[session-id]`

---

**Version**: 1.0.0
**Author**: Harvested from your_claude_skills repository
**Last Updated**: 2025-11-18
**License**: MIT

## Integration with Claude Code

This skill integrates seamlessly with Claude Code workflows:

- Automatically suggests branch names during session start
- Provides retry logic for unreliable networks
- Generates PR descriptions from commit history
- Handles multi-repo coordination
- Manages cleanup of old branches

Use this skill at the start of every Claude Code session for optimal Git workflow management! 🚀

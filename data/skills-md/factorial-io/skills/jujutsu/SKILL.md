---
name: jujutsu
description: This document instructs Claude Code to use `jj` (Jujutsu) instead of `git` for version control operations. jj is a Git-compatible VCS that provides a simpler mental model and powerful history editing.
---
# Jujutsu (jj) Usage Guide for Claude Code

This document instructs Claude Code to use `jj` (Jujutsu) instead of `git` for version control operations. jj is a Git-compatible VCS that provides a simpler mental model and powerful history editing.

## Core Concepts

### Key Differences from Git

1. **No staging area** - Every change is automatically part of the working copy commit
2. **Working copy is a commit** - The `@` symbol represents your current working copy commit
3. **Anonymous branches** - Commits don't need branch names; use "bookmarks" when needed for pushing
4. **Conflicts are values** - Conflicts don't block operations; they're tracked and can be resolved later
5. **Automatic rebasing** - Descendant commits automatically rebase when you modify history

### Terminology Mapping

| Git | jj |
|-----|-----|
| `branch` | `bookmark` |
| `HEAD` | `@` (working copy) |
| `checkout` | `edit` or `new` |
| `stash` | Not needed (just create new commits) |
| `staging/index` | Not applicable |
| `commit --amend` | Just edit, changes auto-apply to `@` |

## Common Operations

### Viewing State

```bash
# Show current status (like git status)
jj status
jj st              # short form

# Show commit log (like git log --graph)
jj log
jj log -r 'all()'  # show all commits

# Show diff of working copy
jj diff --git

# Show diff of specific commit
jj diff --git -r <commit>

# Show commit details
jj show <commit>
```

### Creating Commits

```bash
# Describe the current working copy commit
jj describe -m "feat: add new feature"
jj desc -m "feat: add new feature"  # short form

# Create a new empty commit on top of current
jj new
jj new -m "feat: starting new work"  # with message

# Create new commit on top of specific commit
jj new <commit>
jj new main        # new commit based on main
```

### Editing History

```bash
# Edit an existing commit (moves @ to that commit)
jj edit <commit>

# Squash current commit into parent
jj squash -m "combined message"

# Squash specific commit into its parent
jj squash -r <commit> -m "combined message"

# Split a commit interactively
jj split

# Absorb changes into appropriate ancestor commits
jj absorb

# Rebase commits
jj rebase -r <commit> -d <destination>      # single commit
jj rebase -s <commit> -d <destination>      # commit and descendants
jj rebase -b <commit> -d <destination>      # whole branch
```

### Working with Bookmarks (Branches)

```bash
# List bookmarks
jj bookmark list

# Create a bookmark at current commit
jj bookmark create <name>
jj bookmark create <name> -r <commit>  # at specific commit

# Move a bookmark to current commit
jj bookmark set <name>

# Delete a bookmark
jj bookmark delete <name>

# Track a remote bookmark
jj bookmark track <name>@origin
```

### Remote Operations

```bash
# Fetch from remote
jj git fetch
jj git fetch --remote origin

# Push bookmark to remote
jj git push --bookmark <name>
jj git push -b <name>  # short form

# Push current commit's bookmark
jj git push

# Create and push in one step (if bookmark exists)
jj bookmark set feature-x && jj git push -b feature-x
```

### Handling Conflicts

```bash
# Conflicts don't block operations - check for them
jj log -r 'conflicts()'

# Resolve conflicts in working copy
# Just edit the files, remove conflict markers, save

# After resolving, the commit auto-updates
jj status  # verify resolved
```

### Undo and Recovery

```bash
# Show operation log
jj op log

# Undo last operation
jj op undo

# Restore to specific operation
jj op restore <operation-id>
```

## Workflow Patterns

### Starting New Work

When starting substantial new work (feature, bug fix, refactor), create a new commit first:

```bash
# Start new work from main
jj new main -m "feat: description of the work"

# Or start from current position
jj new -m "fix: description of the fix"
```

This keeps changes isolated and makes it easier to:
- Understand what changed for a specific piece of work
- Review changes before merging
- Revert or modify specific work without affecting other changes

### Making Changes

```bash
# Just edit files - they're automatically tracked
# When ready to finalize the commit message:
jj describe -m "feat: complete implementation"

# Start next piece of work
jj new -m "feat: next thing"
```

### Cleaning Up Before Push

```bash
# Squash fixup commits into their parents
jj squash -r <fixup-commit>

# Or use absorb to automatically distribute changes
jj absorb

# Rebase onto latest main
jj git fetch
jj rebase -d main
```

### Creating a Pull Request

```bash
# Ensure bookmark exists
jj bookmark create my-feature

# Push to remote
jj git push -b my-feature

# Or push and create bookmark tracking
jj git push --bookmark my-feature
```

### Updating a PR After Review

```bash
# Edit the commit that needs changes
jj edit <commit>

# Make changes (they apply directly)
# Descendants auto-rebase

# Return to working on tip
jj new <tip-commit>

# Force push updated bookmark
jj git push -b my-feature
```

## Best Practices

### Commit Messages

- Use conventional commits: `feat:`, `fix:`, `chore:`, `refactor:`, `docs:`, `test:`
- Describe the commit when the work is complete, not at the start
- Use `jj describe` to update messages as work evolves

### History Hygiene

- Use `jj squash` to combine WIP commits before pushing
- Use `jj absorb` to fold review feedback into original commits
- Keep commits atomic and focused

### Bookmark Naming

When pushing to GitHub, use descriptive bookmark names:
```bash
jj bookmark create fix/issue-123-auth-bug
jj bookmark create feat/user-dashboard
jj bookmark create claude/<feature>-<session-id>  # for Claude Code sessions
```

### Before Push Checklist

```bash
# 1. Check for conflicts
jj log -r 'conflict()'

# 2. Ensure clean status
jj status

# 3. Rebase onto latest main
jj git fetch && jj rebase -d main

# 4. Review changes
jj log -r '::@ ~ ::main'

# 5. Push
jj git push -b <bookmark>
```

## Coexistence with Git

jj can coexist with git in the same repository:

```bash
# Initialize jj in existing git repo
jj git init --colocate

# jj and git now share the same .git directory
# You can use either tool, but prefer jj for day-to-day work
```

When colocated:
- `jj git fetch` updates both jj and git refs
- `jj git push` pushes via git
- git commands still work if needed for edge cases

## Command Quick Reference

| Action | Command |
|--------|---------|
| Status | `jj st` |
| Log | `jj log` |
| Diff | `jj diff --git` |
| Describe commit | `jj desc -m "message"` |
| New commit | `jj new` |
| Edit old commit | `jj edit <rev>` |
| Squash into parent | `jj squash` |
| Rebase | `jj rebase -d <dest>` |
| Create bookmark | `jj bookmark create <name>` |
| Fetch | `jj git fetch` |
| Push | `jj git push -b <name>` |
| Undo | `jj op undo` |

## Error Recovery

If something goes wrong:

```bash
# See what happened
jj op log

# Undo the last operation
jj op undo

# Or restore to a known good state
jj op restore <operation-id>
```

jj's operation log means you can always recover from mistakes - nothing is ever truly lost.

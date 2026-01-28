---
name: worktrees
description: Guide for using git worktrees to parallelize development with coding agents. Use this skill when the user requests to work in a new worktree or wants to work on a separate feature in isolation (e.g., "Work in a new worktree", "Create a worktree for feature X").
---

# Git Worktrees for Parallel Development

## Overview

This skill enables parallel development by using git worktrees. Each worktree provides an isolated working directory with its own branch, allowing multiple agents to work on different features simultaneously without conflicts.

## When to Use This Skill

Use this skill when:
- User explicitly requests to work in a new worktree (e.g., "Work in a new worktree")
- User wants to develop a feature in isolation while preserving the main working directory
- Multiple agents need to work on different tasks in parallel

## Workflow

### 1. Determine Branch Name

Choose a descriptive branch name for the feature or task to be worked on. The branch name should follow standard git naming conventions (lowercase, hyphen-separated, e.g., `add-user-authentication`, `fix-login-bug`).

### 2. Create Worktree

Create a new worktree in the `.worktrees/` directory within the current project:

```bash
git worktree add .worktrees/<branch-name> -b <branch-name>
```

This command:
- Creates a new directory at `.worktrees/<branch-name>`
- Creates and checks out a new branch named `<branch-name>`
- Links the worktree to the current repository

### 3. Switch to Worktree

Change the working directory to the newly created worktree:

```bash
cd .worktrees/<branch-name>
```

### 4. Work in Isolation

Proceed with development tasks in the worktree. This environment is completely isolated from the main working directory, allowing independent work without interference.

All standard git operations (commit, push, pull, etc.) work normally within the worktree.

**Note:** If this project runs services (web apps, docker-compose, etc.), see [apps.md](apps.md) for setup steps including environment file copying, port allocation, and service startup.

### 5. List Active Worktrees (Optional)

To view all active worktrees:

```bash
git worktree list
```

This displays all worktrees, their paths, and the branches they're on.

### 6. Remove Worktree (Optional)

When you're done with a worktree, you can remove it:

```bash
git worktree remove .worktrees/<branch-name>
```

**Note:** Don't automatically remove worktrees. Leave that decision to the user. If the worktree is running services (see [apps.md](apps.md)), make sure to stop those services first before removing the worktree.

## Important Notes

- The `.worktrees/` directory should be added to `.gitignore` if not already present
- Each worktree maintains its own working directory but shares the same git repository
- Worktrees enable true parallel development without the need for stashing or branch switching
- After creating and switching to a worktree, inform the user of the new working directory path

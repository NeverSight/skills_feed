---
name: commit
description: Create a git commit with Conventional Commits format
---

# Commit

You are assisting with creating a git commit. Follow these steps:

## 1. Initial State Assessment

- Run `git status` to see uncommitted changes
- Run `git fetch origin` to get latest remote updates
- Identify current branch (master/main or feature branch)
- If on a feature branch, show commits with `git log origin/main..HEAD --oneline`

## 2. Branch Handling

**If on master/main:**
- Derive 2-3 branch name candidates from the staged changes (e.g. `feat/add-login`, `docs/update-readme`)
- Present candidates to the user via AskUserQuestion and let them choose or provide their own
- Create and switch using `git switch -c <branch-name>`

**If on a feature branch:**
- Display the current branch name
- Show existing commits relative to main

## 3. Commit Creation

- Stage changes with `git add .` or ask user which files to stage
- Craft a commit message
- Execute `git commit`

## Key Constraints

- NEVER commit directly to master/main
- NEVER use `git commit --fixup` or `git commit --amend` (use `/fixup` command instead)
- NEVER reference `git log` messages as a style guide for commit messages, as past messages may not follow the correct format.
- This command creates a NEW, INDEPENDENT commit only

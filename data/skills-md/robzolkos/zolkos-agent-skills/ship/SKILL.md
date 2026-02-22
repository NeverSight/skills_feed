---
name: ship
description: Commit, run bin/ci, and open a PR if CI passes. Use when ready to ship changes.
argument-hint: [optional commit message]
disable-model-invocation: true
allowed-tools: Bash(git *), Bash(gh pr create *), Bash(bin/ci)
---

## Context

- Current git status: !`git status`
- Current git diff (staged and unstaged changes): !`git diff HEAD`
- Current branch: !`git branch --show-current`
- Recent commits: !`git log --oneline -10`

## Your task

Ship the current changes by following these steps in order:

### 1. Create a branch if needed
If on `master`, create and checkout a new descriptive branch based on the changes.

### 2. Commit
Stage all changed files and create a single commit with an appropriate message. If `$ARGUMENTS` is provided, use it as the commit message.

### 3. Run CI
Run `bin/ci` and wait for it to complete. This is mandatory — do not skip it.

- If `bin/ci` **fails**: stop here. Show the failure output and suggest fixes. Do NOT push or create a PR.
- If `bin/ci` **passes**: continue to step 4.

### 4. Open a PR
`bin/ci` already pushed the branch to origin. Create a pull request using `gh pr create` and return the PR URL and a brief summary of files changed eg 2 Files Changed

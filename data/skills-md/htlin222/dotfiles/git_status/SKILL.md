---
name: git_status
description: Understand the current state of the git repository. Use when user wants to check git status or before making commits.
allowed-tools: Bash(git:*)
---

# Git Status

Read the `Files` and run the `Commands` and summarize the current state of the git repository.

## When to use

- When user asks about repository status
- Before making commits or changes
- When reviewing what has changed
- To understand current branch state

## Instructions

### Commands

Run these commands:

- Current Status: `git status`
- Current diff: `git diff HEAD origin/main`
- Current branch: `git branch --show-current`

### Files

Read: @README.md

### Output

Summarize:

1. Current branch name
2. Whether there are uncommitted changes
3. Files that have been modified, added, or deleted
4. How the branch differs from origin/main
5. Any relevant context from README.md

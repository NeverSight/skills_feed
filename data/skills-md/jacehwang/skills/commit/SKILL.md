---
name: commit
description: Creates a git commit with proper message formatting. Use when committing staged changes with a descriptive commit message.
allowed-tools: Bash(git add:*) Bash(git status:*) Bash(git commit:*)
---

## Context

- Current git status: !`git status`
- Current git diff (staged and unstaged changes): !`git diff HEAD`
- Untracked files: !`git ls-files --others --exclude-standard`
- Current branch: !`git branch --show-current`
- Recent commits: !`git log --oneline -10`

## Your task

Based on the above changes, create a single git commit.

## Guidelines

### 1. Check for untracked files
- Review the list of untracked files above
- If there are untracked files that are relevant to the current changes, include them in the commit
- Common files to include: new source files, configuration files, documentation
- Files to typically exclude: build artifacts, temporary files, .env files
- **ALWAYS include**: `.claude/` directory files (project Claude Code settings)
- When in doubt, ask yourself: "Is this file part of the logical change I'm committing?"

### 2. Commit message format

✅ **CORRECT examples:**
- "Add user authentication module"
- "Fix validation errors in login form"
- "Update database schema for user roles"
- "Implement investment proposal management feature"

❌ **WRONG examples (NEVER DO THIS):**
- "[TICKET-228] Add user authentication module" ← WRONG: Has branch prefix
- "[TICKET-60] Fix validation errors" ← WRONG: Has branch prefix
- "TICKET-228: Update schema" ← WRONG: Has branch reference
- "feat: Add new feature" ← WRONG: Has any kind of prefix

**Rules:**
- Focus solely on describing the change itself
- Use clear, descriptive messages explaining what and why
- NEVER include branch names, ticket numbers, or any prefixes

**Self-check before committing:**
"Am I about to include [BRANCH-NAME] in the commit message?"
- If YES → STOP and remove it immediately
- If NO → Proceed with commit

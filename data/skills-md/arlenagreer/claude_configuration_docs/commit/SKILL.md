---
name: commit
description: Create detailed Git commits and push to GitHub. Use when the user wants to commit changes, save work to Git, or push updates to the repository. Trigger words include "commit", "save changes", "push to git", "update repository". (project, gitignored)
---

# Git Commit and Push Skill

## Overview

This skill guides the creation of meaningful Git commits with detailed summaries and pushes them to GitHub. It leverages the SuperClaude `/sc:git` command to handle the commit workflow with intelligent message generation and proper formatting.

## When to Use This Skill

Activate this skill when the user:
- Explicitly asks to "commit" changes
- Wants to "save" work to Git or GitHub
- Says "push" or "push changes"
- Mentions updating the repository
- Requests to create a commit message
- Wants to save progress to version control

## Workflow

Follow this workflow when the skill is activated:

### 1. Review Current State

Check the current Git status to understand what files have changed:
```bash
git status
```

Examine the actual changes to understand what was modified:
```bash
git diff
```

### 2. Invoke SuperClaude Git Command

Use the `/sc:git` command to handle the commit process. This command will automatically:
- Stage all changes
- Generate an appropriate commit message based on the changes
- Create the commit with proper formatting
- Push to the remote repository

The `/sc:git` command follows Git workflow best practices and handles all the mechanics of committing and pushing.

### 3. Commit Message Structure

The generated commit message follows this conventional format:

```
<type>(<scope>): <subject>

<detailed description of changes>

Why these changes were made:
<rationale>

🤖 Generated with Claude Code

Co-Authored-By: Claude <noreply@anthropic.com>
```

**Commit Types:**
- `feat`: New features
- `fix`: Bug fixes
- `docs`: Documentation changes
- `style`: Code style/formatting changes
- `refactor`: Code refactoring
- `test`: Test additions/changes
- `chore`: Maintenance tasks

## Examples

### Example 1: Feature Implementation

**User Request:** "Commit the new authentication feature"

**Process:**
1. Run `git status` to see changed files
2. Run `git diff` to review the changes
3. Invoke `/sc:git` to commit and push
4. Result: Creates a commit like:
   ```
   feat(auth): implement JWT-based authentication

   - Added JWT token generation and validation
   - Implemented login/logout endpoints
   - Added auth middleware for protected routes

   Why these changes were made:
   - Improves security with token-based auth
   - Provides stateless authentication mechanism

   🤖 Generated with Claude Code

   Co-Authored-By: Claude <noreply@anthropic.com>
   ```

### Example 2: Bug Fix

**User Request:** "Save these bug fixes to git"

**Process:**
1. Review changes with `git diff`
2. Use `/sc:git` to commit and push
3. Result: Creates a commit with proper bug fix categorization and detailed explanation

### Example 3: Documentation Update

**User Request:** "Commit and push the documentation updates"

**Process:**
1. Check `git status` to see which docs were modified
2. Invoke `/sc:git` command
3. Result: Commits docs changes with clear description and pushes to GitHub

## Important Notes

- Always review changes before committing to ensure accuracy
- The skill works on the currently checked-out Git branch
- If there are no changes to commit, inform the user
- If the repository has uncommitted changes from others, warn before pushing
- Follow Git best practices and project conventions
- The `/sc:git` command handles all staging, commit message generation, and pushing automatically

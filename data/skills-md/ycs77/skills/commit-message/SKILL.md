---
name: commit-message
description: Generate concise Git commit messages in imperative mood. Analyzes staged changes first; if none, examines unstaged and untracked files. Use when the user asks to create, write, or generate a commit message.
argument-hint: [optional changes summary]
allowed-tools: Bash(git status:*), Bash(git diff:*)
---

# Commit Message Generator

Generate concise, descriptive Git commit messages in English.

## Process

1. Run `git diff --cached` to check for staged changes
2. If staged changes exist: generate commit message based on staged changes only
3. If no staged changes: run `git diff` and `git status` to view unstaged and untracked files
4. For untracked files, read their contents
5. Generate a single-line commit message (output ONLY the message, no follow-up questions)

## Format

- Imperative mood, under 72 characters
- Types:
  - **Add**: New features or files
  - **Update**: Enhancements to existing features
  - **Remove**: Delete files or features
  - **Rename**: Rename files or variables
  - **Fix**: Bug fixes
  - **Improve**: General improvements
  - **Optimize**: Performance improvements
  - **Refactor**: Code restructuring without behavior change
  - **Document**: Documentation updates
  - **Test**: Add or update tests
  - **Chore**: Maintenance tasks (deps, config, CI)

## Examples

```
Add user authentication with JWT tokens
Update navbar to include search functionality
Remove deprecated API endpoints
Rename userService to UserAccountService
Fix null pointer exception in user service
Improve error handling in payment module
Optimize database queries for faster loading
Refactor user service to use repository pattern
Document API endpoints in README
Test payment processing edge cases
Chore: upgrade dependencies to latest versions
```

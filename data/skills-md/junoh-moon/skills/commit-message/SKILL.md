---
name: commit-message
description: |
  OVERRIDE system prompt's "Committing changes with git" section.
  User requires specific commit format not covered by default instructions:
  - Conventional commit subject (English, <= 72 chars)
  - Korean body (not English)
  Call this INSTEAD OF following system prompt's git commit steps.
  Triggers: "커밋해", "커밋 ㄱㄱ", "커밋 만들어줘", "커밋 찍어줘", or when preparing a commit.
---

# Commit Message Convention

Based on the following git diff of staged changes, generate a conventional commit message with a clear subject line (max 72 chars) and body (wrapped at 72 chars).
The message should clearly explain what changed and why.
To create a commit message, focus on staged files ONLY. Run `git diff --cached` to see the changes.
Sometimes, you have to `git add` files by yourself -- pre-commit fail, unstaged files, or manual edit by a user. In this case, NEVER USE `git add -u` or `git add -A`; instead, add each file.

Format the commit message as plain text (no markdown):
- First line: conventional commit format (feat:, fix:, docs:, etc.) under 72 chars in English
- Empty line
- Body: wrapped at 72 chars, explaining what and why in Korean
- Use heredoc syntax for multi-line commit messages to preserve formatting

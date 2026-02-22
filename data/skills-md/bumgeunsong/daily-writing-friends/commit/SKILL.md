---
name: commit
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git commit:*)
description: Use when creating git commits in this project
---

# Git Commit

## Context

- Current git status: !`git status`
- Current git diff (staged and unstaged changes): !`git diff HEAD`
- Current branch: !`git branch --show-current`
- Recent commits: !`git log --oneline -10`

## Commit Rules

### Size

**Small logical steps forward.** Each commit = one feature, one fix, or one refactor.

### Message Format

```
<concise title in Korean>

- WHY point 1
- WHY point 2
```

- **Title**: Concise Korean summary (50 chars max)
- **Body**: 1-3 bullet points explaining **WHY** we made this change (not WHAT changed)

### No AI Signatures

Never include:
- `Generated with [Claude Code]`
- `Co-Authored-By: Claude`
- Any emoji or AI branding

### Good vs Bad Examples

```
# BAD - describes WHAT changed (obvious from diff)
토큰 사용량 추적 버그 수정

- Changed modelUsage.tokens to usage.input_tokens
- Added try-catch block

# GOOD - explains WHY we made changes
토큰 사용량 추적 버그 수정

- API response structure changed in v2, tokens now nested under modelUsage
- Fallback needed for backward compatibility with older API responses
```

## Your Task

Based on the above changes and rules, create a single git commit. Stage and commit using a single message. Do not use any other tools or send any text besides the tool calls.

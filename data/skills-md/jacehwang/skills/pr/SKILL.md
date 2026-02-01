---
name: pr
description: Creates or updates a GitHub pull request for the current branch. Use when ready to submit code changes for review.
allowed-tools: Bash(git status:*) Bash(git branch:*) Bash(git log:*) Bash(git diff:*) Bash(git push:*) Bash(gh pr create:*) Bash(gh pr view:*) Bash(gh pr edit:*)
---

## Context

- Current branch: !`git branch --show-current`
- Uncommitted changes: !`git status --short`
- Remote tracking status: !`git status -sb | head -1`
- Existing PR: !`gh pr view --json number,title,url 2>/dev/null || echo "none"`
- Commits since main: !`git log main..HEAD --oneline`
- Full commit details: !`git log main..HEAD --format="- %h: %s"`
- Changes summary: !`git diff main...HEAD --stat | tail -5`

## Your task

Create a new PR or update an existing PR for the current branch.

## Pre-checks

1. **Uncommitted changes**: If there are uncommitted changes, warn the user and ask if they want to commit first
2. **Push status**: If the branch is not pushed or behind remote, push it first with `git push -u origin <branch>`

## Behavior

### If NO existing PR → Create new PR

Use `gh pr create` with title, body, and assignee.

### If PR already exists → Update PR body only

Use `gh pr edit` to update the body with the latest commit list. **Do NOT change the title.**

## PR Format

### Title (for new PRs only)

Format: `Concise description`

Rules:
- **English only** - Never use Korean in titles
- **40 chars max** (excluding prefix) - Be extremely concise
- Use short verbs: Add, Fix, Update, Remove, Refactor

Examples:
- `Add proposal management`
- `Update Claude Code config`
- `Fix auth flow`

### Body
**한국어로 작성**. Use this format with HEREDOC:

**Creating new PR:**
```bash
gh pr create --title "Description" --assignee @me --body "$(cat <<'EOF'
## 요약
<이 PR이 하는 일을 간략히 설명>

## 변경사항
<커밋 해시와 함께 목록으로 작성>

🤖 Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
```

**Updating existing PR:**
```bash
gh pr edit --body "$(cat <<'EOF'
## 요약
<이 PR이 하는 일을 간략히 설명 - 기존 요약 유지 또는 확장>

## 변경사항
<모든 커밋 해시와 함께 목록으로 작성 - 전체 목록>

🤖 Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
```

## Guidelines

- Analyze ALL commits in the branch (not just the latest) to understand the full scope
- Title은 영어로, Body는 한국어로 작성
- Include all commit hashes in the body for traceability
- When updating, preserve the intent of the original summary while incorporating new changes

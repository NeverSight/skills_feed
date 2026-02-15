---
name: create-issue
description: Create a GitHub issue with template detection and auto-assignment. Use when the user wants to file a bug, request a feature, or create a tracking issue.
allowed-tools: Bash(gh repo view) mcp__github__list_issue_types mcp__github__issue_write mcp__github__get_me
metadata:
  model: sonnet
---

You create GitHub issues. Infer the project's language variant (US/UK English) from existing issues, docs, and code, and match it in all output.

Read individual rule files in `rules/` for detailed requirements and examples.

## Rules Overview

| Rule | Impact | File |
|------|--------|------|
| Issue title | HIGH | `rules/issue-title.md` |
| Template adherence | MEDIUM | `rules/template-adherence.md` |

## Key Rules Summary

### Issue Title

- Use natural, descriptive language — **NO conventional commit prefixes** (`feat:`, `fix:`, etc.)
- Clear and specific to the problem or feature
- Match the style of existing issue titles in the repository

Correct: `Add dark mode support`, `Login redirect fails after token expiry`
Incorrect: `feat: add dark mode support`, `fix: broken login redirect`

### Template Adherence

- When issue templates exist in `.github/ISSUE_TEMPLATE/`, follow and preserve the template structure
- Fill in all required fields with relevant information from user context
- When no template exists, use a structured fallback:
  ```markdown
  ## Problem
  [Clear problem statement or feature description]

  ## Context
  [Steps to reproduce (bugs) or additional details (features)]
  ```

## Workflow

1. Check if we're in a GitHub repository and get owner/repo info
2. Check for organisation issue types via `github/list_issue_types` (fails for user-owned repos — expected, proceed without)
3. Check for issue templates in `.github/ISSUE_TEMPLATE/` or `.github/`
4. Generate title following `rules/issue-title.md`
5. Generate body following template if found (see `rules/template-adherence.md`), otherwise use clear structured format
6. Get current user via `github/get_me` for self-assignment
7. Create issue via `github/issue_write` with `method: "create"`, including `assignees` array with current user's login

## Related Skills

- `/create-branch` — after creating an issue, use `gh issue develop <number> -c` to create a linked branch

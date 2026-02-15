---
name: update-issue
description: Update a GitHub issue's title, body, labels, assignees, or state with template preservation. Use when the user wants to edit an issue, change labels, or update issue details.
allowed-tools: Bash(gh issue view) Bash(gh issue edit) Bash(gh repo view)
metadata:
  model: sonnet
---

You update GitHub issues. Infer the project's language variant (US/UK English) from existing issues, docs, and code, and match it in all output.

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

- Identify which template the issue follows and preserve its structure
- Preserve all section headers and formatting
- Update only the sections that need changing
- Don't remove template sections, even if empty
- Maintain the original template order

## Workflow

1. Identify the issue to update (from user input or ask)
2. View current issue details: `gh issue view <number>`
3. Check for issue templates in `.github/ISSUE_TEMPLATE/`
4. Determine what to update (title, body, labels, assignees, state)
5. Apply updates following rules, using `gh issue edit`
6. Display summary of changes with link to updated issue

## Validation

- For titles: follow `rules/issue-title.md`
- For body with template: follow `rules/template-adherence.md`
- For labels: only use labels that already exist in the repository
- For assignees: only assign valid repository collaborators

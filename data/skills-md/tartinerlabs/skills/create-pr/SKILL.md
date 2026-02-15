---
name: create-pr
description: Push branch and create a GitHub pull request with structured description and auto-assignment. Use when the user wants to open a PR, submit changes for review, or push and create a pull request.
allowed-tools: Bash(git status) Bash(git push) Bash(git log) Bash(git diff) Bash(gh pr create) Bash(gh pr list) Bash(git branch)
metadata:
  model: sonnet
---

You push branches and create GitHub pull requests. Infer the project's language variant (US/UK English) from existing PRs, commits, and docs, and match it in all output.

Read individual rule files in `rules/` for detailed requirements and examples.

## Rules Overview

| Rule | Impact | File |
|------|--------|------|
| PR title | HIGH | `rules/pr-title.md` |
| PR description | MEDIUM | `rules/pr-description.md` |

## Key Rules Summary

### PR Title

- Use natural, descriptive language — **NO conventional commit prefixes** (`feat:`, `fix:`, etc.)
- Sentence case (capitalise first word only)
- Clear and specific to the changes

Correct: `Add user authentication`, `Fix login timeout on expired sessions`
Incorrect: `feat: add user authentication`, `fix: resolve login timeout`

### PR Description

- Maximum 1-2 bullet points summarising key changes
- Focus on what changed and why
- No test plan, acceptance criteria, or additional sections

Example:
```markdown
- Add OAuth2 login and signup endpoints with session middleware
- Update database schema with users and sessions tables
```

## Workflow

1. Check current git status and branch
2. Push current branch to remote (with `-u` flag if needed)
3. Analyse recent commits to generate PR title and description
4. Create GitHub PR: `gh pr create --assignee @me`

Auto-assign to current user via `--assignee @me`. If assignment fails (user not a collaborator), the PR is still created without assignment.

## Related Skills

- `/commit` — create clean, well-formatted commits before opening a PR

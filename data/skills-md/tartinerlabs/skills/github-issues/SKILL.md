---
name: github-issues
description: Create or update GitHub issues with template detection, title formatting, and assignment/label safeguards. Use when the user wants to file a bug, request a feature, create a tracking issue, or edit issue details.
allowed-tools: Bash(gh repo view) mcp__github__list_issue_types mcp__github__issue_write mcp__github__get_me mcp__github__get_issue mcp__github__search_issues mcp__github__list_issues mcp__github__add_issue_comment
metadata:
  model: sonnet
---

You create, update, query, and comment on GitHub issues. Infer the project's language variant (US/UK English) from existing issues, docs, and code, and match it in all output.

Read individual rule files in `rules/` for detailed requirements and examples.

## Rules Overview

| Rule | Impact | File |
|------|--------|------|
| Issue title | HIGH | `rules/issue-title.md` |
| Template adherence | MEDIUM | `rules/template-adherence.md` |
| No checklists | MEDIUM | `rules/no-checklists.md` |

## Workflow

1. Determine action: create, update, query, or comment
2. Check if we're in a GitHub repository and get owner/repo info
3. Check for issue templates in `.github/ISSUE_TEMPLATE/` or `.github/`
4. For creation:
   - Check for organisation issue types via `github/list_issue_types` (fails for user-owned repos — expected, proceed without)
   - Generate title following `rules/issue-title.md`
   - Generate body following template if found (see `rules/template-adherence.md`), otherwise use clear structured format
   - Get current user via `github/get_me` for self-assignment
   - Create issue via `github/issue_write` with `method: "create"`, including `assignees` array with current user's login
5. For updates:
   - Identify issue number from user input
   - Fetch current issue details via `mcp__github__get_issue`
   - Determine fields to update (title, body, labels, assignees, state)
   - Apply updates using `mcp__github__issue_write` with `method: "update"`
6. For queries:
   - Use `mcp__github__get_issue` for a specific issue number
   - Use `mcp__github__search_issues` for filters, keywords, and cross-repo lookups
   - Use `mcp__github__list_issues` for repository issue lists
7. For comments:
   - Fetch issue context first when needed via `mcp__github__get_issue`
   - Add the comment using `mcp__github__add_issue_comment`
8. Display a summary with issue links and what changed

## Validation

- For titles: follow `rules/issue-title.md`
- For body with template: follow `rules/template-adherence.md`
- For labels: only use labels that already exist in the repository
- For assignees: only assign valid repository collaborators

---
name: managing-github-issues
description: Use when starting a session to find work, creating/triaging issues, or completing work and updating issue status
---

# Managing GitHub Issues

Use this skill when starting a session to find work, creating/triaging issues, or completing work and updating issue status.

## Finding Work

Start of session — check what's ready:
```
gh issue list --label priority:high --label status:ready
gh issue list --label priority:high
gh issue list --milestone "v0.1.0" --state open
```

## Creating Issues

Use structured bodies with Summary + Acceptance Criteria checklist:
```
gh issue create --title "Add X component" \
  --body "## Summary\n\nBrief description.\n\n## Acceptance Criteria\n\n- [ ] Criterion 1\n- [ ] Criterion 2" \
  --label "type:feature,area:components,priority:medium"
```

## Working on Issues

- Reference `#N` in commit messages
- Use `Fixes #N` in PR descriptions to auto-close

## Completing Work

- Close issues via PR merge (preferred) or `gh issue close N`
- After closing, check for newly unblocked work

## Label Taxonomy

| Category | Labels |
|----------|--------|
| Type | `type:feature`, `type:bug`, `type:task` |
| Priority | `priority:high` (do next), `priority:medium` (soon), `priority:low` (backlog) |
| Area | `area:components`, `area:tokens`, `area:infra`, `area:docs`, `area:storybook` |
| Status | `status:ready` (can start), `status:needs-design` (needs decisions) |
| OSS | `good first issue` |

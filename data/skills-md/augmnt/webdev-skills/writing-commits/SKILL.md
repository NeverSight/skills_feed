---
name: writing-commits
description: Generates commit messages and PR descriptions following Conventional Commits. Use when committing code, writing PR titles, reviewing git history, or when asked to describe changes. Triggers on git commit, PR creation, or changelog generation.
---

# Writing Commits

Follow Conventional Commits: `<type>(<scope>): <subject>`

## Types

| Type | Use For |
|------|---------|
| `feat` | New user-facing feature |
| `fix` | Bug fix |
| `docs` | Documentation only |
| `refactor` | Code change, no behavior change |
| `test` | Adding/fixing tests |
| `chore` | Build, deps, tooling |

## Rules

1. Subject: imperative mood, no period, ≤50 chars
2. Scope: optional area indicator (auth, api, ui)
3. Breaking changes: add `!` after type

## Examples

```bash
feat(auth): add Google OAuth login
fix(api): handle null user in profile endpoint
feat(api)!: change auth response format
chore(deps): upgrade Next.js to 15
```

## Anti-patterns

```bash
# ❌ Avoid
"fix stuff"
"updates"
"WIP"

# ✅ Prefer
"fix(auth): resolve token refresh race condition"
```

## PR Titles

Same format as commits. PR title becomes the squash commit message.

## PR Body

```markdown
## What
[Brief description]

## Why
[Context/motivation]

## Testing
[How verified]
```

## Branch Naming

```bash
# Format: type/short-description
feat/oauth-login
fix/token-refresh
chore/upgrade-deps

# With ticket numbers
feat/PROJ-123-oauth-login
fix/PROJ-456-token-refresh
```

Keep branches short-lived. Delete after merge.

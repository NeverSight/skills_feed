---
name: git-best-practices
description: Safe-by-default git workflow and Conventional Commits. Use for git operations (diffs, staging, commits, branches, merges, conflict resolution, rebase/cherry-pick), PR review, and releases (tagging). Prevent destructive operations without consent.
---

# Git Best Practices

## Safety Rules

- **Read-only by default**: Prefer `git status`, `git diff`, `git log`, `git show`, `git blame` before making changes
- **Push requires explicit request**: Never push unless user asks
- **Checkout allowed for**: PR review, explicit user request
- **Branch changes require consent**: Ask before creating/switching branches
- **History rewriting requires consent**: Ask before `commit --amend`, interactive rebase, or force push (especially if anything may be shared)
- **Destructive ops require explicit user consent**:
  - Allow previews like `git clean -n` (no deletion); do not run `git clean -fd` without consent
  - Do not discard worktree changes with `git reset --hard` or `git restore .` without consent
  - Do not delete branches/tags or force push without consent

## Preferred Commands

- Prefer modern porcelain: `git switch` (branches) and `git restore` (undo) when appropriate
- `git restore --staged <path>` is usually safe; discarding worktree changes (e.g., `git restore .`) requires explicit consent

## Conventional Commits

Format: `<type>[optional scope][optional !]: <description>`

### Subject Line

- Use imperative mood (“add”, “fix”, “remove”)
- Keep it short and specific; avoid trailing periods

### Types

| Type | Use for |
|------|---------|
| `feat` | New features |
| `fix` | Bug fixes |
| `docs` | Documentation only |
| `style` | Formatting, whitespace (no code change) |
| `refactor` | Code change that neither fixes nor adds |
| `perf` | Performance improvements |
| `test` | Adding or correcting tests |
| `build` | Build system or dependencies |
| `ci` | CI configuration |
| `chore` | Other changes (tooling, config) |
| `revert` | Reverting a previous commit |

### Scope

- Use the smallest sensible scope
- Omit scope if unclear or too broad
- Examples: `feat(auth):`, `fix(api):`, `docs(readme):`

### Breaking Changes

Mark with `!` before the colon OR add a `BREAKING CHANGE:` footer:

```
feat(api)!: remove deprecated endpoints

BREAKING CHANGE: /v1/users endpoint removed, use /v2/users
```

### Body and Footers

- Use body only when the subject line needs elaboration
- Footers follow git-trailer style: `Token: value`
- Common footers: `BREAKING CHANGE:`, `Fixes:`, `Refs:`, `Co-authored-by:`

### Examples

```
feat(auth): add OAuth2 login flow

fix: prevent race condition in queue processing

docs: update API authentication examples

refactor(db)!: migrate from MySQL to PostgreSQL

BREAKING CHANGE: database connection config format changed
```

## Pre-Commit Checklist

- Review `git status`
- Review `git diff` and `git diff --staged`
- Run the smallest relevant checks if known (or ask what to run)
- Scan for secrets (tokens, keys, credentials) and unintended debug logs
- Prefer small, logical commits; use `git add -p` when changes are mixed
- Propose a commit split and draft commit messages before staging/committing

## Workflow

After reviewing changes, end with:
1. Short summary of proposed commits
2. Clear question for next steps (stage/commit/push)

If anything is ambiguous, ask short, direct questions with options.

---
name: commit
description: Clean git commits with conventional commit detection and GitLeaks secret scanning. Use when the user wants to commit changes, stage files, or create git commits.
allowed-tools: Bash(git status) Bash(git add) Bash(git diff) Bash(git commit) Bash(git log) Bash(git pull) Bash(gitleaks) Read Edit Glob
metadata:
  model: sonnet
---

You create git commits with short, readable messages. Infer the project's language variant (US/UK English) from existing commits, docs, and code, and match it in all output.

Read individual rule files in `rules/` for detailed requirements and examples.

## Rules Overview

| Rule | Impact | File |
|------|--------|------|
| Message format | HIGH | `rules/message-format.md` |
| Issue references | MEDIUM | `rules/issue-references.md` |
| Change scope | MEDIUM | `rules/change-scope.md` |

## Key Rules Summary

### Message Format

- **Maximum 50 characters** (including any prefix). Present tense verbs. No trailing period.
- **Detect commitlint** first: look for `commitlint.config.*` or `commitlint` key in `package.json`
- **Conventional commit** (when commitlint is present): `type: description` or `type(scope): description`
  - Types: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`, `revert`
  - Example: `fix: handle auth redirect for expired tokens`
- **Plain format** (when no commitlint): start with a verb, no prefix
  - Example: `fix auth redirect for expired tokens`

### Issue References

When a GitHub issue is mentioned in conversation context, add a footer:

- `Closes #N` — changes fully resolve the issue
- `Relates to #N` — changes are related but don't fully close the issue

### Change Scope

- Keep related changes in a single commit (default)
- Only split when the changeset mixes unrelated functionality
- Stage specific file paths, not `git add .`

## Pre-Commit Security Check

Before committing, ensure GitLeaks is configured:

1. Check for `.husky/pre-commit` containing `gitleaks protect`
2. If missing, add `gitleaks protect --staged --verbose` before any `lint-staged` command
3. If `.husky/` doesn't exist, run `npx husky init` first

## Workflow

1. Pull latest changes from remote (`git pull`)
2. Show current `git status` and analyse all changes
3. Detect commitlint config to determine message format (see `rules/message-format.md`)
4. Check conversation context for GitHub issue references (see `rules/issue-references.md`)
5. Assess scope of changes (see `rules/change-scope.md`)
6. Stage files and create commit with message following `rules/message-format.md`

## Related Skills

- `/security` — run a pre-commit security audit for secrets and vulnerabilities
- `/setup` — configure GitLeaks, Husky, and commitlint if not already present

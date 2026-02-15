---
name: create-branch
description: Create and checkout a git branch with naming validation and GitHub issue linking. Use when the user wants to create a branch, start work on an issue, or set up a feature branch.
allowed-tools: Bash(git status) Bash(git branch) Bash(git checkout) Bash(git push) Bash(git rev-parse) Bash(git ls-remote) Bash(gh issue develop) Bash(gh issue list) Bash(gh issue view)
metadata:
  model: sonnet
---

You create and checkout git branches with validation. Infer the project's language variant (US/UK English) from existing branches, commits, and docs, and match it in all output.

Read individual rule files in `rules/` for detailed requirements and examples.

## Rules Overview

| Rule | Impact | File |
|------|--------|------|
| Branch naming | HIGH | `rules/branch-naming.md` |
| Prefix detection | MEDIUM | `rules/prefix-detection.md` |

## Key Rules Summary

### Branch Naming

Format: `prefix/kebab-case-description`

Validation:
- Lowercase only, spaces and underscores converted to hyphens
- Reject special characters: `~`, `^`, `:`, `?`, `*`, `[`, `]`, `\`, `@{`, `..`
- No leading or trailing slashes or hyphens
- Minimum 3 characters (excluding prefix), maximum 100 characters total

Examples: `feature/add-user-search`, `bugfix/login-redirect`, `docs/update-readme`

### Auto-Prefix Detection

Detect keywords in user input and apply the appropriate prefix:

| Prefix | Keywords |
|--------|----------|
| `feature/` | add, implement, create, new, feature |
| `bugfix/` | fix, bug, resolve, patch, repair |
| `hotfix/` | hotfix, urgent, critical, emergency |
| `chore/` | chore, refactor, update, upgrade, maintain |
| `docs/` | docs, documentation, readme, guide |

If user input already starts with a recognised prefix, keep it as-is.

## Workflow

1. If an issue number is provided, use `gh issue develop <number> -c` to create a linked branch and skip to step 4
2. Auto-detect prefix from user input (see `rules/prefix-detection.md`), validate name (see `rules/branch-naming.md`), and check for duplicates locally and remotely
3. Create and checkout from `main` → `master` → current HEAD: `git checkout -b <name> <base>`
4. Offer remote push: `git push -u origin <name>`

## Related Skills

- `/create-issue` — create a GitHub issue first, then use its number with `gh issue develop` to create a linked branch

---
name: commit
description: Commits staged changes using the conventional commits format with proper type, scope, and description. Use when committing code changes to maintain a clean, standardized git history.
---

# Conventional Commit

Commit the current changes to the repository using the conventional commits format:

`"$type${[(scope)]}{[!]}: $description"` where `[]` is optional and `!` is a breaking change

Types: fix | feat | chore | docs | refactor | test | perf | build | ci | style | revert | $other

## Rules

- When committing, don't log about logging in the commit message.
- Limit the first commit message line length to 50 characters.
- Use conventional commits with a scope, title and body.
- Do NOT add new things to the CHANGELOG.md file.

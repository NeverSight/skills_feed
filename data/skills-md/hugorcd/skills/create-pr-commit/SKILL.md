---
name: create-pr-commit
description: "Suggest conventional commit or pull request titles in the format type(scope): title, written in lowercase English. Use when asked to propose commit messages or PR titles, especially for /create-commit or /create-pr requests."
---

# Create Commit/PR Titles

## Workflow

1. Identify the change type: feat, fix, docs, style, refactor, perf, test, build, ci, chore, or revert.
2. Check repo health files (e.g., .github/ or contributing docs) for recommended scopes or naming tips.
3. Propose a concise scope (optional) that names the affected area (e.g., api, ui, docs, ci, auth).
4. Write a short, imperative title in lowercase English (no trailing period).
5. Output 1-3 options that follow `type(scope): title` or `type: title`.

## Heuristics

- Prefer clarity over cleverness.
- Keep titles under ~72 characters when possible.
- If the scope is unclear, omit it rather than guessing.
- When multiple change types apply, pick the primary one.

## Examples

- `docs: update contributing guide`
- `feat(auth): add oauth callback handler`
- `fix(ui): prevent double submit on form`

---
name: git-commit
description: Create git commits using conventional commits with scopes. Use when the user asks to commit, make a commit, save changes, or any git commit operation. Never include Co-Authored-By lines, AI agent mentions, or any reference to Claude, AI, or automated tooling in commit messages.
---

# Git Commit

## Rules

- **Never** add `Co-Authored-By` lines to commit messages
- **Never** mention Claude, AI, agent, copilot, or any automated tooling
- **Never** commit two unrelated changes together. Commits should be atomic.
- Commits must look like they were written by a human developer

## Format

```text
type(scope): subject

body (optional)
```

- **subject**: lowercase, imperative mood, no period, max 72 chars
- **body**: wrap at 72 chars, explain _why_ not _what_, separated by blank line

## Types

| Type       | Use for                                  |
| ---------- | ---------------------------------------- |
| `feat`     | New feature                              |
| `fix`      | Bug fix                                  |
| `refactor` | Code change that neither fixes nor adds  |
| `docs`     | Documentation only                       |
| `style`    | Formatting, semicolons, no code change   |
| `test`     | Adding or updating tests                 |
| `chore`    | Build, tooling, deps, no production code |
| `perf`     | Performance improvement                  |
| `ci`       | CI/CD configuration                      |

## Scope

Derive the scope from the primary area of change:

- Module or package name (`auth`, `api`, `db`)
- Feature area (`login`, `checkout`, `search`)
- Layer (`ui`, `server`, `cli`)

Omit scope only when the change is truly project-wide.

## Workflow

1. Run `git status` and `git diff --staged` (or `git diff` if nothing staged)
2. Identify the primary change type and scope
3. Write the commit message
4. Stage relevant files by name (avoid `git add .` or `git add -A`)
5. Commit using a HEREDOC:

```bash
git commit -m "$(cat <<'EOF'
type(scope): subject

optional body
EOF
)"
```

## Examples

```text
feat(auth): add password reset flow

Allow users to reset their password via email link.
Tokens expire after 30 minutes.
```

```text
fix(api): handle null response from payment gateway
```

```text
refactor(db): extract query builder into separate module
```

```text
chore(deps): upgrade react to v19
```

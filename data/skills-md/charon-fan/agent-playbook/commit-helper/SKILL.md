---
name: commit-helper
description: Helps write Git commit messages following the Conventional Commits specification. Use this skill when the user asks to commit changes, write commit messages, format commits, or mentions git commits.
allowed-tools: Read, Write, Edit, Bash, Grep
metadata:
  hooks:
    after_complete:
      - trigger: session-logger
        mode: auto
        reason: "Log commit activity"
---

# Commit Message Helper

A skill for creating properly formatted Git commit messages following the [Conventional Commits](https://www.conventionalcommits.org/) specification.

## When This Skill Activates

This skill activates when you:
- Ask to commit changes
- Mention commit messages
- Request git commit formatting
- Say "commit" or "git commit"

## Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

## Types

| Type | Description |
|------|-------------|
| `feat` | A new feature |
| `fix` | A bug fix |
| `docs` | Documentation only changes |
| `style` | Changes that do not affect the meaning of the code (formatting, etc.) |
| `refactor` | A code change that neither fixes a bug nor adds a feature |
| `perf` | A code change that improves performance |
| `test` | Adding missing tests or correcting existing tests |
| `chore` | Changes to the build process or auxiliary tools |
| `ci` | Changes to CI configuration files and scripts |
| `build` | Changes that affect the build system or external dependencies |

## Scope

The scope should indicate the area of the codebase affected:
- For frontend: `components`, `hooks`, `store`, `styles`, `utils`
- For backend: `api`, `models`, `services`, `database`, `auth`
- For devops: `ci`, `deploy`, `docker`
- Project-specific scopes are also acceptable

## Guidelines

### Subject Line
- Use imperative mood ("add feature" not "added feature" or "adds feature")
- No period at the end
- Maximum 50 characters
- Be specific and concise

### Body
- Separate subject from body with a blank line
- Use the body to explain **what** and **why**, not **how**
- Wrap at 72 characters per line
- Mention any breaking changes

### Footer
- Reference issues: `Closes #123`, `Fixes #456`, `Refs #789`
- Multiple issues: `Closes #123, #456, #789`
- Breaking changes: Start with `BREAKING CHANGE:` followed by description

## Examples

### Good Examples

```
feat(auth): add OAuth2 login support

Implement OAuth2 authentication flow to allow users to log in
with their Google or GitHub accounts.

This change adds:
- New OAuth2 middleware for handling callbacks
- Updated login UI with social login buttons
- User profile synchronization

Closes #123
```

```
fix(api): resolve race condition in user creation

The concurrent user creation requests could result in duplicate
email entries. Added unique constraint and proper error handling.

Fixes #456
```

```
refactor(user): simplify profile update logic

Extracted common validation logic into a reusable function
to reduce code duplication across profile update endpoints.
```

```
docs: update API documentation with new endpoints

Added documentation for the v2 user management endpoints
including request/response examples and error codes.
```

### Bad Examples

```
updated stuff                    # Too vague, no type/scope
fixed bug                        # No context about which bug
feat: added feature              # Redundant ("feat" means new feature)
Feat(User): Add Login            # Incorrect capitalization
feat: A really really really long subject line that exceeds the recommended limit  # Too long
```

## Breaking Changes

When introducing breaking changes, add `BREAKING CHANGE:` to the footer:

```
feat(api): migrate to REST v2

The API endpoints have been restructured for better consistency.
Old endpoints are deprecated and will be removed in v3.0.

BREAKING CHANGE: `/api/v1/users` is now `/api/v2/users`.
All consumers must update their integration by 2025-03-01.
```

## Workflow

When writing a commit message:

1. **Review changes** - Run `git diff` to understand what changed
2. **Identify type** - Determine the type of change
3. **Identify scope** - Determine which area is affected
4. **Write subject** - Create a clear, concise subject line
5. **Write body** - Explain what and why (if needed)
6. **Add footer** - Reference issues or note breaking changes

## Validation

Use the validation script to check commit message format:

```bash
python scripts/validate_commit.py "your commit message"
```

## Reference Documents

- See `references/conventional-commits.md` for full specification
- See `references/examples.md` for more examples
- See `references/scopes.md` for recommended scope naming

---
name: commit
description: "Create well-formatted commits with conventional commit messages. Use when user asks to commit, wants to commit changes, or needs help with commit messages."
metadata:
  author: nweii
  version: "1.0.1"
---

# Commit

Create well-formatted git commits following conventional commit conventions.

## Convention

Follow the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) specification:

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `style`: Formatting, missing semi-colons, etc. (no code change)
- `refactor`: Code change that neither fixes a bug nor adds a feature
- `perf`: Performance improvement
- `test`: Adding missing tests
- `chore`: Maintenance tasks (build process, dependencies, etc.)

### Guidelines

- **Subject line**: Max 50 characters, imperative mood ("add" not "added")
- **Body**: Wrap at 72 characters, explain *what* and *why* (not *how*)
- **Scope**: Optional, indicates section of codebase (e.g., `feat(auth):`)
- **Breaking changes**: Add exclamation mark after type/scope (e.g., `feat!:`) and explain in footer

## Process

1. Review staged changes (`git diff --staged`)
2. Determine appropriate type and scope
3. Write concise, descriptive subject line
4. Add body if the change needs explanation
5. Execute the commit

## Examples

```
feat(auth): add OAuth2 login support

Implements Google and GitHub OAuth providers.
Closes #123
```

```
fix: resolve race condition in data fetcher

The previous implementation could return stale data
when multiple requests were in flight.
```

```
chore: update dependencies to latest versions
```

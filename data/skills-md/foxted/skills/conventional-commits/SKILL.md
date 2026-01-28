---
name: conventional-commits
description: Ensures commit messages follow conventional commit format with proper type, scope, and description. Use when generating commit messages, reviewing staged changes, or when the user asks for help writing commit messages.
---

# Conventional Commits

This project follows the [Conventional Commits](https://www.conventionalcommits.org/) specification for commit messages.

## Commit Format

```
type(scope): description

[optional body]

[optional footer]
```

## Commit Types

Use one of these types:

- `feat` - A new feature
- `fix` - A bug fix
- `docs` - Documentation only changes
- `chore` - Maintenance tasks, dependency updates, config changes
- `refactor` - Code restructuring without changing behavior
- `test` - Adding or updating tests
- `style` - Formatting, whitespace, missing semicolons (no code change)
- `perf` - Performance improvements
- `ci` - CI/CD configuration changes
- `build` - Build system or external dependencies changes

## Scope

Scope is optional but recommended for monorepo projects. Use workspace/app names:

- `cms` - CMS/Payload changes
- `clients` - Clients app changes
- `lawyers` - Lawyers app changes
- `website` - Website app changes
- `packages` - Shared package changes

Examples:

- `feat(cms): add new collection`
- `fix(clients): resolve form validation issue`
- `docs(website): update API documentation`

## Description

- Use imperative mood ("add" not "added" or "adds")
- Lowercase first letter (unless starting with proper noun)
- No period at the end
- Keep it concise (50-72 characters recommended)

## Examples

**Good:**

```
feat: introduce editors field for enhanced content management
docs: add AI Elements skill for manual component installation
fix: add CollectionCards to import map for UI components
refactor: simplify AI chat components and enhance conversation handling
chore: update dependencies and configurations for CMS packages
feat(cms): add new blog post collection
fix(clients): resolve authentication token expiration
```

**Bad:**

```
Added new feature
fix bug
Update README.md
feat: Added new feature for users
fix(clients): Fixed the bug that was causing issues
```

## When to Use Each Type

**feat** - New functionality that users will notice
**fix** - Bug fixes that resolve incorrect behavior
**docs** - README, comments, documentation files
**chore** - Package.json updates, lock files, config tweaks
**refactor** - Restructuring code without changing what it does
**test** - Test files only
**style** - Code style changes (formatting, whitespace)
**perf** - Performance optimizations
**ci** - GitHub Actions, CI config files
**build** - Build tools, bundlers, transpilers

## Multi-line Commits

For complex changes, use body:

```
feat(cms): add draft/publish workflow

- Add draft status field to collections
- Implement publish endpoint
- Add validation for draft content
```

---
name: conventional-commits
description: Generate conventional commit messages following the project's commitlint rules with proper scopes. Use when committing changes to ensure semantic versioning works correctly.
allowed-tools: Bash, Read
---

# Conventional Commits Skill

This skill helps you create proper conventional commit messages for semantic versioning.

## When to Use This Skill

- Creating git commits
- Ensuring semantic release works correctly
- Understanding commit message format
- Fixing commit message errors
- Planning version bumps
- Writing meaningful commit messages

## Conventional Commits Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Required Elements

- **type**: Category of change (feat, fix, chore, etc.)
- **subject**: Brief description (imperative mood, lowercase, no period)

### Optional Elements

- **scope**: Package or area affected (api, web, database, etc.)
- **body**: Detailed description
- **footer**: Breaking changes, issue references

## Commit Types

### Version Bumping Types

**feat** - New feature (minor version bump)
```bash
git commit -m "feat: add user authentication"
git commit -m "feat(api): add COE data endpoint"
```

**fix** - Bug fix (patch version bump)
```bash
git commit -m "fix: resolve database connection timeout"
git commit -m "fix(web): fix chart rendering issue"
```

**feat!** or **BREAKING CHANGE** - Breaking change (major version bump)
```bash
git commit -m "feat!: change API response format"
git commit -m "fix!: remove deprecated endpoints"

# Or with footer
git commit -m "feat: redesign auth system

BREAKING CHANGE: Auth tokens now use JWT format"
```

### Non-Version Bumping Types

**chore** - Maintenance tasks, no production code change
```bash
git commit -m "chore: update dependencies"
git commit -m "chore(deps): upgrade Next.js to v16"
```

**docs** - Documentation only
```bash
git commit -m "docs: update README with deployment steps"
git commit -m "docs(api): add API documentation"
```

**refactor** - Code refactoring, no functional changes
```bash
git commit -m "refactor: simplify cache logic"
git commit -m "refactor(database): optimize query performance"
```

**test** - Adding or updating tests
```bash
git commit -m "test: add unit tests for auth service"
git commit -m "test(web): add E2E tests for checkout flow"
```

**style** - Code style changes (formatting, whitespace)
```bash
git commit -m "style: format code with Biome"
git commit -m "style: fix linting errors"
```

**perf** - Performance improvements
```bash
git commit -m "perf: optimize database queries"
git commit -m "perf(web): reduce bundle size"
```

**ci** - CI/CD changes
```bash
git commit -m "ci: add deployment workflow"
git commit -m "ci: fix GitHub Actions syntax"
```

**build** - Build system changes
```bash
git commit -m "build: update Turbo configuration"
git commit -m "build: add new package to monorepo"
```

**revert** - Revert previous commit
```bash
git commit -m "revert: revert 'feat: add feature X'"
```

## Available Scopes

Project-specific scopes:

- **api**: API service (apps/api)
- **web**: Web application (apps/web)
- **admin**: Admin application (apps/admin)
- **docs**: Documentation (apps/docs)
- **database**: Database package (packages/database)
- **types**: Types package (packages/types)
- **ui**: UI package (packages/ui)
- **utils**: Utils package (packages/utils)
- **logos**: Logos package (packages/logos)
- **infra**: Infrastructure (infra/)
- **deps**: Dependency updates
- **release**: Release-related changes

## Commit Message Guidelines

### Subject Line

**✅ Good:**
```
feat: add user authentication
fix: resolve memory leak in cache
chore: update Next.js to v16
```

**❌ Bad:**
```
feat: Add user authentication.  # No period
Fix: resolve memory leak        # Capitalized
added new feature               # No type
```

### Rules

1. **Imperative mood**: Use "add" not "added" or "adds"
2. **Lowercase**: Subject should be lowercase
3. **No period**: Don't end subject with period
4. **50 chars max**: Keep subject concise (72 chars absolute max)
5. **Be specific**: Describe what changed, not how

### Body

Use body for detailed explanation:

```bash
git commit -m "feat: add blog post generation

Implemented LLM-powered blog generation using Google Gemini.
Posts are automatically generated from car registration data
and published to the website.

Features:
- Gemini API integration
- Automated content generation
- Publishing workflow"
```

### Footer

Use footer for breaking changes and issue references:

```bash
git commit -m "feat: redesign API authentication

BREAKING CHANGE: Authentication now requires JWT tokens
instead of API keys. Update clients to use new auth flow.

Closes #123
Refs #456"
```

## Examples by Scenario

### Adding a Feature

```bash
# Simple feature
git commit -m "feat(web): add dark mode toggle"

# Feature with scope
git commit -m "feat(api): add COE bidding data endpoint"

# Feature with body
git commit -m "feat(web): add interactive charts

Implemented interactive charts for car registration data
using Recharts library. Charts support filtering by make,
model, and date range."
```

### Fixing a Bug

```bash
# Simple fix
git commit -m "fix(api): resolve database connection timeout"

# Fix with details
git commit -m "fix(web): fix chart rendering on mobile

Charts were not rendering correctly on mobile devices
due to incorrect responsive container configuration.
Updated chart components to use proper breakpoints."

# Critical fix
git commit -m "fix!: resolve security vulnerability in auth

BREAKING CHANGE: Auth tokens now require additional
signature verification. Clients must update to new SDK."
```

### Updating Dependencies

```bash
# Single dependency
git commit -m "chore(deps): upgrade Next.js to v16"

# Multiple dependencies
git commit -m "chore(deps): update dependencies

- Next.js 15 → 16
- React 18 → 19
- Drizzle ORM 0.28 → 0.30"

# Security update
git commit -m "fix(deps): update vulnerable packages

Updated packages with known security vulnerabilities:
- axios 0.27.0 → 1.6.0 (CVE-2023-45857)
- express 4.17.1 → 4.18.2"
```

### Refactoring

```bash
# Code refactoring
git commit -m "refactor(database): simplify migration logic"

# Extract component
git commit -m "refactor(web): extract reusable Button component"

# Rename
git commit -m "refactor(api): rename getCwd to getCurrentWorkingDirectory"
```

### Documentation

```bash
# Update docs
git commit -m "docs: update deployment instructions"

# Add docs
git commit -m "docs(api): add API endpoint documentation"

# Fix typos
git commit -m "docs: fix typos in README"
```

### Tests

```bash
# Add tests
git commit -m "test(api): add unit tests for auth service"

# Update tests
git commit -m "test(web): update E2E tests for new flow"

# Fix failing tests
git commit -m "test: fix flaky integration tests"
```

### Chores

```bash
# Update config
git commit -m "chore: update TypeScript config"

# Clean up
git commit -m "chore: remove unused dependencies"

# Tooling
git commit -m "chore: add Biome configuration"
```

## Version Bump Examples

### Patch (0.0.x)

Bug fixes, no new features:
```bash
git commit -m "fix: resolve login error"
git commit -m "fix(web): fix broken link in navigation"
```

### Minor (0.x.0)

New features, backwards compatible:
```bash
git commit -m "feat: add export to CSV functionality"
git commit -m "feat(api): add pagination to car data endpoint"
```

### Major (x.0.0)

Breaking changes:
```bash
git commit -m "feat!: redesign API response format"
git commit -m "fix!: remove deprecated auth method

BREAKING CHANGE: API keys no longer supported.
Use JWT tokens for authentication."
```

## Multi-Package Commits

When changes affect multiple packages:

```bash
# Scoped to main package
git commit -m "feat(web): add new dashboard page

Also updates:
- packages/ui: add new components
- packages/types: add dashboard types"

# No scope if truly cross-cutting
git commit -m "chore: update TypeScript to v5

Updates TypeScript across all packages to v5.0"
```

## Breaking Changes

### Explicit Breaking Change

```bash
git commit -m "feat!: change database schema

BREAKING CHANGE: User table renamed to users.
Run migration before deploying."
```

### With Description

```bash
git commit -m "refactor!: redesign authentication

BREAKING CHANGE: Authentication flow completely redesigned.

Migration Guide:
1. Update auth tokens to JWT format
2. Replace getUser() with getCurrentUser()
3. Update middleware to use new auth context

Closes #234"
```

## Issue References

Link commits to issues:

```bash
# Closes an issue
git commit -m "fix: resolve login timeout

Closes #123"

# References an issue
git commit -m "feat: add user profile page

Refs #456"

# Multiple issues
git commit -m "fix: resolve multiple auth bugs

Closes #123, #124, #125"
```

## Commit Message Template

Create a commit template:

```bash
# ~/.gitmessage
# <type>(<scope>): <subject>
#
# <body>
#
# <footer>
#
# Types: feat, fix, docs, style, refactor, perf, test, chore
# Scopes: api, web, admin, docs, database, types, ui, utils, infra, deps
#
# Remember:
# - Use imperative mood (add, fix, update)
# - Keep subject under 50 characters
# - Separate subject from body with blank line
# - Wrap body at 72 characters
# - Use body to explain what and why, not how
# - Use footer for breaking changes and issue refs
```

Set as default:
```bash
git config --global commit.template ~/.gitmessage
```

## Commitlint Configuration

The project uses commitlint to enforce rules:

```javascript
// commitlint.config.js
module.exports = {
  extends: ["@commitlint/config-conventional"],
  rules: {
    "type-enum": [
      2,
      "always",
      [
        "feat",
        "fix",
        "docs",
        "style",
        "refactor",
        "perf",
        "test",
        "build",
        "ci",
        "chore",
        "revert",
      ],
    ],
    "scope-enum": [
      2,
      "always",
      [
        "api",
        "web",
        "admin",
        "docs",
        "database",
        "types",
        "ui",
        "utils",
        "logos",
        "infra",
        "deps",
        "release",
      ],
    ],
    "subject-case": [2, "always", "lower-case"],
    "subject-empty": [2, "never"],
    "subject-full-stop": [2, "never", "."],
    "header-max-length": [2, "always", 72],
  },
};
```

## Husky Integration

Commits are validated on commit:

```bash
# .husky/commit-msg
npx --no -- commitlint --edit $1
```

If commit fails:
```bash
git commit -m "bad commit"
# ✖ subject may not be empty [subject-empty]
# ✖ type may not be empty [type-empty]
```

Fix and retry:
```bash
git commit -m "feat: add new feature"
# ✔ Commit message passes validation
```

## Amending Commits

Fix commit message:

```bash
# Amend last commit message
git commit --amend

# Amend without changing message
git commit --amend --no-edit
```

## Viewing Commit History

```bash
# See recent commits
git log --oneline -10

# See commits with type
git log --oneline --grep="^feat"
git log --oneline --grep="^fix"

# See commits for specific scope
git log --oneline --grep="(web)"
git log --oneline --grep="(api)"
```

## Semantic Release

The project uses semantic-release to automatically:
1. Determine version bump based on commits
2. Generate changelog
3. Create git tag
4. Publish release

Commit types → Version bump:
- `feat:` → Minor (0.x.0)
- `fix:` → Patch (0.0.x)
- `feat!:` or `BREAKING CHANGE:` → Major (x.0.0)
- Other types → No bump

## Quick Reference

```bash
# New feature
feat: <description>
feat(<scope>): <description>

# Bug fix
fix: <description>
fix(<scope>): <description>

# Breaking change
feat!: <description>
fix!: <description>

# No version bump
chore: <description>
docs: <description>
refactor: <description>
test: <description>
style: <description>

# With body and footer
type(scope): subject

Detailed explanation here

BREAKING CHANGE: Description
Closes #123
```

## Troubleshooting

### Commit Rejected

**Error**: `subject may not be empty`
**Fix**: Add subject after colon
```bash
git commit -m "feat: add user login"
```

**Error**: `type may not be empty`
**Fix**: Add valid type
```bash
git commit -m "feat: add feature"
```

**Error**: `scope must be one of [...]`
**Fix**: Use valid scope or omit
```bash
git commit -m "feat(api): add endpoint"
# or
git commit -m "feat: add endpoint"
```

**Error**: `header must not be longer than 72 characters`
**Fix**: Shorten subject, use body for details
```bash
git commit -m "feat: add feature

Detailed explanation goes in body, not subject line"
```

## References

- Conventional Commits: https://www.conventionalcommits.org
- Commitlint: https://commitlint.js.org
- Semantic Release: https://semantic-release.gitbook.io
- Related files:
  - `commitlint.config.js` - Commitlint configuration
  - Root CLAUDE.md - Commit message guidelines

## Best Practices

1. **Clear Subjects**: Write clear, concise subjects
2. **Proper Types**: Use correct type for the change
3. **Scopes**: Add scope when change is package-specific
4. **Breaking Changes**: Mark breaking changes explicitly
5. **Issue Links**: Reference issues in footer
6. **Imperative Mood**: Use "add" not "added"
7. **Lowercase**: Keep subject lowercase
8. **No Period**: Don't end subject with period

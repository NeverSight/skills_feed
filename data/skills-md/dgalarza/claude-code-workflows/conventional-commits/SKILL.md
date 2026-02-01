---
name: conventional-commits
description: This skill should be used when creating Git commits to ensure they follow the Conventional Commits specification. It provides guidance on commit message structure, types, scopes, and best practices for writing clear, consistent, and automated-friendly commit messages. Use when committing code changes or reviewing commit history.
---

# Conventional Commits

This skill provides guidance for writing Git commits that follow the Conventional Commits specification (v1.0.0).

## Purpose

Conventional Commits is a specification for adding human and machine-readable meaning to commit messages. It provides an easy set of rules for creating an explicit commit history, which makes it easier to understand project changes and improve collaboration.

## When to Use This Skill

Use this skill when:
- Creating Git commits
- Reviewing commit messages in PRs
- Writing clear, structured commit messages
- Collaborating on projects with multiple contributors

## Commit Message Structure

### Basic Format

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

### Examples

```
feat: add user authentication
feat(api): add JWT token generation
fix: resolve memory leak in image processor
docs: update README with setup instructions
refactor(database): optimize user query performance
```

## Commit Types

### Primary Types

**feat** - A new feature for the user
```
feat: add export to PDF functionality
feat(api): add webhook signature verification
```

**fix** - A bug fix for the user
```
fix: resolve login redirect loop
fix(api): handle null response from GitHub webhook
```

**docs** - Documentation only changes
```
docs: update API endpoint documentation
docs(readme): add troubleshooting section
```

**style** - Changes that don't affect code meaning (formatting, whitespace)
```
style: format code with StandardRB
style(css): update button padding
```

**refactor** - Code change that neither fixes a bug nor adds a feature
```
refactor: extract user validation to service object
refactor(models): simplify tenant scoping logic
```

**perf** - Performance improvements
```
perf: add database index for user lookups
perf(queries): reduce N+1 queries in artifacts index
```

**test** - Adding or updating tests
```
test: add specs for user authentication
test(integration): add webhook processing tests
```

**chore** - Changes to build process, dependencies, or maintenance
```
chore: update Rails to 7.2.0
chore(deps): bump sidekiq from 7.1.0 to 7.2.0
```

### Additional Types (Less Common)

**build** - Changes to build system or dependencies
```
build: configure Docker for production
build(webpack): update asset compilation settings
```

**ci** - Changes to CI configuration
```
ci: add security scanning to GitHub Actions
ci(tests): run RSpec in parallel
```

**revert** - Reverts a previous commit
```
revert: revert "feat: add export feature"

This reverts commit abc123.
```

## Scope (Optional)

Scope provides additional context about what part of the codebase changed:

```
feat(auth): add two-factor authentication
fix(api): handle rate limit errors
docs(contributing): update PR guidelines
refactor(services): extract common validation logic
```

**Common scope examples:**
- `auth` - Authentication/authorization
- `api` - API endpoints
- `ui` - User interface components
- `database` or `db` - Database models/migrations
- `services` - Service objects
- `jobs` - Background jobs
- `tests` - Test suite
- `deps` - Dependencies
- `config` - Configuration changes
- `docs` - Documentation

Choose scopes that match your project's architecture and domain areas.

## Description

The description is a short summary of the code change:

**Rules:**
- Use imperative, present tense: "add" not "added" or "adds"
- Don't capitalize first letter
- No period (.) at the end
- Keep under 72 characters (ideally under 50)

**Good descriptions:**
```
add user profile page
fix memory leak in file upload
update email templates for notifications
remove deprecated API endpoint
```

**Bad descriptions:**
```
Added user profile page          # Past tense
Fix Memory Leak In File Upload   # Capitalized
Updated email templates.          # Period at end
Lots of changes to the codebase   # Vague
```

## Body (Optional)

The body provides additional context about the change:

**When to include a body:**
- Complex changes needing explanation
- Non-obvious design decisions
- Breaking changes
- Migration instructions

**Format:**
- Separate from description with blank line
- Use imperative mood like description
- Wrap at 72 characters
- Can include multiple paragraphs

**Example:**
```
feat(api): add webhook signature verification

Add HMAC-SHA256 signature verification for all incoming webhooks
to prevent unauthorized access and replay attacks.

The signature is validated using a secret key stored per
installation. Requests with invalid signatures are rejected
with a 401 response.
```

## Footer (Optional)

Footers provide metadata about the commit:

### Breaking Changes

Use `BREAKING CHANGE:` footer for incompatible API changes:

```
feat(api): change authentication endpoint

BREAKING CHANGE: The /auth endpoint now requires a client_id parameter.
Update all API clients to include client_id in authentication requests.
```

Or use `!` after type/scope:

```
feat!: change authentication endpoint
feat(api)!: remove deprecated /login endpoint
```

### Issue References

Reference issues and pull requests:

```
fix(auth): resolve session timeout bug

Fixes #123
Closes #456
Related to #789
```

**Common reference types:**
- `Fixes #123` - Closes the issue
- `Closes #123` - Closes the issue
- `Resolves #123` - Closes the issue
- `Related to #123` - References without closing
- `See also #123` - Additional reference

### Co-authors

Credit multiple contributors:

```
feat: add data export feature

Co-authored-by: Jane Doe <jane@example.com>
Co-authored-by: John Smith <john@example.com>
```

## Complete Examples

### Simple Feature

```
feat: add password reset functionality
```

### Feature with Scope

```
feat(api): add rate limiting for endpoints
```

### Bug Fix with Body

```
fix(api): handle rate limit errors from GitHub

When GitHub API returns 429 status, retry the request
with exponential backoff up to 3 attempts before failing.

Fixes #234
```

### Breaking Change

```
feat(api)!: redesign webhook payload structure

BREAKING CHANGE: Webhook payloads now use a nested structure.

Before:
{
  "event": "issue.created",
  "data": {...}
}

After:
{
  "type": "issue",
  "action": "created",
  "payload": {...}
}

Clients must update their webhook handlers to use the new structure.
```

### Refactoring

```
refactor(services): extract validation to concern

Move common validation logic from multiple services into
a shared ValidationConcern module. No behavior changes.
```

### Multiple Footers

```
fix(auth): resolve concurrent login race condition

Add database-level locking to prevent race condition when
multiple login attempts occur simultaneously for the same user.

Fixes #567
Related to #432
Reviewed-by: Jane Doe <jane@example.com>
```

## Best Practices

### Do:
✅ Use present tense imperative mood ("add" not "added")
✅ Keep first line under 50 characters when possible
✅ Reference issues/PRs in footer
✅ Explain "why" in body, not "what" (code shows what)
✅ Break up large changes into multiple commits
✅ Make commits atomic (one logical change per commit)

### Don't:
❌ Use vague descriptions ("fix stuff", "updates")
❌ Combine multiple unrelated changes in one commit
❌ Capitalize first letter of description
❌ End description with period
❌ Use past tense ("added", "fixed")
❌ Commit broken code (each commit should work)

## Summary

Conventional Commits provide:
- ✅ Clear, consistent commit history
- ✅ Better collaboration through explicit intent
- ✅ Easier code review and git history navigation
- ✅ Improved project documentation through structured messages

**Key formula:**
```
<type>(<scope>): <description>

[body]

[footer]
```

For detailed examples and edge cases, see `references/commit-examples.md`.

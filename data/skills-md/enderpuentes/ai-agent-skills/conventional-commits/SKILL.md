---
name: conventional-commits
description: Generate and validate commit messages following the Conventional Commits specification. Use when creating git commits, writing commit messages, reviewing commit history, generating changelogs, or when the user mentions commits, commit messages, semantic versioning, or changelog generation.
---

# Conventional Commits

## Overview

Conventional Commits is a specification for commit messages that provides an explicit structure for creating a clear commit history. It enables automated tools for generating changelogs, determining semantic version bumps, and communicating changes effectively.

**Core Principle**: Every commit message follows a structured format that clearly communicates the type and scope of changes.

## Commit Message Structure

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

## Quick Reference

| Element         | Required    | Format                   | Purpose                             |
| --------------- | ----------- | ------------------------ | ----------------------------------- |
| **Type**        | ✅ Yes      | `feat`, `fix`, or custom | Indicates the nature of the change  |
| **Scope**       | ❌ Optional | Parentheses: `(parser)`  | Provides additional context         |
| **Breaking**    | ❌ Optional | `!` after type/scope     | Indicates breaking changes          |
| **Description** | ✅ Yes      | Short summary            | Brief description of the change     |
| **Body**        | ❌ Optional | Free-form paragraphs     | Detailed explanation                |
| **Footer**      | ❌ Optional | `Token: value` format    | Metadata (e.g., `BREAKING CHANGE:`) |

## Commit Types

### Standard Types

- **`feat`**: A new feature (correlates with MINOR in SemVer)
- **`fix`**: A bug fix (correlates with PATCH in SemVer)

### Additional Types (Common)

- **`build`**: Changes to build system or dependencies
- **`chore`**: Maintenance tasks, no production code change
- **`ci`**: Changes to CI configuration
- **`docs`**: Documentation only changes
- **`hotfix`**: Emergency bug fix applied directly to production, bypassing normal development workflow (correlates with PATCH in SemVer)
- **`perf`**: Performance improvements
- **`refactor`**: Code refactoring without behavior change
- **`style`**: Code style changes (formatting, missing semicolons, etc.)
- **`test`**: Adding or updating tests

## Breaking Changes

Breaking changes can be indicated in two ways:

1. **In the type/scope prefix**: Append `!` before the colon

   ```
   feat!: remove deprecated API
   feat(api)!: change authentication method
   ```

2. **In the footer**: Use `BREAKING CHANGE:` token

   ```
   feat: add new authentication system

   BREAKING CHANGE: Old authentication tokens are no longer valid
   ```

## Examples

### Basic Feature Commit

```
feat: add user authentication endpoint

Implement JWT-based authentication with login and token validation
```

### Feature with Scope

```
feat(auth): implement password reset flow

Add forgot password endpoint and email notification system
```

### Bug Fix

```
fix(parser): correct array parsing with multiple spaces

Handle edge case where strings contained multiple consecutive spaces
```

### Breaking Change (Prefix)

```
feat(api)!: remove deprecated v1 endpoints

BREAKING CHANGE: All v1 API endpoints have been removed. Migrate to v2.
```

### Breaking Change (Footer)

```
feat: update database schema

BREAKING CHANGE: Environment variables now take precedence over config files
```

### Documentation

```
docs: update API reference for authentication endpoints
```

### Refactoring

```
refactor(auth): extract token validation to separate module

Improve code organization and testability
```

### Performance

```
perf(queries): optimize database query for user lookup

Reduce query time from 500ms to 50ms by adding index
```

### Hotfix

#### Security Hotfix

```
hotfix(auth): fix critical security vulnerability in token validation

Immediate fix for CVE-2024-XXXX. Patch token validation to prevent unauthorized access.
```

#### Database Hotfix

```
hotfix(db): fix connection pool exhaustion causing service outage

Emergency patch to increase pool size and add connection timeout. Applied directly to production to restore service.
```

#### Payment Hotfix

```
hotfix(payment): fix incorrect currency conversion in checkout

Critical bug causing incorrect charges. Immediate fix applied to prevent financial impact.
```

#### API Hotfix

```
hotfix(api): fix null pointer exception in user endpoint

Emergency fix for production crash. Bypassed normal deployment process.
```

#### Performance Hotfix

```
hotfix(cache): fix memory leak causing server crashes

Immediate fix for production instability. Applied hotfix to prevent service degradation.
```

#### Data Integrity Hotfix

```
hotfix(data): fix corrupted data migration affecting user accounts

Emergency fix applied directly to production database to prevent data loss.
```

## Common Mistakes

### ❌ Missing Colon and Space

```
feat add authentication
```

✅ **Correct:**

```
feat: add authentication
```

### ❌ Uppercase Type

```
FEAT: add authentication
```

✅ **Correct:**

```
feat: add authentication
```

### ❌ Description Too Long

```
feat: add user authentication with JWT tokens, password hashing, session management, and email verification
```

✅ **Correct:**

```
feat(auth): implement JWT-based authentication

Add login endpoint, password hashing, session management, and email verification
```

### ❌ Using Wrong Type

```
fix: add new feature for user dashboard
```

✅ **Correct:**

```
feat: add user dashboard
```

### ❌ Breaking Change Not Indicated

```
feat(api): remove deprecated endpoints
```

✅ **Correct:**

```
feat(api)!: remove deprecated endpoints

BREAKING CHANGE: All v1 endpoints have been removed
```

### ❌ Scope Without Parentheses

```
feat auth: implement login
```

✅ **Correct:**

```
feat(auth): implement login
```

## Workflow Guidelines

### When Creating Commits

1. **Determine the type**: Is this a feature, fix, or other type?
   - Use `hotfix` for emergency fixes applied directly to production, bypassing normal development workflow
   - Use `fix` for regular bug fixes in normal development workflow
2. **Identify scope** (optional): Which part of the codebase is affected?
3. **Check for breaking changes**: Does this change break existing functionality?
4. **Write concise description**: Keep under 72 characters when possible
5. **Add body if needed**: Provide context, motivation, or details
6. **Include footer if applicable**: Add breaking changes, references, etc.

### Description Best Practices

- Use imperative mood: "add feature" not "added feature" or "adds feature"
- Don't end with a period
- Keep it concise (50-72 characters ideal)
- Focus on what changed, not why (why goes in body)

### Body Best Practices

- Separate from description with blank line
- Explain the "why" behind the change
- Provide context or background
- Reference related issues or PRs

## Semantic Versioning Correlation

| Commit Type       | SemVer Impact             |
| ----------------- | ------------------------- |
| `fix`             | PATCH (1.0.0 → 1.0.1)     |
| `hotfix`          | PATCH (1.0.0 → 1.0.1)     |
| `feat`            | MINOR (1.0.0 → 1.1.0)     |
| `BREAKING CHANGE` | MAJOR (1.0.0 → 2.0.0)     |
| Other types       | No automatic version bump |

## Validation Checklist

Before finalizing a commit message, verify:

- [ ] Type is lowercase and valid
- [ ] Colon and space follow type/scope
- [ ] Description is concise and imperative
- [ ] Breaking changes are properly indicated
- [ ] Body is separated by blank line (if present)
- [ ] Footer tokens use hyphens (e.g., `BREAKING CHANGE`, not `BREAKING_CHANGE`)
- [ ] Message doesn't exceed 120 characters in title (if team standard)

## Special Cases

### Revert Commits

```
revert: let us never again speak of the noodle incident

Refs: 676104e, a215868
```

### Multiple Commits for One Feature

If a commit conforms to multiple types, split into separate commits when possible:

```
feat(auth): add login endpoint
test(auth): add login endpoint tests
docs(auth): update API documentation for login
```

## Integration with Tools

Conventional Commits enables:

- **Automatic changelog generation**: Tools parse commit history
- **Semantic versioning**: Automated version bumps based on commit types
- **Release notes**: Extract features and fixes from commits
- **Build triggers**: Different build processes for different commit types

## Specification Reference

This skill is based on the official [Conventional Commits specification v1.0.0](https://www.conventionalcommits.org/en/v1.0.0/).

All rules, examples, and guidelines in this skill follow the official specification. For the complete specification, examples, and FAQ, refer to the [official documentation](https://www.conventionalcommits.org/en/v1.0.0/).

---
name: Conventional Commits
description: Ensures all commit messages and PR titles follow the Conventional Commits specification.
---

# Conventional Commits Standard

This skill ensures that project history is clean, readable, and machine-parseable.

## Format Structure

Messages should follow this structure:

```text
<type>(<scope>): <subject>
<空行>
[body]
<空行>
[footer]
```

**Subject Regex**: `^(build|chore|ci|docs|feat|fix|perf|refactor|revert|style|test)(\([a-z0-9-]+\))?!?: .+$`

## Types

- **feat**: A new feature (correlates with MINOR in SemVer).
- **fix**: A bug fix (correlates with PATCH in SemVer).
- **docs**: Documentation only changes.
- **style**: Changes that do not affect the meaning of the code (white-space, formatting, missing semi-colons, etc).
- **refactor**: A code change that neither fixes a bug nor adds a feature.
- **perf**: A code change that improves performance.
- **test**: Adding missing tests or correcting existing tests.
- **build**: Changes that affect the build system or external dependencies (example scopes: gulp, broccoli, npm).
- **ci**: Changes to our CI configuration files and scripts (example scopes: Travis, Circle, BrowserStack, SauceLabs).
- **chore**: Other changes that don't modify src or test files.
- **revert**: Reverts a previous commit.

## Extended Content Guidelines

### 1. Body (Optional)

The body provides a place to explain the **why** and **how** of the change. Use it for:

- Explaining the motivation for the change.
- Describing the technical approach or trade-offs.
- Listing multiple related changes in a single commit.

**Rules for Body**:

- Separate from the subject with a blank line.
- Use a blank line between paragraphs.
- Keep lines wrapped at ~72 characters for readability in CLI tools.

### 2. Footer (Optional)

The footer is used for metadata and tracking.

- **Breaking Changes**: Must start with `BREAKING CHANGE:` followed by a description.
- **Issue Tracking**: Reference issues (e.g., `Fixes #123`, `Closes #456`).

## Rules

1. **Imperative Mood**: Use "add feature" instead of "added feature" in the subject.
2. **No Period**: Do not end the subject line with a period.
3. **Lowercase Subject**: Keep the subject line lowercase (except for proper nouns).
4. **Separation**: Always use blank lines between Subject, Body, and Footer.

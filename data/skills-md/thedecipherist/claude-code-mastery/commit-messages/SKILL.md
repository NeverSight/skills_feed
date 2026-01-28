---
name: commit-messages
description: Generate clear, conventional commit messages from git diffs. Use when writing commit messages, reviewing staged changes, or preparing releases.
---

# Commit Message Skill

Generate consistent, informative commit messages following the Conventional Commits specification.

## When to Use This Skill

- User asks to "commit", "write a commit message", or "prepare commit"
- User has staged changes and mentions commits
- Before any `git commit` command

## Process

1. **Analyze changes**: Run `git diff --staged` to see what's being committed
2. **Identify the type**: Determine the primary change category
3. **Find the scope**: Identify the main area affected
4. **Write the message**: Follow the format below

## Commit Message Format

```
<type>(<scope>): <description>

[optional body]

[optional footer(s)]
```

### Types

| Type | Description | Example |
|------|-------------|---------|
| `feat` | New feature | `feat(auth): add OAuth2 login` |
| `fix` | Bug fix | `fix(api): handle null response` |
| `docs` | Documentation only | `docs(readme): add setup instructions` |
| `style` | Formatting, no code change | `style: fix indentation` |
| `refactor` | Code change, no new feature/fix | `refactor(db): extract query builder` |
| `perf` | Performance improvement | `perf(search): add result caching` |
| `test` | Adding/fixing tests | `test(auth): add login unit tests` |
| `build` | Build system changes | `build: update webpack config` |
| `ci` | CI configuration | `ci: add GitHub Actions workflow` |
| `chore` | Maintenance tasks | `chore(deps): update dependencies` |
| `revert` | Revert previous commit | `revert: feat(auth): add OAuth2` |

### Scope

The scope should be a noun describing the section of the codebase:
- `auth`, `api`, `db`, `ui`, `config`
- Feature names: `search`, `checkout`, `dashboard`
- Or omit if change is broad

### Subject Line Rules

- Use imperative mood: "add" not "added" or "adds"
- Don't capitalize first letter after colon
- No period at the end
- Max 72 characters total

### Body (when needed)

- Separate from subject with blank line
- Explain *what* and *why*, not *how*
- Wrap at 72 characters
- Use bullet points for multiple changes

### Footer (when needed)

- `BREAKING CHANGE:` for breaking changes
- `Fixes #123` to close issues
- `Refs #456` to reference without closing

## Examples

### Simple feature
```
feat(search): add fuzzy matching support

Implement Levenshtein distance algorithm for typo tolerance
in search queries. Configurable via FUZZY_THRESHOLD env var.
```

### Bug fix with issue reference
```
fix(cart): prevent duplicate items on rapid clicks

Add debounce to add-to-cart button and check for existing
items before insertion.

Fixes #234
```

### Breaking change
```
feat(api)!: change response format to JSON:API

BREAKING CHANGE: API responses now follow JSON:API spec.
All clients need to update their parsers.

- Wrap data in `data` object
- Move metadata to `meta` object  
- Add `links` for pagination
```

### Multiple related changes
```
refactor(auth): consolidate authentication logic

- Extract JWT handling to dedicated service
- Move session management from controller to middleware
- Add refresh token rotation

This prepares for the upcoming OAuth2 integration.
```

## Output

When generating a commit message:

1. Show the staged changes summary
2. Propose the commit message
3. Explain the type/scope choice if non-obvious
4. Ask if the user wants to proceed or modify

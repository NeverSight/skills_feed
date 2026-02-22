---
name: conventional-commit
description: Create one or more Conventional Commits following the spec and push the current branch. Use when the user asks to create commits, write a conventional commit message, commit and push changes, or prepare commits before opening a pull request.
license: MIT
metadata:
  author: kota
  version: "1.2.0"
---

# Conventional Commit

Follow the [Conventional Commits specification](https://www.conventionalcommits.org/en/v1.0.0/) for all commits.

## Preconditions

### Validate branch

Run `git rev-parse --abbrev-ref HEAD`.

If on `main` or `master`, stop and ask the user to create a feature branch.

Branch names should follow: `<TICKET_PREFIX>-<number>-<kebab-case-description>` (e.g., `ENG-1333-migrate-review-flow`). If invalid, ask the user to rename the branch.

## Conventional Commits Spec

The commit message format:

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

### Types (required)

| Type | Purpose |
|------|---------|
| `feat` | A new feature (correlates with MINOR in SemVer) |
| `fix` | A bug fix (correlates with PATCH in SemVer) |
| `docs` | Documentation only changes |
| `style` | Changes that do not affect meaning (whitespace, formatting) |
| `refactor` | Code change that neither fixes a bug nor adds a feature |
| `perf` | Code change that improves performance |
| `test` | Adding or correcting tests |
| `build` | Changes to build system or external dependencies |
| `ci` | Changes to CI configuration files and scripts |
| `chore` | Other changes that don't modify src or test files |

### Scope (optional)

A noun describing the section of codebase affected, in parentheses:

- `feat(parser): add ability to parse arrays`
- `fix(auth): resolve token expiration bug`

### Breaking Changes

Append `!` after type/scope OR add `BREAKING CHANGE:` footer:

```
feat(api)!: remove deprecated endpoints

BREAKING CHANGE: The /v1/users endpoint has been removed. Use /v2/users instead.
```

Breaking changes correlate with MAJOR in SemVer.

## Steps

1. Review current state

   ```bash
   git status
   git diff
   git log -1 --oneline
   ```

2. Group changes logically - prefer multiple small commits over one large commit

3. Create commits

   For each logical group:
   - Stage relevant files or hunks
   - Commit using Conventional Commit format

   **Option A**: Use git commit directly (recommended for agents):

   ```bash
   git commit -m "feat(auth): add OAuth2 support"
   ```

   Multi-line with body:

   ```bash
   git commit -m "feat(api): add pagination to list endpoints" \
     -m "Implements cursor-based pagination for all list endpoints." \
     -m "BREAKING CHANGE: Response format changed from array to object with data/meta keys."
   ```

   **Option B**: Use `git-cz` non-interactive mode (streamich/git-cz, not standard cz):

   ```bash
   npx git-cz --non-interactive --type=feat --scope=auth --subject="add OAuth2 support"
   ```

   With body/breaking changes:

   ```bash
   npx git-cz --non-interactive \
     --type=feat \
     --scope=api \
     --subject="add pagination to list endpoints" \
     --body="Implements cursor-based pagination for all list endpoints" \
     --breaking="Response format changed from array to object with data/meta keys"
   ```

   > **Note**: The standard `npx cz` (commitizen/cz-cli) is interactive-only and cannot be used by agents. Use `git commit` or `npx git-cz --non-interactive` instead.

4. Push the branch

   ```bash
   git push -u origin HEAD  # if no upstream
   git push                 # otherwise
   ```

## Commit Message Guidelines

- **Description**: Use imperative mood ("add" not "added" or "adds")
- **Description**: Lowercase, no period at end
- **Body**: Explain what and why, not how
- **Footer**: Reference issues (`Fixes #123`, `Closes #456`)

## Notes

- Do not commit secrets, credentials, or environment files
- Describe intent and impact, not implementation detail
- When in doubt, split commits
- This skill does not perform rebases, squashes, or force pushes

## References

- [Conventional Commits Specification](https://www.conventionalcommits.org/en/v1.0.0/)
- [git-cz (non-interactive mode)](https://github.com/streamich/git-cz)

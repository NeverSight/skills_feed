---
name: conventional-commit
description: Generates git commit messages following Conventional Commits 1.0.0 specification with semantic types (feat, fix, etc.), optional scope, and breaking change annotations. Use when committing code changes or creating commit messages.
---

# Conventional Commit Generator

Generate commit messages following [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/).

## Workflow

1. Run `git status` and `git diff HEAD` to analyze changes
2. Stage files: user-specified only, or `git add -A` for all
3. Determine type and scope from changes
4. Generate commit message incorporating user hints
5. Commit using HEREDOC format to preserve formatting:

   ```bash
   git commit -m "$(cat <<'EOF'
   <type>(<scope>): <description>

   <body>

   <footer>
   EOF
   )"
   ```

6. Output: `<hash> <subject>`

## Scope Boundaries

**DO:** Analyze git changes, generate messages, stage files, commit

**DO NOT:** Modify code, push (unless asked), create branches, amend without request

## Commit Format

```text
<type>[optional scope][!]: <description>

[optional body]

[optional footer(s)]
```

## Type Selection

| Change                                  | Type       | SemVer |
| --------------------------------------- | ---------- | ------ |
| New feature                             | `feat`     | MINOR  |
| Bug fix                                 | `fix`      | PATCH  |
| Performance improvement                 | `perf`     | PATCH  |
| Code restructuring (no behavior change) | `refactor` | -      |
| Code style/formatting (no logic change) | `style`    | -      |
| Adding/updating tests                   | `test`     | -      |
| Documentation only                      | `docs`     | -      |
| Build system/dependencies               | `build`    | -      |
| CI/CD configuration                     | `ci`       | -      |
| Reverts a previous commit               | `revert`   | -      |
| Other maintenance tasks                 | `chore`    | -      |

> **Note:** Only `feat` and `fix` have SemVer implications. Breaking changes (any type with exclamation mark or `BREAKING CHANGE` footer) trigger MAJOR.

## Subject Line

- **Max length:** 72 characters (50 recommended for readability)
- **Format:** `type(scope): description` or `type: description`
- **Mood:** Imperative present tense ("add" not "added" or "adds")
- **Case:** Lowercase first letter
- **Punctuation:** No trailing period

## Scope

Scope provides context about which part of the codebase is affected. Use a noun describing the module, component, or area.

**Common scope patterns:**

- Component/module: `feat(auth):`, `fix(parser):`, `refactor(api):`
- File/area: `docs(readme):`, `test(unit):`, `build(webpack):`
- Feature: `feat(dark-mode):`, `fix(checkout):`

## Body

- Separate from subject with one blank line
- Explain *what* and *why*, not *how*
- Can contain multiple paragraphs (separate with blank lines)
- Wrap at 72 characters

## Footer

Footers follow [git trailer format](https://git-scm.com/docs/git-interpret-trailers) with `:<space>` or `<space>#` separator.

**Common footers:**

- `BREAKING CHANGE: <description>` - Breaking API change
- `Refs: #123` or `Refs: JIRA-456` - Reference issues
- `Closes: #123` or `Fixes: #123` - Close issues
- `Co-authored-by: Name <email>` - Credit co-authors
- `Reviewed-by: Name <email>` - Credit reviewers
- `Acked-by: Name` - Acknowledgment

> **Note:** Footer tokens use `-` instead of spaces (e.g., `Reviewed-by` not `Reviewed by`). Exception: `BREAKING CHANGE` allows space.

## Breaking Changes

Two ways to indicate breaking changes (can use both for emphasis):

1. **Exclamation mark:** Add exclamation mark before colon in subject

   ```text
   feat(api)!: remove deprecated endpoints
   ```

2. **Footer:** Add `BREAKING CHANGE:` or `BREAKING-CHANGE:` in footer

   ```text
   feat(api): redesign authentication flow

   BREAKING CHANGE: OAuth tokens now expire after 1 hour instead of 24 hours.
   ```

## Examples

**Simple feature:**

```text
feat: add email notifications for new messages
```

**Bug fix with scope:**

```text
fix(cart): prevent ordering with empty shopping cart
```

**Documentation update:**

```text
docs(api): add authentication examples to README
```

**Breaking change with body and footer:**

```text
feat(api)!: redesign user authentication endpoints

Migrate from session-based auth to JWT tokens for better scalability.
The new system supports refresh tokens and configurable expiration.

BREAKING CHANGE: /api/login now returns JWT instead of session cookie.
Clients must include Authorization header with Bearer token.
Refs: JIRA-1337
```

**Revert commit:**

```text
revert: let us never again speak of the noodle incident

Refs: 676104e, a215868
```

**Multi-scope change (use most significant):**

```text
feat(auth): add OAuth2 support with Google provider

Adds Google OAuth2 login flow with automatic account linking.

Co-authored-by: Jane Doe <jane@example.com>
Closes: #42
```

## Anti-patterns

Avoid these common mistakes:

| Bad            | Good                                   | Reason                |
| -------------- | -------------------------------------- | --------------------- |
| `Update code`  | `fix(auth): validate token expiration` | Be specific           |
| `Fixed bug`    | `fix: prevent null pointer in parser`  | Use present tense     |
| `WIP`          | Don't commit WIP                       | Commit complete units |
| `Add feature.` | `feat: add dark mode toggle`           | No trailing period    |
| `Added tests`  | `test: add unit tests for parser`      | Use imperative mood   |
| `FEAT: Add...` | `feat: add...`                         | Types are lowercase   |
| `misc changes` | `chore: update dependencies`           | Be descriptive        |

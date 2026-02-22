---
name: conventional-commits
description: Generate commit messages following the Conventional Commits v1.0.0 specification with Angular convention types. Use when creating git commits, writing commit messages, or when the user asks for help with commit messages.
---

# Conventional Commits

Based on the [Conventional Commits v1.0.0](https://www.conventionalcommits.org/en/v1.0.0/) specification.

The keywords MUST, MUST NOT, REQUIRED, SHALL, SHALL NOT, SHOULD, SHOULD NOT, RECOMMENDED, MAY, and OPTIONAL are interpreted as described in [RFC 2119](https://www.ietf.org/rfc/rfc2119.txt):
- **MUST / REQUIRED / SHALL** — absolute requirement
- **MUST NOT / SHALL NOT** — absolute prohibition
- **SHOULD / RECOMMENDED** — may be ignored with good reason, but implications must be understood
- **SHOULD NOT / NOT RECOMMENDED** — may be acceptable with good reason, but implications must be understood
- **MAY / OPTIONAL** — truly optional

## Commit Message Format

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

Prefer the shortest form that fully conveys the change. Most commits SHOULD be a single line (`type[scope]: description`). Only add body or footers when the description alone cannot convey enough context.

## Types

`feat` MUST be used for new features (correlates with SemVer MINOR). `fix` MUST be used for bug fixes (correlates with SemVer PATCH). Other types MAY be used. The following are RECOMMENDED (based on the [Angular convention](https://github.com/angular/angular/blob/22b96b9/CONTRIBUTING.md#type)):

| Type | Purpose |
|------|---------|
| `feat` | New feature |
| `fix` | Bug fix |
| `build` | Build system or external dependency changes |
| `chore` | Maintenance tasks, no production code change |
| `ci` | CI configuration and scripts |
| `docs` | Documentation only |
| `style` | Formatting, whitespace — no logic change |
| `refactor` | Code restructuring — no feature or fix |
| `perf` | Performance improvement |
| `test` | Adding or updating tests |

## Rules

### Structure

1. Commits MUST be prefixed with a type (a lowercase noun), followed by an OPTIONAL scope, an OPTIONAL `!`, and a REQUIRED terminal colon and space (`: `)
2. A scope MAY be provided after the type. A scope MUST be a noun in parentheses describing a section of the codebase: `fix(parser): ...`
3. A description MUST immediately follow the `: ` after the type/scope prefix
4. A body MAY be provided after the description. It MUST begin one blank line after the description, is free-form, and MAY consist of any number of newline-separated paragraphs
5. One or more footers MAY be provided one blank line after the body. Each footer MUST consist of a word token followed by `:<space>` or `<space>#` separator, followed by a string value. Footer tokens MUST use `-` in place of whitespace (exception: `BREAKING CHANGE`)
6. Footer values MAY contain spaces and newlines; parsing terminates when the next valid footer token/separator pair is observed

### Breaking changes

7. Breaking changes MUST be indicated by a `!` immediately before the `: ` in the type/scope prefix, OR as a `BREAKING CHANGE:` footer entry (or both). A `BREAKING CHANGE` footer MUST be uppercase text followed by colon, space, and description. When `!` is used, the `BREAKING CHANGE:` footer MAY be omitted. Breaking changes correlate with SemVer MAJOR
8. `BREAKING-CHANGE` MUST be synonymous with `BREAKING CHANGE` when used as a footer token

### Case sensitivity

9. All structural elements MUST NOT be treated as case sensitive, with the exception of `BREAKING CHANGE` which MUST be uppercase

## Scope Conventions

Use short, lowercase nouns that identify the section of the codebase:

- Module or feature area: `auth`, `api`, `billing`, `editor`
- Layer: `hooks`, `ui`, `domain`, `infra`
- App or package name in a monorepo: `frontend`, `functions`

Keep scopes consistent across the project — reuse existing scopes before inventing new ones.

## Examples

**Simple feature (preferred short form):**
```
feat: add user avatar upload
```

**Fix with scope:**
```
fix(api): prevent race condition in request handler
```

**Breaking change with `!` (short form):**
```
feat(auth)!: replace session-based auth with JWT
```

**Breaking change with `!` and footer (long form, when context is needed):**
```
feat(auth)!: replace session-based auth with JWT

BREAKING CHANGE: all endpoints now require Bearer token instead of session cookie
```

**Body for additional context (only when the description is not enough):**
```
fix: prevent racing of requests

Introduce a request id and a reference to latest request. Dismiss
incoming responses other than from latest request.

Remove timeouts which were used to mitigate the racing issue but are
obsolete now.

Refs: #123
```

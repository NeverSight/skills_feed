---
name: commit
description: >
  Guidance for writing git commit messages that follow the Conventional Commits
  1.0.0 specification. Use when preparing commit messages, summarizing code
  changes for a commit, or validating commit text for compliance.
---

# Conventional Commits

## Overview

The commit skill summarizes the Conventional Commits 1.0.0 specification and
common best practices, supporting compliant commit messages. Reference:
[Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/).

## Commit Format

```text
<type>[optional scope][!]: <description>

[optional body]

[optional footer(s)]
```

**Elements:**

- **type** (required): Primary intent of the change. `feat` and `fix` map to
  semantic versioning. Additional allowed types include: `docs`, `style`,
  `refactor`, `perf`, `test`, `build`, `ci`, `chore`, `revert`.
- **scope** (optional): Short component or package name in parentheses, e.g.,
  `feat(parser): ...`.
- **!** (optional): Indicates a breaking change and can appear after type or
  scope.
- **description** (required): Short, imperative summary in lower case (no
  trailing period). Aim for ≤ 72 characters.
- **body** (optional): Explain what/why; wrap at ~72 characters.
- **footers** (optional): Git trailer format, e.g., `BREAKING CHANGE: ...`,
  `Refs: #123`, `Closes: #123`.

## Workflow

1. Review changes and identify the primary intent (feature, fix, docs, etc.).
2. Choose the `type` and optional `scope`. If changes span multiple intents,
   prefer separate commits; otherwise pick the highest-impact type.
3. Determine whether the change is breaking. If yes, add `!` and/or a
   `BREAKING CHANGE:` footer.
4. Write a concise description in imperative mood.
5. Add body and footers as needed for context, rationale, or issue links.
6. Validate against the checklist below.

## Checklist

- Header matches `<type>(<scope>): <description>` format.
- Type is correct for the change (`feat`/`fix` for user-facing behavior).
- Description is imperative, ≤ 72 chars, and has no trailing period.
- Breaking changes are marked with `!` and/or `BREAKING CHANGE:`.
- Footers follow `Token: value` format.

## Examples

- `feat(auth): add refresh token rotation`
- `fix(api): handle empty payloads`
- `docs: add migration guide`
- `refactor(ui): extract button variants`
- `perf(db): batch writes to reduce roundtrips`
- `chore(deps): bump eslint to 9.0.0`

Breaking change:

```text
feat(api)!: drop deprecated v1 endpoints

BREAKING CHANGE: v1 endpoints were removed. Use /v2 instead.
```

Revert:

```text
revert: feat(auth): add refresh token rotation

This reverts commit 1234abcd.
```

## Tips

- Use scopes for packages or subsystems (e.g., `api`, `ui`, `cli`).
- Avoid mixing unrelated changes in a single commit.
- Use `style` or `chore` for formatting-only changes.
- Use `ci` or `build` for pipeline and dependency changes.
- Use `test` for changes limited to tests.

---
name: ashik-commitlint-practice
version: 1.0.0
description: Use when the user wants help crafting commit messages that pass the
  @cbashik/commitlint rules, or mentions commitlint, conventional commits, commit
  message linting, or commit types/scopes/subjects.
---

# Ashik Commitlint Practice

You are an expert in writing commit messages that satisfy the @cbashik/commitlint
configuration in `index.js`. Your goal is to help users produce compliant commit
messages and understand the rules.

## Initial Assessment

Before proposing a commit message, confirm:

1. **Change intent** - What is the change and why was it made?
2. **Scope** - Is there a specific area/module? (Optional, lowercase, max 20)
3. **Required format** - Single commit or multiple? Any release or hotfix intent?

---

## Core Principles

### 1. Use the Required Structure
The parser expects `type(scope): subject` or `type: subject`.

```
<type>[optional scope]: <subject>

[optional body]

[optional footer]
```

### 2. Choose an Allowed Type
Only these types are allowed:

- feat: new feature
- fix: bug fix
- docs: documentation changes
- style: formatting/whitespace-only changes
- refactor: refactoring without feature/bug changes
- perf: performance improvement
- test: add or update tests
- build: build system or external dependency changes
- ci: CI configuration changes
- chore: maintenance tasks
- revert: revert a previous commit
- hotfix: critical production fix
- release: release commit

### 3. Enforce Length and Case Rules
- Header length: 10-100 characters
- Type: required, lowercase, must be in the allowed list
- Scope: optional, lowercase, max 20 characters
- Subject: required, lowercase, 3-80 characters, no trailing period
- Body: optional, max line length 100, blank line before body (warning)
- Footer: optional, max line length 100, blank line before footer (warning)

---

## Examples

Valid:

- feat: add user authentication
- fix(auth): handle token refresh
- docs(readme): update setup instructions
- chore: update dependencies

Invalid:

- FEAT: add feature (type must be lowercase)
- feat: Add feature. (subject must be lowercase, no period)
- feat:add feature (space required after colon)
- f: add feature (header too short)

## Help

See the canonical format guidance:
https://github.com/projectashik/commitlint#commit-message-format

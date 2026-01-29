---
name: code-committing
description: Generate semantic commit messages following conventional commits format. Use when committing code, staging changes, writing commit messages, requesting git commit, or when user mentions commit, commit message, conventional commits, semantic commits, git commit, stage changes, create commit. Supports monorepo package version tracking.
license: Unlicense
---

# Code Committing

## Format

### Language Requirement

Always write in English only

```text
<type>(<scope>): summary
```

- **Summary**: ≤50 chars, imperative mood, no period
- **Scope**: Module/package name (monorepo: exact package name or `all`)
- **Body** (optional): Bullet list `- {emoji} {text}` (≤100 chars/line)
- **Breaking**: Add `!` after type and `BREAKING CHANGE:` footer
- **Issues**: End the body with a bullet like `- Fixes #123` or `- Fixes PROJ-456`

**Types**: feat ✨, fix 🐛, docs 📚, style 💄, refactor ♻️, perf ⚡, test ✅, build 🔧, ci 👷, chore 🔨, revert ⏪

## Examples

**Simple feature:**

```text
feat(button): add loading state

- ✨ Add spinner icon during async operations
- 📦 @ui/icons: v1.0.0 → v1.1.0
- Fixes #42
```

**Breaking change:**

```text
feat(theme)!: redesign color tokens

- ✨ Replace RGB values with HSL format
- 💄 Update all component styles to use new tokens
- 📦 @ui/theme: v2.1.0 → v3.0.0

BREAKING CHANGE: Color token values changed from RGB to HSL format
```

For more examples, see [references/examples.md](references/examples.md)

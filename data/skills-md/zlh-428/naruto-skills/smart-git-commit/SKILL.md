---
name: smart-git-commit
description: Create well-formatted git commits with conventional commit format and emoji. Automatically runs pre-commit checks (lint, build, docs), analyzes changes, suggests splitting when appropriate, and generates emoji-prefixed conventional commit messages. Use when creating commits in any repository to ensure consistent, professional commit history.
---

# Smart Git Commit

Create well-formatted commits with conventional commit format and emoji: `$ARGUMENTS`

## Quick Start

```bash
# Basic commit with auto-generated message
/smart-git-commit

# Provide custom message
/smart-git-commit "add user authentication"

# Skip pre-commit checks
/smart-git-commit --no-verify

# Amend last commit
/smart-git-commit --amend
```

## Workflow

### 1. Pre-Commit Checks (Default)

Unless `--no-verify` is specified, automatically runs:
- `pnpm lint` - Ensure code quality
- `pnpm build` - Verify build succeeds
- `pnpm generate:docs` - Update documentation

If checks fail, asks whether to proceed or fix issues first.

### 2. Stage Analysis

Checks git status to determine staged files:
- **Files already staged**: Only commits those files
- **No files staged**: Automatically stages all modified/new files

### 3. Change Analysis

Performs `git diff --cached` to understand changes and:
- Detects commit type (feat, fix, docs, refactor, etc.)
- Identifies if multiple distinct changes are present
- Suggests splitting when appropriate

### 4. Message Generation

Creates commit message in format: `<emoji> <type>: <description>`

See [commit-types.md](references/commit-types.md) for full emoji/type reference.

## Commit Types

| Type | Emoji | Description |
|------|-------|-------------|
| `feat` | ✨ | New feature |
| `fix` | 🐛 | Bug fix |
| `docs` | 📝 | Documentation |
| `style` | 💄 | Formatting/style |
| `refactor` | ♻️ | Code refactoring |
| `perf` | ⚡️ | Performance |
| `test` | ✅ | Tests |
| `chore` | 🔧 | Tooling, config |
| `ci` | 🚀 | CI/CD |

## Command Options

| Option | Description |
|--------|-------------|
| `[message]` | Custom commit description (optional) |
| `--no-verify` | Skip pre-commit checks (lint, build, docs) |
| `--amend` | Amend the previous commit |

## Splitting Guidelines

Consider splitting when:
1. **Different concerns**: Unrelated codebase areas
2. **Different types**: Features + fixes + docs mixed
3. **File patterns**: Source code vs documentation vs tests
4. **Size**: Large changes clearer if broken down

See [examples.md](references/examples.md) for splitting examples.

## Examples

```bash
# Auto-generated from staged changes
/smart-git-commit
# Output: ✨ feat: add user authentication system

# Custom message
/smart-git-commit "resolve memory leak in parser"
# Output: 🐛 fix: resolve memory leak in parser

# Skip checks for quick fixes
/smart-git-commit --no-verify "typo fix"
# Output: ✏️ fix: typo fix
```

## Best Practices

- **Atomic commits**: Each commit serves one purpose
- **Present tense**: "add feature" not "added feature"
- **Concise**: First line under 72 characters
- **Review diff**: Ensure message matches changes

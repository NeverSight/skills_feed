---
name: commit
description: Enforces Conventional Commits format when creating git commits. Use this skill whenever you need to create a commit message. Triggers on "commit", "git commit", "コミット", "変更をコミット".
---

# Conventional Commit

Enforces [Conventional Commits](https://www.conventionalcommits.org/) format for all git commit messages. This skill applies to both AI agents and human users.

## Commit Message Format

```
<type>[optional scope][optional !]: <description>

[optional body]

[optional footer(s)]
```

### Types (Required)

| Type | Description |
|------|-------------|
| `feat` | A new feature |
| `fix` | A bug fix |
| `docs` | Documentation only changes |
| `style` | Changes that do not affect the meaning of the code (white-space, formatting, etc.) |
| `refactor` | A code change that neither fixes a bug nor adds a feature |
| `perf` | A code change that improves performance |
| `test` | Adding missing tests or correcting existing tests |
| `build` | Changes that affect the build system or external dependencies |
| `ci` | Changes to CI configuration files and scripts |
| `chore` | Other changes that don't modify src or test files |
| `revert` | Reverts a previous commit |

### Scope (Optional)

Scope provides additional context. Determine scope by checking recent commits:

```bash
git log --oneline -10
```

Common scope patterns:
- Feature/module name: `feat(auth):`, `fix(api):`
- File/directory: `docs(readme):`, `refactor(utils):`
- Component: `style(button):`, `test(login):`

### Breaking Changes

Add `!` before the colon for breaking changes:
```
feat(api)!: change authentication endpoint
```

Or add `BREAKING CHANGE:` in the footer.

## Examples

### Basic (No Scope)

```
feat: add user registration form
fix: resolve memory leak in event handler
docs: update installation instructions
```

### With Scope

```
feat(auth): implement OAuth2 login
fix(api): handle null response from server
refactor(utils): simplify date formatting logic
```

### With Body (Japanese)

```
feat(検索): 全文検索機能を追加

Elasticsearchを使用した全文検索機能を実装。
日本語形態素解析にはkuromojiを使用。
```

### Breaking Change

```
feat(api)!: change response format to JSON:API

BREAKING CHANGE: API responses now follow JSON:API specification.
Clients need to update their response parsers.
```

## Validation

To validate a commit message before committing:

```bash
bash /mnt/skills/user/conventional-commit/scripts/validate-commit.sh "feat: add new feature"
```

## For AI Agents

When creating commits:

1. **Always** use Conventional Commits format
2. **Check** recent commits for scope patterns: `git log --oneline -10`
3. **Use** the appropriate type based on the change
4. **Do NOT** use emojis in commit messages
5. **Write** clear, concise descriptions
6. **Add** body for complex changes
7. **Mark** breaking changes with `!` or `BREAKING CHANGE:`

### Language

- Use the same language as the codebase or user's preference
- Japanese descriptions are fully supported
- Keep type prefixes in English (feat, fix, etc.)

## Git Hooks (Optional)

To enforce validation via git hooks, add to `.git/hooks/commit-msg`:

```bash
#!/bin/bash
bash /mnt/skills/user/conventional-commit/scripts/validate-commit.sh "$(cat $1)" || exit 1
```

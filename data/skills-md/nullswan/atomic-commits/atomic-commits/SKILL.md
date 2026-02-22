---
name: atomic-commits
description: Organize git changes into clean, atomic commits for better history. Use when the user has accumulated multiple changes and wants to split them into separate, logical commits. Triggers on "atomic commits", "split commits", "organize my changes", "clean commit history", or when many unrelated changes are staged together.
license: MIT
metadata:
  author: nullswan
  version: "1.0.0"
allowed-tools: Bash(git:*)
---

# Atomic Commits

Organize multiple git changes into clean, atomic commits that maintain a proper git history.

## Workflow

### 1. Analyze Changes

```bash
git status
git diff --stat
git diff
```

### 2. Group Changes Logically

Categorize by type:
- **feat**: New features
- **fix**: Bug fixes
- **refactor**: Code improvements
- **docs**: Documentation
- **test**: Test changes
- **chore**: Maintenance

### 3. Commit Incrementally

Stage specific files for each logical commit:

```bash
git add path/to/related/files
git commit -m "feat: add user authentication"

git add path/to/other/files
git commit -m "fix: correct null check in validator"
```

### 4. Push

```bash
git log --oneline -10  # Verify commits
git push origin <branch>
```

## Commit Order

1. Documentation (lowest risk)
2. Tests (verification setup)
3. Bug fixes (independent corrections)
4. Features (main changes)
5. Refactoring (improvements)

## Commit Message Format

```
<type>(<scope>): <description>

[optional body]
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

## Example

Given changes to login page, avatar fix, README update, and new tests:

```bash
git add README.md
git commit -m "docs: update README with login instructions"

git add tests/login.test.ts
git commit -m "test: add login component tests"

git add src/components/Avatar.tsx
git commit -m "fix: correct avatar display on retina screens"

git add src/pages/Login.tsx src/components/LoginForm.tsx
git commit -m "feat: add login page with validation"

git push origin feature/login
```

## Tips

- Each commit should be independently reviewable
- Each commit should leave codebase in working state
- When in doubt, prefer more commits over fewer
- Use `git add -p` for interactive staging of partial files

See [references/advanced.md](references/advanced.md) for advanced patterns.

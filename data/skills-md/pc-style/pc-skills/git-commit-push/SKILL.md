---
name: git-commit-push
description: Stage changes, commit with conventional commits, and push to origin. Use when the user wants to commit and push in one go, save changes to GitHub, or after completing work on a branch. Combines staging, committing, and pushing into a single workflow.
---

# Git Commit and Push

Stage changes, create a conventional commit, and push to origin in one workflow.

## When to Use

- Ready to save changes to GitHub
- Work is complete and tested
- Any request to "commit and push" or "save changes"

## Workflow

### 1. Check Current State

```bash
git status
git branch --show-current
```

### 2. Review Changes

```bash
git diff
# or if files already staged:
git diff --staged
```

### 3. Stage Files

**Stage all changes:**
```bash
git add .
```

**Stage specific files:**
```bash
git add path/to/file1 path/to/file2
```

**Stage by pattern:**
```bash
git add src/components/*.tsx
```

### 4. Create Conventional Commit

Analyze the diff to determine type and scope:

```bash
git commit -m "<type>[optional scope]: <description>"
```

**Types:**
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation
- `style:` - Formatting
- `refactor:` - Code refactoring
- `perf:` - Performance
- `test:` - Tests
- `chore:` - Maintenance

**Examples:**
```bash
git commit -m "feat(auth): add OAuth2 login flow"
git commit -m "fix(api): resolve null pointer exception"
git commit -m "docs: update README with setup instructions"
```

### 5. Push to Origin

**Push current branch:**
```bash
git push
```

**First push (set upstream):**
```bash
git push -u origin HEAD
```

### 6. Verify

```bash
git log --oneline -3
git status
```

## Complete Examples

**Commit and push all changes:**
```bash
git add .
git commit -m "feat: add dark mode toggle"
git push
```

**Commit specific files:**
```bash
git add src/auth.ts src/middleware.ts
git commit -m "feat(auth): implement JWT verification"
git push
```

**Commit with body:**
```bash
git add .
git commit -m "feat(search): add elasticsearch integration

- Configure ES client
- Add search endpoint
- Implement result ranking

Closes #234"
git push
```

## Git Safety Protocol

- NEVER commit secrets (.env, credentials)
- NEVER run `git push --force` to main/master
- NEVER use `--no-verify` unless explicitly asked
- If commit fails due to hooks, fix issues and create NEW commit

## Best Practices

- Commit related changes together
- Write clear, imperative commit messages
- Keep commits atomic (one logical change)
- Push frequently to back up work
- Verify CI passes after push
---
name: prepare-pull-request
description: Prepares pull request branches by stashing changes, creating feature branch from main, reviewing changes, running code quality checks on modified files only, generating conventional commit messages, and pushing. Use when preparing a PR, creating a branch for pull request, or committing changes following conventional commits.
---

# Prepare Pull Request Workflow

Complete workflow for preparing PR branches: stash changes, create branch, review changes, run quality checks, commit, and push.

## Workflow Steps

### 1. Stash and Create Branch

**Important:** Always pull latest main branch code before creating new branch.

```bash
git status  # Confirm uncommitted changes exist
git stash push -m "temp: stash before creating branch"
git checkout main
git pull origin main  # Pull latest code from main branch (use actual main branch name if different, e.g., master)
git checkout -b <branch-name>
git stash pop
```

**Branch naming:** Infer from changes if not specified. Use prefixes: `feat/`, `fix/`, `refactor/`, `docs/`, `style/`, `test/`, `chore/`.

### 2. Review Changes

```bash
git diff
git diff --name-only  # Get modified files list
```

**Check for unnecessary modifications:**
- Identify formatting-only changes (whitespace, line endings, indentation)
- If only formatting detected, ask user: keep, revert, or proceed

### 3. Run Code Quality Checks

**Only on modified files** - never format entire project.

1. Detect tools from project config:
   - JS/TS: `package.json` scripts, `.eslintrc*`, `eslint.config.*`, `.prettierrc*`
   - Python: `pyproject.toml`, `.ruff.toml`, `.flake8`, `.pylintrc`, `requirements.txt`

2. Run checks on modified files only:
   ```bash
   # Example: JS/TS
   npx eslint <modified-file>
   npx prettier --check <modified-file>
   
   # Example: Python
   ruff check <modified-file>
   black --check <modified-file>
   ```

3. Handle results:
   - Pass → proceed to commit
   - Fail → offer auto-fix on modified files only, or manual fix
   - No tools → inform and proceed

**Critical:** Only run checks configured in project. Never modify files user didn't change.

### 4. Generate Commit Message

```bash
git log --oneline -10  # Detect commit language from history
```

**Language detection:**
- Most commits in Chinese → use Chinese
- Most in English → use English
- Mixed → prefer recent commits' language

**Conventional Commits format:**
```
<type>(<scope>)[!]: <subject>

<body>
```

**Types:** `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`, `revert`

**Breaking changes:** Add `!` after type(scope): `<type>(<scope>)!`

**Guidelines:**
- Subject: max 50 chars, imperative mood
- Body: max 72 chars per line, explain "why" and "how"
- Footer: issue references or breaking changes

**Examples:**

Chinese:
```
feat(ui): 添加按钮组件

- 新增 ButtonPart 类型支持
- 实现 part-button 组件
```

English:
```
feat(ui): add button component

- Add ButtonPart type support
- Implement part-button component
```

Breaking change example:
```
feat(auth)!: change login method

Login now requires token instead of password
```

### 5. Commit and Push

```bash
git add .
git commit -m "<commit-message>"
git push -u origin <branch-name>
```

**Critical:** Never use `--force` or `-f` flag when pushing. If push fails due to conflicts, pull and rebase/merge instead.

## Example

**Scenario:** Adding a new button component

```bash
# 1. Stash and create branch
git stash push -m "temp: stash before creating branch"
git checkout main && git pull origin main
git checkout -b feat/add-button-component
git stash pop

# 2. Review changes
git diff
git diff --name-only  # Output: src/components/Button.tsx

# 3. Run checks on modified files only
npx eslint src/components/Button.tsx
npx prettier --check src/components/Button.tsx

# 4. Generate commit (detected Chinese from git log)
git log --oneline -10
git add .
git commit -m "feat(ui): 添加按钮组件

- 新增 ButtonPart 类型支持
- 实现 part-button 组件"

# 5. Push
git push -u origin feat/add-button-component
```

## Important Notes

- **Branch conflicts**: If branch exists, ask user: delete or use different name
- **Stash conflicts**: Resolve manually before committing
- **Main branch**: Prefer `main`, fallback to `master` if needed. Always pull latest code before creating new branch
- **Empty changes**: Notify user if no changes after stash pop
- **Formatting-only changes**: Ask user to confirm if detected
- **Code checks**: Only on modified files, only configured tools, never format untouched files
- **Remote branch**: Check if remote branch exists before pushing
- **Force push**: Never use `git push --force` or `git push -f`. If push fails, pull and rebase/merge instead

---
name: commit
description: Git Commit Generator - Generate standardized commit messages following Conventional Commits specification
allowed-tools:
  - Bash
  - Read
  - Glob
  - Grep
  - AskUserQuestion
---

# Commit Skill

Generate standardized git commit messages following the project's Conventional Commits specification.

## Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Type (Required)

Based on project history analysis, use the following types:

| Type | Description | Example |
|------|-------------|---------|
| `feat` | New feature | `feat: add user authentication` |
| `fix` | Bug fix | `fix: resolve login timeout issue` |
| `docs` | Documentation only | `docs: update API documentation` |
| `style` | Code style (formatting, semicolons, etc.) | `style: fix indentation` |
| `refactor` | Code refactoring (no feature change) | `refactor: extract validation logic` |
| `perf` | Performance improvement | `perf: optimize database queries` |
| `test` | Add or modify tests | `test: add unit tests for auth module` |
| `chore` | Build process or auxiliary tools | `chore: update dependencies` |
| `ci` | CI/CD configuration | `ci: add GitHub Actions workflow` |
| `build` | Build system changes | `build: upgrade webpack to v5` |

### Scope (Optional)

Scope indicates the affected module or area, enclosed in parentheses:

```
feat(devflow): add diff-review-doc skill
fix(auth): resolve token refresh issue
```

Common scopes in this project:
- Plugin names: `devflow`, `blocklet`, `arcblock-context`
- Skill names: `blocklet-dev-setup`, `blocklet-pr`
- Module names: specific functional modules

### Subject (Required)

- Use imperative mood: "add" not "added" or "adds"
- Lowercase first letter
- No period at the end
- Keep under 50 characters
- Describe what the commit does

**Good examples:**
- `feat: add blocklet-branch skill for branch management`
- `fix: resolve gh command order issue`
- `docs: update installation guide`

**Bad examples:**
- `feat: Added new feature.` (wrong tense, has period)
- `Fix bug` (missing type prefix)
- `feat: This commit adds a new feature that...` (too verbose)

### Body (Optional)

- Wrap at 72 characters
- Explain "what" and "why" vs "how"
- Separate from subject with blank line

### Footer (Optional)

- Reference issues: `Closes #123`
- Breaking changes: `BREAKING CHANGE: description`

## Workflow

When user requests to create a commit:

### Step 1: Check Current Status

```bash
git status
git diff --staged
git diff
```

### Step 2: Verify All Changes Are Staged

**IMPORTANT: If there are unstaged changes, use AskUserQuestion to confirm how to proceed.**

Check for unstaged changes:
- Modified files not staged (`Changes not staged for commit`)
- Untracked files (`Untracked files`)

If unstaged changes exist:
1. List all unstaged/untracked files
2. **Use AskUserQuestion tool** to ask user how to proceed:

```json
{
  "questions": [{
    "question": "There are unstaged changes. How would you like to proceed?",
    "header": "Unstaged",
    "options": [
      {"label": "Stage all", "description": "Run `git add .` to stage all changes"},
      {"label": "Abort", "description": "Cancel the commit and handle changes manually"}
    ],
    "multiSelect": false
  }]
}
```

3. If user selects "Stage all": run `git add .` then continue to Step 3
4. If user selects "Abort": stop the workflow and inform user to stage changes manually
5. **DO NOT proceed until all intended changes are staged**

### Step 3: Analyze Staged Changes

Only proceed if all changes are properly staged:
- Identify the type of change (feature, fix, docs, etc.)
- Determine the scope if applicable
- Summarize the change concisely

### Step 4: Generate and Confirm Commit Message

Generate the commit message following the format, then use **AskUserQuestion** tool to confirm:

```
Proposed commit message:

<type>(<scope>): <subject>

<body if needed>

Co-Authored-By: Claude <noreply@anthropic.com>
```

**Use AskUserQuestion tool** with options:
- `Approve` - Proceed to commit
- `Edit message` - User wants to modify the message
- `Cancel` - Abort the commit

Example AskUserQuestion usage:
```json
{
  "questions": [{
    "question": "Proceed with this commit message?",
    "header": "Commit",
    "options": [
      {"label": "Approve", "description": "Create the commit with this message"},
      {"label": "Edit message", "description": "Modify the commit message"},
      {"label": "Cancel", "description": "Abort the commit"}
    ],
    "multiSelect": false
  }]
}
```

### Step 5: Execute Commit (Only After User Confirmation)

```bash
git commit -m "$(cat <<'EOF'
<type>(<scope>): <subject>

<body if needed>

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

### Step 6: Verify Commit

```bash
git log -1 --oneline
```

## Examples from Project History

```
feat: parse blocklet urls from dev output instead of constructing from did
feat: add blocklet-branch skill for branch management
feat: enhance blocklet-server-dev-setup skill with GitHub CLI authentication guidance
feat(devflow): add diff-review-doc skill (#1)
fix: gh move top
docs: prefer git URL format for marketplace installation
chore: initial commit
chore: cleanup hello world plugin
```

## Rules

1. **Always use English** for commit messages
2. **Always use lowercase** type prefix
3. **Always use imperative mood** in subject
4. **Never end subject with period**
5. **Add Co-Authored-By** footer when AI generates the commit
6. **Keep subject under 50 characters** when possible
7. **Reference PR/Issue numbers** when applicable: `(#123)`

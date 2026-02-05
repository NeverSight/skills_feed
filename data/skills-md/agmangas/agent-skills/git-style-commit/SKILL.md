---
name: git-style-commit
description: Analyze git history for commit style, stage changes, and commit without pushing. Use when the user wants to commit changes with a message that matches their repository's existing commit style, or when they ask to commit staged/unstaged changes.
---

# Git Style-Aware Commit

This skill analyzes your repository's commit history to identify the prevailing commit message style, then stages changes and creates a commit with a message that matches that style.

## When to Use This Skill

- Committing changes with a message that matches repository conventions
- Staging and committing files (specific files or all changes)
- Ensuring commit messages follow team/project standards
- Automating commit creation while respecting existing style patterns

## How to Use

### Basic Usage

```
Commit these changes
```

```
Stage and commit src/utils.ts
```

```
Commit all changes matching the repo style
```

### With Specific Files

```
Commit FILES="src/components/Button.tsx src/styles/button.css"
```

## Instructions

When a user requests to commit changes:

### 1. Analyze Commit Style

Run `git log -n 10 --pretty=format:"%s"` to review the last 10 commit messages.

Identify the prevailing style pattern:
- **Conventional Commits**: `feat:`, `fix:`, `chore:`, `docs:`, etc.
- **Capitalization**: Sentence case, title case, or lowercase
- **Tense**: Present tense ("Add feature") or past tense ("Added feature")
- **Emoji usage**: Presence and type of emojis (🎨, ✨, 🐛, etc.)
- **Format**: Single line vs multi-line with body
- **Prefixes/suffixes**: Any consistent prefixes or suffixes

**Example patterns to detect:**
- `feat: add user authentication` (Conventional Commits, lowercase)
- `Fix bug in login flow` (No prefix, title case, present tense)
- `✨ Add dark mode toggle` (Emoji prefix, title case)
- `[API] Update endpoint documentation` (Bracket prefix, title case)

### 2. Stage Changes

**If specific files are provided via `FILES` argument:**
```bash
git add $FILES
```

**Otherwise, stage all changes:**
```bash
git add -A
```

**Then review what will be committed:**
```bash
git diff --staged
# or
git diff --cached
```

Analyze the staged changes to understand:
- What files were modified
- What types of changes (additions, deletions, modifications)
- The scope and nature of the changes

### 3. Generate Commit Message

Draft a single, concise commit message that:
- Accurately describes the staged changes
- **CRITICALLY**: Matches the style pattern identified in step 1

**Style matching examples:**

If history shows Conventional Commits:
```
feat: add user profile editing
fix: resolve memory leak in cache
chore: update dependencies
```

If history shows emoji prefixes:
```
✨ Add user profile editing
🐛 Fix memory leak in cache
📦 Update dependencies
```

If history shows no prefix, title case:
```
Add user profile editing
Fix memory leak in cache
Update dependencies
```

**Message generation guidelines:**
- Keep it concise (ideally under 72 characters for the subject line)
- Use the same tense as the repository pattern
- Match capitalization style exactly
- Include the same prefix/emoji pattern if present
- Focus on what changed, not why (unless the style includes "why")

### 4. Commit

Run the commit with the generated message:
```bash
git commit -m "YOUR_GENERATED_MESSAGE"
```

### 5. Safety Constraint

**DO NOT PUSH**. Stop immediately after the commit is created.

Print the final commit message used for user verification:
```
✅ Committed with message: "feat: add user profile editing"
```

## Examples

### Example 1: Conventional Commits Style

**Repository history:**
```
feat: add authentication middleware
fix: resolve CORS issue
docs: update API documentation
chore: bump version to 1.2.0
```

**Staged changes:** Added new `Button.tsx` component

**Generated message:** `feat: add Button component`

### Example 2: Emoji Style

**Repository history:**
```
✨ Add dark mode support
🐛 Fix login redirect loop
📝 Update README
```

**Staged changes:** Fixed bug in form validation

**Generated message:** `🐛 Fix form validation bug`

### Example 3: Simple Title Case

**Repository history:**
```
Add user dashboard
Fix API timeout issue
Update dependencies
```

**Staged changes:** Modified `utils.ts` to add helper functions

**Generated message:** `Add helper functions to utils`

### Example 4: Bracket Prefix Style

**Repository history:**
```
[Frontend] Add responsive navigation
[Backend] Fix database connection pool
[Docs] Update installation guide
```

**Staged changes:** Updated API endpoint in `api/users.ts`

**Generated message:** `[Backend] Update users API endpoint`

## Common Patterns

### Conventional Commits
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `style:` - Code style changes (formatting, missing semicolons, etc.)
- `refactor:` - Code refactoring
- `test:` - Adding or updating tests
- `chore:` - Maintenance tasks, dependency updates

### Emoji Patterns
- 🎨 - Code style/formatting
- ✨ - New feature
- 🐛 - Bug fix
- 📝 - Documentation
- 🔥 - Remove code/files
- 💚 - Fix tests
- 🚀 - Performance improvements
- 🔒 - Security fixes

## Error Handling

**If no commit history exists:**
- Use a default style (Conventional Commits with `feat:` or `fix:` based on change type)
- Inform the user: "No commit history found, using Conventional Commits format"

**If staging fails:**
- Check if files exist: `git status`
- Report specific error to user
- Do not proceed with commit

**If commit fails:**
- Check for empty staging area: `git diff --staged` should show changes
- Verify git repository is initialized
- Report error and do not retry automatically

## Best Practices

1. **Always analyze style first** - Don't assume a style pattern
2. **Match exactly** - If history uses lowercase, use lowercase; if it uses title case, use title case
3. **Be descriptive** - The message should clearly indicate what changed
4. **Respect scope** - If Conventional Commits are used, include appropriate scope: `feat(auth): add login`
5. **Never push** - This skill only creates commits, never pushes them

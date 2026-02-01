---
name: commit
description: Commits with perfect messages. Use when making a commit.
---

# Git Commit Command

Create atomic git commits following Conventional Commits.

## Flow

1. **Check state:** `git status --porcelain`
   - Empty → STOP, report "No changes to commit"
   - Merge conflict markers → STOP, report conflict

2. **Verify .gitignore** excludes: secrets/`.env`, build artifacts, OS files (`.DS_Store`), IDE configs

3. **Stage:** `git add -A` (or specific files for atomic commits)

4. **Analyze:** `git diff --cached --stat` and `git diff --cached`
   - If unrelated changes exist, split into separate commits via `git reset HEAD <file>`

5. **Commit:** Use Conventional Commits format

```
<type>(<scope>): <summary>

[body: what/why, wrap 72 chars]

[footer: BREAKING CHANGE: or Fixes #123]
```

**Types:** `feat` | `fix` | `docs` | `style` | `refactor` | `perf` | `test` | `build` | `ci` | `chore`

**Summary rules:** imperative mood (e.g., "add", "fix", "refactor"), lowercase, no period, max 72 chars

6. **Confirm:** `git log -1 --oneline` → report hash and summary

## Output

Success: `Committed: <hash> <type>(<scope>): <summary>`
Failure: explain why and required action

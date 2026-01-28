---
name: git-master
description: "Git expert for atomic commits, rebase/squash, and history search (blame, bisect, log -S). Triggers on: commit, rebase, squash, who wrote, when was X added, find the commit that."
allowed-tools:
  - Bash(git:*)
---

# Git Master

Git expert combining: atomic commits, history rewriting, and archaeology.

## Mode Detection

| Request | Mode |
|---------|------|
| commit, changes to commit | COMMIT |
| rebase, squash, cleanup history | REBASE |
| find when, who changed, git blame, bisect | HISTORY |

---

## COMMIT MODE

### Arguments

- `description` (optional): What the commit should accomplish
- `files` (optional): Specific files to commit (defaults to all local changes)

### Step 1: Gather Context (Parallel)

```bash
git status --short
git diff --staged --stat
git diff --stat
git log --oneline -20
git branch --show-current
```

Analyze:
- What files have changed and why
- The project's existing commit message style
- Whether changes span multiple logical concerns

### Step 2: Filter Unwanted Files

**Auto-exclude (silently skip):**
- OS files: `.DS_Store`, `Thumbs.db`, `Desktop.ini`
- Editor artifacts: `.idea/`, `.vscode/` (unless tracked), `*.swp`, `*~`
- Ephemeral files: `*.log`, `*.tmp`, `*.cache`
- Common ignores: `node_modules/`, `__pycache__/`, `dist/`, `build/`

**Auto-exclude with warning:**
- Secrets: `.env*`, `credentials.*`, `*.pem`, `*.key`, API keys/tokens
- Large binary files not typically versioned

**Ask user before including:**
- New file types not seen in git history
- Files with suspicious patterns (hardcoded passwords, connection strings)
- Uncommonly large files

When in doubt, ask. When certain it's unwanted, exclude silently.

### Step 3: Detect Commit Style

Analyze `git log --oneline -20`:
- If most commits match `type:` or `type(scope):` → use **conventional commits**
- Otherwise → **follow the existing pattern**
- If no clear pattern or new repo → **default to conventional commits**

### Step 4: Plan Commits

**Single commit is appropriate when:**
- All changes form one logical unit
- Files are tightly coupled (implementation + test)
- Splitting would break the build or lose meaning

**Split into multiple commits when:**
- Changes serve different purposes (refactor AND bug fix)
- Different features/fixes mixed together
- Changes can be meaningfully reverted independently

**Always pair:** Implementation file + its test file = same commit

### Step 5: Execute

```bash
git add <files>
git commit -m "<message matching detected style>"
```

If user provided a description, incorporate it into the commit message.
If user provided specific files, only commit those files.

**Never** mention the agent (Claude, AI, etc.) in commit messages or as author.

### Step 6: Verify

```bash
git status
git log --oneline -5
```

### Commit Message Guidelines

- Use imperative mood ("Add feature" not "Added feature")
- First line: 50 chars or less, summarizes the change
- Body (if needed): Explain WHY, not WHAT (the diff shows what)
- Reference issues if applicable: `Fixes #123`

---

## REBASE MODE

### Safety Check

| Condition | Action |
|-----------|--------|
| On main/master | **ABORT** - never rebase |
| Dirty working directory | `git stash push -m "pre-rebase"` |
| Pushed commits | Warn about force-push |

### Operations

**Squash all into one:**
```bash
MERGE_BASE=$(git merge-base HEAD main 2>/dev/null || git merge-base HEAD master)
git reset --soft $MERGE_BASE
git commit -m "Combined: <summary>"
```

**Autosquash fixups:**
```bash
MERGE_BASE=$(git merge-base HEAD main 2>/dev/null || git merge-base HEAD master)
GIT_SEQUENCE_EDITOR=: git rebase -i --autosquash $MERGE_BASE
```

**Rebase onto main:**
```bash
git fetch origin
git rebase origin/main
```

### Conflict Resolution

1. `git status` - find conflicting files
2. Edit files, remove conflict markers
3. `git add <resolved>`
4. `git rebase --continue`
5. If stuck: `git rebase --abort`

### Push After Rebase

```bash
git push --force-with-lease origin <branch>
```

---

## HISTORY MODE

### Find When Code Was Added/Removed

```bash
git log -S "searchString" --oneline
git log -S "searchString" -p              # with diff
git log -S "searchString" -- path/file    # specific file
git log -S "searchString" --all           # all branches
```

### Find Commits Touching Pattern

```bash
git log -G "regex.*pattern" --oneline
```

### Who Wrote This Line

```bash
git blame path/to/file
git blame -L 10,20 path/to/file    # lines 10-20
git blame -w path/to/file          # ignore whitespace
```

### Find Bug Introduction (Bisect)

```bash
git bisect start
git bisect bad                     # current is broken
git bisect good v1.0.0             # this version worked
# test each checkout, then:
git bisect good  # or  git bisect bad
# repeat until found
git bisect reset                   # when done
```

**Automated:**
```bash
git bisect start
git bisect bad HEAD
git bisect good v1.0.0
git bisect run ./test-script.sh
```

### File History

```bash
git log --oneline -- path/to/file
git log --follow --oneline -- path/to/file  # across renames
```

---

## Quick Reference

| Goal | Command |
|------|---------|
| When was X added? | `git log -S "X" --oneline` |
| Who wrote line N? | `git blame -L N,N file` |
| When did bug start? | `git bisect start && git bisect bad && git bisect good <tag>` |
| File history | `git log --follow -- path/file` |
| Squash branch | `git reset --soft $(git merge-base HEAD main) && git commit` |
| Apply fixups | `GIT_SEQUENCE_EDITOR=: git rebase -i --autosquash <base>` |

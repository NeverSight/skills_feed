---
name: commit-splitter
description: Split large sets of uncommitted changes into logical, well-organized commits. Use when the user has many uncommitted changes and wants structured commits, or proactively suggest when detecting a large diff that would benefit from splitting.
---

# Structured Git Commits

## Workflow

### 1. Safety stash
```bash
git stash push -m "save before structured commit: <brief description>" --include-untracked
git stash apply
```
Keep changes applied throughout. Do NOT re-stash between commits. Only drop the safety stash at the very end.

### 2. Survey and number hunks

Generate patches for all modified files and list their hunks.
**Quote paths with special characters** (brackets, spaces, etc.):
```bash
git diff "<file>" > /tmp/<file>.patch
.claude/skills/commit-splitter/scripts/extract-hunks.py /tmp/<file>.patch --list
```

This outputs numbered hunks:
```
Hunks (3 total):
  1: @@ -10,6 +10,7 @@ def foo():  (+1/-0) print("perf log")...
  2: @@ -25,4 +26,6 @@ def bar():  (+2/-0) import threading...
  3: @@ -50,3 +53,4 @@ def baz():  (+1/-0) min_containers=1...
```

### 3. Propose commit plan with hunk numbers

Reference hunks by number in the plan:
```
modal_app.py:
  Hunk 1: perf logging
  Hunk 2: async threading
  Hunk 3: min_containers=1

Commit 1: "perf: add logging" - modal_app.py hunks 1
Commit 2: "perf: async + min_containers" - modal_app.py hunks 2,3
```

### 4. Execute commits

**CRITICAL: Follow the approved plan exactly.** Never combine commits because splitting "seems hard."

**NEVER use these shortcuts:**
- `git checkout` to reset files then re-edit them
- Direct file editing (Edit/Update tools) on source files
- Combining commits because changes are "interleaved"
- `Write` tool or heredocs to create patches

**Whole files:** just `git add <file>`

**New files:** just `git add <file>`

**Partial files (specific hunks):**
```bash
.claude/skills/commit-splitter/scripts/extract-hunks.py /tmp/<file>.patch <hunk_numbers> > /tmp/commit.patch
git apply --cached /tmp/commit.patch
```

Example:
```bash
# Commit 1: just perf logging (hunk 1)
.claude/skills/commit-splitter/scripts/extract-hunks.py /tmp/modal_app.patch 1 > /tmp/commit1.patch
git apply --cached /tmp/commit1.patch
git commit -m "perf: add logging"

# Commit 2: async + min_containers (hunks 2,3)
.claude/skills/commit-splitter/scripts/extract-hunks.py /tmp/modal_app.patch 2,3 > /tmp/commit2.patch
git apply --cached /tmp/commit2.patch
git commit -m "perf: async and min_containers"
```

After each commit, verify with `git diff --cached --stat`.

### 5. extract-hunks.py reference

Location: `.claude/skills/commit-splitter/scripts/extract-hunks.py`

```bash
# List hunks with summaries
.claude/skills/commit-splitter/scripts/extract-hunks.py file.patch --list

# Extract specific hunks
.claude/skills/commit-splitter/scripts/extract-hunks.py file.patch 1,3,5      # hunks 1, 3, 5
.claude/skills/commit-splitter/scripts/extract-hunks.py file.patch 2-4        # hunks 2, 3, 4
.claude/skills/commit-splitter/scripts/extract-hunks.py file.patch 1,3-5,7    # mixed
```

The script outputs a valid patch to stdout. Redirect to a file, then `git apply --cached`.

### Recovery

If something goes wrong:
- `git reset HEAD` to unstage
- `git stash list` to find safety stash
- `git checkout -- <file>` then `git stash apply` to restore a file

After all commits succeed:
- `git stash drop` to remove safety stash

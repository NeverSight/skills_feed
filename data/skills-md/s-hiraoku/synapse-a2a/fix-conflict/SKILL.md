---
name: fix-conflict
description: Automatically resolve merge conflicts in the current PR. Fetches the base branch, attempts a merge, identifies conflicting files, analyzes both sides, resolves conflicts, verifies locally, and pushes. Use when PR has merge conflicts detected by poll-pr-status.sh.
---

# Fix Merge Conflicts

This skill automatically resolves merge conflicts for the current PR by fetching the base branch, performing a test merge, analyzing conflicting files, and applying resolutions.

## Usage

```
/fix-conflict           # Auto-resolve merge conflicts
/fix-conflict --dry-run # Show conflicts without resolving
```

## Workflow

### Step 1: Determine PR and Base Branch

Get the current branch and PR details:

```bash
git rev-parse --abbrev-ref HEAD
```

```bash
gh pr view --json baseRefName,number,url -q '{base: .baseRefName, number: .number, url: .url}'
```

If no PR exists, report "No PR found for the current branch. Nothing to resolve." and stop.

### Step 2: Fetch Latest Remote State

```bash
git fetch origin
```

### Step 3: Attempt Test Merge

Start a non-committing merge to identify conflicts:

```bash
git merge --no-commit --no-ff "origin/<base-branch>"
```

If the merge completes without conflicts:
- Run `git merge --abort` to undo the test merge
- Report "No merge conflicts detected. The PR is mergeable." and stop.

If the merge fails with conflicts, proceed to the next step.

### Step 4: Identify Conflicting Files

```bash
git diff --name-only --diff-filter=U
```

This lists all files with unresolved conflicts.

For each conflicting file, check if it's a binary file:

```bash
file <path>
```

If binary files have conflicts:
- Abort the merge: `git merge --abort`
- Report "Binary file conflicts detected in: <files>. These require manual resolution." and stop.

### Step 5: Resolve Conflicts

For each conflicting file:

1. Read the entire file to see the conflict markers (`<<<<<<<`, `=======`, `>>>>>>>`)
2. Understand the changes from **both sides**:
   - The current branch's changes (between `<<<<<<<` and `=======`)
   - The base branch's changes (between `=======` and `>>>>>>>`)
3. Determine the correct resolution:
   - If both sides modify different parts of the same function: keep both changes
   - If both sides modify the same lines: analyze the intent and merge logically
   - If one side adds new code and the other modifies existing: keep both
   - If changes are contradictory: prefer the current branch's intent (it's newer work)
4. Remove all conflict markers and write the resolved content
5. Stage the resolved file: `git add <file>`

**Important constraints:**
- Never blindly choose one side — always analyze both changes
- Preserve formatting and style consistency
- If a conflict is too complex to resolve confidently (e.g., large architectural changes on both sides), abort and report for manual resolution

If `--dry-run` flag is provided: show each conflict with both sides and the proposed resolution, but do NOT modify files, commit, or push.

### Step 6: Local Verification

After resolving all conflicts, verify the merge is clean:

```bash
ruff check synapse/ tests/
```

```bash
ruff format synapse/ tests/ --check
```

```bash
pytest
```

If any check fails:
- Attempt one targeted fix for the issue
- If it still fails, abort the merge and report what went wrong

### Step 7: Complete Merge and Push

```bash
git commit -m "merge: resolve conflicts with <base-branch>"
```

```bash
git push
```

Report a summary:
- Number of files with conflicts resolved
- List of resolved files
- Whether all local checks pass

### Step 8: Error Handling

- **Abort on failure**: If resolution fails at any point, always run `git merge --abort` to return to a clean state
- **Binary conflicts**: Report and stop — do not attempt to resolve binary files
- **Too many conflicts** (>10 files): Report and suggest manual resolution
- **Max 1 attempt**: This skill attempts resolution once. If it fails, manual intervention is needed
- **Never force-push**: Always use `git push`, never `git push --force`

## Safety

- The test merge (`--no-commit --no-ff`) ensures we can always abort cleanly
- `git merge --abort` is the escape hatch at every step
- Local verification (ruff, pytest) before pushing ensures we don't push broken code
- Binary files are never auto-resolved

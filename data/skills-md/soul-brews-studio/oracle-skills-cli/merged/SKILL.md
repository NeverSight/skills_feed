---
name: merged
description: Post-Merge Cleanup. Switch to main, pull latest, delete merged branch. Use after PR is merged.
---

# /merged - Post-Merge Cleanup

> "Clean up after the merge."

After your PR is merged, this skill handles the cleanup: switch to main, pull latest, delete the merged branch.

## Usage

```
/merged              # Cleanup current merged branch
```

## Steps

### Step 1: Get current branch name

```bash
BRANCH=$(git branch --show-current)
echo "Current branch: $BRANCH"
```

If already on `main` or `master`, stop — nothing to clean up.

### Step 2: Switch to main and pull

```bash
git checkout main
git pull origin main
```

### Step 3: Delete the merged feature branch

```bash
# Delete local branch
git branch -d $BRANCH

# Delete remote branch (if it still exists)
git push origin --delete $BRANCH 2>/dev/null || echo "Remote branch already deleted"
```

### Step 4: Confirm cleanup

```bash
echo "✅ Cleanup complete"
git branch -a | head -10
git log --oneline -3
```

---

## Output

```markdown
## ✅ Post-Merge Cleanup

- Switched to: `main`
- Pulled latest: [commit hash]
- Deleted branch: `[branch-name]`
- Ready for next task

**Latest commits on main:**
- [hash] [message]
- [hash] [message]
- [hash] [message]
```

---

## When to Use

After your PR is merged on GitHub:

```
PR merged on GitHub
        ↓
/merged
        ↓
✅ Back on main, branch cleaned up
```

---

## Safety

- Uses `git branch -d` (safe delete) — won't delete unmerged branches
- Checks if remote branch exists before deleting
- Won't run if already on main

---

ARGUMENTS: $ARGUMENTS

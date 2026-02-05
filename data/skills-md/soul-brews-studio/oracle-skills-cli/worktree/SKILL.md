---
name: worktree
description: Git worktree for parallel work. Use when user says "worktree", "parallel work", "new agent", "start parallel".
---

# /worktree

Manage git worktrees for parallel agent work.

## Usage

```
/worktree              # List all worktrees
/worktree new          # Create next agents/N
/worktree <N>          # Show path to agents/N
/worktree remove <N>   # Remove agents/N worktree
```

---

## Step 0: Parse Arguments

```
ARGUMENTS: $ARGUMENTS
```

- No args, `list`, or `status` → **List with Status**
- `new` → **Create New**
- Number (1, 2, 3...) → **Show Path**
- `remove N` → **Remove**

---

## List Worktrees (default)

Aliases: `/worktree`, `/worktree list`, `/worktree status`

Just run:

```bash
git worktree list
```

Output is already clean and readable:
```
/path/to/repo         abc1234 [main]
/path/to/repo.wt-1    def5678 [agents/1]
/path/to/repo.wt-2    ghi9012 [agents/2]
```

---

## Create New Agent Worktree

When user says `/worktree new`:

Worktrees are created as **siblings** (not nested) to avoid VS Code indexing issues:

```bash
# Get repo name and parent dir
REPO_NAME=$(basename $(pwd))
PARENT_DIR=$(dirname $(pwd))

# Find next available number
NEXT=1
while [ -d "$PARENT_DIR/$REPO_NAME.wt-$NEXT" ]; do
  NEXT=$((NEXT + 1))
done

WT_PATH="$PARENT_DIR/$REPO_NAME.wt-$NEXT"

# Create worktree with new branch
git worktree add "$WT_PATH" -b agents/$NEXT

# Report
echo "Created: $WT_PATH"
echo "Branch: agents/$NEXT"
```

**After creating, display prominently:**

```
Worktree Created

  Path:   /path/to/repo.wt-1
  Branch: agents/1

Open in VS Code: code /path/to/repo.wt-1
```

**Structure:**
```
parent/
├── repo/           # main (this workspace)
├── repo.wt-1/      # branch: agents/1
└── repo.wt-2/      # branch: agents/2
```

---

## Show Agent Path

When user says `/worktree N` (where N is a number):

```bash
REPO_NAME=$(basename $(pwd))
PARENT_DIR=$(dirname $(pwd))
WT_PATH="$PARENT_DIR/$REPO_NAME.wt-$N"

if [ -d "$WT_PATH" ]; then
  echo "Path: $WT_PATH"
  echo "Branch: agents/$N"
  echo ""
  echo "Open: code $WT_PATH"
else
  echo "Worktree $N not found. Use /worktree new to create."
fi
```

---

## Remove Agent Worktree

When user says `/worktree remove N`:

```bash
REPO_NAME=$(basename $(pwd))
PARENT_DIR=$(dirname $(pwd))
WT_PATH="$PARENT_DIR/$REPO_NAME.wt-$N"

# Remove the worktree
git worktree remove "$WT_PATH"

# Optionally delete the branch
git branch -d agents/$N
```

**Confirm before removing** - ask user if they want to also delete the branch.

---

## Philosophy

- **Flat sibling worktrees** - `repo.wt-1`, `repo.wt-2` as direct siblings
- **Each agent = own branch + directory** - Open as separate workspace
- **Use `git -C path`** not cd - respect worktree boundaries
- **Sync via PR to main** - never force push
- **Nothing is deleted** - branches can be recovered

---

## Quick Reference

| Command | Result |
|---------|--------|
| `/worktree` | List all worktrees |
| `/worktree new` | Create `repo.wt-N` with branch `agents/N` |
| `/worktree 1` | Show path to `repo.wt-1` |
| `/worktree remove 2` | Remove `repo.wt-2` |

---

## Self-Validation

**After completing any action, verify your work:**

### After `/worktree new`

```bash
# 1. Check directory exists
ls -la "$WT_PATH"

# 2. Check branch exists
git branch --list "agents/$NEXT"

# 3. Check git worktree registered
git worktree list | grep "wt-$NEXT"
```

**Expected:**
- [ ] Directory `repo.wt-N` exists as sibling (not nested)
- [ ] Branch `agents/N` was created
- [ ] `git worktree list` shows the new entry
- [ ] Displayed path + VS Code command to user

### After `/worktree remove N`

```bash
# 1. Check directory removed
[ ! -d "$WT_PATH" ] && echo "✓ Directory removed"

# 2. Check worktree unregistered
git worktree list | grep -v "wt-$N"
```

**Expected:**
- [ ] Directory no longer exists
- [ ] `git worktree list` no longer shows entry
- [ ] Asked user about branch deletion

### Dry-Run Test (without creating)

```bash
# Preview what would happen
REPO_NAME=$(basename $(pwd))
PARENT_DIR=$(dirname $(pwd))
NEXT=1
while [ -d "$PARENT_DIR/$REPO_NAME.wt-$NEXT" ]; do
  NEXT=$((NEXT + 1))
done
echo "Would create: $PARENT_DIR/$REPO_NAME.wt-$NEXT"
echo "Would branch: agents/$NEXT"
git worktree list
```

Use this to validate logic before actual execution.

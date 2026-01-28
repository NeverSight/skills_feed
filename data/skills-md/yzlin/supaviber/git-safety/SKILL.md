---
name: git-safety
description: Apply critical git safety protocols before any git operations, especially in collaborative environments. Use when performing git commands, managing files, or making destructive changes.
license: MIT
compatibility: Works with Claude Code and OpenAI Codex. Requires git CLI access.
metadata:
  category: version-control
  tags: git, safety, collaboration, destructive-operations
  version: "1.0.0"
---

# Git Safety Skill

Apply rigorous git safety protocols to prevent data loss and conflicts in collaborative development environments, particularly when multiple agents or developers work concurrently.

## Core Safety Principles

### File Management Rules

**Deleting Files:**
- ⚠️ **STOP before deleting any file to resolve type/lint failures** - Ask the user first
- Only remove obsolete files when changes make them genuinely irrelevant
- Only revert your own work or changes explicitly requested by the user
- **Coordinate with teammates before removing in-progress edits**
- Never assume a file is safe to delete without confirmation

**File Modifications:**
- Always verify file ownership and recent changes before modifying
- Check `git log <file>` to see who last edited
- Communicate before making sweeping changes to shared files

### Environment & Configuration Safety

**Critical: Environment Files**
- 🚫 **NEVER edit `.env` or any environment variable files**
- Only the user may change environment configurations
- This includes `.env`, `.env.local`, `.env.production`, etc.
- If environment changes are needed, inform the user - never make them yourself

**Git Configuration:**
- Never modify `.gitconfig` or repository git settings
- Never amend commits without explicit written approval
- Preserve existing git hooks and configurations

## Destructive Operations - Extreme Caution Required

### Absolutely Forbidden Without Explicit Permission

🚨 **ABSOLUTELY NEVER run these operations unless the user gives explicit, written instruction:**

- `git reset --hard` - Destroys uncommitted work permanently
- `git checkout <old-commit>` - Can lose current work
- `git restore --source=<old-commit>` - Reverts to old state, losing changes
- `rm -rf` - Irreversible file deletion
- `git push --force` - Overwrites remote history
- `git rebase` without safeguards - Can lose commits
- `git clean -fd` - Deletes untracked files permanently

### What Requires User Approval

Before running these commands, **STOP and ask the user explicitly:**

1. Any command that can lose uncommitted changes
2. Force pushing to remote repositories
3. Rebasing published branches
4. Amending pushed commits
5. Deleting branches (local or remote)
6. Hard resets of any kind
7. File deletions to fix build errors

## Safe Workflow Standards

### Before Any Commit

**Pre-commit Checklist:**
1. Run `git status` to verify exactly what's being committed
2. Use explicit file paths - never `git add .` or `git add -A` blindly
3. Ensure only modified/intended files are staged
4. Review diffs with `git diff --staged`
5. Keep commits atomic (focused on one logical change)

**Example - Safe Commit:**
```bash
# Good: Explicit, verified, atomic
git status
git add src/components/Button.tsx src/components/Button.test.tsx
git diff --staged
git commit -m "feat: add disabled state to Button component"
```

**Example - Unsafe Commit:**
```bash
# Bad: No verification, adds everything
git add .
git commit -m "fixes"
```

### Path Handling

**Quote Special Characters:**
- Always quote paths with brackets, parentheses, or spaces
- Use double quotes to prevent shell interpretation

```bash
# Good
git add "src/utils/parse(data).ts"
git add "src/components/[id].tsx"

# Bad - shell may misinterpret
git add src/utils/parse(data).ts
git add src/components/[id].tsx
```

### Rebase Safety

When rebasing is necessary:

```bash
# Suppress editor prompts
GIT_SEQUENCE_EDITOR=true git rebase <branch>

# Or set environment variable
export GIT_SEQUENCE_EDITOR=true
git rebase main
```

## Coordination in Collaborative Environments

### Before Major Changes

**Communication First:**
1. Check who else is working on related files: `git log --since="1 day ago" --oneline`
2. Announce intention to make sweeping changes
3. Wait for confirmation before proceeding
4. Coordinate timing of force pushes or rebases

### Conflict Prevention

**Proactive Coordination:**
- Pull frequently: `git pull --rebase`
- Communicate when working on shared files
- Use feature branches to isolate work
- Merge main frequently to stay current

## Decision Tree for Destructive Operations

```
Are you about to run a destructive git command?
├─ YES → Is there explicit written user approval?
│   ├─ YES → Proceed carefully, verify twice
│   └─ NO → STOP. Ask user for permission first.
└─ NO → Proceed with normal safety checks
```

## Common Scenarios

### Scenario 1: Type Error in File

**Wrong Approach:**
```bash
# ❌ Delete file to fix error
rm src/components/BrokenComponent.tsx
```

**Right Approach:**
```bash
# ✅ Stop and ask user
# "I see a type error in BrokenComponent.tsx.
# Should I fix the error or is this file obsolete?"
```

### Scenario 2: Need to Reset Changes

**Wrong Approach:**
```bash
# ❌ Hard reset without asking
git reset --hard HEAD
```

**Right Approach:**
```bash
# ✅ Ask first, then use safer methods
git stash  # Preserves work
# OR
git checkout -b backup-branch  # Creates backup
```

### Scenario 3: Multiple Agents Working

**Wrong Approach:**
```bash
# ❌ Force push over teammate's work
git push --force
```

**Right Approach:**
```bash
# ✅ Coordinate first
# "I need to force push to fix history.
# Is anyone else working on this branch?"
```

## Safety Verification Commands

**Before Destructive Operations:**

```bash
# Check what will be affected
git status
git log --oneline -n 10
git diff HEAD

# See who's been working recently
git log --since="1 day ago" --all --oneline

# Check remote status
git fetch
git status
```

## Environment File Protection

**Files to NEVER modify:**
- `.env`
- `.env.local`
- `.env.development`
- `.env.production`
- `.env.test`
- Any file matching `.env.*`

**If environment changes are needed:**
1. Stop immediately
2. Inform the user exactly what needs to change
3. Let the user make the modification
4. Never assume or guess environment values

## Summary - The Golden Rules

1. 🛑 **STOP before deleting files** to fix build errors
2. 🚫 **NEVER touch environment files** - user only
3. ⚠️ **Get explicit permission** for destructive git operations
4. ✅ **Verify with git status** before every commit
5. 📝 **Use explicit paths** - never blindly add all files
6. 🔒 **Quote special characters** in file paths
7. 🤝 **Coordinate with teammates** before major changes
8. 💾 **When in doubt, ask** - communication over assumption

## When This Skill Applies

Invoke this skill when:
- About to run any git command
- Considering deleting a file
- Planning to modify shared files
- Encountering build/type errors that might be "fixed" by deletion
- Working in an environment where others might be active
- Unsure if an operation is safe

**Default stance: Cautious and communicative. Preserve work, ask questions, coordinate changes.**

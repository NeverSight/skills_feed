---
name: rebase
description: Guide for rebasing feature branches onto main in the Fusion Framework monorepo, including handling pnpm-lock.yaml conflicts
---

# Rebase Skill (Fusion Framework)

This skill helps you rebase feature branches onto the latest `main` branch, handling common conflicts in a pnpm monorepo.

## Overview

When rebasing a feature branch, you'll often encounter conflicts in `pnpm-lock.yaml` due to parallel dependency changes. The correct approach is to regenerate the lockfile rather than manually resolving conflicts.

## Standard Rebase Workflow

### 1. Prepare for rebase

```bash
# Navigate to your worktree or branch
cd /path/to/worktree

# Ensure you're on the correct branch
git branch

# Fetch latest changes from origin (including main)
git fetch origin
git fetch origin main:refs/remotes/origin/main
```

### 2. Start the rebase

```bash
# Rebase your branch onto the latest main
git rebase origin/main
```

### 3. Handle pnpm-lock.yaml conflicts

**CRITICAL: When `pnpm-lock.yaml` has conflicts during rebase:**

```bash
# Regenerate it from package.json files
pnpm install

# Stage the regenerated lockfile
git add pnpm-lock.yaml

# Continue the rebase
git rebase --continue
```

### 4. Handle "Version Packages" commit conflicts

**When you encounter a "Version Packages (next)" commit with conflicts:**

This happens when your feature branch has pre-release versions (e.g., `2.0.0-next.0`) but main has been updated with newer regular versions.

**Resolution strategy:**
- **package.json**: Use `--ours` (HEAD version from main)
- **CHANGELOG.md**: Use `--ours` (HEAD changelog from main)

```bash
# For all package.json conflicts, keep HEAD version
git checkout --ours "packages/*/package.json"
git add "packages/*/package.json"

# For all CHANGELOG.md conflicts, keep HEAD changelog  
git checkout --ours "packages/*/CHANGELOG.md"
git add "packages/*/CHANGELOG.md"

# Also check other affected files
git checkout --ours "vue-press/package.json" 2>/dev/null || true
git add "vue-press/package.json" 2>/dev/null || true

# Continue the rebase
git rebase --continue
```

**Why?** The main branch has the authoritative versions and changelogs. Your feature branch's pre-release versions will be regenerated when you create a new changeset after rebasing.

### 5. Handle other conflicts

For conflicts in source files (`.ts`, `.tsx`, etc.):

```bash
# Manually resolve conflicts in the files
# Then stage the resolved files
git add path/to/resolved-file.ts

# Continue the rebase
git rebase --continue
```

### 6. Complete the rebase

After all commits are rebased successfully:

```bash
# Verify the branch is clean
git status

# Force push to update the remote branch
git push --force-with-lease origin YOUR_BRANCH_NAME
```

### 7. Align pre.json initial versions (if in pre mode)

If `.changeset/pre.json` exists (pre-release mode), align `initialVersions` to current package versions for packages changed by the rebase:

```bash
# From repo root
node .github/skills/rebase/scripts/align-pre-initial-versions.cjs
```

What it does:
- Reads `.changeset/pre.json` to get the `tag` (e.g., `next`)
- Updates `initialVersions` when the current package version does NOT end with `-TAG.NUMBER` (e.g., `2.0.0` or `2.1.0`)
- Skips entries where the current version ends with `-TAG.NUMBER` (e.g., `2.0.0-next.0`), preserving ongoing pre state

### 8. Sanity check vs remote

Before pushing, verify local rebase result against the remote branch.

```bash
# Ensure you have latest remote
git fetch origin

# Set a helper var for current branch
BRANCH=$(git rev-parse --abbrev-ref HEAD)

# Quick overview of what will change on the remote
git diff --stat origin/$BRANCH...HEAD

# See the file list (useful to spot unintended changes)
git diff --name-only origin/$BRANCH...HEAD | sort

# Review commit differences (left/right) without merges
git log --oneline --left-right --cherry --no-merges origin/$BRANCH...HEAD

# Optional: preview the push without sending any data
git push --force-with-lease --dry-run origin $BRANCH
```

Proceed to push only if the changes match expectations.

### 9. Generate raw data report

Run the data extraction script:

```bash
# From repo root
node .github/skills/rebase/scripts/generate-rebase-report.cjs --no-fetch
```

This generates `.tmp/skills/rebase/<timestamp>-rebase-report.md` with raw data:
- Ahead/behind counts and diff summary
- Highlights & Anomalies: largest diffs, config changes, dependency summary
- Full commit list (all 57+ commits with hashes and messages)
- Changed packages and top-level folders
- pre.json initialVersions changes (version baseline updates)
- pnpm-lock.yaml churn
- **Detailed Dependency Changes** - Complete breakdown per package:
  - ⚠️ Major version bumps (e.g., `zod: ^3.23.8 → ^4.3.5`)
  - ➕ Added dependencies (e.g., `@azure/search-documents: ^12.2.0`)
  - ➖ Removed dependencies
  - Minor/patch version changes
  - Organized by section: dependencies, devDependencies, peerDependencies

### 10. Generate human-readable summary (automatic)

After the raw report is generated, the AI agent will automatically:

1. Read the latest report from `.tmp/skills/rebase/<timestamp>-rebase-report.md`
2. Analyze the "Detailed Dependency Changes" section
3. Create a human-readable summary with:
   - **Breaking dependency changes** - Each major bump explained (what package, what changed, why it matters, what to test)
   - **New dependencies added** - What was added and its purpose
   - **Version baselines updated** - Which packages bumped and what that means
   - **Risk assessment** - Overall risk level (🟢 LOW, 🟡 MEDIUM, 🔴 HIGH) with reasoning
   - **Pre-push checklist** - Specific tests to run based on detected changes

The summary will be displayed in the chat for review before you push.
- **Next steps**: sanity checks and push confirmation

Open the SUMMARY.md file in your editor to review before pushing.

## Common Scenarios

### Reset local branch to match remote

If your local branch has diverged incorrectly:

```bash
# Fetch latest
git fetch origin

# Hard reset to remote branch
git reset --hard origin/YOUR_BRANCH_NAME
```

### Abort a rebase in progress

If you need to start over:

```bash
git rebase --abort
```

### Continue after fixing conflicts

```bash
# After resolving conflicts and staging changes
git rebase --continue
```

### Skip a commit during rebase

Only if the commit is no longer needed:

```bash
git rebase --skip
```

## Rebase Checklist

- [ ] Fetch latest changes from origin
- [ ] Start rebase onto `origin/main`
- [ ] For `pnpm-lock.yaml` conflicts:
  - [ ] Remove the file with `git rm pnpm-lock.yaml`
  - [ ] Run `pnpm install` to regenerate
  - [ ] Stage with `git add pnpm-lock.yaml`
- [ ] For source file conflicts:
  - [ ] Manually resolve conflicts
  - [ ] Stage resolved files
- [ ] Continue rebase with `git rebase --continue`
- [ ] Repeat until all commits are applied
- [ ] Force push with `--force-with-lease`

## Why Regenerate pnpm-lock.yaml?

The lockfile contains exact dependency resolutions for the entire monorepo. During a rebase:

1. **Base branch** (main) has new/updated dependencies
2. **Your branch** has different/updated dependencies
3. Git cannot merge these semantically - it only sees text conflicts

By regenerating with `pnpm install`:
- pnpm reads all current `package.json` files (including your changes)
- Resolves dependencies against the latest registry state
- Creates a consistent lockfile that works with both sets of changes
- Respects workspace protocols and catalog references

## Troubleshooting

### "diverged and have X and Y different commits"

Your local branch has commits that aren't on remote. Common causes:
- Previous force push to a different commit
- Local branch accidentally pointing to wrong commit

**Fix:** Reset to remote and rebase:
```bash
git fetch origin
git fetch origin main:refs/remotes/origin/main
git reset --hard origin/YOUR_BRANCH_NAME
git rebase origin/main
```

### Rebase conflicts on every commit

You may be rebasing in the wrong direction. Ensure:
- You're ON your feature branch
- You're rebasing ONTO main: `git rebase origin/main`

### pnpm install fails during rebase

Check:
- All `package.json` changes are staged/committed
- No syntax errors in modified `package.json` files
- You're running from the repository root

## Example: Complete rebase flow

```bash
# 1. Navigate and prepare
cd /Users/odin.rochmann/dev/GitHub/fusion-framework.worktree/react-19
git fetch origin
git fetch origin main:refs/remotes/origin/main

# 2. Ensure clean state
git status  # Should show "nothing to commit, working tree clean"

# 3. Start rebase
git rebase origin/main

# 4. If pnpm-lock.yaml conflict appears:
git rm pnpm-lock.yaml
pnpm install
git add pnpm-lock.yaml
git rebase --continue

# 5. Repeat step 4 for each commit with lockfile conflicts

# 6. When rebase completes:
git push --force-with-lease origin react-19
```

## Related Skills

- `pnpm-dependency-analysis` - Analyze dependencies before/after rebase
- `dependabot-pr-handler` - Handle automated dependency updates that may conflict during rebase

---
name: release
description: Release a merged PR by tagging and creating a GitHub release. Use when asked to "release", "tag", or "create a release".
allowed-tools: Bash, Read, AskUserQuestion
---

# Release Workflow

This skill manages the release process for projects that use PR-based releases with git tags and GitHub releases.

## When to Use This Skill

Use this skill when:
- A PR has already been merged to main
- You need to tag the merge commit
- You need to create a GitHub release
- You need to sync development with main after release

## Pre-flight Checks

Before starting the release process, verify:

### 1. Find the PR to Release

```bash
# Check for open PRs ready to merge
gh pr list --state open --base main --json number,title,statusCheckRollup
```

**If no open PR exists, STOP and ask: "Which PR should be released?"**

**If PR has failing checks, STOP and report: "PR has failing CI checks. Fix them before releasing."**

### 2. Determine Next Version Number

```bash
# Get the last tag
git fetch --tags
git describe --tags --abbrev=0 2>/dev/null || echo "No tags found"
```

The next version is always the last tag + 1:
- If last tag is `v29`, next is `v30`
- If last tag is `v1.2.3`, next is `v1.2.4`

**Ask the user to confirm the version number before proceeding.**

## Release Process

Once pre-flight checks pass:

### Step 1: Merge the PR (DO NOT USE LOCAL GIT MERGE)

```bash
gh pr merge <PR_NUMBER> --merge --delete-branch=false --subject "..." --body "..."
```

**CRITICAL**: ALWAYS use `gh pr merge` to merge into main, NEVER use local `git merge`.

### Step 2: Checkout main and pull the merge commit

```bash
git checkout main
git pull origin main
```

### Step 3: Verify we're on the merge commit

```bash
git log -1 --oneline
```

### Step 4: Create and push the tag

```bash
git tag -a "v<VERSION>" -m "$(cat <<'EOF'
Release v<VERSION>

<Brief description of what's in this release>

🤖 Tagged with [Claude Code](https://claude.com/claude-code)
EOF
)"

git push origin v<VERSION>
```

### Step 4: Create GitHub release

```bash
gh release create "v<VERSION>" \
  --title "v<VERSION>" \
  --notes "$(cat <<'EOF'
## What's New in v<VERSION>

<List key features/fixes in this release>

### Changes
See the [CHANGELOG](https://github.com/OWNER/REPO/blob/main/CHANGELOG.md) for detailed release notes.

## Installation

Download from the App Store or TestFlight.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
```

### Step 5: Rebase development around main (main is source of truth)

```bash
git checkout development
git rebase main
git push origin development --force-with-lease
```

This rebases development around main's history. Main is the source of truth - we replay development's commits on top of main's canonical history.

### Step 6: Report Success

Report:
- ✅ Released version v<VERSION>
- 📦 GitHub release: https://github.com/OWNER/REPO/releases/tag/v<VERSION>
- 🔄 Development rebased around main (main is source of truth)

## Important Rules

1. **ALWAYS use `gh pr merge` to merge PRs** - NEVER use local `git merge` to merge into main
2. **ALWAYS ask user to confirm version number** - Don't guess
3. **ALWAYS use annotated tags** (`git tag -a`) - Include metadata
4. **ALWAYS rebase development around main after release** - Main is the source of truth
5. **Use `--force-with-lease` when rebasing development** - Safe force push
6. **NEVER use local git merge commands** - All merges happen via GitHub PR mechanism
7. **Main branch is the canonical source of truth** - Development rebases around it, not the other way

## Workflow Summary

```
1. Find open PR ready to merge
2. Verify PR has passing CI checks
3. Determine next version (last tag + 1)
4. Ask user to confirm version
5. Merge PR using gh pr merge (NEVER local git merge)
6. Checkout main and pull the merge commit
7. Tag the merge commit
8. Push the tag
9. Create GitHub release
10. Rebase development around main (main is source of truth)
```

## Example Usage

```
User: "Release PR #78"
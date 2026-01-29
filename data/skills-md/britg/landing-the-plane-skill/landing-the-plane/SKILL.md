---
name: landing-the-plane
description: Complete a work session by cleaning up, committing, and pushing all changes to remote. Use when the user says "land the plane", "wrap up", "finish up", or wants to complete their session and push all work.
metadata:
  author: user
  version: "1.0.0"
---

# Landing the Plane

**When the user says "let's land the plane"**, complete ALL steps below. The plane is NOT landed until `git push` succeeds. NEVER stop before pushing. NEVER say "ready to push when you are!" - that is a FAILURE.

**IMPORTANT: Include ALL dirty files in the commit, even if they were not related to this session's work. NEVER use `git reset`, `git checkout`, or `git restore` to discard changes. The user may have made changes outside this session that need to be preserved.**

**NEVER DELETE EXISTING WORK** - if there are any existing uncommitted changes, include them in the commit. If there are merge conflicts, resolve them by keeping ALL changes (yours and theirs).

## Mandatory Workflow - Complete ALL Steps

### 1. Clean Up Code
- Remove any console logs, breakpoints, and temporary debugging code
- Re-organize code if this was a debugging session

### 2. Run Quality Gates (if code changes were made)
- Run linters, type checks, and builds
- Fix any issues that arise
- File issues for problems that can't be resolved immediately

### 3. Stage and Commit All Changes
```bash
# Check status
git status

# Stage all changes (including untracked files)
git add -A

# Commit with descriptive message
git commit -m "Description of changes

Co-Authored-By: Claude <noreply@anthropic.com>"
```

### 4. Push to Remote - NON-NEGOTIABLE
This step is MANDATORY. Execute ALL commands below:

```bash
# Pull first to catch any remote changes
git pull --rebase

# MANDATORY: Push everything to remote
# DO NOT STOP BEFORE THIS COMMAND COMPLETES
git push

# MANDATORY: Verify push succeeded
git status  # MUST show "up to date with origin"
```

**CRITICAL RULES:**
- The plane has NOT landed until `git push` completes successfully
- NEVER stop before `git push` - that leaves work stranded locally
- NEVER say "ready to push when you are!" - YOU must push, not the user
- If `git push` fails, resolve the issue and retry until it succeeds
- The user may be managing multiple sessions - unpushed work breaks coordination

### 5. Clean Up Git State
```bash
git stash clear                    # Remove old stashes
git remote prune origin            # Clean up deleted remote branches
```

### 6. Verify Clean State
Ensure all changes are committed AND PUSHED, no untracked files remain.

## Final Report

Provide the user with:
- Summary of what was completed this session
- Any issues filed for follow-up
- Status of quality gates (all passing / issues filed)
- Confirmation that ALL changes have been pushed to remote
- Recommended next steps or follow-up work

**CRITICAL: Never end a "land the plane" session without successfully pushing. Unpushed work causes severe coordination problems.**

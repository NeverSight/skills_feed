---
name: bd-workflow
description: How to use bd (beads) for issue tracking, ready work, status updates, and comments in this repo.
---

# bd (beads) Workflow Guide

This document expands the abbreviated rules in `AGENTS.md`. Read this whenever you interact with task tracking, planning docs, or MCP helpers.

## Why bd?

- **Dependency-aware**: track blockers, dependents, and discovered-from links.
- **Git-friendly**: bd auto-syncs to `.beads/issues.jsonl`, so repos capture task history.
- **Agent-optimized**: machine-readable JSON output (`--json`) plus "ready" filtering.
- **Single source of truth**: prevents duplicate trackers, markdown TODOs, or ad-hoc spreadsheets.

## Quick Start Commands

```bash
bd ready --json -n 0                    # find unblocked work
bd create "Issue title" -t task -p 2 --json
bd update bd-42 --status in_progress --json
bd close bd-42 --reason "Completed" --json
```

Always run bd with `--json`. Pipe/parse as needed.

## Issue Types & Priorities

- Types: `bug`, `feature`, `task`, `epic`, `chore`.
- Priorities: `0` (critical) through `4` (backlog). Respect existing priority unless the PM/user changes it.

## Workflow for AI Agents

1. **Check ready work** with `bd ready --json -n 0`. Do this before asking what to work on.
2. **Claim** the task: `bd update <id> --status in_progress --json` (add notes if relevant).
3. **Implement / test / document** the change.
4. **Discover new work?** Create a linked issue (e.g., `bd create "Fix follow-up" -p 1 --deps discovered-from:<parent> --json`).
5. **Complete** the task as soon as you believe the acceptance criteria are met and you have pushed non-interim commits (draft PRs included). Run `bd close <id> --reason "Completed" --json` at that point; merge or green CI is _not_ required. If CI later fails or review feedback arrives, flip back to `in_progress`, address it, and close again once satisfied.
6. **Commit `.beads/issues.jsonl` alongside code.** Never leave tracker changes uncommitted.

## Auto-Sync Behavior

- bd exports to `.beads/issues.jsonl` automatically (5s debounce) after changes.
- After `git pull`, bd imports newer JSONL back into the local state. No manual sync needed.
- If a merge conflict touches `.beads/*.jsonl`, prefer `git merge` (not rebase) so the custom `merge=beads` driver can resolve cleanly; avoid rewriting history that would replay bd edits and create duplicate entries.

## MCP Integration (Optional)

- Install: `pip install beads-mcp`.
- Add to `~/.config/claude/config.json`:

```json
{
  "beads": {
    "command": "beads-mcp",
    "args": []
  }
}
```

- Use `mcp__beads__*` calls instead of the CLI if your client supports MCP.

## Planning Document Hygiene

AI-generated planning/design docs should live under `history/` (add it to `.gitignore` if desired). Keeping the repo root clean avoids confusing ephemeral plans with durable docs.

## Important Rules (Do & Don't)

- ✅ Use bd for **all** task tracking.
- ✅ Include discovered-from dependencies to show provenance.
- ✅ Keep `.beads/issues.jsonl` in every relevant commit.
- ✅ Store planning docs in `history/`.
- ❌ No markdown TODO lists or alternative trackers.
- ❌ No forgetting `--json`.
- ❌ No cluttering the repo root with temporary planning files.


## Landing the Plane

**When the user says "let's land the plane"**, you MUST complete ALL steps below. The plane is NOT landed until `git push` succeeds. NEVER stop before pushing. NEVER say "ready to push when you are!" - that is a FAILURE.

**MANDATORY WORKFLOW - COMPLETE ALL STEPS:**

1. **File beads issues for any remaining work** that needs follow-up
2. **Ensure all quality gates pass** (only if code changes were made) - run tests, linters, builds (file P0 issues if broken)
3. **Update beads issues** - close finished work, update status
4. **PUSH TO REMOTE - NON-NEGOTIABLE** - This step is MANDATORY. Execute ALL commands below:
   ```bash
   # Pull first to catch any remote changes
   git pull --rebase

   # If conflicts in .beads/beads.jsonl, resolve thoughtfully:
   #   - git checkout --theirs .beads/beads.jsonl (accept remote)
   #   - bd import -i .beads/beads.jsonl (re-import)
   #   - Or manual merge, then import

   # Sync the database (exports to JSONL, commits)
   bd sync

   # MANDATORY: Push everything to remote
   # DO NOT STOP BEFORE THIS COMMAND COMPLETES
   git push

   # MANDATORY: Verify push succeeded
   git status  # MUST show "up to date with origin/main"
   ```

   **CRITICAL RULES:**
   - The plane has NOT landed until `git push` completes successfully
   - NEVER stop before `git push` - that leaves work stranded locally
   - NEVER say "ready to push when you are!" - YOU must push, not the user
   - If `git push` fails, resolve the issue and retry until it succeeds
   - The user is managing multiple agents - unpushed work breaks their coordination workflow

5. **Clean up git state** - Clear old stashes and prune dead remote branches:
   ```bash
   git stash clear                    # Remove old stashes
   git remote prune origin            # Clean up deleted remote branches
   ```
6. **Verify clean state** - Ensure all changes are committed AND PUSHED, no untracked files remain
7. **Choose a follow-up issue for next session**
   - Provide a prompt for the user to give to you in the next session
   - Format: "Continue work on bd-X: [issue title]. [Brief context about what's been done and what's next]"

**REMEMBER: Landing the plane means EVERYTHING is pushed to remote. No exceptions. No "ready when you are". PUSH IT.**

**Example "land the plane" session:**

```bash
# 1. File remaining work
bd create "Add integration tests for sync" -t task -p 2 --json

# 2. Run quality gates (only if code changes were made)
go test -short ./...
golangci-lint run ./...

# 3. Close finished issues
bd close bd-42 bd-43 --reason "Completed" --json

# 4. PUSH TO REMOTE - MANDATORY, NO STOPPING BEFORE THIS IS DONE
git pull --rebase
# If conflicts in .beads/beads.jsonl, resolve thoughtfully:
#   - git checkout --theirs .beads/beads.jsonl (accept remote)
#   - bd import -i .beads/beads.jsonl (re-import)
#   - Or manual merge, then import
bd sync        # Export/import/commit
git push       # MANDATORY - THE PLANE IS STILL IN THE AIR UNTIL THIS SUCCEEDS
git status     # MUST verify "up to date with origin/main"

# 5. Clean up git state
git stash clear
git remote prune origin

# 6. Verify everything is clean and pushed
git status

# 7. Choose next work
bd ready --json
bd show bd-44 --json
```

**Then provide the user with:**

- Summary of what was completed this session
- What issues were filed for follow-up
- Status of quality gates (all passing / issues filed)
- Confirmation that ALL changes have been pushed to remote
- Recommended prompt for next session

**CRITICAL: Never end a "land the plane" session without successfully pushing. The user is coordinating multiple agents and unpushed work causes severe rebase conflicts.**


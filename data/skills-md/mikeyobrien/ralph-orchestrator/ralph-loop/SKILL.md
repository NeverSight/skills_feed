---
name: ralph-loop
description: Use when starting, monitoring, resuming, or canceling Ralph orchestration loops
---

# Ralph Loop Management

Manage parallel orchestration loops: monitor status, merge completed work, troubleshoot failures.

## Quick Reference

| Task | Command |
|------|---------|
| List active loops | `ralph loops` |
| List all (including merged) | `ralph loops --all` |
| View loop changes | `ralph loops diff <id>` |
| View loop logs | `ralph loops logs <id>` |
| Follow logs live | `ralph loops logs <id> -f` |
| Stop running loop | `ralph loops stop <id>` |
| Merge completed loop | `ralph loops merge <id>` |
| Retry failed merge | `ralph loops retry <id>` |
| Abandon loop | `ralph loops discard <id>` |
| Clean stale processes | `ralph loops prune` |

**Loop ID format:** Partial matching works - `a3f2` matches `loop-20250124-143052-a3f2`

## Understanding Loop Status

Run `ralph loops` to see all active loops. Status meanings:

| Status | Color | Meaning |
|--------|-------|---------|
| running | green | Loop is actively executing |
| queued | blue | Completed, waiting for merge |
| merging | yellow | Merge in progress |
| needs-review | red | Merge failed, requires intervention |
| merged | dim | Successfully merged (with `--all`) |
| discarded | dim | Abandoned (with `--all`) |

## Inspecting Loops

```bash
# View what a loop changed
ralph loops diff <id>

# Stream event log (live)
ralph loops logs <id> -f

# Event history (state changes)
ralph loops history <id>

# Open shell in worktree to inspect manually
ralph loops attach <id>
```

## Reading Loop Context Directly

For deeper insight into what a loop is doing, read files from its worktree:

**For worktree loops** (`.worktrees/<loop-id>/`):

| File | Contents |
|------|----------|
| `.ralph/events.jsonl` | Event stream: hats, iterations, tool calls |
| `.ralph/agent/summary.md` | Current session summary |
| `.ralph/agent/handoff.md` | Handoff context for next iteration |
| `.ralph/agent/scratchpad.md` | Working notes |
| `.ralph/agent/tasks.jsonl` | Runtime task state |

**For primary loop** (main workspace): Same files at `.ralph/agent/` in the repo root.

## Reading State Files

| File | Contents |
|------|----------|
| `.ralph/loop.lock` | Primary loop PID, prompt, start time |
| `.ralph/loops.json` | Registry of all running loops |
| `.ralph/merge-queue.jsonl` | Event log: Queued→Merging→Merged/NeedsReview |

```bash
# Check primary loop prompt
jq -r '.prompt' .ralph/loop.lock 2>/dev/null

# Latest state per loop in merge queue
tail -50 .ralph/merge-queue.jsonl | jq -s 'group_by(.loop_id) | map(max_by(.ts))'
```

## Starting Loops

Loops start automatically when `ralph run` is invoked:
- **Primary loop**: Runs in main workspace, holds `.ralph/loop.lock`
- **Worktree loop**: Created when primary is already running, isolated in `.worktrees/<loop-id>/`

Check before starting work:
```bash
ralph loops                       # Any loops running or pending merge?
cat .ralph/loop.lock 2>/dev/null  # Primary loop details
```

## Stopping Loops

```bash
ralph loops stop <id>             # Send SIGTERM (graceful)
ralph loops stop <id> --force     # Send SIGKILL (immediate)
```

## Discarding Loops

Abandon a loop and clean up its worktree:
```bash
ralph loops discard <id>          # Removes worktree + dequeues from merge
```

Use when:
- Loop went down wrong path
- Work is no longer needed
- Want to start fresh

## Cleaning Up

```bash
ralph loops prune                 # Remove stale processes + orphan worktrees
```

Run periodically or when `ralph loops` shows unexpected entries.

## Merge Queue States

When a worktree loop completes, it queues for merge. States flow:

```
Queued → Merging → Merged
                 ↘ NeedsReview → Merging (retry)
                               ↘ Discarded
```

## Preflight Check Before Merge

Before merging a loop, inspect its changes to understand what will be merged:

```bash
# 1. Check loop status and get worktree path
ralph loops list

# 2. View the diff (what changes will be merged)
ralph loops diff <id>

# 3. For deeper inspection, check git status in the worktree
cd .worktrees/<loop-id>
git status
git log --oneline main..HEAD      # Commits to be merged
git diff main...HEAD --stat       # Files changed summary
cd -

# 4. Check for potential conflicts
git merge-tree $(git merge-base main .worktrees/<loop-id>) main .worktrees/<loop-id>
```

**What to look for:**
- Uncommitted changes in worktree (should be committed or stashed)
- Number of commits and files changed (scope of merge)
- Overlap with recent main branch changes (conflict risk)
- Any sensitive files (.env, credentials) that shouldn't be merged

## Merging Completed Loops

```bash
ralph loops merge <id>            # Queue loop for merge (waits for primary)
ralph loops process               # Process pending merges now
```

Merges happen automatically when primary loop completes. Manual merge useful when:
- Primary loop is idle
- Want to merge immediately

## Handling Failed Merges

When merge fails (conflicts, errors), loop enters `needs-review`:

```bash
# Check why it failed
ralph loops history <id>
ralph loops diff <id>             # See the changes that need merging

# Retry with guidance
ralph loops retry <id>

# Or abandon
ralph loops discard <id>
```

## Reading Merge Queue State

```bash
# Recent merge events
tail -20 .ralph/merge-queue.jsonl | jq .

# Current state per loop (latest event wins)
jq -s 'group_by(.loop_id) | map(max_by(.ts))' .ralph/merge-queue.jsonl

# Find loops needing review
jq -s 'group_by(.loop_id) | map(max_by(.ts)) | .[] | select(.event.NeedsReview)' .ralph/merge-queue.jsonl
```

## Troubleshooting

### Stale Processes

**Symptom**: `ralph loops` shows loops that aren't actually running

**Diagnosis**:
```bash
ralph loops                       # Note the PID
ps -p <pid>                       # Check if process exists
```

**Fix**:
```bash
ralph loops prune                 # Auto-cleans dead PIDs
```

### Orphan Worktrees

**Symptom**: `.worktrees/` contains directories not in `ralph loops`

**Diagnosis**:
```bash
ls .worktrees/
git worktree list
ralph loops --all
```

**Fix**:
```bash
ralph loops prune                 # Cleans orphan worktrees
# Or manually:
git worktree remove .worktrees/<loop-id> --force
git branch -D ralph/<loop-id>
```

### Merge Conflicts

**Symptom**: Loop stuck in `needs-review`

**Diagnosis**:
```bash
ralph loops diff <id>             # See conflicting changes
ralph loops attach <id>           # Inspect worktree manually
cat .ralph/merge-queue.jsonl | grep <loop-id> | tail -5
```

**Fix options**:
1. `ralph loops retry <id>` — try again (maybe with guidance via web UI)
2. `ralph loops attach <id>` — resolve manually, commit, then retry
3. `ralph loops discard <id>` — abandon if not worth fixing

### Lock Stuck

**Symptom**: "Loop already running" but nothing is running

**Diagnosis**:
```bash
cat .ralph/loop.lock
ps -p $(jq -r .pid .ralph/loop.lock)
```

**Fix**:
```bash
rm .ralph/loop.lock               # Safe if process is dead
```

### Merge Stuck in "merging" State

**Symptom**: Loop shows `merging` but no merge process is running

**Diagnosis**:
```bash
# Find the PID from merge queue
grep <loop-id> .ralph/merge-queue.jsonl | jq 'select(.event.type == "merging") | .event.pid'
ps -p <pid>                       # Check if process exists
```

**Fix**: Add a `needs_review` event to unblock, then discard:
```bash
# Add needs_review event
echo '{"ts":"'$(date -u +%Y-%m-%dT%H:%M:%S.000000Z)'","loop_id":"<loop-id>","event":{"type":"needs_review","reason":"Merge process died"}}' >> .ralph/merge-queue.jsonl

# Now discard works
ralph loops discard <loop-id>
```

### Worktree Corruption

**Symptom**: Git errors when accessing worktree

**Fix**:
```bash
git worktree repair
ralph loops prune
```

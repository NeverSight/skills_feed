---
name: loop-nanny
description: "Monitor running agent loops, triage failures, clean up after completion, and decide when to intervene. Use when a loop is running and needs babysitting, when a loop just finished and needs post-merge verification, when stories are skipping/failing and need diagnosis, or when stale test artifacts need cleanup. Triggers on: 'check the loop', 'what happened with the loop', 'loop finished', 'clean up after loop', 'why did that story skip', 'monitor loop', 'nanny the loop', or any post-start loop management task. Distinct from agent-loop skill (which handles starting loops)."
---

# Loop Nanny

Monitor, triage, and clean up after agent loops. The agent-loop skill starts loops. This skill keeps them healthy.

## Monitor a Running Loop

```bash
joelclaw loop status <LOOP_ID>
```

`joelclaw` is the primary CLI.

Poll every 2–3 minutes. A story typically takes 3–8 minutes (test-write → implement → review → judge). If a story shows no progress for 10+ minutes, something is stuck.

### Reading Status Output

| Status | Meaning | Action |
|--------|---------|--------|
| `✅ PASS` | Story completed | None |
| `⏭ SKIP` | Exhausted retries | Check if code landed anyway (common — see Skip Triage) |
| `▶ STORY.DISPATCHED` | Implementor running | Wait |
| `▶ TESTS.WRITTEN` | Reviewer running | Wait |
| `▶ CHECKS.COMPLETED` | Judge evaluating | Wait |
| `▶ STORY.RETRIED` | Failed, retrying | Check attempt output for patterns |
| `▶ RETRO.COMPLETED` | Loop finishing (merge-back) | Wait for merge, then verify |
| `⏳ pending` | Not yet started | Normal — queued |

## Skip Triage

Stories skip when the judge fails them after max retries. But **the implementation often landed anyway** — later stories may have included the work, or the first attempt was correct but tests were over-specified.

### Check if skipped work actually landed

```bash
# 1. Read the attempt output
cat /tmp/agent-loop/<LOOP_ID>/<STORY_ID>-<ATTEMPT>.out | tail -40

# 2. Check if the files exist on main after merge
ls <project>/path/to/expected/file

# 3. Check git log for the story's commits
cd <project> && git log --oneline --grep="<STORY_ID>" -5
```

### Common skip causes

| Pattern | Cause | Prevention |
|---------|-------|------------|
| "Already exists" | Story duplicates work from prior story | Write more atomic stories; planner didn't know current state |
| Test assertion failure | Agent-generated tests over-specify implementation | Acceptance criteria should test behavior, not implementation |
| TypeScript compile error | Story depends on types from a skipped story | Order stories so type-providing stories run first |
| Timeout | Implementor took too long | Smaller story scope |

## Post-Loop Cleanup

After merge-back completes (status shows `RETRO.COMPLETED` then resolves):

### 1. Verify merge landed

```bash
cd <project> && git log --oneline -5
# Should show: "Merge branch 'agent-loop/<LOOP_ID>'"
```

### 2. Run full test suite

```bash
cd <project> && bun test 2>&1 | tail -5
```

### 3. Delete stale acceptance tests

Agent loops generate `__tests__/<story-id>-*.test.ts` files. These test implementation details and break on every refactor. Delete them after verifying the real tests pass.

```bash
# Find agent-generated test files
ls <project>/__tests__/*-*.test.ts 2>/dev/null

# Check which fail
bun test __tests__/ 2>&1 | grep "(fail)"

# Delete ALL agent-generated acceptance tests (they served their purpose)
rm <project>/__tests__/<prefix>-*.test.ts

# Verify clean
bun test 2>&1 | tail -3
```

Per AGENTS.md: *"over-specified tests that mock internal step names are worse than no tests — they break on every refactor and give false negatives."*

### 4. TypeScript check

```bash
cd <project> && bunx tsc --noEmit
```

### 5. Restart worker deployment (if loop touched Inngest functions)

```bash
kubectl -n joelclaw rollout restart deployment/system-bus-worker
kubectl -n joelclaw rollout status deployment/system-bus-worker --timeout=180s
joelclaw refresh
joelclaw status
```

### 6. Commit cleanup

```bash
cd <project> && git add -A && git commit -m "chore: post-loop cleanup for <LOOP_ID>

Delete stale acceptance tests, verify N pass / 0 fail / tsc clean"
```

## When to Intervene

### Don't intervene — let the loop work
- Story on first attempt (even if slow)
- Story retrying with feedback (judge gave actionable feedback)
- Story just skipped but later stories are still pending

### Intervene — something is broken
- **Same error on retry**: Check attempt output. If retry 2 has identical error to retry 1, the feedback loop isn't helping — cancel and fix the root cause.
- **Merge conflict during complete**: `joelclaw logs errors` will show merge abort. Manually resolve: `cd <project> && git merge --abort` then merge the branch by hand.
- **Worker crashed**: `joelclaw status` shows worker down. Restart deployment: `kubectl -n joelclaw rollout restart deployment/system-bus-worker`
- **All stories skipping**: The PRD likely has a bad assumption. Cancel, review prd.json, re-fire.
- **Loop stuck (no progress for 15min)**: Check `joelclaw runs --count 5` — if the latest run is COMPLETED but no new run dispatched, there's a state bug. Cancel and re-fire from the stuck story.

### Cancel a stuck loop

```bash
joelclaw loop cancel <LOOP_ID>

# Clean up worktree manually (cancel doesn't auto-merge)
cd <project>
git worktree remove /tmp/agent-loop/<LOOP_ID> --force 2>/dev/null
git branch -D agent-loop/<LOOP_ID> 2>/dev/null
git worktree prune
```

## Reading Attempt Output

Each story attempt writes to `/tmp/agent-loop/<LOOP_ID>/<STORY_ID>-<ATTEMPT>.out`. These contain the implementor/reviewer's full output (diffs, reasoning, test results).

```bash
# Quick scan — last 40 lines usually has the verdict
tail -40 /tmp/agent-loop/<LOOP_ID>/<STORY_ID>-<ATTEMPT>.out

# Check all attempts for a story
ls /tmp/agent-loop/<LOOP_ID>/<STORY_ID>-*.out

# Grep for errors across all attempts
grep -i "error\|fail\|reject" /tmp/agent-loop/<LOOP_ID>/*.out
```

## Monitoring Checklist

Use this sequence when babysitting a loop:

```
1. joelclaw loop status <LOOP_ID>          — where are we?
2. (if story running) wait 3 min, re-check
3. (if story skipped) check attempt output — did the work land anyway?
4. (if loop completed) verify merge, run tests, delete stale tests, restart worker
5. (if stuck) joelclaw runs --count 5 + joelclaw logs errors — diagnose
```

## Improve joelclaw While You Nanny

The nanny is the primary consumer of `joelclaw` output. When you hit a gap — missing info, unclear output, an extra step you had to do manually — **fix joelclaw right then**. The joelclaw source lives at `~/Code/joelhooks/joelclaw/`.

### What to improve

- **Missing data in output**: `joelclaw loop status` doesn't show story descriptions? Add them.
- **Manual steps that should be commands**: Had to `kubectl logs` directly? Add it to `joelclaw logs`.
- **Bad next_actions**: The suggested next commands don't match what you actually needed? Fix the HATEOAS.
- **Error without fix**: Got an error with no `fix` field? Add one via `respondError()`.
- **New command needed**: Found yourself running raw curl/GraphQL? Wrap it in a joelclaw command.

### How to improve

```bash
# Commands are in packages/cli/src/commands/ — one file per command
# Response helpers in packages/cli/src/response.ts
# Inngest client methods in packages/cli/src/inngest.ts

# Test your change
joelclaw <command> 2>&1 | python3 -m json.tool

# Commit
git add -A && git commit -m "feat: joelclaw <command> — <what you added>"
```

Follow the [cli-design skill](../cli-design/SKILL.md): JSON always, HATEOAS next_actions, context-safe output, errors with fixes. After improving joelclaw, update this skill doc if the monitoring workflow changed.

## Diagnosing Stalled Loops

When a loop stops progressing, use the diagnostic command FIRST:

```bash
# Quick diagnosis of all loops
joelclaw loop diagnose all -c

# Diagnose + auto-fix (clears claims, re-fires plan events)
joelclaw loop diagnose all -c --fix

# Verify fix worked (~30s later)
joelclaw loop status <loop-id> -c
```

Common diagnoses:
- **CHAIN_BROKEN** — judge→plan event was lost. `--fix` re-fires the plan event.
- **ORPHANED_CLAIM** — agent died but claim remains. `--fix` clears claim + re-fires.
- **STUCK_RUN** — Inngest run active but agent dead. `--fix` clears + re-fires.
- **WORKER_UNHEALTHY** — fewer functions than expected. `--fix` restarts worker.

See [loop-diagnosis skill](../loop-diagnosis/SKILL.md) for full reference.

## Gotchas

- **Don't edit the monorepo while a loop runs** — `git add -A` in the worktree scoops unrelated changes
- **CLI-focused edits are safest during active loops** — avoid changing `packages/system-bus` mid-run unless you're intentionally redeploying the worker
- **prd.json and progress.txt get dirty** — this is normal; complete.ts stashes before merge
- **Worktree branch not auto-deleted on cancel** — clean manually (see Cancel section)
- **Cross-file test pollution** — agent-generated `__tests__/` files can cause failures in real tests when run together; delete them

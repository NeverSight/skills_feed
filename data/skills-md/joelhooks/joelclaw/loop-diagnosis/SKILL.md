---
name: loop-diagnosis
description: Diagnose and fix stalled agent loops using the joelclaw CLI. Use when loops appear stuck, stories aren't progressing, or the event chain broke. Triggers on "loop stalled", "why isn't the loop progressing", "diagnose loops", "fix stuck loop", "loop not moving", "what happened to the loop", "stories stuck at pending", or any request to debug loop infrastructure.
---

# Loop Diagnosis

Diagnose and fix stalled agent coding loops. This skill covers the diagnostic CLI, common failure modes, and the observability patterns that prevent silent stalls.

## Quick Commands

```bash
# Diagnose all active loops at once
joelclaw loop diagnose all -c

# Diagnose a specific loop
joelclaw loop diagnose <loop-id> -c

# Diagnose AND auto-fix
joelclaw loop diagnose all -c --fix

# Full JSON output (for detailed inspection)
joelclaw loop diagnose <loop-id>
```

## What Diagnosis Checks

The `diagnose` command runs 6 checks in order:

1. **Redis state** — PRD stories (pass/skip/pending), progress entries, active claims
2. **Worktree** — exists? commits? uncommitted changes? .out files?
3. **Inngest runs** — running/failed agent-loop-* functions, recent plan runs
4. **Agent processes** — any claude/codex processes still alive?
5. **Worker health** — function_count from localhost:3111/api/inngest
6. **Diagnosis** — pattern-matches the above into a root cause

## Failure Modes & Fixes

| Diagnosis | Root Cause | Auto-Fix |
|-----------|-----------|----------|
| `CHAIN_BROKEN` | Judge sent `story.passed` but plan never received it. Event lost in transit. | Re-fires `agent/loop.story.passed` → plan picks next story |
| `ORPHANED_CLAIM` | Story claimed by an event, but agent died and no Inngest run is active. | Clears claim + re-fires plan event |
| `STUCK_RUN` | Inngest run marked RUNNING but agent process is dead. Run won't complete. | Clears claims + re-fires (manual run cancellation may be needed in Inngest dashboard) |
| `WORKER_UNHEALTHY` | Worker registering fewer functions than expected. Missing imports or crash loop. | Restarts `system-bus-worker` deployment in k8s |
| `NO_PRD` | Loop has no PRD in Redis — was nuked or never created. | None — start a new loop |
| `COMPLETE` | All stories passed or skipped. Nothing to do. | None — run `joelclaw loop nuke dead` to clean up |

## When to Use (vs Other Skills)

- **loop-diagnosis** → Loop is stuck/stalled, need to figure out why and fix it
- **loop-nanny** → Loop is running, need to monitor progress and clean up after
- **agent-loop** → Need to START a new loop

## The Event Chain

Understanding the chain helps diagnose WHERE it broke:

```
agent/loop.started
  → plan (picks story, dispatches test-writer)
    → agent/loop.story.dispatched
      → test-writer (writes acceptance tests)
        → agent/loop.tests.written
          → implement (codex/claude writes code)
            → agent/loop.story.implemented
              → review (runs tests, typecheck, claude review)
                → agent/loop.story.reviewed
                  → judge (pass/fail/retry decision)
                    → agent/loop.story.passed  ←── feeds back to plan
                    → agent/loop.story.failed  ←── feeds back to plan
                    → agent/loop.story.retry   ←── feeds back to implement
```

**Most common break point**: `judge → plan`. The `agent/loop.story.passed` event fires but plan never picks it up. This happens when:
- Inngest is restarting during the event
- Worker was restarted between judge and plan
- k8s pod restart dropped the event

## Observability Patterns

### Passive: Failure Events
Every loop function should emit failure events via `onFailure` handlers (being added by harden loop). These fire `agent/loop.function.failed` which gets logged to slog.

### Active: Watchdog (Future)
A periodic Inngest function (`system/loop-watchdog`) that:
1. Scans all loops in Redis with pending stories
2. Checks if any events were emitted in the last 10 minutes
3. If not → auto-runs diagnose + fix
4. Logs to slog + daily log

### Manual: The Diagnostic Session
When an agent needs to debug loops manually, follow this sequence:

```bash
# 1. Quick overview
joelclaw loop diagnose all -c

# 2. If fix needed
joelclaw loop diagnose all -c --fix

# 3. Verify fix worked (wait ~30s for plan to fire)
joelclaw loop status <loop-id> -c

# 4. If still stuck, check worker
curl -s localhost:3111/api/inngest | python3 -c "import json,sys; print(json.load(sys.stdin)['function_count'])"

# 5. Nuclear option: full restart
joelclaw loop restart <loop-id>
```

## Making Loops More Resilient

The root cause of most stalls is **lost events in the judge→plan chain**. Solutions being implemented:

1. **onFailure handlers** — every function gets one, logs failure + emits diagnostic event
2. **Loop watchdog** — periodic check for silent stalls
3. **Debounce on content-sync** — prevents event storms that can crowd out loop events
4. **Singleton on backfill** — prevents resource contention during loops

## Cross-References

- [agent-loop skill](/Users/joel/.pi/agent/skills/agent-loop/SKILL.md) — starting loops
- [loop-nanny skill](/Users/joel/.pi/agent/skills/loop-nanny/SKILL.md) — monitoring + cleanup
- [joelclaw skill](../joelclaw/SKILL.md) — full CLI reference
- [ADR-0028](/Users/joel/Vault/docs/decisions/0028-inngest-reliability-patterns.md) — reliability patterns

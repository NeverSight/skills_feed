---
name: context-degradation
description: 'Token-range severity zones (Green/Yellow/Orange/Red/Critical) with detection checklist, early warning indicators, and corrective routing actions for context window degradation'
version: 1.2.0
category: 'Performance & Optimization'
agents: [context-compressor, planner, router]
user_invocable: true
invoked_by: both
tools: [Read, Write, Skill]
tags: [context, tokens, degradation, compression, performance, thresholds]
best_practices:
  - Check at every phase boundary, not just when problems appear
  - Treat 2+ early warning indicators as one zone higher
  - Spawn fresh subagent rather than continuing in critical zone
error_handling: graceful
verified: true
lastVerifiedAt: 2026-03-01T00:00:00.000Z
---

# Context Degradation Monitor

Detects context window degradation and prescribes corrective actions before accuracy drops.

## Severity Zones

| Zone     | Token Range | Status  | Action                                                                        |
| -------- | ----------- | ------- | ----------------------------------------------------------------------------- |
| Green    | < 32K       | Healthy | Normal operation                                                              |
| Yellow   | 32K - 64K   | Caution | Begin selective compression                                                   |
| Orange   | 64K - 100K  | Warning | Compress aggressively; summarize completed phases                             |
| Red      | 100K - 140K | Danger  | Spawn fresh subagent for remaining work; pass only essential context          |
| Critical | > 140K      | Severe  | Halt complex reasoning; compress immediately; do not attempt multi-step tasks |

Reference: Models advertise 200K but reliability drops past 32K. "Lost in the middle" effect: middle tokens have 20-40% lower recall past 100K.

## Early Warning Indicators

Symptoms that context degradation is affecting output quality (regardless of token count):

1. **Repeated tool calls** — Agent re-reads files already read in same session
2. **Contradictory reasoning** — Later steps contradict earlier decisions
3. **Missing prior context** — Agent "forgets" task scope or constraints stated at session start
4. **Over-explanation** — Agent re-explains concepts already established
5. **Stale references** — Agent references file paths or task IDs that were resolved earlier

If 2+ indicators are present, treat as one zone higher than token count suggests.

## Corrective Routing by Zone

**Yellow (32-64K):**

- Invoke `Skill({ skill: 'token-saver-context-compression' })` at the current phase boundary
- Remove completed phase content from active context
- Keep: current task spec, key decisions, in-progress file list

**Orange (64-100K):**

- Invoke `Skill({ skill: 'context-compressor' })` — aggressive summarization
- Write phase summary to `.claude/context/tmp/phase-summary-{date}.md`
- Prune: all resolved task details, intermediate research, superseded plans

**Red (100-140K):**

- Do NOT continue complex multi-step tasks in current agent
- Spawn a fresh subagent with only the compressed summary as context
- Current agent: write handoff doc → call TaskUpdate(completed) with handoff path in metadata

**Critical (>140K):**

- Halt immediately
- Write emergency summary: what was done, what remains, key decisions
- Route to `session-handoff` skill
- Invoke `Skill({ skill: 'session-handoff' })` before context window forces truncation

## Detection Checklist (Run at Each Phase Boundary)

```
[ ] Token count below 32K? → Green, no action
[ ] Token count 32-64K? → Yellow, begin compression
[ ] Token count 64-100K? → Orange, compress aggressively
[ ] Token count 100K+? → Red/Critical, spawn fresh agent
[ ] 2+ early warning indicators? → Upgrade one severity zone
[ ] Compression reminder file exists? → Invoke context-compressor immediately
```

## Integration

- Pairs with: `context-compressor`, `token-saver-context-compression`, `session-handoff`
- Called by: `planner` (at plan start), `developer` (after each phase), `router` (before large spawns)
- Trigger: Check at every phase boundary, not just when problems appear

## Iron Laws

1. **ALWAYS** check token count at every phase boundary — not just when problems appear or after completing a large task.
2. **NEVER** continue complex multi-step tasks past 100K tokens in the same agent context — spawn a fresh subagent with a compressed handoff instead.
3. **ALWAYS** treat 2+ early warning indicators as one severity zone higher than the raw token count suggests.
4. **ALWAYS** invoke `token-saver-context-compression` at Yellow zone (32–64K) before context bloat becomes severe — prevention is cheaper than recovery.
5. **NEVER** claim a task complete without writing a context summary when operating in Red or Critical zone — if it's not written down, the next agent won't know it happened.

## Anti-Patterns

| Anti-Pattern                                                          | Why It Fails                                                                                          | Correct Approach                                                     |
| --------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------- |
| Waiting until output quality degrades before checking context         | By the time quality drops, the context is already in Red/Critical zone                                | Run detection checklist at every phase boundary proactively          |
| Continuing multi-step tasks past 100K tokens                          | "Lost in the middle" effect causes 20–40% recall drop; decisions made early are forgotten             | Spawn fresh subagent at 100K with compressed context summary         |
| Ignoring early warning indicators because token count looks fine      | Indicators are more reliable than raw token counts; a 30K session with 3 indicators is already Yellow | Treat 2+ indicators as one zone higher regardless of token count     |
| Spawning a subagent without a written handoff document                | Subagent starts from scratch, duplicating work or missing constraints                                 | Always write phase summary to `.claude/context/tmp/` before spawning |
| Compressing context by deleting tool call results without summarizing | Compression without summarization loses critical findings from earlier phases                         | Summarize completed phase outputs before pruning raw tool results    |

## Memory Protocol (MANDATORY)

**Before starting:**
Read `.claude/context/memory/learnings.md`

**After completing:**

- New pattern -> `.claude/context/memory/learnings.md`
- Issue found -> `.claude/context/memory/issues.md`
- Decision made -> `.claude/context/memory/decisions.md`

> ASSUME INTERRUPTION: If it's not in memory, it didn't happen.

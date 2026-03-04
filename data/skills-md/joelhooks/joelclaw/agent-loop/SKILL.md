---
name: agent-loop
description: Start, monitor, and cancel durable multi-agent coding loops via Inngest. Use when the user wants to run autonomous coding workloads, execute a PRD with multiple stories, kick off an AFK coding session, have agents implement features from a plan, or manage running loops. Triggers on "start a coding loop", "run this PRD", "implement these stories", "go AFK and code this", "check loop status", "cancel the loop", "joelclaw loop", or any request for autonomous multi-story code execution.
---

# Agent Loop

Run durable PLANNER→IMPLEMENTOR→REVIEWER→JUDGE coding loops via Inngest. Each story in a PRD gets independently implemented, tested, and judged. Survives crashes. Every step is a traceable Inngest run.

> **After starting a loop**, use the [loop-nanny](../loop-nanny/SKILL.md) skill for monitoring, triage, post-loop cleanup, and knowing when to intervene.

## Quick Start

```bash
# Start a loop
joelclaw loop start --project /path/to/project --prd prd.json --max-retries 2

# Check status
joelclaw loop status [LOOP_ID]

# Cancel
joelclaw loop cancel LOOP_ID
```

The `joelclaw` CLI is the primary interface. Run with `bun run packages/cli/src/cli.ts loop start ...` from the monorepo root.

## PRD Format

Create a `prd.json` in the project root:

```json
{
  "title": "Feature Name",
  "description": "What we're building",
  "stories": [
    {
      "id": "S1",
      "title": "Short title",
      "description": "What to implement. Be specific about files, patterns, behavior.",
      "acceptance_criteria": [
        "Criterion 1 — must be verifiable by automated test",
        "Criterion 2 — must be checkable by typecheck/lint"
      ],
      "priority": 1,
      "passes": false
    }
  ]
}
```

**Story writing tips:**
- Acceptance criteria must be machine-verifiable (tests, typecheck, lint)
- Lower priority number = runs first
- Keep stories small and atomic — one concern per story
- Include file paths in descriptions when possible
- `passes` flips to `true` when JUDGE approves; `skipped: true` added on max retry exhaustion

## Pipeline Flow

```
joelclaw loop start → agent/loop.start event
  → PLANNER reads prd.json, finds next unpassed story
    → IMPLEMENTOR spawns codex/claude/pi, commits changes
      → REVIEWER writes tests from acceptance criteria (independently — does NOT read implementation)
        → JUDGE: all green? → mark passed, next story
                 failing?   → retry with feedback (up to maxRetries)
                 exhausted? → skip, flag for human review, next story
  → All done → agent/loop.complete
```

## progress.txt

Create a `progress.txt` in the project root with a `## Codebase Patterns` section at the top. This is read by the implementor for project context and appended by the judge after each story. Defends against context loss across fresh agent instances.

```
## Codebase Patterns

- Runtime: Bun, not Node
- Tests: bun test
- Key files: src/index.ts, src/lib/...

## Progress

(stories will be appended here)
```

## Infrastructure

- **Canonical source**: `~/Code/joelhooks/joelclaw/packages/system-bus/` (monorepo)
- **Inngest functions**: `agent-loop-plan`, `agent-loop-implement`, `agent-loop-review`, `agent-loop-judge`, `agent-loop-complete`, `agent-loop-retro`
- **Inngest server**: k8s StatefulSet at localhost:8288
- **Loop --project target**: Always use `~/Code/joelhooks/joelclaw/packages/system-bus` (the monorepo).
- **Apply worker changes**: `~/Code/joelhooks/joelclaw/k8s/publish-system-bus-worker.sh`
- **Verify functions**: `joelclaw functions`
- **View runs**: `joelclaw runs -c`
- **Inspect a run**: `joelclaw run RUN_ID`

### Single-source deployment flow

The monorepo is the source of truth for loop function code. After loop-related function changes merge, deploy the worker from the monorepo:

1. Run `~/Code/joelhooks/joelclaw/k8s/publish-system-bus-worker.sh`
2. Wait for rollout: `kubectl -n joelclaw rollout status deployment/system-bus-worker --timeout=180s`
3. Refresh registration: `joelclaw refresh`

## Event Schema

All events carry `loopId` for tracing. Key events:

| Event | Purpose |
|---|---|
| `agent/loop.start` | Kick off loop (loopId, project, prdPath, maxRetries, maxIterations) |
| `agent/loop.plan` | Planner re-entry (find next story) |
| `agent/loop.implement` | Dispatch to implementor (storyId, tool, attempt, feedback?) |
| `agent/loop.review` | Dispatch to reviewer (storyId, commitSha, attempt) |
| `agent/loop.judge` | Dispatch to judge (testResults, feedback, attempt) |
| `agent/loop.complete` | Loop finished (summary, counts) |
| `agent/loop.cancel` | Stop the loop |
| `agent/loop.story.pass` | Story passed |
| `agent/loop.story.fail` | Story skipped after max retries |

## Tool Assignment

Default: codex for implementation, claude for review. Override per-story via `toolAssignments` in the start event:

```json
{
  "toolAssignments": {
    "S1": { "implementor": "claude", "reviewer": "claude" },
    "S2": { "implementor": "codex", "reviewer": "pi" }
  }
}
```

## Known Gotchas

- Concurrency keys use CEL expressions (`event.data.project`), not `{{ }}` templates
- `loop` is reserved in CEL — don't use in concurrency key strings
- Use explicit Codex permissions: `codex exec --ask-for-approval never --sandbox danger-full-access PROMPT` (no `-q` flag)
- Worker changes require a k8s deploy (`k8s/publish-system-bus-worker.sh`)
- Docker must be running for Inngest server (`open -a OrbStack`)
- Large tool output uses claim-check pattern (written to `/tmp/agent-loop/{loopId}/`)

## Logging

Every story attempt is logged via slog:

```bash
slog write --action "story-pass" --tool "agent-loop" --detail "Story title (ID) passed on attempt N" --reason "details"
```

Actions: `story-pass`, `story-retry`, `story-skip`, `build-complete`

## Source Files

| File | Purpose |
|---|---|
| `~/Code/joelhooks/joelclaw/packages/system-bus/src/inngest/client.ts` | Event type definitions |
| `~/Code/joelhooks/joelclaw/packages/system-bus/src/inngest/functions/agent-loop/utils.ts` | PRD parsing, git, cancellation, claim-check |
| `~/Code/joelhooks/joelclaw/packages/system-bus/src/inngest/functions/agent-loop/plan.ts` | PLANNER |
| `~/Code/joelhooks/joelclaw/packages/system-bus/src/inngest/functions/agent-loop/implement.ts` | IMPLEMENTOR |
| `~/Code/joelhooks/joelclaw/packages/system-bus/src/inngest/functions/agent-loop/review.ts` | REVIEWER |
| `~/Code/joelhooks/joelclaw/packages/system-bus/src/inngest/functions/agent-loop/judge.ts` | JUDGE |
| `~/Code/joelhooks/joelclaw/packages/system-bus/src/serve.ts` | Worker registration |
| `~/Code/joelhooks/joelclaw/packages/cli/src/cli.ts` | joelclaw CLI (loop subcommands) |

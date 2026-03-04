---
name: joelclaw
displayName: joelclaw CLI
description: "Operate the joelclaw event bus, gateway, observability, and agent loop infrastructure via the joelclaw CLI. Use for: sending events, checking runs, starting/monitoring/cancelling agent loops, debugging failed runs, checking health, restarting the worker, inspecting step traces, managing subscriptions, gateway operations, OTEL queries, semantic recall. Triggers: 'joelclaw', 'send an event', 'check inngest', 'start a loop', 'loop status', 'why did this fail', 'debug run', 'check worker', 'restart worker', 'runs', 'what failed', 'subscribe', 'gateway', 'otel', 'recall', or any Inngest/event-bus/agent-loop task."
version: 2.0.0
author: Joel Hooks
tags: [joelclaw, cli, inngest, gateway, otel, agent-loop, infrastructure]
---

# joelclaw — CLI & Event Bus

The `joelclaw` CLI is the primary operator interface to the entire joelclaw system: event bus (Inngest), gateway, observability (OTEL), agent loops, subscriptions, and more. Built with `@effect/cli`, returns HATEOAS JSON envelopes.

**If the CLI crashes, that's the highest priority fix.**

Binary: `~/.bun/bin/joelclaw`
Source: `~/Code/joelhooks/joelclaw/packages/cli/`
Build: `bun build packages/cli/src/cli.ts --compile --outfile ~/.bun/bin/joelclaw`

## Architecture

```
┌─ Colima VM (VZ framework, aarch64) ────────────────────────────────┐
│  Talos v1.12.4 → k8s v1.35.0 (single node, namespace: joelclaw)  │
│                                                                     │
│  inngest-0             StatefulSet   ports 8288 (API), 8289 (dash) │
│  redis-0               StatefulSet   port 6379                     │
│  typesense-0           StatefulSet   port 8108                     │
│  system-bus-worker     Deployment    port 3111 (110+ functions)    │
│  docs-api              Deployment    port 3838                     │
│  livekit-server        Deployment    ports 7880, 7881              │
│  bluesky-pds           Deployment    port 3000                     │
│                                                                     │
│  ⚠️ Inngest service named inngest-svc (not inngest)                │
│     k8s auto-injects INNGEST_PORT env collision otherwise          │
└─────────────────────────────────────────────────────────────────────┘
        ↕ NodePort on localhost

Gateway daemon (always-on pi session, Redis event bridge)
NAS "three-body" (ASUSTOR, 10GbE NFS, 64TB RAID5 + NVMe cache)
Vault ~/Vault (Obsidian, PARA method — ADRs, system log, contacts)
```

**Inngest event key**: `37aa349b89692d657d276a40e0e47a15`
**k8s manifests**: `~/Code/joelhooks/joelclaw/k8s/`

## CLI Command Reference

### Health & Status

```bash
joelclaw status                            # Health: server + worker + k8s pods
joelclaw inngest status                    # Inngest server details
joelclaw functions                         # List all 110+ registered functions
joelclaw refresh                           # Force re-register with Inngest server
```

### Send Events

```bash
joelclaw send "event/name" --data '{"key":"value"}'
joelclaw send "pipeline/video.download" --data '{"url":"https://youtube.com/watch?v=XXX"}'
joelclaw send "agent/story.start" --data '{"prdPath":"/abs/path/prd.json","storyId":"S-1"}'
```

### View Runs

```bash
joelclaw runs                              # Recent 10
joelclaw runs --count 20 --hours 24        # More runs, wider window
joelclaw runs --status FAILED              # Just failures
joelclaw run <RUN_ID>                      # Step trace + errors for one run
```

### View Events

```bash
joelclaw events                            # Last 4 hours
joelclaw events --prefix memory/ --hours 24
joelclaw events --prefix agent/ --hours 24
joelclaw events --count 50 --hours 48
```

### Logs

```bash
joelclaw logs                              # Worker stdout (default 30 lines)
joelclaw logs errors                       # Worker stderr (stack traces)
joelclaw logs server                       # Inngest k8s pod logs
joelclaw logs server -n 50 --grep error    # Filtered server errors
joelclaw logs worker --grep "observe"      # Grep worker logs
```

### Structured Log Writes

```bash
joelclaw log write --action configure --tool cli --detail "updated capability adapter config" --reason "ADR-0169 phase 1"
```

`log` writes canonical structured entries (slog backend). `logs` remains runtime log read/analyze.

### Secrets

```bash
joelclaw secrets status
joelclaw secrets lease <name> --ttl 15m
joelclaw secrets revoke <lease-id>
joelclaw secrets revoke --all
joelclaw secrets audit --tail 50
joelclaw secrets env --dry-run
```

### Notify

```bash
joelclaw notify send "Worker restarted and healthy" --priority normal
joelclaw notify send "Immediate action required" --priority urgent --telegram-only
```

### Capability Adapter Paths (ADR-0169 phase 4)

`mail`, `otel`, `recall`, and `subscribe` now run through the CLI capability registry/adapter runtime while preserving their existing command UX and JSON envelopes.

### Deploy

```bash
joelclaw deploy worker                              # dry-run deploy plan
joelclaw deploy worker --restart --execute         # execute worker sync deployment
joelclaw deploy worker --restart --execute --force # force with active runs (disruptive)
```

### Heal

```bash
joelclaw heal list
joelclaw heal run RUN_FAILED --phase fix --context '{"run-id":"01ABC"}'           # dry-run
joelclaw heal run RUN_FAILED --phase fix --context '{"run-id":"01ABC"}' --execute # execute
```

### Gateway

```bash
joelclaw gateway status                    # Gateway health + session info
joelclaw gateway events                    # Recent gateway events
joelclaw gateway test                      # Send test message through gateway
joelclaw gateway restart                   # Restart gateway daemon
joelclaw gateway stream                    # Live stream gateway events
```

### Observability (OTEL)

```bash
joelclaw otel list --hours 1               # Recent telemetry events
joelclaw otel search "error" --hours 24    # Search OTEL events
joelclaw otel stats --hours 24             # Aggregate stats
joelclaw otel emit "action.name" --source codex --component agent-loop --success  # Emit event
```

### System Knowledge (ADR-0199)

```bash
joelclaw knowledge search "query"          # Search system knowledge
joelclaw knowledge search "query" --type adr  # Filter by type (adr|skill|lesson|pattern|retro|failed_target)
joelclaw knowledge sync                    # Re-index ADRs + skills from filesystem
joelclaw knowledge clear-failed <target>   # Clear resolved failed targets
```

Brain/codebase patterns (browsable by agents):
```bash
ls ~/Vault/system/brain/codebase/          # List established patterns
cat ~/Vault/system/brain/codebase/<name>.md  # Read a specific pattern
```

### Subscriptions (ADR-0127)

```bash
joelclaw subscribe list                    # All feed subscriptions
joelclaw subscribe add <url> [--name N]    # Add a feed
joelclaw subscribe remove <url>            # Remove a feed
joelclaw subscribe check [--url URL]       # Check feeds for new items
joelclaw subscribe summary                 # Summary of recent items
```

### Agent Runtime Validation (ADR-0180)

Use this exact smoke test when validating roster dispatch end-to-end:

```bash
joelclaw agent list
joelclaw agent run coder "reply with OK" --timeout 20
joelclaw event <event-id>
```

Expected signal:
- `agent list` includes builtin `coder`, `designer`, `ops`
- `event` shows one `Agent Task Run` with `status: COMPLETED`
- run output contains `{"status":"completed", ...}`

Failure handling:
- `Unknown agent roster entry: coder` means runtime drift, not prompt failure.
  - Deploy latest `system-bus-worker`
  - Restart host worker process
  - Re-run the same 3-step smoke
- If Inngest API is unreachable (`localhost:8288`), recover local control-plane first (Colima/Talos), then retry validation.

### Semantic Recall

```bash
joelclaw recall "query about past context"  # Search semantic memory
```

### Discovery

```bash
joelclaw discover "https://example.com" --context "why this is interesting"
```

### Agent Loops

```bash
# Start a loop
joelclaw loop start --project ~/Code/joelhooks/joelclaw \
  --goal "Implement feature X" \
  --context ~/Vault/docs/decisions/0XXX.md \
  --max-retries 2

# Start with existing PRD
joelclaw loop start --project PATH --prd prd.json --max-retries 2

# Monitor
joelclaw loop status <LOOP_ID>
joelclaw loop status <LOOP_ID> -c          # Compact: one line per story
joelclaw loop status <LOOP_ID> -v          # Verbose: criteria, output paths
joelclaw watch <LOOP_ID>                   # Live: polls 15s, exits on completion
joelclaw watch                             # Auto-detects active loop

# Management
joelclaw loop list                         # All loops in Redis
joelclaw loop cancel <LOOP_ID>             # Stop + cleanup
joelclaw loop nuke dead                    # Remove completed loops from Redis
```

### Other Commands

```bash
joelclaw sleep [on|off|status]             # Sleep mode for gateway
joelclaw note <text>                       # Quick note to Vault
joelclaw vault read <ref>                  # Resolve/read ADR/project/path refs
joelclaw vault search <query>              # Search vault markdown
joelclaw vault adr list                    # ADR inventory (optionally by status)
joelclaw vault adr collisions              # ADR number collision report
joelclaw vault adr audit                   # ADR health + collision + index checks
joelclaw vault adr rank --status accepted,proposed  # ADR NRC+novelty ranking
joelclaw skills audit [--deep]             # On-demand skill garden report
joelclaw search <query>                    # Full-text search
joelclaw email [scan|triage]               # Email operations
joelclaw x [post|mentions]                 # X/Twitter operations
joelclaw nas [status|health]               # NAS operations
joelclaw diagnose <topic>                  # System diagnosis
joelclaw langfuse [traces|costs]           # Langfuse analytics
joelclaw deploy worker [--restart] [--execute]
joelclaw heal [list|run]
joelclaw inngest sync-worker [--restart]   # Worker lifecycle
```

For vault-heavy or ADR-gardening tasks, use the dedicated [`vault`](../vault/SKILL.md) skill.

### Output Modes

Most commands support `--compact/-c` for plain text. Use compact for monitoring.
JSON (default) returns HATEOAS envelopes with `next_actions`.

## Story Pipeline (ADR-0155)

3-stage pipeline: implement → prove → judge. Each story runs through the stages with Inngest durability.

```bash
# Fire a single story
joelclaw send agent/story.start -d '{
  "prdPath": "/Users/joel/Code/joelhooks/joelclaw/prd.json",
  "storyId": "CFP-2"
}'
# ⚠️ ALWAYS use absolute path for prdPath — worker CWD is packages/system-bus/
```

**PRD format** (Zod-validated):
```json
{
  "name": "Project Name",
  "context": {},
  "stories": [
    {
      "id": "STORY-1",
      "title": "What to build",
      "description": "Details",
      "priority": 1,
      "acceptance": ["criterion 1", "criterion 2"],
      "files": ["path/to/relevant/file.ts"]
    }
  ]
}
```

**Critical:**
- `context` must be `{}` or object — NEVER null or string
- Every story needs `priority` (number)
- **NEVER set `retries: 0`** on Inngest functions — breaks restart safety (ADR-0156)

## Event Types

### Pipelines
| Event | Chain |
|-------|-------|
| `pipeline/video.download` | → video-download → transcript-process → content-summarize |
| `pipeline/transcript.process` | → transcript-process → content-summarize |
| `content/summarize` | → content-summarize |
| `content/updated` | → content-sync (git commit vault changes) |
| `docs/ingest` | → docs-ingest (PDF/markdown → vector store) |

### Memory
| Event | Chain |
|-------|-------|
| `memory/session.compaction.pending` | → observe-session |
| `memory/session.ended` | → observe-session |
| `memory/observations.accumulated` | → reflect |
| `memory/observations.reflected` | → promote (if proposals pending) |

### Agent Loops
| Event | Flow |
|-------|------|
| `agent/story.start` | → story-pipeline (implement → prove → judge) |
| `agent/loop.started` | → plan → story pipeline → complete |
| `agent/loop.story.passed` | → plan (next story) |
| `agent/loop.story.failed` | → plan (retry or next) |
| `agent/loop.completed` | → complete (merge-back + cleanup) |

### Gateway & Channels
| Event | Purpose |
|-------|---------|
| `gateway/message.received` | Incoming message from any channel |
| `gateway/heartbeat` | Gateway health ping |
| `channel/telegram.callback` | Telegram callback queries |

### Subscriptions & Discovery
| Event | Purpose |
|-------|---------|
| `discovery/noted` | URL/idea captured → enrichment pipeline |
| `subscriptions/check` | Poll feeds for new items |

### System & Scheduled
| Event | Purpose |
|-------|---------|
| `system/log` | System log entry |
| `system/health.check` | Scheduled health monitoring |
| `cron/daily-digest` | Morning digest generation |
| `cron/check-email` | Periodic email scan |
| `cron/check-calendar` | Calendar check |
| `cron/nightly-maintenance` | Typesense + system maintenance |

### Notifications
| Event | Source |
|-------|--------|
| `webhook/github` | GitHub webhook events |
| `webhook/vercel` | Vercel deploy events |
| `webhook/todoist` | Todoist webhook events |
| `webhook/front` | Front webhook events |

## Debugging Failed Runs

```bash
joelclaw runs --status FAILED              # 1. Find the failure
joelclaw run <RUN_ID>                      # 2. Step trace + inline errors
joelclaw logs errors                       # 3. Worker stderr
joelclaw logs server --grep error          # 4. Inngest server errors
joelclaw otel search "error" --hours 1     # 5. OTEL telemetry
```

### Common Failure Patterns

| Symptom | Cause | Fix |
|---------|-------|-----|
| Events accepted but functions never run | Inngest can't reach worker | `joelclaw refresh`, check worker pod |
| "Unable to reach SDK URL" | Worker unreachable from cluster | Restart worker, `joelclaw refresh` |
| Loop story SKIPPED | Tests/typecheck failed in worktree | Check attempt output |
| Run stuck in RUNNING | Worker crashed mid-step | `joelclaw logs errors`, restart worker |
| `INNGEST_PORT` env collision | k8s service named `inngest` | Service is `inngest-svc` — keep this |
| Implement step killed on deploy | Worker restart killed in-flight step | ADR-0156: retries: 2 survives this |

### Stale RUNNING forensics (SDK unreachable ghosts)

When `joelclaw runs --status RUNNING` shows old health jobs that never clear:

1. **Use the operator command first**
   - Preview: `joelclaw inngest sweep-stale-runs`
   - Apply (backup + transaction): `joelclaw inngest sweep-stale-runs --apply`
2. **Validate the symptom class**
   - `joelclaw run <run-id>`
   - Look for trace/finalization errors containing `Unable to reach SDK URL` or `EOF writing request to SDK`.
3. **Treat list vs detail disagreements as a known mask issue**
   - `runs` list can show stale metadata.
   - `run` detail + trace/history is the source of truth.
4. **Raw runtime DB edits are last resort only**
   - Inngest state is in k8s StatefulSet PVC: `inngest-0:/data/main.db`.
   - Backup first: `kubectl -n joelclaw exec inngest-0 -- sqlite3 /data/main.db '.backup /data/main.db.pre-sweep-<ts>.sqlite'`.
5. **Terminalize stale runs with full contract, not partial edits**
   - Insert missing `history.type='FunctionCancelled'` for stale runs.
   - Ensure `function_finishes` row exists.
   - Then set `trace_runs.status=500` (cancelled) for stale candidates.
6. **Verify after mutation**
   - `joelclaw run <run-id>` should resolve terminal state.
   - `joelclaw runs --status RUNNING` should only show genuinely active runs.

Never mutate `main.db` without a point-in-time backup.

## Deploying Worker Changes

Use the publish script — it handles build, push, k8s apply, and rollout:
```bash
~/Code/joelhooks/joelclaw/k8s/publish-system-bus-worker.sh
```

See the [sync-system-bus skill](../sync-system-bus/SKILL.md) for the full deploy workflow.

## Key Paths

| What | Path |
|------|------|
| CLI source | `packages/cli/src/` |
| CLI commands | `packages/cli/src/commands/` |
| CLI binary | `~/.bun/bin/joelclaw` |
| Worker source | `packages/system-bus/` |
| Inngest functions | `packages/system-bus/src/inngest/functions/` |
| Function index (host) | `packages/system-bus/src/inngest/functions/index.host.ts` |
| Function index (cluster) | `packages/system-bus/src/inngest/functions/index.cluster.ts` |
| Inference utility | `packages/system-bus/src/lib/inference.ts` |
| Gateway source | `packages/gateway/` |
| k8s manifests | `k8s/` |
| Deploy script | `k8s/publish-system-bus-worker.sh` |
| ADRs | `~/Vault/docs/decisions/` |
| System log | `~/Vault/system/system-log.jsonl` |
| Loop attempt output | `/tmp/agent-loop/{loopId}/{storyId}-{attempt}.out` |

## Building the CLI

```bash
cd ~/Code/joelhooks/joelclaw
bun build packages/cli/src/cli.ts --compile --outfile ~/.bun/bin/joelclaw
```

**Test after every change:**
```bash
joelclaw status
joelclaw send --help
joelclaw runs --count 1
```

CLI commands are in `packages/cli/src/commands/`, one file per command. Follow the [cli-design skill](../cli-design/SKILL.md). Heavy deps must be lazy-loaded — top-level import crashes are unacceptable.

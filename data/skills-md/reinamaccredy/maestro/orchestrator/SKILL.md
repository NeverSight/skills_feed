---
name: orchestrator
description: Multi-agent parallel execution with autonomous workers. Use when plan.md has Track Assignments section or user triggers /conductor-orchestrate, "run parallel", "spawn workers". MUST load maestro-core skill first for routing.
---

# Orchestrator - Multi-Agent Parallel Execution

> **Spawn autonomous workers to execute tracks in parallel using Agent Mail coordination.**

## Agent Mail: CLI Primary, MCP Fallback

This skill uses a **lazy-load pattern** for Agent Mail:

| Priority | Tool | When Available |
|----------|------|----------------|
| **Primary** | `bun toolboxes/agent-mail/agent-mail.js` | Always (via Bash) |
| **Fallback** | MCP tools (via `mcp.json`) | When skill loaded + MCP server running |

**Detection flow:**
```
1. Try CLI: bun toolboxes/agent-mail/agent-mail.js health-check
   ↓ success? → Use CLI for all Agent Mail operations
   ↓ fails?
2. Fallback: MCP tools (lazy-loaded via skills/orchestrator/mcp.json)
```

**CLI benefits:** Zero token cost until used, no MCP server dependency.

## Core Principles

- **Load core first** - Load [maestro-core](../maestro-core/SKILL.md) for routing table and fallback policies
- **CLI first** - Use `bun toolboxes/agent-mail/agent-mail.js` CLI before falling back to MCP tools
- **Pre-register workers** before spawning (Agent Mail validates recipients)
- **Workers own their beads** - can `bd claim/close` directly (unlike sequential mode)
- **File reservations prevent conflicts** - reserve before edit, release on complete
- **Summary before exit** - all workers MUST send completion message
- **TDD by default** - workers follow RED → GREEN → REFACTOR cycle (use `--no-tdd` to disable)

## When to Use

| Trigger | Condition |
|---------|-----------| 
| Auto-routed | `/conductor-implement` when plan has Track Assignments |
| File-scope | `/conductor-implement` when ≥2 non-overlapping file groups detected |
| Direct | `/conductor-orchestrate` or `co` |
| Phrase | "run parallel", "spawn workers", "dispatch agents" |
| **See also** | `ca` for [autonomous execution](../conductor/references/workflows/autonomous.md) |

## Auto-Trigger Behavior

Parallel execution starts **automatically** when detected - no confirmation needed:

```
📊 Parallel execution detected:
- Track A: 2 tasks (src/api/)
- Track B: 2 tasks (lib/)
- Track C: 1 task (schemas/)

⚡ Spawning workers...
```

## Quick Reference

| Action | Tool |
|--------|------|
| Parse plan.md | `Read("conductor/tracks/<id>/plan.md")` |
| Initialize | `bun toolboxes/agent-mail/agent-mail.js macro-start-session` |
| Spawn workers | `Task()` for each track |
| Monitor | `bun toolboxes/agent-mail/agent-mail.js fetch-inbox` |
| Resolve blockers | `bun toolboxes/agent-mail/agent-mail.js reply-message` |
| Complete | `bun toolboxes/agent-mail/agent-mail.js send-message`, `bd close epic` |
| Track threads | `bun toolboxes/agent-mail/agent-mail.js summarize-thread` |
| Auto-routing | Auto-detect parallel via `metadata.json.beads` |

## 8-Phase Orchestrator Protocol

0. **Preflight** - Session identity, detect active sessions
1. **Read Plan** - Parse Track Assignments from plan.md
2. **Validate** - Health check Agent Mail CLI (HALT if unavailable)
3. **Initialize** - ensure_project, register orchestrator + all workers
4. **Spawn Workers** - Task() for each track (parallel)
5. **Monitor + Verify** - fetch_inbox, verify worker summaries
   - Workers use track threads (`TRACK_THREAD`) for bead-to-bead context
6. **Resolve** - reply_message for blockers
7. **Complete** - Send summary, close epic, `rb` review

See [references/workflow.md](references/workflow.md) for full protocol.

## Worker 4-Step Protocol

All workers MUST follow this exact sequence:

```
┌──────────────────────────────────────────────────────────────────────────────┐
│  STEP 1: INITIALIZE  - bun toolboxes/agent-mail/agent-mail.js macro-start-session   │
│  STEP 2: EXECUTE     - claim beads, do work, close beads                            │
│  STEP 3: REPORT      - bun toolboxes/agent-mail/agent-mail.js send-message          │
│  STEP 4: CLEANUP     - bun toolboxes/agent-mail/agent-mail.js release-file-reservations │
└──────────────────────────────────────────────────────────────────────────────┘
```

| Step | Tool | Required |
|------|------|----------|
| 1 | `bun toolboxes/agent-mail/agent-mail.js macro-start-session` | ✅ FIRST |
| 2 | `bd update`, `bd close` | ✅ |
| 3 | `bun toolboxes/agent-mail/agent-mail.js send-message` | ✅ LAST |
| 4 | `bun toolboxes/agent-mail/agent-mail.js release-file-reservations` | ✅ |

**Critical rules:**
- ❌ Never start work before `macro-start-session`
- ❌ Never return without `send-message` to orchestrator
- ❌ Never touch files outside assigned scope

See [references/worker-prompt.md](references/worker-prompt.md) for full template.

## Agent Routing

| Intent Keywords | Agent Type | File Reservation |
|-----------------|------------|------------------|
| `research`, `find`, `locate` | Research | None (read-only) |
| `review`, `check`, `audit` | Review | None (read-only) |
| `plan`, `design`, `architect` | Planning | `conductor/tracks/**` |
| `implement`, `build`, `create` | Execution | Task-specific scope |
| `fix`, `debug`, `investigate` | Debug | None (read-only) |

See [references/intent-routing.md](references/intent-routing.md) for mappings.

## Anti-Patterns

| ❌ Don't | ✅ Do |
|----------|-------|
| Spawn workers without pre-registration | Register all workers BEFORE spawning |
| Skip completion summary | Always send_message before exit |
| Ignore file reservation conflicts | Wait or resolve before proceeding |
| Use orchestration for simple tasks | Use sequential `/conductor-implement` |

## Lazy References

Load references only when needed:

| Phase | Trigger Condition | Reference |
|-------|-------------------|-----------|
| Always | On skill load | SKILL.md (this file) |
| Phase 3 (Initialize) | Setting up Agent Mail, project registration | [agent-mail.md](references/agent-mail.md) |
| Phase 4 (Spawn) | Before dispatching worker agents | [worker-prompt.md](references/worker-prompt.md) |
| Phase 6 (Handle Issues) | Cross-track dependencies, blocker resolution | [agent-coordination.md](references/agent-coordination.md) |

### All References

| Topic | File |
|-------|------|
| Full workflow | [workflow.md](references/workflow.md) |
| Architecture | [architecture.md](references/architecture.md) |
| Coordination modes | [coordination-modes.md](references/coordination-modes.md) |
| Agent Mail protocol | [agent-mail.md](references/agent-mail.md) |
| Agent Mail CLI | [agent-mail-cli.md](references/agent-mail-cli.md) |
| Worker prompt template | [worker-prompt.md](references/worker-prompt.md) |
| Preflight/session brain | [preflight.md](references/preflight.md) |
| Intent routing | [intent-routing.md](references/intent-routing.md) |
| Summary format | [summary-protocol.md](references/summary-protocol.md) |
| Auto-routing | [auto-routing.md](references/auto-routing.md) |
| Track threads | [track-threads.md](references/track-threads.md) |

## Related

- [maestro-core](../maestro-core/SKILL.md) - Routing and fallback policies
- [conductor](../conductor/SKILL.md) - Track management, `/conductor-implement`
- [tracking](../tracking/SKILL.md) - Issue tracking, `bd` commands

---
name: koko
displayName: Koko Development
description: Develop and extend Koko — the Elixir/OTP agent living alongside joelclaw. Covers OTP patterns, Redis bridge protocol, shadow execution, and workload implementation.
version: 1.0.0
author: joel
tags: [elixir, beam, otp, koko, agent]
---

# Koko Development

Use this skill when working on the Koko Elixir project — the BEAM co-resident agent alongside joelclaw.

## When to Use

- Building new GenServers, supervisors, or event handlers in Koko
- Implementing workloads (health pulse, event digest, shadow executor)
- Wiring Koko to new Redis channels or joelclaw events
- Debugging OTP supervision trees or process crashes
- Comparing Koko shadow results against TypeScript equivalents

Triggers: `koko`, `elixir agent`, `beam`, `otp`, `shadow executor`, `koko workload`, `koko event`, `mix`

## Project Location

- **Repo**: `~/Code/joelhooks/koko` ([github.com/joelhooks/koko](https://github.com/joelhooks/koko))
- **Host**: Overlook (Mac Mini M4 Pro), accessible via `ssh joel@panda`
- **AGENTS.md**: Full context in repo root

## ADR Awareness

**Always check relevant ADRs before implementing.** Koko's architecture is ADR-driven.

| ADR | Title | Status | URL |
|-----|-------|--------|-----|
| 0114 | Elixir/BEAM/Jido Migration | proposed | [joelclaw.com/adrs/0114-elixir-beam-jido-migration](https://joelclaw.com/adrs/0114-elixir-beam-jido-migration) |
| 0115 | Koko Project Charter | proposed | [joelclaw.com/adrs/0115-koko-project-charter](https://joelclaw.com/adrs/0115-koko-project-charter) |
| 0116 | Redis Bridge Protocol | proposed | [joelclaw.com/adrs/0116-koko-redis-bridge-protocol](https://joelclaw.com/adrs/0116-koko-redis-bridge-protocol) |
| 0117 | First Workloads | proposed | [joelclaw.com/adrs/0117-koko-first-workloads](https://joelclaw.com/adrs/0117-koko-first-workloads) |
| 0118 | Shadow Executor | proposed | [joelclaw.com/adrs/0118-koko-shadow-executor](https://joelclaw.com/adrs/0118-koko-shadow-executor) |

**Before adding a new workload**: Check ADR-0117 for the workload plan and ADR-0118 for shadow execution patterns.

**Before changing Redis integration**: Check ADR-0116 for the bridge protocol and phase boundaries.

**Before any architectural change**: Propose or update an ADR in `~/Vault/docs/decisions/`.

## Key Constraints

1. **Koko is read-only (Phase 1).** PubSub observer only. No LPUSH drain, no authoritative writes.
2. **Shadow results only.** Write to `joelclaw:koko:shadow:<function>` in Redis or local files. Never to Typesense, Todoist, gateway, or any production state.
3. **If Koko crashes, nothing breaks.** The TypeScript stack doesn't depend on it.
4. **Redis at localhost:6379** — k8s NodePort on Overlook.

## Development Commands

```bash
# Run
cd ~/Code/joelhooks/koko
mix deps.get
mix run --no-halt

# Test
mix test

# Interactive
iex -S mix
Koko.events_seen()

# Format
mix format

# Remote (from another machine)
ssh joel@panda "cd ~/Code/joelhooks/koko && mix run --no-halt"
```

## OTP Patterns to Follow

- **One GenServer per concern** — health checker, event accumulator, shadow runner are separate processes
- **Supervisor strategy**: `one_for_one` unless processes are coupled (then `rest_for_one`)
- **Pattern match event types** in `handle_info` — don't use if/else chains
- **Use `Logger.info("[koko]")`** prefix for all log output
- **Crash early** — let supervisors handle recovery, don't defensive-code around failures

## Implementation Phases

### Phase 1: Passive Observer (current)
- Subscribe to `joelclaw:gateway:events` via PubSub ✅
- Log and classify events ✅
- Next: Add health pulse GenServer (Workload 1 from ADR-0117)

### Phase 2: Dedicated Channel
- Create `joelclaw:koko:events` for claimed work
- TypeScript fans out to Koko: `LPUSH joelclaw:koko:events <payload>`
- Koko writes results to `joelclaw:koko:results`

### Phase 3: Shadow Executor
- Mirror select Inngest functions as Koko GenServers
- Same inputs, parallel execution, compare results
- Shadow log at `joelclaw:koko:shadow:<function>`

### Phase 4: Graduation
- Koko handles a workload more reliably than TypeScript
- Survived 30 days without manual intervention
- DX is enjoyable

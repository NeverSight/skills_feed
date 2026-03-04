---
name: gateway
displayName: Gateway
description: "Operate the joelclaw gateway daemon — the always-on pi session that receives events, notifications, and messages. Use the joelclaw CLI for ALL gateway operations. Use when: 'restart gateway', 'gateway status', 'is gateway healthy', 'push to gateway', 'gateway not responding', 'telegram not working', 'messages not going through', 'gateway stuck', 'gateway debug', 'check gateway', 'drain queue', 'test gateway', 'stream events', or any task involving the gateway daemon."
version: 1.0.2
author: Joel Hooks
tags: [joelclaw, gateway, daemon, redis, telegram]
---

# Gateway Operations

The gateway daemon is the always-on pi session that receives events from Inngest functions, Telegram, and webhooks. It's the system's notification and communication layer.

**Rule: Always use `joelclaw gateway` CLI. Never use `launchctl`, `curl`, or log file grep directly.**

## CLI Commands

```bash
joelclaw gateway status    # Sessions, queue depths, Redis health
joelclaw gateway restart   # Roll daemon, clean Redis, fresh session
joelclaw gateway enable    # Re-enable launch agent + start daemon
joelclaw gateway test      # Push test event, verify delivery
joelclaw gateway push --type <type> [--payload JSON]  # Push to all sessions
joelclaw gateway events    # Peek at pending events per session
joelclaw gateway drain     # Clear all event queues
joelclaw gateway stream    # NDJSON stream of all gateway events (ADR-0058)
```

`joelclaw gateway restart` is the canonical restart. It kills the process, cleans Redis state, re-enables `com.joel.gateway` if launchd disabled it, waits for launchd to respawn, and verifies the new session. `joelclaw gateway enable` is the direct recovery path when launchd drift disabled the service. Never use `launchctl bootout/bootstrap` directly.

## Quick Triage

Run in order, stop at first failure:

```bash
joelclaw gateway status    # 1. Is it alive? Sessions registered?
joelclaw gateway test      # 2. Can events flow end-to-end?
joelclaw gateway events    # 3. Are events piling up? (backpressure)
joelclaw gateway restart   # 4. If stuck, restart
```

If `joelclaw gateway status` shows pending > 0 on sessions, the agent is mid-stream or stuck. If it persists after a minute, restart.

## Sending Events from Inngest Functions

Every Inngest function receives `gateway` via middleware (ADR-0035):

```typescript
async ({ event, step, ...rest }) => {
  const gateway = (rest as any).gateway as GatewayContext | undefined;

  await step.run("notify", async () => {
    if (!gateway) return;
    await gateway.notify("my.event.type", {
      message: "Human-readable summary",
      data: "structured-payload",
    });
  });
}
```

| Method | Purpose | Routing |
|--------|---------|---------|
| `gateway.progress(msg, extra?)` | Pipeline/loop progress | Origin session + central gateway |
| `gateway.notify(type, payload?)` | Notifications (task done, webhook) | Origin session + central gateway |
| `gateway.alert(msg, extra?)` | System warnings (disk, service down) | Central gateway only |

Import: `import type { GatewayContext } from "../middleware/gateway";`

Always null-check `gateway` — functions can run without a gateway session.

## Low-Level: pushGatewayEvent()

For code outside the middleware:

```typescript
import { pushGatewayEvent } from "./agent-loop/utils";

await pushGatewayEvent({
  type: "video.downloaded",
  source: "inngest/video-download",
  payload: { message: "Downloaded: My Talk" },
  originSession: event.data.originSession,
});
```

## Common Failure Modes

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| Status shows healthy but messages don't arrive | Session stuck mid-stream on hung tool call | `joelclaw gateway restart` |
| Pending events growing on a session | Agent processing or blocked | Wait 1min, then `joelclaw gateway restart` |
| Telegram messages not delivered | HTML parsing error in response | Check `joelclaw gateway status`, restart |
| Gateway restarts every few seconds | Crash loop — bad secret lease or code error | Check `/tmp/joelclaw/gateway.err`, fix cause |
| Redis connection failed | Redis pod down | `joelclaw status` to check k8s health |

## Architecture

```
launchd (com.joel.gateway)
  └─ gateway-start.sh (leases secrets, sets env)
       └─ bun run daemon.ts
            ├─ createAgentSession() → headless pi session (reads SOUL.md)
            ├─ Redis channel (joelclaw:notify:gateway)
            ├─ Telegram channel (@JoelClawPandaBot)
            ├─ WebSocket (port 3018, for TUI attach)
            ├─ Command queue (serial — one prompt at a time)
            └─ Heartbeat runner (periodic autonomous checks)
```

The gateway reads `~/.pi/agent/` at boot for identity/prompt context (SOUL.md, AGENTS.md, MEMORY.md, daily log), but the **gateway extension itself is context-local**:

- Canonical source: `~/Code/joelhooks/joelclaw/pi/extensions/gateway/index.ts`
- Active path: `~/.joelclaw/gateway/.pi/extensions/gateway` (symlink)
- Do **not** install/restore `~/.pi/agent/extensions/gateway` globally

Daemon startup enforces this invariant and will fail if local extension is missing or a global gateway extension is detected.

This keeps gateway automation hooks out of normal interactive pi sessions.

## Key Files

| File | Purpose |
|------|---------|
| `packages/gateway/src/daemon.ts` | Daemon entry — session creation, channels, heartbeat |
| `packages/gateway/src/channels/redis.ts` | Redis subscribe, drain, prompt build |
| `packages/gateway/src/channels/telegram.ts` | Telegram bot channel |
| `packages/gateway/src/command-queue.ts` | Serial FIFO queue → `session.prompt()` |
| `packages/gateway/src/heartbeat.ts` | Periodic autonomous task runner |
| `packages/system-bus/src/inngest/middleware/gateway.ts` | Middleware injecting `gateway` context |
| `packages/cli/src/commands/gateway.ts` | CLI subcommands |
| `~/.joelclaw/scripts/gateway-start.sh` | launchd start script |
| `/tmp/joelclaw/gateway.{log,err,pid}` | Runtime logs and PID |

## Related

- ADR-0038: Gateway daemon architecture
- ADR-0049: Gateway hung session detection + bash timeout
- ADR-0058: Gateway NDJSON streaming
- Skill: [joelclaw](../joelclaw/SKILL.md) — event bus CLI
- Skill: [webhooks](../webhooks/SKILL.md) — inbound webhook providers

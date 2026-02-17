---
name: cli-design
description: "Design and build agent-first CLIs with HATEOAS JSON responses, context-protecting output, and self-documenting command trees. Use when creating new CLI tools, adding commands to existing CLIs (joelclaw, slog, igs), or reviewing CLI design for agent-friendliness. Triggers on 'build a CLI', 'add a command', 'CLI design', 'agent-friendly output', or any task involving command-line tool creation."
---

# Agent-First CLI Design

CLIs in this system are **agent-first, human-distant-second**. Every command returns structured JSON that an agent can parse, act on, and follow. Humans are welcome to pipe through `jq`.

## Core Principles

### 1. JSON always

Every command returns JSON. No plain text. No tables. No color codes. Agents parse JSON; they don't parse prose.

```bash
# This is the ONLY output format
joelclaw status
# → { "ok": true, "command": "joelclaw status", "result": {...}, "next_actions": [...] }
```

No `--json` flag. No `--human` flag. JSON is the default and only format.

### 2. HATEOAS — every response tells you what to do next

Every response includes `next_actions` — an array of commands the agent can run next, with descriptions. The agent never has to guess what's available.

```json
{
  "ok": true,
  "command": "joelclaw send pipeline/video.download",
  "result": {
    "event_id": "01KHF98SKZ7RE6HC2BH8PW2HB2",
    "status": "accepted"
  },
  "next_actions": [
    {
      "command": "joelclaw run 01KHF98SKZ7RE6HC2BH8PW2HB2",
      "description": "Check run status for this event"
    },
    {
      "command": "joelclaw logs --follow",
      "description": "Watch worker logs in real-time"
    },
    {
      "command": "joelclaw health",
      "description": "Check system health"
    }
  ]
}
```

`next_actions` are **contextual** — they change based on what just happened. A failed command suggests different next steps than a successful one.

### 3. Self-documenting command tree

The root command (no args) returns the full command tree so an agent can discover everything in one call:

```json
{
  "ok": true,
  "command": "joelclaw",
  "result": {
    "description": "JoelClaw — personal AI system CLI",
    "health": { "server": {...}, "worker": {...} },
    "commands": [
      { "name": "send", "description": "Send event to Inngest", "usage": "joelclaw send <event> -d '<json>'" },
      { "name": "status", "description": "System status", "usage": "joelclaw status" },
      { "name": "health", "description": "Health check all services", "usage": "joelclaw health" }
    ]
  },
  "next_actions": [...]
}
```

### 4. Context-protecting output

Agents have finite context windows. CLI output must not blow them up.

**Rules:**
- Terse by default — minimum viable output
- Auto-truncate large outputs (logs, lists) at a reasonable limit
- When truncated, include a file path to the full output
- Never dump raw logs, full transcripts, or unbounded lists

```json
{
  "ok": true,
  "command": "joelclaw logs",
  "result": {
    "lines": 20,
    "total": 4582,
    "truncated": true,
    "full_output": "/var/folders/.../joelclaw-logs-abc123.log",
    "entries": ["...last 20 lines..."]
  },
  "next_actions": [
    { "command": "joelclaw logs --tail 100", "description": "Show more log lines" }
  ]
}
```

### 5. Errors suggest fixes

When something fails, the response includes a `fix` field — plain language telling the agent what to do about it.

```json
{
  "ok": false,
  "command": "joelclaw send pipeline/video.download",
  "error": {
    "message": "Inngest server not responding",
    "code": "SERVER_UNREACHABLE"
  },
  "fix": "Start the Inngest server: cd ~/Code/system-bus && docker compose up -d",
  "next_actions": [
    { "command": "joelclaw health", "description": "Re-check system health after fix" },
    { "command": "docker ps", "description": "Check if Docker containers are running" }
  ]
}
```

## Response Envelope

Every command uses this exact shape:

### Success

```typescript
{
  ok: true,
  command: string,          // the command that was run
  result: object,           // command-specific payload
  next_actions: Array<{
    command: string,        // exact command to copy-paste/run
    description: string     // what it does
  }>
}
```

### Error

```typescript
{
  ok: false,
  command: string,
  error: {
    message: string,        // what went wrong
    code: string            // machine-readable error code
  },
  fix: string,              // plain-language suggested fix
  next_actions: Array<{
    command: string,
    description: string
  }>
}
```

### Reference implementations

- `slog` — `~/Code/system-bus/` (Effect CLI, system log)
- `igs` — `~/Code/system-bus/` (Effect CLI, Inngest operations)

Both follow this exact envelope. Copy their patterns.

## Implementation

### Framework: Effect CLI (@effect/cli)

All CLIs use `@effect/cli` with Bun. This is non-negotiable — consistency across the system matters more than framework preference.

```typescript
import { Command, Options } from "@effect/cli"
import { NodeContext, NodeRuntime } from "@effect/platform-node"

const send = Command.make("send", {
  event: Options.text("event"),
  data: Options.optional(Options.text("data").pipe(Options.withAlias("d"))),
}, ({ event, data }) => {
  // ... execute, return JSON envelope
})

const root = Command.make("joelclaw", {}, () => {
  // Root: return health + command tree
}).pipe(Command.withSubcommands([send, status, health]))
```

### Binary distribution

Build with Bun, install to `~/.bun/bin/`:

```bash
bun build src/cli.ts --compile --outfile joelclaw
cp joelclaw ~/.bun/bin/
```

### Adding a new command

1. Define the command with `Command.make`
2. Return the standard JSON envelope (ok, command, result, next_actions)
3. Include contextual `next_actions` — what makes sense AFTER this specific command
4. Handle errors with the error envelope (ok: false, error, fix, next_actions)
5. Add to the root command's subcommands
6. Add to the root command's `commands` array in the self-documenting output
7. Rebuild and install

## Anti-Patterns

| Don't | Do |
|-------|-----|
| Plain text output | JSON envelope |
| Tables with ANSI colors | JSON arrays |
| `--json` flag to opt into JSON | JSON is the only format |
| Dump 10,000 lines | Truncate + file pointer |
| `Error: something went wrong` | `{ ok: false, error: {...}, fix: "..." }` |
| Undiscoverable commands | Root returns full command tree |
| Static help text | HATEOAS next_actions |
| `console.log("Success!")` | `{ ok: true, result: {...} }` |
| Exit code as the only error signal | Error in JSON + exit code |
| Require the agent to read --help | Root command self-documents |

## Naming Conventions

- Commands are **nouns or verbs**, lowercase, no hyphens: `send`, `status`, `health`, `logs`
- Subcommands follow naturally: `joelclaw memory search`, `joelclaw loop start`
- Flags use `--kebab-case`: `--max-quality`, `--follow`
- Short flags for common options: `-d` for `--data`, `-f` for `--follow`
- Event names use `domain/action`: `pipeline/video.download`, `content/summarize`

## Checklist for New Commands

- [ ] Returns JSON envelope (ok, command, result, next_actions)
- [ ] Error responses include fix field
- [ ] Root command lists this command in its tree
- [ ] Output is context-safe (truncated if potentially large)
- [ ] next_actions are contextual to what just happened
- [ ] No plain text output anywhere
- [ ] No ANSI colors or formatting
- [ ] Works when piped (no TTY detection)
- [ ] Builds and installs to ~/.bun/bin/

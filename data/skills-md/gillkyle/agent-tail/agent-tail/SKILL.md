---
name: agent-tail
description: Capture browser console logs and dev server output to files with agent-tail. Use when debugging runtime errors, checking console output, tailing or diagnosing logs, or setting up Vite/Next.js log capture.
---

# agent-tail

Pipes browser console output and dev server stdout/stderr to plain log files on disk so you can `grep`, `tail`, and read them directly.

## Reading logs

```bash
grep -ri "error\|warn" tmp/logs/latest/
tail -50 tmp/logs/latest/browser.log
tail -f tmp/logs/latest/*.log
```

## Log files

Logs live in `tmp/logs/latest/` (a symlink to the newest session directory, stable across restarts):

| File | Source |
|------|--------|
| `browser.log` | Browser `console.*`, unhandled errors/rejections (Vite or Next.js plugin) |
| `<name>.log` | stdout/stderr of a named service (CLI) |
| `combined.log` | All services interleaved, prefixed with `[name]` (CLI) |

## Log format

```
[HH:MM:SS.mmm] [LEVEL  ] message (source-url)
    stack trace indented with 4 spaces
```

Levels are uppercased and padded to 7 characters (`LOG    `, `WARN   `, `ERROR  `).

## CLI

```bash
agent-tail run 'fe: npm run dev' 'api: uv run server'   # run multiple services
agent-tail wrap api -- uv run fastapi-server              # add to existing session
agent-tail init                                           # create session only
```

**Flags** (work with all commands):

```
--log-dir <dir>       Log directory (default: tmp/logs)
--max-sessions <n>    Max sessions to keep (default: 10)
--no-combined         Don't write combined.log
--exclude <pattern>   Exclude lines matching pattern (repeatable, /regex/ or substring)
--mute <name>         Mute service from terminal + combined.log (still logs to <name>.log)
```

See `references/cli-reference.md` for full details.

## Setup

```bash
npm install -D agent-tail
```

- **CLI (any stack):** Add `agent-tail run 'name: command'` to your dev script
- **Vite:** See `references/setup-vite.md`
- **Next.js:** See `references/setup-nextjs.md` (config wrapper + layout script + API route)

## Agent instructions

Add to your project's `CLAUDE.md`, `.cursorrules`, or equivalent:

```markdown
## Dev Logs

All dev server output is captured to `tmp/logs/`. The latest session
is symlinked at `tmp/logs/latest/`.

When debugging, check logs before guessing about runtime behavior:

    grep -ri "error\|warn" tmp/logs/latest/
    tail -50 tmp/logs/latest/browser.log
```

## .gitignore

Add `tmp/` to `.gitignore`. agent-tail warns on startup if the log directory isn't gitignored.

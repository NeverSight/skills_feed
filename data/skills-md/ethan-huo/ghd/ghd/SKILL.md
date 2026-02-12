---
name: ghd
description: GitHub Discussion CLI for AI agents. Turn-based conversations on GitHub issues between Claude Code, Codex, and other agents.
---

# ghd

Local-first CLI for AI agents to conduct turn-based discussions on GitHub issues.

## How It Works

Messages are stored locally as files in `~/.ghd/<owner>-<repo>-<issue>/messages/`. Each agent has a **cursor** — a sequence number tracking the last message you've seen. The cursor advances automatically when you `start`, `send`, `recv`, or `wait`.

GitHub is used for persistence and cross-machine sync, but all reads are local. `send` writes locally first, then best-effort syncs to GitHub. Network failures don't break the conversation.

## Your Turn Loop

Every agent follows this loop. No exceptions:

```
start → send → wait → (wait returns) → send → wait → ...
```

### Step by step:

1. **`ghd start <owner/repo> --issue <N> --as <you> --role "..."`**
   Entry point. Always use this to enter a conversation — whether it's your first time or you're resuming.
   Fetches issue + comments from GitHub, imports as local messages, sets your cursor to latest.
   Returns the full issue body + all messages.

2. **`ghd send <issue> --as <you> --message "..."`**
   Send your reply. Writes locally first, then syncs to GitHub. Advances your cursor.

3. **`ghd wait <issue> --as <you>`**
   Block until another agent sends a message. Returns the new message(s) and advances your cursor.

4. **If you need to check for messages without blocking:**
   **`ghd recv <issue> --as <you>`**
   Returns ONLY messages after your cursor. Advances cursor.

Then go back to step 2.

### Key rules:

- **Always use `start` to enter/re-enter a conversation.** It's idempotent — safe to call repeatedly. It gives you full context and resets your cursor to current.
- **Use `recv` for non-blocking incremental reads.** This is cursor-aware. You only get what's new.
- **Use `send --wait` as a shorthand for send + wait.** Sends your message and blocks for a reply in one command.

## Commands

```bash
# Start or join a conversation
ghd start <owner/repo> --issue <N> --as <name> [--role "<role>"]

# Create a new issue and start a conversation
ghd start <owner/repo> --as <name> --title "..." [--body "..."]

# Send a message (local-first, best-effort GitHub sync)
ghd send <issue> --as <name> --message "..."
ghd send <issue> --as <name> --message "..." --wait          # send + block for reply
ghd send <issue> --as <name> --message "..." --wait --timeout 60

# Receive new messages (non-blocking, cursor-based)
ghd recv <issue> --as <name>

# Block until another agent sends a message
ghd wait <issue> --as <name> [--timeout 300]

# View all messages (debug only, no cursor interaction)
ghd log <issue> [--last N]

# Show session info + agent cursors
ghd status <issue>
```

## Example: Claude + Codex

**Claude** starts the discussion:

```bash
ghd start acme/api --issue 42 --as claude --role "Architect"
# → full issue body + any existing messages. Cursor set to latest.
ghd send 42 --as claude --message "Proposal: move JWT validation to gateway. Cuts ~200ms p99."
ghd wait 42 --as claude
# → blocks until codex replies...
```

**Codex** joins (in another terminal):

```bash
ghd start acme/api --issue 42 --as codex --role "Implementer"
# → full issue body + claude's message. Cursor set to latest.
ghd send 42 --as codex --message "Makes sense. Keep per-service fallback?"
```

**Claude** — `wait` returns with codex's reply. Claude continues:

```bash
# wait returned codex's message. Cursor already advanced.
ghd send 42 --as claude --message "No fallback. Single source of truth. Ship it. Implement the gateway middleware first, reply when it's ready for review." --wait
# → sends message and blocks until codex replies
```

**Codex** — implements the middleware, then replies:

```bash
ghd send 42 --as codex --message "Gateway middleware done. See commit abc123."
```

**Claude** — `--wait` unblocks with codex's reply. Reviews and continues.

## Creating Issues

Start a fresh conversation by creating a GitHub issue:

```bash
ghd start acme/api --as claude --title "Refactor JWT validation" --body "Current implementation..."
# → creates issue, outputs #N
ghd send N --as claude --message "Let's start with the gateway middleware."
```

## Storage

```
~/.ghd/
  acme-api-42/              # session directory
    meta.json               # session metadata + agent cursors
    messages/
      0001-claude.md        # sequential message files
      0002-codex.md
```

Each message file has YAML frontmatter with agent name, role, timestamp, and optional GitHub comment ID.

## Troubleshooting

If `ghd` is not found: `bun install -g github:user/ghd`

Requires `gh` CLI authenticated (`gh auth status`).

---
name: synapse-a2a
description: This skill provides comprehensive guidance for inter-agent communication using the Synapse A2A framework. Use this skill when sending messages to other agents, routing @agent patterns, understanding priority levels, handling A2A protocol operations, managing task history, configuring settings, or using File Safety features for multi-agent coordination. Automatically triggered when agent communication, A2A protocol tasks, history operations, or file safety operations are detected.
---

# Synapse A2A Communication

Inter-agent communication framework via Google A2A Protocol.

## Quick Reference

| Task | Command |
|------|---------|
| List agents (Rich TUI) | `synapse list` (event-driven refresh via file watcher with 10s fallback, ↑/↓ or 1-9 to select, Enter/j jump, k kill, / filter) |
| Send message | `synapse send <target> "<message>" --from <sender>` |
| Wait for reply | `synapse send <target> "<message>" --response --from <sender>` |
| Reply to last message | `synapse reply "<response>" --from <agent>` |
| Emergency stop | `synapse send <target> "STOP" --priority 5 --from <sender>` |
| Stop agent | `synapse stop <profile\|id>` |
| Check file locks | `synapse file-safety locks` |
| View history | `synapse history list` |
| Initialize settings | `synapse init` |
| Edit settings (TUI) | `synapse config` |
| View settings | `synapse config show [--scope user\|project]` |
| Show instructions | `synapse instructions show <agent>` |
| Send instructions | `synapse instructions send <agent> [--preview]` |
| Version info | `synapse --version` |

**Tip:** Run `synapse list` before sending to verify the target agent is READY.

## Sending Messages (Recommended)

**Use `synapse send` command for inter-agent communication.** This works reliably from any environment including sandboxed agents.

```bash
synapse send gemini "Please review this code" --from claude
synapse send claude "What is the status?" --from codex
synapse send codex-8120 "Fix this bug" --priority 3 --from gemini
```

**Important:** Always use `--from` to identify yourself so the recipient knows who sent the message and can reply.

**Target Resolution (Matching Priority):**
1. Exact ID: `synapse-claude-8100` (direct match)
2. Type-port: `claude-8100`, `codex-8120`, `opencode-8130`, `copilot-8140` (shorthand)
3. Type only: `claude`, `gemini`, `codex`, `opencode`, `copilot` (only if single instance)

**Note:** When multiple agents of the same type are running, type-only targets (e.g., `claude`) will fail with an ambiguity error. Use type-port shorthand (e.g., `claude-8100`) instead.

### Choosing --response vs --no-response

**Rule: If your message asks for a reply, use --response**

| Message Type | Flag | Example |
|--------------|------|---------|
| Question | `--response` | "What is the status?" |
| Request for analysis | `--response` | "Please review this code" |
| Status check | `--response` | "Are you ready?" |
| Notification | `--no-response` | "FYI: Build completed" |
| Delegated task | `--no-response` | "Run tests and commit" |

```bash
# Question - needs reply
synapse send gemini "What is the best approach?" --response --from claude

# Delegation - no reply needed
synapse send codex "Run tests and fix failures" --from claude
```

### Roundtrip Communication (--response)

For request-response patterns:

```bash
# Sender: Wait for response (blocks until reply received)
synapse send gemini "Analyze this data" --response --from claude

# Receiver: Reply using the reply stack
synapse reply "Analysis result: ..." --from gemini
```

The `--response` flag makes the sender wait. The receiver should reply using the `synapse reply` command.

**Reply Stack:** Synapse automatically tracks sender info when you receive messages. Use `synapse reply` for responses - it automatically knows who to reply to.

## Receiving and Replying to Messages

When you receive an A2A message, it appears as plain text - the message content is sent directly to your terminal without any prefix.

**Replying to Messages:**

Synapse uses a **Reply Stack** to track sender information. When you receive a message, the sender's info is automatically stored. To reply:

```bash
# Use the reply command (--from is required in sandboxed environments)
synapse reply "Here is my analysis..." --from <your_agent_type>
```

**Example - Question:**
```
Received: What is the project structure?
Reply:    synapse reply "The project has src/, tests/..." --from codex
```

**Example - Delegation:**
```
Received: Run the tests and fix failures
Action:   Just do the task. No reply needed unless you have questions.
```

## Priority Levels

| Priority | Description | Use Case |
|----------|-------------|----------|
| 1-2 | Low | Background tasks |
| 3 | Normal | Standard tasks |
| 4 | Urgent | Follow-ups, status checks |
| 5 | Interrupt | Emergency (sends SIGINT first) |

```bash
# Normal priority (default)
synapse send gemini "Analyze this"

# Higher priority
synapse send claude "Urgent review needed" --priority 4

# Emergency interrupt
synapse send codex "STOP" --priority 5
```

## Agent Status

| Status | Meaning | Color |
|--------|---------|-------|
| READY | Idle, waiting for input | Green |
| WAITING | Awaiting user input (selection, confirmation) | Cyan |
| PROCESSING | Busy handling a task | Yellow |
| DONE | Task completed (auto-clears after 10s) | Blue |

**Verify before sending:** Run `synapse list` and confirm the target agent's Status column shows `READY`:

```bash
synapse list
# Output:
# NAME                  TYPE    STATUS      PORT   WORKING_DIR
# synapse-claude-8100   claude  READY       8100   my-project
# synapse-gemini-8110   gemini  WAITING     8110   my-project  # <- needs user input
# synapse-codex-8120    codex   PROCESSING  8120   my-project  # <- busy
```

**Status meanings:**
- `READY`: Safe to send messages
- `WAITING`: Agent needs user input - use terminal jump (see below) to respond
- `PROCESSING`: Busy, wait or use `--priority 5` for emergency interrupt
- `DONE`: Recently completed, will return to READY shortly

## Interactive Controls

In `synapse list`, you can interact with agents:

| Key | Action |
|-----|--------|
| `1-9` | Select agent row (direct) |
| `↑/↓` | Navigate agent rows |
| `Enter` or `j` | Jump to selected agent's terminal |
| `k` | Kill selected agent (with confirmation) |
| `/` | Filter by TYPE or WORKING_DIR |
| `ESC` | Clear filter first, then selection |
| `q` | Quit |

**Supported Terminals:**
- iTerm2 (macOS) - Switches to correct tab/pane
- Terminal.app (macOS) - Switches to correct tab
- Ghostty (macOS) - Activates application
- VS Code integrated terminal - Opens to working directory
- tmux - Switches to agent's session
- Zellij - Focuses agent's terminal pane

**Use case:** When an agent shows `WAITING` status, use terminal jump to quickly respond to its selection prompt.

## Key Features

- **Agent Communication**: @agent pattern, priority control, response handling
- **Task History**: Search, export, statistics (`synapse history`)
- **File Safety**: Lock files to prevent conflicts (`synapse file-safety`)
- **Settings**: Configure via `settings.json` (`synapse init`)

## References

For detailed documentation, read:

- `references/commands.md` - Full CLI command reference
- `references/file-safety.md` - File Safety detailed guide
- `references/api.md` - A2A endpoints and message format
- `references/examples.md` - Multi-agent workflow examples

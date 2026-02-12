---
name: agent-notifier
description: >
  Multi-platform, multi-channel notification skill for AI code agents.
  Sends notifications (sound, macOS alert, Telegram, Email, Slack, Discord)
  when the agent needs user interaction or completes a task.
  Supports Claude Code, GitHub Copilot CLI, Cursor, Codex, and Aider.
license: Apache-2.0
metadata:
  author: crossoverJie
  version: "1.0"
---

# Agent Notifier Skill

Deterministic, hook-driven notifications for AI code agents. Never miss when your agent needs input or finishes a task.

## Why

LLM-based "play a sound when done" prompts are unreliable — context compression drops them, and the model's judgement of "done" is inconsistent. This skill uses each platform's **Hooks system** for guaranteed triggering.

## Prerequisites

- **Python 3** (standard library only, no external dependencies)
- At least one supported AI agent platform

## Supported Platforms

| Platform | Hook Event |
|----------|-----------|
| Claude Code | `Notification` (idle_prompt, permission_prompt) |
| GitHub Copilot CLI | `sessionEnd`, `postToolUse` |
| Cursor | `stop`, `afterFileEdit` |
| Codex | `agent-turn-complete` |
| Aider | `--notifications-command` |

## Quick Start

```bash
# Interactive setup — detects platforms, configures channels, installs hooks
python3 skills/agent-notifier/setup.py
```

### Copilot CLI Users

Copilot CLI loads hooks from the project's `.github/hooks/` directory (no global hook support). Create the hook file in **each project** where you want notifications:

```bash
mkdir -p .github/hooks
cat > .github/hooks/agent-notifier.json << 'EOF'
{
  "version": 1,
  "hooks": {
    "sessionEnd": [
      {"type": "command", "bash": "python3 $HOME/.claude/skills/agent-notifier/notify.py"}
    ],
    "postToolUse": [
      {"type": "command", "bash": "python3 $HOME/.claude/skills/agent-notifier/notify.py"}
    ]
  }
}
EOF
```

## Manual Usage

```bash
# Test with simulated Claude Code event
echo '{"notification_type":"idle_prompt","message":"Waiting for input"}' | python3 skills/agent-notifier/notify.py

# Test with command-line args (Aider style)
python3 skills/agent-notifier/notify.py "Task completed"
```

## Notification Channels

| Channel | Default | Requirements |
|---------|---------|-------------|
| Sound | Enabled | macOS (`afplay`) or Linux (`paplay`/`aplay`) |
| macOS Notification | Enabled | macOS only |
| Telegram | Disabled | Bot token + Chat ID |
| Email | Disabled | SMTP credentials |
| Slack | Disabled | Incoming Webhook URL |
| Discord | Disabled | Webhook URL |

## Configuration

Config file is searched in order:
1. `~/.claude/notify-config.json`
2. `skills/agent-notifier/notify-config.json` (template)

Run `python3 skills/agent-notifier/setup.py` to configure interactively, or edit the JSON directly.

## Output

Notifications are sent concurrently to all enabled channels. Individual channel failures are logged to stderr without affecting other channels.

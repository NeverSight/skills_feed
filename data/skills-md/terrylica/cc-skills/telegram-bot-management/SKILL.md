---
name: telegram-bot-management
description: Telegram bot management and monitoring. TRIGGERS - telegram bot, claude-orchestrator, bot status, bot restart.
---

# Telegram Bot Management

## Overview

Multi-workspace Telegram bot workflow orchestration with full supervision (launchd + watchexec). Manages the claude-orchestrator Telegram bot for headless Claude Code interactions.

## When to Use This Skill

- Check bot status, restart, or troubleshoot issues
- Monitor bot health and resource usage
- View bot logs and debug problems
- Manage bot lifecycle (start/stop/restart)

## Production Mode

As of v5.8.0, production mode is the only operational mode.

## Bot Management Commands

### Check Status

```bash
bot-service.sh status
# Or use alias
bot status
```

Shows:

- launchd supervision status
- watchexec process (PID, uptime, memory)
- Bot process (PID, uptime, memory)
- Full process tree
- Recent log activity

### View Logs

```bash
bot-service.sh logs
# Or use alias
bot logs
```

Tails all logs:

- Launchd logs (supervision layer)
- Bot logs (application layer)

### Restart Bot

```bash
bot-service.sh restart
# Or use alias
bot restart
```

Rarely needed due to automatic code reload via watchexec.

### Stop Bot

```bash
bot-service.sh stop
# Or use alias
bot stop
```

---

## Reference Documentation

For detailed information, see:

- [Operational Commands](./references/operational-commands.md) - Status, restart, logs, monitoring commands
- [Troubleshooting](./references/troubleshooting.md) - Common issues and diagnostic steps

---

## Troubleshooting

| Issue                    | Cause                         | Solution                                      |
| ------------------------ | ----------------------------- | --------------------------------------------- |
| Bot not responding       | Process crashed               | Run `bot status` to check, then `bot restart` |
| launchd not starting     | Service not loaded            | Load with `launchctl load` command            |
| Logs empty               | Log rotation or path issue    | Verify log path in launchd plist              |
| watchexec not reloading  | File patterns not matching    | Check watchexec filter patterns               |
| High memory usage        | Memory leak in bot code       | Restart bot, investigate Python memory usage  |
| Permission denied        | Script not executable         | Run `chmod +x bot-service.sh`                 |
| Environment vars missing | .env not loaded               | Verify environment setup in launchd plist     |
| Multiple bot instances   | Previous instance not stopped | Kill all bot processes, then restart cleanly  |

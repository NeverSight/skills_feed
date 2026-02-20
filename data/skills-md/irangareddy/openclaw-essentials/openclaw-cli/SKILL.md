---
name: openclaw-cli
description: Master the OpenClaw CLI - gateway, agents, channels, skills, hooks, and automation
---

# OpenClaw CLI

Complete reference for openclaw command-line interface operations.

## When to Use

Managing OpenClaw gateway, agents, channels, skills, hooks, and automation.

## Core Commands

### Setup & Onboarding

**Initial setup:**
```bash
# Quick onboarding with daemon install
openclaw onboard --install-daemon

# Setup workspace and config
openclaw setup --workspace ~/.openclaw/workspace

# Interactive configuration
openclaw configure
```

**Health check:**
```bash
openclaw doctor
```

### Gateway Management

**Run gateway:**
```bash
# Interactive mode
openclaw gateway

# With specific port
openclaw gateway --port 18789

# With tailscale
openclaw gateway --tailscale serve
```

**Gateway service:**
```bash
# Install as system service
openclaw gateway install

# Control service
openclaw gateway start
openclaw gateway stop
openclaw gateway restart
openclaw gateway status
```

**Gateway health:**
```bash
openclaw status
openclaw status --deep     # Probe channels
openclaw health
```

### Agent Management

**List agents:**
```bash
openclaw agents list
openclaw agents list --bindings    # Show routing
```

**Add agent:**
```bash
# Interactive wizard
openclaw agents add <name>

# Non-interactive
openclaw agents add dev \
  --workspace ~/.openclaw/workspace-dev \
  --model claude-sonnet-4.5 \
  --non-interactive
```

**Delete agent:**
```bash
openclaw agents delete <id>
```

**Set identity:**
```bash
# From IDENTITY.md
openclaw agents set-identity --agent main --from-identity

# Explicit values
openclaw agents set-identity --agent main \
  --name "MyAgent" \
  --emoji "🤖" \
  --avatar avatars/bot.png
```

### Skills Management

**List skills:**
```bash
openclaw skills list
openclaw skills list --eligible    # Only ready skills
openclaw skills list --json        # JSON output
```

**Skill info:**
```bash
openclaw skills info <skill-name>
```

**Check eligibility:**
```bash
openclaw skills check
```

### Hooks Management

**List hooks:**
```bash
openclaw hooks list
openclaw hooks list --eligible
openclaw hooks list --verbose      # Show missing requirements
```

**Hook info:**
```bash
openclaw hooks info <hook-name>
```

**Enable/disable:**
```bash
openclaw hooks enable session-memory
openclaw hooks disable command-logger
```

**Install hooks:**
```bash
# From npm
openclaw hooks install @openclaw/my-hooks

# Local directory
openclaw hooks install ./my-hooks

# Link (development)
openclaw hooks install -l ./my-hooks
```

**Update hooks:**
```bash
openclaw hooks update <id>
openclaw hooks update --all
```

### Channel Management

**List channels:**
```bash
openclaw channels list
```

**Channel status:**
```bash
openclaw channels status
openclaw channels status --probe
```

**Add channel:**
```bash
# Interactive
openclaw channels add

# Telegram bot
openclaw channels add --channel telegram \
  --account alerts \
  --name "Alerts Bot" \
  --token $TELEGRAM_BOT_TOKEN

# Discord
openclaw channels add --channel discord \
  --account work \
  --token $DISCORD_BOT_TOKEN
```

**Remove channel:**
```bash
openclaw channels remove --channel telegram --account alerts
openclaw channels remove --channel discord --account work --delete
```

**WhatsApp login:**
```bash
openclaw channels login --channel whatsapp
```

**Channel logs:**
```bash
openclaw channels logs
openclaw channels logs --channel whatsapp --lines 100
```

### Models & Authentication

**Status:**
```bash
openclaw models status
openclaw models status --probe               # Live check
openclaw models status --probe-provider anthropic
```

**List models:**
```bash
openclaw models list
openclaw models list --all
openclaw models list --provider anthropic
```

**Set default:**
```bash
openclaw models set claude-sonnet-4.5
openclaw models set-image claude-sonnet-4.5
```

**Auth setup:**
```bash
# Anthropic (recommended)
claude setup-token
openclaw models auth setup-token --provider anthropic

# Or paste token
openclaw models auth paste-token --provider anthropic
```

**Fallbacks:**
```bash
openclaw models fallbacks list
openclaw models fallbacks add claude-opus-4.6
openclaw models fallbacks remove claude-haiku-4.5
openclaw models fallbacks clear
```

**Scan for models:**
```bash
openclaw models scan
openclaw models scan --set-default
```

### Messaging

**Send message:**
```bash
openclaw message send \
  --target +15555550123 \
  --message "Hello from OpenClaw"

# Discord channel
openclaw message send \
  --channel discord \
  --target channel:123456 \
  --message "Deployment complete"
```

**Send poll:**
```bash
openclaw message poll \
  --channel discord \
  --target channel:123 \
  --poll-question "Lunch?" \
  --poll-option "Pizza" \
  --poll-option "Sushi"
```

**Other message operations:**
```bash
openclaw message read --target +15555550123
openclaw message react --target <id> --emoji "👍"
openclaw message edit --target <id> --message "Updated"
openclaw message delete --target <id>
```

### Browser Control

**Status & control:**
```bash
openclaw browser status
openclaw browser start
openclaw browser stop
openclaw browser tabs
```

**Navigate:**
```bash
openclaw browser open https://example.com
openclaw browser navigate https://example.com --target-id <id>
```

**Interact:**
```bash
openclaw browser click "#submit-button"
openclaw browser type "#email" "user@example.com"
openclaw browser press Enter
```

**Capture:**
```bash
openclaw browser screenshot
openclaw browser screenshot --full-page
openclaw browser snapshot --format ai
```

**Profiles:**
```bash
openclaw browser profiles
openclaw browser create-profile --name dev
openclaw browser delete-profile --name old
```

### Nodes & Devices

**List nodes:**
```bash
openclaw nodes list
openclaw nodes status --connected
```

**Node operations:**
```bash
# Describe node
openclaw nodes describe --node <id>

# Run command on node
openclaw nodes run --node <id> --cwd /path -- ls -la

# Notify (macOS)
openclaw nodes notify --node <id> \
  --title "Build Complete" \
  --body "Success" \
  --sound default
```

**Camera:**
```bash
openclaw nodes camera list --node <id>
openclaw nodes camera snap --node <id> --facing front
openclaw nodes camera clip --node <id> --duration 10s
```

**Canvas:**
```bash
openclaw nodes canvas snapshot --node <id>
openclaw nodes canvas present --node <id> --target index.html
openclaw nodes canvas hide --node <id>
```

**Screen recording:**
```bash
openclaw nodes screen record --node <id> --duration 30s
```

### System Commands

**System event:**
```bash
openclaw system event --text "Deployment complete" --mode now
```

**Heartbeat:**
```bash
openclaw system heartbeat last
openclaw system heartbeat enable
openclaw system heartbeat disable
```

**Presence:**
```bash
openclaw system presence
```

### Cron Jobs

**List jobs:**
```bash
openclaw cron list
openclaw cron list --all
openclaw cron status
```

**Add job:**
```bash
# System event every hour
openclaw cron add \
  --name "hourly-check" \
  --every "1h" \
  --system-event "Hourly check"

# Message at specific time
openclaw cron add \
  --name "morning-reminder" \
  --at "09:00" \
  --message "Good morning!"
```

**Manage jobs:**
```bash
openclaw cron enable <id>
openclaw cron disable <id>
openclaw cron rm <id>
openclaw cron run <id>
```

**Job runs:**
```bash
openclaw cron runs --id <id> --limit 10
```

### Configuration

**Get/set config:**
```bash
# Get value
openclaw config get agents.defaults.model.primary

# Set value
openclaw config set agents.defaults.model.primary "claude-sonnet-4.5"

# Unset value
openclaw config unset some.config.path
```

### Memory Operations

**Memory status:**
```bash
openclaw memory status
```

**Index memory:**
```bash
openclaw memory index
```

**Search memory:**
```bash
openclaw memory search "GraphQL implementation patterns"
```

### Logs

**Tail logs:**
```bash
openclaw logs
openclaw logs --follow
openclaw logs --limit 200
openclaw logs --json
```

### Sandbox

**List sandboxes:**
```bash
openclaw sandbox list
```

**Recreate sandbox:**
```bash
openclaw sandbox recreate
```

### Security

**Security audit:**
```bash
openclaw security audit
openclaw security audit --deep
openclaw security audit --fix
```

### Plugins

**List plugins:**
```bash
openclaw plugins list
openclaw plugins list --json
```

**Plugin info:**
```bash
openclaw plugins info <plugin-id>
```

**Install plugin:**
```bash
openclaw plugins install <path-or-spec>
```

**Enable/disable:**
```bash
openclaw plugins enable <id>
openclaw plugins disable <id>
```

**Plugin health:**
```bash
openclaw plugins doctor
```

### Update & Maintenance

**Update OpenClaw:**
```bash
openclaw update
```

**Reset config:**
```bash
openclaw reset --scope config
openclaw reset --scope config+creds+sessions
openclaw reset --scope full
```

**Uninstall:**
```bash
openclaw uninstall --service
openclaw uninstall --state
openclaw uninstall --workspace
openclaw uninstall --all
```

## Global Flags

**Available everywhere:**
```bash
--dev               # Use ~/.openclaw-dev for isolation
--profile <name>    # Use ~/.openclaw-<name>
--no-color         # Disable ANSI colors
--json             # Machine-readable output
-V, --version      # Show version
```

## Common Workflows

### First-Time Setup

```bash
# 1. Onboard with daemon
openclaw onboard --install-daemon

# 2. Pair WhatsApp (or other channel)
openclaw channels login

# 3. Start gateway
openclaw gateway

# 4. Test with message
openclaw message send --target +1234567890 --message "Test"
```

### Multi-Agent Setup

```bash
# 1. Add agent
openclaw agents add work --workspace ~/.openclaw/workspace-work

# 2. Set identity
openclaw agents set-identity --agent work --from-identity

# 3. Add binding (in openclaw.json)
# bindings: [{ agentId: "work", match: { channel: "discord" } }]

# 4. List to verify
openclaw agents list --bindings
```

### Hook Automation

```bash
# 1. Enable session memory hook
openclaw hooks enable session-memory

# 2. Enable command logger
openclaw hooks enable command-logger

# 3. Verify
openclaw hooks check

# 4. Restart gateway
openclaw gateway restart
```

### Channel Setup

```bash
# 1. Add Telegram bot
openclaw channels add --channel telegram \
  --account alerts \
  --token $TELEGRAM_BOT_TOKEN

# 2. Verify
openclaw channels status

# 3. Send test message
openclaw message send --channel telegram \
  --target <chat-id> \
  --message "Bot online"
```

### Model Configuration

```bash
# 1. Setup auth
claude setup-token

# 2. Set default model
openclaw models set claude-sonnet-4.5

# 3. Add fallbacks
openclaw models fallbacks add claude-opus-4.6
openclaw models fallbacks add claude-haiku-4.5

# 4. Verify
openclaw models status
```

## Debugging

**Check gateway status:**
```bash
openclaw status --deep
openclaw doctor
openclaw health
```

**View logs:**
```bash
openclaw logs --follow
openclaw channels logs --lines 200
```

**Test channel:**
```bash
openclaw channels status --probe
```

**Check skills/hooks:**
```bash
openclaw skills check
openclaw hooks check
openclaw plugins doctor
```

## Tips

1. **Use `--json` for scripting** - All commands support JSON output
2. **Profile isolation** - Use `--profile` for testing without affecting main config
3. **Doctor fixes** - Run `openclaw doctor` regularly to catch issues
4. **Logs location** - `~/.openclaw/logs/` for file logs
5. **Config location** - `~/.openclaw/openclaw.json`
6. **Workspace** - `~/.openclaw/workspace` (or custom path)

## Resources

- [OpenClaw Docs](https://docs.openclaw.org/)
- [CLI Reference](https://docs.openclaw.org/cli/)
- [Multi-Agent Routing](https://docs.openclaw.org/concepts/multi-agent)
- [Hooks System](https://docs.openclaw.org/automation/hooks)
- [Skills System](https://docs.openclaw.org/tools/skills)

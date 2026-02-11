---
name: openclaw-self-healing
version: 2.0.1
description: 4-tier autonomous self-healing system for OpenClaw Gateway with persistent learning, reasoning logs, and multi-channel alerts. Features Claude Code as Level 3 emergency doctor for AI-powered diagnosis and repair.
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": ["tmux", "claude", "jq"] },
        "install":
          [
            {
              "id": "tmux",
              "kind": "brew",
              "package": "tmux",
              "bins": ["tmux"],
              "label": "Install tmux (brew)",
            },
            {
              "id": "claude",
              "kind": "node",
              "package": "@anthropic-ai/claude-code",
              "bins": ["claude"],
              "label": "Install Claude Code CLI (npm)",
            },
            {
              "id": "jq",
              "kind": "brew",
              "package": "jq",
              "bins": ["jq"],
              "label": "Install jq (brew) - for metrics dashboard",
            },
          ],
      },
  }
---

# OpenClaw Self-Healing System

> **"The system that heals itself — or calls for help when it can't."**

A 4-tier autonomous self-healing system for OpenClaw Gateway.

## Architecture

```
Level 1: Watchdog (180s)     → Process monitoring (OpenClaw built-in)
Level 2: Health Check (300s) → HTTP 200 + 3 retries
Level 3: Claude Recovery     → 30min AI-powered diagnosis 🧠
Level 4: Discord Alert       → Human escalation
```

## What's Special (v2.0)

- **World's first** Claude Code as Level 3 emergency doctor
- **Persistent Learning** - Automatic recovery documentation (symptom → cause → solution → prevention)
- **Reasoning Logs** - Explainable AI decision-making process
- **Multi-Channel Alerts** - Discord + Telegram support
- **Metrics Dashboard** - Success rate, recovery time, trending analysis
- Production-tested (verified recovery Feb 5-6, 2026)
- macOS LaunchAgent integration

## Quick Setup

### 1. Install Dependencies

```bash
brew install tmux
npm install -g @anthropic-ai/claude-code
```

### 2. Configure Environment

```bash
# Copy template to OpenClaw config directory
cp .env.example ~/.openclaw/.env

# Edit and add your Discord webhook (optional)
nano ~/.openclaw/.env
```

### 3. Install Scripts

```bash
# Copy scripts
cp scripts/*.sh ~/openclaw/scripts/
chmod +x ~/openclaw/scripts/*.sh

# Install LaunchAgent
cp launchagent/com.openclaw.healthcheck.plist ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/com.openclaw.healthcheck.plist
```

### 4. Verify

```bash
# Check Health Check is running
launchctl list | grep openclaw.healthcheck

# View logs
tail -f ~/openclaw/memory/healthcheck-$(date +%Y-%m-%d).log
```

## Scripts

| Script | Level | Description |
|--------|-------|-------------|
| `gateway-healthcheck.sh` | 2 | HTTP 200 check + 3 retries + escalation |
| `emergency-recovery.sh` | 3 | Claude Code PTY session for AI diagnosis (v1) |
| `emergency-recovery-v2.sh` | 3 | Enhanced with learning + reasoning logs (v2) ⭐ |
| `emergency-recovery-monitor.sh` | 4 | Discord/Telegram notification on failure |
| `metrics-dashboard.sh` | - | Visualize recovery statistics (NEW) |

## Configuration

All settings via environment variables in `~/.openclaw/.env`:

| Variable | Default | Description |
|----------|---------|-------------|
| `DISCORD_WEBHOOK_URL` | (none) | Discord webhook for alerts |
| `OPENCLAW_GATEWAY_URL` | `http://localhost:18789/` | Gateway health check URL |
| `HEALTH_CHECK_MAX_RETRIES` | `3` | Restart attempts before escalation |
| `EMERGENCY_RECOVERY_TIMEOUT` | `1800` | Claude recovery timeout (30 min) |

## Testing

### Test Level 2 (Health Check)

```bash
# Run manually
bash ~/openclaw/scripts/gateway-healthcheck.sh

# Expected output:
# ✅ Gateway healthy
```

### Test Level 3 (Claude Recovery)

```bash
# Inject a config error (backup first!)
cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.bak

# Wait for Health Check to detect and escalate (~8 min)
tail -f ~/openclaw/memory/emergency-recovery-*.log
```

## Links

- **GitHub:** https://github.com/Ramsbaby/openclaw-self-healing
- **Docs:** https://github.com/Ramsbaby/openclaw-self-healing/tree/main/docs

## License

MIT License - do whatever you want with it.

Built by @ramsbaby + Jarvis 🦞

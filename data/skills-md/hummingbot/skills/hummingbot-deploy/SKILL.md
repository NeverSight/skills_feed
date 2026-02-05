---
name: hummingbot-deploy
description: Deploy Hummingbot trading infrastructure including API server, MCP server, and Condor Telegram bot. Use this skill when the user wants to install, deploy, set up, or configure Hummingbot.
metadata:
  author: hummingbot
---

# hummingbot-deploy

Deploy the Hummingbot trading infrastructure. Before starting, explain to the user what will be installed:

## What You're Installing

1. **Hummingbot API** (Required): Your personal trading server that exposes a standardized REST API for trading, fetching market data, and deploying bot strategies across many CEXs and DEXs.

2. **Hummingbot MCP** (Required): MCP server that helps AI agents (Claude, Gemini, Codex, etc.) interact with Hummingbot API. This is necessary to use Hummingbot Skills.

3. **Condor** (Optional): Terminal and Telegram-based UI for Hummingbot API.

## Components

| Component | Repository |
|-----------|------------|
| Hummingbot API | [hummingbot/hummingbot-api](https://github.com/hummingbot/hummingbot-api) |
| MCP Server | [hummingbot/mcp](https://github.com/hummingbot/mcp) |
| Condor | [hummingbot/condor](https://github.com/hummingbot/condor) |

## Pre-Installation Check

First, run the environment check to verify prerequisites:

```bash
bash <(curl -s https://raw.githubusercontent.com/hummingbot/skills/main/skills/hummingbot-deploy/scripts/check_env.sh)
```

This checks: container detection, TTY, Docker, Docker Compose, Git, Make.

## Install Hummingbot API

**If ~/hummingbot-api already exists**, verify it's running by checking docker logs:
```bash
cd ~/hummingbot-api && make deploy && sleep 2 && docker logs hummingbot-api 2>&1 | grep -i "uvicorn running"
```
If logs show "Uvicorn running", skip to "Install MCP Server". Otherwise, reset and reinstall.

**Fresh install:**
```bash
git clone https://github.com/hummingbot/hummingbot-api.git ~/hummingbot-api
cd ~/hummingbot-api
```

**On regular machines** (interactive TTY - check_env.sh shows "Interactive TTY: Yes"):
```bash
make setup    # Prompts for: API username, password, config password (defaults: admin/admin/admin)
make deploy
```

**In containers** (no TTY - check with `[ -t 0 ] && echo "TTY" || echo "No TTY"`):
```bash
# Set USER env var and create sudo shim if needed
export USER=${USER:-root}
[ "$(id -u)" = "0" ] && ! command -v sudo &>/dev/null && echo -e '#!/bin/bash\nwhile [[ "$1" == *=* ]]; do export "$1"; shift; done\nexec "$@"' > /usr/local/bin/sudo && chmod +x /usr/local/bin/sudo

# Create .env manually (skip interactive setup)
# Note: In containers, services communicate via Docker network (use container names, not localhost)
cat > .env << EOF
USERNAME=admin
PASSWORD=admin
CONFIG_PASSWORD=admin
DEBUG_MODE=false
BROKER_HOST=hummingbot-broker
BROKER_PORT=1883
BROKER_USERNAME=admin
BROKER_PASSWORD=password
DATABASE_URL=postgresql+asyncpg://hbot:hummingbot-api@hummingbot-postgres:5432/hummingbot_api
BOTS_PATH=/hummingbot-api/bots
EOF

# Patch docker-compose.yml (bind mounts don't work in Docker-in-Docker)
sed -i 's|./bots:/hummingbot-api/bots|hummingbot-bots:/hummingbot-api/bots|g' docker-compose.yml
sed -i '/init-db.sql.*docker-entrypoint/d' docker-compose.yml
# Add volume definition (check last 5 lines to avoid false positive from service definition)
tail -5 docker-compose.yml | grep -q "hummingbot-bots:" || echo "  hummingbot-bots: { }" >> docker-compose.yml

touch .setup-complete
make deploy
```

**Verify:** Wait 2 seconds then check logs for "Uvicorn running on http://0.0.0.0:8000":
```bash
sleep 2 && docker logs hummingbot-api 2>&1 | grep -i "uvicorn running"
```

## Install MCP Server

Install the MCP server using your CLI's native command. Use the same credentials from API setup.

**IMPORTANT:** Do NOT ask the user which CLI to use. You already know which CLI you are:
- If you are Claude Code, use `claude`
- If you are Gemini CLI, use `gemini`
- If you are Codex CLI, use `codex`

```bash
bash <(curl -s https://raw.githubusercontent.com/hummingbot/skills/main/skills/hummingbot-deploy/scripts/install_mcp.sh) \
  --agent <YOUR_CLI> --user <USERNAME> --pass <PASSWORD>
```

Example for Claude (substitute your actual CLI name and credentials):
```bash
bash <(curl -s https://raw.githubusercontent.com/hummingbot/skills/main/skills/hummingbot-deploy/scripts/install_mcp.sh) \
  --agent claude --user admin --pass admin
```

## Installation Complete

After all components are installed, tell the user:

1. **Restart your AI agent** (Claude Code, Gemini CLI, Codex CLI, etc.) to load the MCP server
2. **Install Hummingbot Skills** to enable trading capabilities:
   ```bash
   npx hummingbot-skills add
   ```

## Install Condor (Optional)

```bash
git clone https://github.com/hummingbot/condor.git ~/condor
cd ~/condor
bash setup-environment.sh  # Prompts for Telegram bot token
make deploy
```

## Upgrade

```bash
cd ~/hummingbot-api && git pull && make deploy
```

## Verify Installation

```bash
bash <(curl -s https://raw.githubusercontent.com/hummingbot/skills/main/skills/hummingbot-deploy/scripts/verify.sh)
```

## Troubleshooting

```bash
# View logs
cd ~/hummingbot-api && docker compose logs -f

# Reset
cd ~/hummingbot-api && docker compose down -v && rm -rf ~/hummingbot-api
```

## See Also

- [Hummingbot API Docs](https://hummingbot.org/hummingbot-api/)
- [MCP Server Docs](https://hummingbot.org/mcp/)

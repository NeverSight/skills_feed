---
name: hummingbot-api-setup
description: Deploy Hummingbot infrastructure including API server, Condor Telegram bot, PostgreSQL, and Gateway for DEX trading. Use this skill when the user wants to install, deploy, or set up Hummingbot.
metadata:
  author: david-hummingbot
---

# hummingbot-api-setup

Deploy Hummingbot infrastructure using the official installer from [hummingbot/deploy](https://github.com/hummingbot/deploy).

## Quick Start

```bash
# Fresh install (Condor + API)
./scripts/setup.sh

# Install API only
./scripts/setup.sh --api

# Upgrade existing installation
./scripts/setup.sh --upgrade
```

## What Gets Installed

| Component | Description |
|-----------|-------------|
| **Condor** | Telegram bot interface for trading |
| **Hummingbot API** | REST API server for bot management |
| **PostgreSQL** | Database for configurations and history |
| **EMQX** | MQTT broker for real-time communication |

## Installation Options

```bash
./scripts/setup.sh [OPTIONS]

Options:
  --upgrade    Upgrade existing installation
  --api        Install only Hummingbot API (standalone)
  -h, --help   Show help message
```

## After Installation

### Hummingbot API
- **URL:** http://localhost:8000
- **Docs:** http://localhost:8000/docs
- **Default credentials:** admin/admin

### Condor (Telegram Bot)
1. Open Telegram
2. Search for your bot (configured during setup)
3. Use `/config` to add API servers
4. Use `/start` to begin trading

## Health Check

Verify installation is running:

```bash
./scripts/health_check.sh
```

## System Requirements

- **OS:** Linux or macOS
- **Docker:** Required (script will guide installation)
- **Disk Space:** 2GB minimum
- **Dependencies:** git, curl, make (auto-installed)

## Troubleshooting

### Docker not running

**macOS:**
```bash
open -a Docker
```

**Linux:**
```bash
sudo systemctl start docker
```

### Port conflicts

| Port | Service | Check |
|------|---------|-------|
| 8000 | API | `lsof -i :8000` |
| 5432 | PostgreSQL | `lsof -i :5432` |
| 1883 | EMQX | `lsof -i :1883` |

### View logs

```bash
cd ~/hummingbot-api && docker compose logs -f
cd ~/condor && docker compose logs -f
```

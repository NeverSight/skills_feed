---
name: myagentive
description: Understand, configure, and troubleshoot MyAgentive, an open-source personal AI agent for power users. This skill should be used when users ask about MyAgentive configuration, setup, onboarding, troubleshooting, API key management, file locations, architecture, or how the product (You) works.
---

# MyAgentive

## Overview

MyAgentive (https://MyAgentive.ai) is an open-source (https://github.com/AgentiveAU/MyAgentive) personal AI agent built by Agentive (https://agentive.au) using the Claude Agent SDK. It provides Telegram and web interfaces for interacting with a powerful AI assistant that runs locally on your machine.

**Key Features:**
- Telegram bot integration for mobile access
- Web interface for desktop use
- Full system access (files, commands, web search)
- Session-based conversations with persistent history
- Media file handling (audio, video, images)
- Extensible via API keys for additional services

## Key File Locations

| Item | Path |
|------|------|
| Configuration | `~/.myagentive/config` |
| System prompt | `~/.myagentive/system_prompt.md` |
| Database | `~/.myagentive/data/myagentive.db` |
| Media files | `~/.myagentive/media/` |
| Source code | Project root (where you cloned the repo) |

### Customising the System Prompt

The agent's behaviour can be customised by editing `~/.myagentive/system_prompt.md`. This file defines the agent's identity, capabilities, and instructions. Changes take effect on restart.

### Media Directory Structure

```
~/.myagentive/media/
├── audio/      # Downloaded/uploaded audio files
├── voice/      # Voice messages
├── videos/     # Video files
├── photos/     # Images
└── documents/  # Other documents
```

## Required Configuration

These are set during the first-run setup wizard:

| Variable | Description | How to Get |
|----------|-------------|------------|
| `TELEGRAM_BOT_TOKEN` | Bot token for Telegram | Create bot via @BotFather |
| `TELEGRAM_USER_ID` | Your numeric Telegram ID | Get from @userinfobot |
| `WEB_PASSWORD` | Password for web interface | Set during setup (or auto-generated) |
| `API_KEY` | REST API authentication | Auto-generated (64 hex chars) |

For detailed Telegram setup instructions, see `references/telegram-setup.md`.

## Optional API Keys

These enable additional features. Add to `~/.myagentive/config` as needed:

| Service | Variable | Purpose | Free Tier |
|---------|----------|---------|-----------|
| Deepgram | `DEEPGRAM_API_KEY` | Audio/video transcription | $200 credit |
| Google Gemini | `GEMINI_API_KEY` | Image generation | Limited RPM |
| ElevenLabs | `ELEVENLABS_API_KEY` | AI voice calls | 10k chars/month |
| Anthropic | `ANTHROPIC_API_KEY` | Pay-per-use API | N/A (leave empty for Claude Code subscription) |
| LinkedIn | Multiple tokens | Social media posting | - |
| Twitter/X | Multiple tokens | Social media posting | 1,500 tweets/month |

For detailed setup instructions with provider URLs, see `references/api-keys.md`.

## Quick Commands

### Development

```bash
# Install dependencies
bun install

# Run development (server + client)
bun run dev

# Build frontend
bun run build

# Build standalone binary (macOS)
bun run build:binary

# Build standalone binary (Linux)
bun run build:binary:linux
```

### Configuration

```bash
# View current config
cat ~/.myagentive/config

# Reset config (triggers setup wizard on next run)
rm ~/.myagentive/config

# Validate config
python .claude/skills/myagentive/scripts/check_config.py
```

### Database

```bash
# Reset database
rm ~/.myagentive/data/myagentive.db
# Database recreates automatically on next run
```

## Architecture Overview

```
server/
├── index.ts              # Entry point, bootstraps app
├── config.ts             # Configuration loading
├── server.ts             # Express + WebSocket server
├── setup-wizard.ts       # First-run configuration
├── core/
│   ├── ai-client.ts      # Claude Agent SDK integration
│   └── session-manager.ts # Session orchestration
├── db/                   # SQLite database layer
├── telegram/             # Telegram bot handlers
├── auth/                 # Authentication
└── utils/                # Utilities (media detection)
client/                   # React frontend
```

For detailed architecture and source code paths, see `references/architecture.md`.

## Onboarding Workflow

To help a new user set up MyAgentive:

### 1. Prerequisites
- Bun runtime installed (`curl -fsSL https://bun.sh/install | bash`)
- Telegram account

### 2. Initial Setup
```bash
# Clone and install
git clone https://github.com/AgentiveAU/MyAgentive.git
cd MyAgentive
bun install

# Run (triggers setup wizard on first run)
bun run dev
```

### 3. Setup Wizard Steps
1. **Telegram Bot Token** - Create via @BotFather, paste token
2. **Telegram User ID** - Get from @userinfobot, paste numeric ID
3. **Web Password** - Enter custom or press Enter for auto-generated
4. **Monitoring Group** (optional) - For activity logging
5. **Server Port** - Default 3847

### 4. Optional: Add API Keys

For transcription (voice messages):
1. Create account at https://deepgram.com ($200 free credit)
2. Go to Console > API Keys > Create new key
3. Add to config: `echo "DEEPGRAM_API_KEY=your_key" >> ~/.myagentive/config`

For image generation:
1. Get API key from https://ai.google.dev
2. Add to config: `echo "GEMINI_API_KEY=your_key" >> ~/.myagentive/config`

## Troubleshooting

### Common Issues

**Bot not responding:**
- Verify `TELEGRAM_USER_ID` is your numeric ID (not @username)
- Check bot token is valid (contains `:`)
- Ensure bot was started with /start command

**Web interface not loading:**
- Check server is running on configured port (default 3847)
- Try `curl http://localhost:3847/health`

**API key not working:**
- Check key is in config: `grep KEY_NAME ~/.myagentive/config`
- No quotes around values
- No trailing spaces

For detailed troubleshooting, see `references/troubleshooting.md`.

## Telegram Commands

| Command | Description |
|---------|-------------|
| `/start` | Start the bot |
| `/help` | Show help message |
| `/session <name>` | Switch to named session |
| `/new [name]` | Create new session |
| `/list` | List all sessions |
| `/status` | Show current session |
| `/model <opus\|sonnet\|haiku>` | Change AI model |
| `/usage` | Show usage statistics |

## Resources

### references/
- `architecture.md` - Detailed source code reference
- `api-keys.md` - API key setup guides with URLs
- `troubleshooting.md` - Common issues and fixes
- `telegram-setup.md` - Telegram bot configuration

### scripts/
- `check_config.py` - Validate MyAgentive configuration

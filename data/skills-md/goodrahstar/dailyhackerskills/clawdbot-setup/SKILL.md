---
name: clawdbot-setup
description: Complete installation and setup guide for Clawdbot - a personal AI assistant that runs 24/7. Use when the user wants to install Clawdbot from scratch, configure models (Gemini/Claude), set up Telegram bot, connect Gmail via Composio, or install the browser extension.
---

# Clawdbot Complete Setup

Complete guide for installing and configuring Clawdbot, a personal AI assistant that runs 24/7 and integrates with messaging channels, Gmail, and browser automation.

## Prerequisites

- Node.js ≥22 installed
- npm, pnpm, or bun package manager
- macOS, Linux, or Windows (WSL2 recommended)
- Telegram account (for bot setup)
- Google account (for Gmail integration, optional)
- Composio API key (for Gmail, optional)

## Phase 1: Core Installation

### Install Clawdbot

```bash
npm install -g clawdbot@latest
# or: pnpm add -g clawdbot@latest
```

### Initialize Configuration

```bash
clawdbot setup
```

This creates:
- Config: `~/.clawdbot/clawdbot.json`
- Workspace: `~/clawd`
- Sessions directory

### Configure Gateway

```bash
clawdbot config set gateway.mode local
clawdbot config set gateway.bind loopback
clawdbot config set gateway.port 18789
```

### Install Gateway Daemon

```bash
clawdbot onboard --install-daemon --non-interactive --accept-risk
```

This installs the gateway as a background service (LaunchAgent on macOS, systemd on Linux).

## Phase 2: Model Configuration

### Option A: Google Gemini (Recommended for Cost)

```bash
# Set primary model
clawdbot config set agents.defaults.model.primary "google/gemini-3-pro-preview"

# Configure model aliases
clawdbot config set agents.defaults.models."google/gemini-3-pro-preview".alias "gemini"
clawdbot config set agents.defaults.models."google/gemini-3-flash-preview".alias "gemini-flash"

# Add API key
clawdbot config set env.GEMINI_API_KEY "YOUR_GEMINI_API_KEY"
```

Get API key: https://aistudio.google.com/apikey

### Option B: Anthropic Claude

```bash
clawdbot config set agents.defaults.model.primary "anthropic/claude-opus-4-5"
# Then configure credentials:
clawdbot models configure
```

Get API key: https://console.anthropic.com/

### Verify Model

```bash
clawdbot models list
clawdbot agent --message "Hello" --agent main
```

## Phase 3: Telegram Bot Setup

### Create Telegram Bot

1. Open Telegram, search `@BotFather`
2. Send `/newbot`
3. Name your bot (e.g., "MyAssistant")
4. Choose username ending in "bot" (e.g., "myassistant_bot")
5. Copy the bot token

### Get Your User ID

1. Search `@userinfobot` or `@useridbot` on Telegram
2. Start the bot
3. Copy your user ID (numeric)

### Configure Telegram Channel

```bash
# Add Telegram channel
clawdbot channels add --channel telegram --token "YOUR_BOT_TOKEN"

# Set security (restrict to your user ID)
clawdbot config set channels.telegram.allowFrom '["YOUR_USER_ID"]'
clawdbot config set channels.telegram.dmPolicy "pairing"
```

### Approve Pairing (if needed)

When you first message the bot, you'll get a pairing code. Approve it:

```bash
clawdbot pairing approve telegram PAIRING_CODE
```

### Verify Telegram

```bash
clawdbot channels status
clawdbot health
```

Should show: `Telegram: ok (@your_bot_name)`

## Phase 4: Gmail Integration (Composio)

### Install Composio SDK

```bash
pip3 install composio
```

### Setup Gmail Connection

1. Get Composio API key from https://platform.composio.dev/
2. Connect Gmail account on Composio dashboard
3. Note the connected account ID (starts with `ca_`)

### Create MCP Server

```python
from composio import Composio

composio = Composio(api_key="YOUR_COMPOSIO_API_KEY")

# Create MCP server for Gmail
mcp_server = composio.mcp.create(
    name="clawdbot-gmail-server",
    toolkits=[{"toolkit": "gmail"}],
    allowed_tools=[
        "GMAIL_FETCH_EMAILS",
        "GMAIL_SEND_EMAIL",
        "GMAIL_CREATE_DRAFT",
        "GMAIL_LIST_LABELS",
        "GMAIL_GET_EMAIL"
    ]
)

# Generate user URL
mcp_instance = composio.mcp.generate(
    user_id="clawdbot-user",
    mcp_config_id=mcp_server.id
)
```

### Add Composio to Clawdbot Config

```bash
clawdbot config set env.COMPOSIO_API_KEY "YOUR_COMPOSIO_API_KEY"
```

### Alternative: Using gog CLI

```bash
# Install gog
brew install steipete/tap/gogcli

# Authorize Gmail
gog auth credentials /path/to/client_secret.json
gog auth add your-email@gmail.com --services gmail
```

## Phase 5: Browser Extension Setup

### Install Extension

```bash
clawdbot browser extension install
```

This installs to: `~/.clawdbot/browser/chrome-extension`

### Load in Chrome

1. Open Chrome → `chrome://extensions`
2. Enable "Developer mode" (top right)
3. Click "Load unpacked"
4. Select: `~/.clawdbot/browser/chrome-extension`
5. Pin the extension to toolbar

### Use Extension

1. Open the tab you want to control (e.g., Gmail)
2. Click the Clawdbot extension icon
3. Badge shows "ON" when attached
4. Bot can now control that tab

### Browser Status

```bash
clawdbot browser status
```

Should show:
- profile: chrome
- enabled: true
- controlUrl: http://127.0.0.1:18791
- cdpUrl: http://127.0.0.1:18792

## Phase 6: Verification & Testing

### Check System Status

```bash
clawdbot status
clawdbot health
clawdbot doctor
```

### Test Telegram Bot

Message your bot on Telegram:
- "Hello, are you working?"
- "check my last 10 emails"
- "what can you do?"

### Test Gmail Access

With browser extension attached to Gmail tab:
- "check my last 10 emails"
- "show me unread emails"
- "which emails need a response?"

## Common Issues & Fixes

### Gateway Won't Start

**Error**: `hooks.enabled requires hooks.token`

**Fix**: Disable hooks if not using webhooks:
```bash
clawdbot config set hooks.enabled false
clawdbot gateway restart
```

### Telegram Not Responding

**Check**:
1. Gateway is running: `clawdbot health`
2. Bot token is correct: `clawdbot channels status`
3. User ID is in allowlist: `clawdbot config get channels.telegram.allowFrom`
4. Pairing was approved: Check `~/.clawdbot/credentials/telegram-pairing.json`

**Fix**: Restart gateway and verify config:
```bash
clawdbot gateway restart
clawdbot channels status
```

### Browser Extension Shows "!"

**Error**: Extension badge shows "!" (relay not reachable)

**Fix**:
1. Ensure gateway is running: `clawdbot health`
2. Check browser status: `clawdbot browser status`
3. Verify relay is running (auto-started by gateway on port 18792)

### Model Not Responding

**Check**:
1. API key is set: `clawdbot config get env.GEMINI_API_KEY` (or ANTHROPIC_API_KEY)
2. Model is configured: `clawdbot models list`
3. Test directly: `clawdbot agent --message "test" --agent main`

**Fix**: Verify API key and restart gateway:
```bash
clawdbot config set env.GEMINI_API_KEY "YOUR_KEY"
clawdbot gateway restart
```

### Gmail Not Accessible

**Check**:
1. Composio account is connected: Check Composio dashboard
2. MCP server is created: Verify in Composio dashboard
3. Browser extension is attached: Badge shows "ON" on Gmail tab

**Fix**: Re-attach extension to Gmail tab and verify connection

## Configuration Files

- **Main config**: `~/.clawdbot/clawdbot.json`
- **Workspace**: `~/clawd/`
- **Credentials**: `~/.clawdbot/credentials/`
- **Logs**: `~/.clawdbot/logs/gateway.log`

## Useful Commands

```bash
# Status and health
clawdbot status
clawdbot health
clawdbot doctor

# Gateway control
clawdbot gateway restart
clawdbot gateway status

# Channel management
clawdbot channels status
clawdbot channels list

# Agent interaction
clawdbot agent --message "Your message" --agent main

# Browser control
clawdbot browser status
clawdbot browser extension path

# Configuration
clawdbot config get <key>
clawdbot config set <key> <value>

# Logs
clawdbot logs --follow
tail -f ~/.clawdbot/logs/gateway.log
```

## Security Best Practices

1. **Telegram Security**:
   - Always set `allowFrom` with your user ID
   - Use `dmPolicy: "pairing"` for additional security
   - Run `clawdbot doctor` to check for security issues

2. **Browser Extension**:
   - Only attach when needed
   - Detach when done
   - Consider using a dedicated Chrome profile

3. **API Keys**:
   - Store in config (encrypted by system keyring)
   - Never commit to git
   - Rotate if compromised

4. **Gateway**:
   - Keep on loopback (127.0.0.1) for local use
   - Use Tailscale Serve/Funnel for remote access
   - Require token authentication

## Next Steps After Setup

1. **Test basic functionality**: Message bot on Telegram
2. **Connect Gmail**: Set up Composio or gog CLI
3. **Install browser extension**: For web automation
4. **Add more channels**: WhatsApp, Slack, Discord
5. **Configure skills**: Install additional capabilities
6. **Set up automation**: Cron jobs, webhooks

## Resources

- **Documentation**: https://docs.clawd.bot
- **Getting Started**: https://docs.clawd.bot/start/getting-started
- **Configuration Reference**: https://docs.clawd.bot/gateway/configuration
- **Troubleshooting**: https://docs.clawd.bot/help/troubleshooting
- **GitHub**: https://github.com/clawdbot/clawdbot

## Quick Setup Checklist

- [ ] Clawdbot installed globally
- [ ] Gateway daemon installed and running
- [ ] Model configured (Gemini or Claude) with API key
- [ ] Telegram bot created and configured
- [ ] User ID added to allowlist
- [ ] Pairing approved (if required)
- [ ] Gmail connected (Composio or gog)
- [ ] Browser extension installed and loaded in Chrome
- [ ] Extension attached to Gmail tab (badge shows "ON")
- [ ] Test messages working on Telegram
- [ ] Gmail access tested and working

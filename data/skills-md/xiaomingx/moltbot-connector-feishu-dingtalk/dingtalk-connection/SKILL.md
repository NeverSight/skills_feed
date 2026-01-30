---
name: dingtalk-connection
description: Bridge DingTalk outgoing webhook messages to Clawdbot Gateway and send replies back to DingTalk sessions. Use when setting up DingTalk as a messaging channel, troubleshooting webhook delivery, or running the local bridge service.
---

# DingTalk Bridge

Bridge DingTalk bot messages to Clawdbot Gateway over a local WebSocket connection.

## Architecture

```
DingTalk user -> DingTalk cloud -> webhook (bridge.py) -> Clawdbot Gateway -> AI agent
```

## Setup

### 1. Create DingTalk bot

Create a bot that can send outgoing webhooks and set the callback URL to your public endpoint.

### 2. Run bridge

```bash
cd <skill-dir>/dingtalk-connection
uv sync
DINGTALK_SIGNING_SECRET=your_secret uv run python bridge.py
```

### 3. Auto-start (macOS)

```bash
uv run python setup_service.py
launchctl load ~/Library/LaunchAgents/com.clawdbot.dingtalk-bridge.plist
```

## Environment variables

| Variable | Required | Default |
|---|---|---|
| `DINGTALK_PORT` | — | `3210` |
| `DINGTALK_PATH` | — | `/dingtalk` |
| `DINGTALK_SIGNING_SECRET` | — | — |
| `DINGTALK_BOT_ID` | — | — |
| `DINGTALK_BOT_NAME` | — | — |
| `CLAWDBOT_CONFIG_PATH` | — | `~/.clawdbot/clawdbot.json` |
| `CLAWDBOT_AGENT_ID` | — | `main` |
| `DINGTALK_THINKING_THRESHOLD_MS` | — | `2500` |

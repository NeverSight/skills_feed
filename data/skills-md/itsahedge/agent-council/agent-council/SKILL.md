---
name: agent-council
description: Create autonomous AI agents with Discord bindings. Use when setting up new agents, managing agent cron jobs, or scheduling agent tasks. Covers agent creation, channel binding, cron job patterns, and delivery routing.
---

# Agent Council

Create and manage autonomous AI agents with full Discord integration.

## What It Does

1. **Creates agent workspace** (SOUL.md, HEARTBEAT.md, memory/)
2. **Creates Discord channel** (optional) with topic
3. **Binds agent to channel** (routing)
4. **Adds to allowlist** (permissions)
5. **Sets up cron jobs** (optional daily memory)

## Scripts

| Script | Purpose |
|--------|---------|
| `create-agent.sh` | Full agent setup with Discord integration |
| `bind-channel.sh` | Bind existing agent to additional channel |
| `list-agents.sh` | Show all agents and their Discord bindings |
| `remove-agent.sh` | Remove agent (config, crons, optionally workspace/channel) |
| `claim-category.sh` | Claim a Discord category for an agent |
| `sync-category.sh` | Sync all channels in a category to its owner |
| `list-categories.sh` | Show category ownership

## Usage

### Create Agent with New Discord Channel

```bash
export DISCORD_GUILD_ID="123456789012345678"  # Your server ID

~/.openclaw/skills/agent-council/scripts/create-agent.sh \
  --id watson \
  --name "Watson" \
  --emoji "🔬" \
  --specialty "Deep research and competitive analysis" \
  --create "research" \
  --category "987654321098765432"
```

This will:
- Create `~/workspace/agents/watson/` with SOUL.md, HEARTBEAT.md
- Create Discord #research channel in the specified category
- Set channel topic: "Watson 🔬 — Deep research and competitive analysis"
- Bind watson agent to #research
- Add #research to allowlist
- **Create daily memory cron at 11:00 PM** (default, use `--no-cron` to skip)

### Create Agent with Existing Channel

```bash
./create-agent.sh \
  --id sage \
  --name "Sage" \
  --emoji "💰" \
  --specialty "Personal finance" \
  --channel "234567890123456789"
```

### Bind Agent to Additional Channel

```bash
./bind-channel.sh --agent forge --channel "345678901234567890"
./bind-channel.sh --agent forge --create "defi" --category "456789012345678901"
```

### List Current Setup

```bash
./list-agents.sh
```

### Remove Agent

```bash
# Remove from config only (keeps workspace)
./remove-agent.sh --id test-agent

# Full removal
./remove-agent.sh --id test-agent --delete-workspace --delete-channel
```

### Category Ownership

Agents can own Discord categories. Channels in owned categories can be auto-bound.

```bash
# Claim a category for an agent
./claim-category.sh --agent chief --category 123456789012345678

# Claim and immediately sync all existing channels
./claim-category.sh --agent chief --category 123456789012345678 --sync

# List category ownership
./list-categories.sh

# Sync channels in a category to the owner
./sync-category.sh --category 123456789012345678
```

---

## Agent Cron Jobs

Agents can create and manage their own cron jobs. **Follow these patterns exactly** to ensure messages route to the correct Discord channel.

### Delivery Pattern

Two options for cron job delivery:

**Option A: `--announce` (preferred for simple jobs)**
Use `--announce --channel discord --to channel:<CHANNEL_ID>`. The gateway posts a summary to the channel automatically.

```bash
openclaw cron add \
  --name "My Task" \
  --agent myagent \
  --cron "0 9 * * *" \
  --session isolated \
  --model sonnet \
  --announce --channel discord --to "channel:YOUR_CHANNEL_ID" \
  --message "Do the task."
```

**Option B: `delivery: none` + message tool (for custom formatting)**
Have the agent send to Discord explicitly using the message tool in its payload. Use this when you need full control over formatting, mentions, or multi-message output.

```bash
openclaw cron add \
  --name "My Task" \
  --agent myagent \
  --cron "0 9 * * *" \
  --session isolated \
  --model sonnet \
  --message "Do the task. Then send the result to Discord using the message tool (action=send, channel=discord, target=channel:YOUR_CHANNEL_ID). Prepend <@OWNER_USER_ID>."
```

**⚠️ Common mistake:** Setting `--channel` to a channel ID instead of a platform name (e.g., `discord`). The `--channel` flag expects the platform, `--to` expects the destination.

### Creating a Cron Job That Posts to Discord

Use `sessionTarget: "isolated"` + `payload.kind: "agentTurn"`. The agent runs in a fresh session, does its work, and sends the result to its bound channel via the message tool.

```json
{
  "name": "My Scheduled Task",
  "schedule": { "kind": "cron", "expr": "0 9 * * *", "tz": "America/New_York" },
  "sessionTarget": "isolated",
  "payload": {
    "kind": "agentTurn",
    "message": "Do the task. Then send the result to Discord using the message tool (action=send, channel=discord, target=channel:YOUR_CHANNEL_ID). Prepend <@OWNER_USER_ID>.",
    "timeoutSeconds": 90
  },
  "delivery": { "mode": "none" },
  "enabled": true
}
```

**Key rules:**
- `delivery.mode` MUST be `"none"` — the payload handles its own delivery
- Include the Discord channel ID in the payload message text
- Include the owner's user ID for mentions
- Set a reasonable `timeoutSeconds` (default 60 is often too tight for tool-using tasks — use 90-120)
- Use `model` in the payload to override the agent's default model if needed (e.g., `"model": "sonnet"` for lighter tasks)

### Creating a One-Shot Reminder (Posts to Discord)

Even for simple reminders, use `sessionTarget: "isolated"` + `agentTurn` so the reminder actually posts to your Discord channel:

```json
{
  "name": "Reminder Name",
  "schedule": { "kind": "at", "at": "2026-02-14T12:00:00-05:00" },
  "sessionTarget": "isolated",
  "payload": {
    "kind": "agentTurn",
    "message": "Send a reminder to Discord using the message tool (action=send, channel=discord, target=channel:YOUR_CHANNEL_ID). Prepend <@OWNER_USER_ID>. Message: Your reminder text here.",
    "timeoutSeconds": 60
  },
  "delivery": { "mode": "none" },
  "deleteAfterRun": true,
  "enabled": true
}
```

**⚠️ Do NOT use `sessionTarget: "main"` + `systemEvent` for anything that should appear in Discord.** SystemEvents fire silently into the agent's session context — they do NOT post to any channel. If a user should see it, it MUST be an isolated agentTurn with explicit message tool delivery.

### Silent Cron Jobs (No Discord Post)

For maintenance tasks (memory compaction, index updates), use `delivery: { mode: "none" }` and don't include message tool instructions in the payload:

```json
{
  "name": "Nightly Maintenance",
  "schedule": { "kind": "cron", "expr": "0 23 * * *", "tz": "America/New_York" },
  "sessionTarget": "isolated",
  "payload": {
    "kind": "agentTurn",
    "message": "Run maintenance task. If nothing to do, reply HEARTBEAT_OK."
  },
  "delivery": { "mode": "none" },
  "enabled": true
}
```

### Heartbeat vs Cron

| Use Heartbeat When | Use Cron When |
|---------------------|---------------|
| Multiple checks can batch together | Exact timing matters |
| Need recent conversation context | Task needs isolation |
| Timing can drift (~30 min is fine) | Want a different model |
| Reducing API calls by combining | One-shot reminders |

### Managing Existing Cron Jobs

Before creating, always check for duplicates:
1. `cron action=list` — list all jobs
2. Look for similar names/purposes
3. **Update** existing jobs instead of creating duplicates

---

## Options Reference

### create-agent.sh

| Option | Required | Description |
|--------|----------|-------------|
| `--id` | ✓ | Agent ID (lowercase, no spaces) |
| `--name` | ✓ | Display name |
| `--emoji` | ✓ | Agent emoji |
| `--specialty` | ✓ | What the agent does |
| `--model` | | Model (default: claude-sonnet-4-6) |
| `--channel` | | Existing Discord channel ID |
| `--create` | | Create new channel with this name |
| `--category` | | Category ID for new channel |
| `--topic` | | Channel topic (auto-generated if not set) |
| `--cron` | | Daily memory cron time (default: 23:00) |
| `--no-cron` | | Skip daily memory cron setup |
| `--tz` | | Timezone (default: America/New_York) |
| `--own-category` | | Claim a Discord category (auto-binds all channels) |

## Architecture

```
Gateway receives message
       │
       ▼
Check bindings (first match wins)
       │
       ├─── match: route to bound agent
       │
       └─── no match: route to default agent
```

Bindings are **prepended** (not appended) so new specific bindings take priority over catch-all rules.

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `DISCORD_GUILD_ID` | For `--create` | Your Discord server ID |
| `AGENT_WORKSPACE_ROOT` | No | Agent workspace root (default: `~/workspace/agents`) |

## qmd Integration (Optional)

If [qmd](https://github.com/tobi/qmd) is installed, agent-council automatically updates the index:
- **Create:** Runs `qmd update` so new agent memory is immediately searchable
- **Remove:** Runs `qmd update` to clean up removed agent files

## Finding Discord IDs

To get category/channel IDs:
1. Enable Developer Mode in Discord (User Settings → App Settings → Advanced)
2. Right-click any channel or category → "Copy ID"

Or use: `openclaw message channel-list --guildId YOUR_SERVER_ID`

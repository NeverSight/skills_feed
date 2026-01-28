---
name: discord
description: Discord Bot API via curl. Use this skill to interact with channels, guilds, users, and messages using a bot token.
vm0_secrets:
  - DISCORD_BOT_TOKEN
---

# Discord Bot API

Use the Discord Bot API via direct `curl` calls to **manage channels, guilds, messages, and users**.

> Official docs: `https://discord.com/developers/docs`

---

## When to Use

Use this skill when you need to:

- **Send messages** to specific channels
- **Read messages** from channels
- **Manage channels** (create, edit, delete)
- **Get server info** (guilds, members, roles)
- **React to messages** and moderate content
- **Create webhooks** programmatically

For simple message posting, use `discord-webhook` skill instead.

---

## Prerequisites

### 1. Create Application

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application" and give it a name
3. Go to "Bot" section and click "Add Bot"

### 2. Get Bot Token

1. In Bot section, click "Reset Token"
2. Copy the token (shown only once)

```bash
export DISCORD_BOT_TOKEN="MTIzNDU2Nzg5MDEyMzQ1Njc4OQ.ABcDeF.xxxxx..."
```

### 3. Enable Intents (if needed)

In Bot section, enable:
- Presence Intent (for user status)
- Server Members Intent (for member list)
- Message Content Intent (for reading messages)

### 4. Invite Bot to Server

1. Go to OAuth2 → URL Generator
2. Select scopes: `bot`, `applications.commands`
3. Select permissions needed (e.g., Send Messages, Read Messages)
4. Copy URL and open in browser to invite

### 5. Get IDs

Enable Developer Mode: User Settings → Advanced → Developer Mode
Right-click any channel/user/server → Copy ID

---


> **Important:** When using `$VAR` in a command that pipes to another command, wrap the command containing `$VAR` in `bash -c '...'`. Due to a Claude Code bug, environment variables are silently cleared when pipes are used directly.
> ```bash
> bash -c 'curl -s "https://api.example.com" -H "Authorization: Bearer $API_KEY"' | jq .
> ```

## How to Use

Base URL: `https://discord.com/api/v10`

Authorization header: `Authorization: Bot YOUR_TOKEN`

---

### 1. Get Current Bot User

```bash
bash -c 'curl -s "https://discord.com/api/v10/users/@me" -H "Authorization: Bot ${DISCORD_BOT_TOKEN}"' | jq '{id, username, discriminator}'
```

---

### 2. Send Message to Channel

Write to `/tmp/discord_request.json`:

```json
{
  "content": "Hello from bot!"
}
```

Then run (replace `<your-channel-id>` with the actual channel ID):

```bash
bash -c 'curl -s -X POST "https://discord.com/api/v10/channels/<your-channel-id>/messages" -H "Authorization: Bot ${DISCORD_BOT_TOKEN}" -H "Content-Type: application/json" -d @/tmp/discord_request.json'
```

---

### 3. Send Embed Message

Write to `/tmp/discord_request.json`:

```json
{
  "embeds": [
    {
      "title": "Bot Message",
      "description": "This is from the bot API",
      "color": 5793266
    }
  ]
}
```

Then run (replace `<your-channel-id>` with the actual channel ID):

```bash
bash -c 'curl -s -X POST "https://discord.com/api/v10/channels/<your-channel-id>/messages" -H "Authorization: Bot ${DISCORD_BOT_TOKEN}" -H "Content-Type: application/json" -d @/tmp/discord_request.json'
```

---

### 4. Get Channel Info

Replace `<your-channel-id>` with the actual channel ID:

```bash
bash -c 'curl -s "https://discord.com/api/v10/channels/<your-channel-id>" -H "Authorization: Bot ${DISCORD_BOT_TOKEN}"' | jq '{id, name, type, guild_id}'
```

---

### 5. Get Channel Messages

Replace `<your-channel-id>` with the actual channel ID:

```bash
bash -c 'curl -s "https://discord.com/api/v10/channels/<your-channel-id>/messages?limit=10" -H "Authorization: Bot ${DISCORD_BOT_TOKEN}"' | jq '.[] | {id, author: .author.username, content}'
```

---

### 6. Get Specific Message

Replace `<your-channel-id>` and `<your-message-id>` with the actual IDs:

```bash
bash -c 'curl -s "https://discord.com/api/v10/channels/<your-channel-id>/messages/<your-message-id>" -H "Authorization: Bot ${DISCORD_BOT_TOKEN}"' | jq '{id, content, author: .author.username}'
```

---

### 7. Delete Message

Replace `<your-channel-id>` and `<your-message-id>` with the actual IDs:

```bash
bash -c 'curl -s -X DELETE "https://discord.com/api/v10/channels/<your-channel-id>/messages/<your-message-id>" -H "Authorization: Bot ${DISCORD_BOT_TOKEN}"'
```

---

### 8. Add Reaction

Replace `<your-channel-id>` and `<your-message-id>` with the actual IDs:

```bash
bash -c 'curl -s -X PUT "https://discord.com/api/v10/channels/<your-channel-id>/messages/<your-message-id>/reactions/%F0%9F%91%8D/@me" -H "Authorization: Bot ${DISCORD_BOT_TOKEN}" -H "Content-Length: 0"'
```

Note: Emoji must be URL encoded (👍 = `%F0%9F%91%8D`)

---

### 9. Get Guild (Server) Info

Replace `<your-guild-id>` with the actual guild ID:

```bash
bash -c 'curl -s "https://discord.com/api/v10/guilds/<your-guild-id>" -H "Authorization: Bot ${DISCORD_BOT_TOKEN}"' | jq '{id, name, member_count, owner_id}'
```

---

### 10. List Guild Channels

Replace `<your-guild-id>` with the actual guild ID:

```bash
bash -c 'curl -s "https://discord.com/api/v10/guilds/<your-guild-id>/channels" -H "Authorization: Bot ${DISCORD_BOT_TOKEN}"' | jq '.[] | {id, name, type}'
```

---

### 11. Get Guild Members

Replace `<your-guild-id>` with the actual guild ID:

```bash
bash -c 'curl -s "https://discord.com/api/v10/guilds/<your-guild-id>/members?limit=10" -H "Authorization: Bot ${DISCORD_BOT_TOKEN}"' | jq '.[] | {user: .user.username, nick, joined_at}'
```

---

### 12. Get Guild Roles

Replace `<your-guild-id>` with the actual guild ID:

```bash
bash -c 'curl -s "https://discord.com/api/v10/guilds/<your-guild-id>/roles" -H "Authorization: Bot ${DISCORD_BOT_TOKEN}"' | jq '.[] | {id, name, color, position}'
```

---

### 13. Create Webhook

Write to `/tmp/discord_request.json`:

```json
{
  "name": "My Webhook"
}
```

Then run (replace `<your-channel-id>` with the actual channel ID):

```bash
bash -c 'curl -s -X POST "https://discord.com/api/v10/channels/<your-channel-id>/webhooks" -H "Authorization: Bot ${DISCORD_BOT_TOKEN}" -H "Content-Type: application/json" -d @/tmp/discord_request.json' | jq '{id, token, url: "https://discord.com/api/webhooks/\(.id)/\(.token)"}'
```

---

### 14. List Channel Webhooks

Replace `<your-channel-id>` with the actual channel ID:

```bash
bash -c 'curl -s "https://discord.com/api/v10/channels/<your-channel-id>/webhooks" -H "Authorization: Bot ${DISCORD_BOT_TOKEN}"' | jq '.[] | {id, name, token}'
```

---

### 15. Create Text Channel

Write to `/tmp/discord_request.json`:

```json
{
  "name": "new-channel",
  "type": 0
}
```

Then run (replace `<your-guild-id>` with the actual guild ID):

```bash
bash -c 'curl -s -X POST "https://discord.com/api/v10/guilds/<your-guild-id>/channels" -H "Authorization: Bot ${DISCORD_BOT_TOKEN}" -H "Content-Type: application/json" -d @/tmp/discord_request.json' | jq '{id, name}'
```

---

## Channel Types

| Type | Description |
|------|-------------|
| 0 | Text channel |
| 2 | Voice channel |
| 4 | Category |
| 5 | Announcement |
| 13 | Stage |
| 15 | Forum |

---

## Guidelines

1. **Rate limits**: Check `X-RateLimit-*` headers; implement backoff
2. **Token security**: Never expose bot tokens
3. **Permissions**: Bot needs appropriate permissions for each action
4. **Intents**: Enable required intents in Developer Portal
5. **API version**: Use `/v10` for latest stable API

---
name: telegram-reminders
description: Send reminders and messages to Telegram with cloud-based scheduling. Use when the user wants to send immediate messages or schedule future reminders to Telegram. Supports text messages, timestamp-based scheduling, recurring reminders, viewing and canceling scheduled messages, and message history.
---

# Telegram Reminders Skill

Send immediate messages and schedule reminders to Telegram with cloud-based scheduling powered by Convex. Your reminders run 24/7 in Convex Cloud with zero infrastructure management.

## Quick Reference

IMPORTANT! Always use these commands in order:

- Send now: `tsx scripts/send_message.ts [message_text]`
- Send now with attachment: `tsx scripts/send_message.ts [message_text] /path/to/file.pdf`
- Schedule: `tsx scripts/schedule_message.ts [time expression] [title] [message_text] [file_path]`
- Schedule with attachment: `tsx scripts/schedule_message.ts [time expression] [title] [message_text] /path/to/file`
- List pending: `tsx scripts/list_scheduled.ts`
- Cancel: `tsx scripts/cancel_message.ts <message_id>`
- History: `tsx scripts/view_history.ts [limit]`

## Initial Setup

**Prerequisites** (user must provide):

1. **Bot Token**: Message [@BotFather](https://t.me/BotFather) → `/newbot` → copy token
2. **User ID**: Message [@userinfobot](https://t.me/userinfobot) → copy numeric ID
3. **Deploy Key**: [dashboard.convex.dev](https://dashboard.convex.dev) → Create project → Settings → Deploy Keys → Create "Production" key

**Setup steps**:

```bash
# 1. Install dependencies
cd /mnt/skills/user/telegram-reminders && npm install

# 2. Save configuration
mkdir -p /mnt/user-data/outputs
cat > /mnt/user-data/outputs/telegram_config.json << 'EOF'
{
  "botToken": "YOUR_BOT_TOKEN",
  "userId": "YOUR_USER_ID",
  "deployKey": "YOUR_DEPLOY_KEY",
  "setupDate": "CURRENT_DATE"
}
EOF

# 3. Create .env.local
cat > .env.local << 'EOF'
CONVEX_DEPLOY_KEY=YOUR_DEPLOY_KEY
EOF


# 4. Set environment variables in Convex
npx convex env set TELEGRAM_BOT_TOKEN "YOUR_BOT_TOKEN"
npx convex env set TELEGRAM_USER_ID "YOUR_USER_ID"

# 5. Deploy to Convex
npx convex deploy

# 6. Test with a message
tsx scripts/send_message.ts "Setup complete!"
```

**Critical**: User must start a chat with their bot (search and press "Start") before the bot can send messages.

## Core Operations

### Send Immediate Message

**Send text message**:

```bash
tsx scripts/send_message.ts "Your message text here"
```

**Example with special characters**:

```bash
tsx scripts/send_message.ts "Hello! Here's a test message 🚀"
```

## Timezone

All times use user's configured timezone. The Convex backend stores UTC internally; client scripts handle conversion via chrono-node.

## Limitations

- Files sent as documents (not inline images)
- Maximum file size: 50MB (Telegram limit)
- Cron granularity: 1 minute minimum
- No message editing (cancel and reschedule instead)
- Rate limits: 20 messages/minute per user

## References

- [`references/initial_setup.md`](references/initial_setup.md) - Detailed setup process
- [`references/architecture.md`](references/architecture.md) - System architecture
- [`references/convex.md`](references/convex.md) - Convex platform details
- [`references/telegram_api.md`](references/telegram_api.md) - Telegram Bot API
- [`references/error_handling.md`](references/error_handling.md) - Error resolution guide

---
name: reactions
description: React to the user's Telegram message with an emoji. Use when the message evokes a genuine emotional response.
allowed-tools:
  - Bash
---

# Reactions Skill

React to the user's message with an emoji reaction (Telegram only).

## Set a Reaction

```bash
curl -s -X POST http://localhost:23001/api/reaction/set \
  -H 'Content-Type: application/json' \
  -d '{"emoji": "❤️"}'
```

Response: `{"success": true, "emoji": "❤️"}`

## Available Emoji

Must be one of: 👍 ❤ 🎉 😂 😢 😮 🔥 🤔 👎 🙏 🥰 🤣

## When to Use

- User's message evokes genuine emotion — excitement, gratitude, humor, surprise
- Something funny or heartwarming
- A simple acknowledgment when words aren't needed

## When NOT to Use

- Don't react to every message
- Neutral or factual messages don't need reactions
- Only works for Telegram messages

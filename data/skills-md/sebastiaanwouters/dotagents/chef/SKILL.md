---
name: chef
description: Telegram communication for AI agents. ALL methods are BLOCKING. Use for user interviews, status updates, and feedback collection.
---

# Chef 👨‍🍳

Your witty Telegram sous-chef. **ALL methods are BLOCKING** (except notify).

## Personality

Be funny, concise, smart. Use emojis liberally. Keep it punchy — one-liners > paragraphs.

## Setup

`.env`:
```
TELEGRAM_BOT_TOKEN=xxx
TELEGRAM_CHAT_ID=xxx
```

## API

```typescript
import { chef } from "./skills/chef/scripts/chef.ts";

// Free text - BLOCKING
await chef.ask("📛 Project name?"); // returns string|null

// Yes/No - BLOCKING
await chef.confirm("🚀 Ship it?"); // returns boolean|null

// Multiple choice - BLOCKING
await chef.choice("🛠️ Stack?", ["React", "Vue", "Svelte"]); // returns index|null

// Collect multiple responses until stopword - BLOCKING
await chef.collect("Any remarks?", "lfg", 60000); // returns {responses[], stopped, timedOut}

// Fire & forget notification (only non-blocking method)
await chef.notify("🎬 Lights, camera, coding!");
```

## Rules

- `ask()` → BLOCKING, waits for free text
- `confirm()` → BLOCKING, waits for Yes/No
- `choice()` → BLOCKING, waits for selection
- `collect()` → BLOCKING, waits for stopword
- `notify()` → fire & forget (only non-blocking)
- Always use emojis in messages
- Keep messages under 280 chars (tweet-sized)
- Be clever, not cringe

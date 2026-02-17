---
name: telegram-bot
description: >
  Send messages, images, and marketing content to Telegram channels and groups via Bot API.
  Create formatted posts, polls, and media content for Telegram communities. Trigger phrases:
  "post to telegram", "telegram message", "telegram channel", "telegram bot", "telegram marketing",
  "send to telegram", "telegram announcement", "telegram broadcast".
allowed-tools:
  - Bash
  - WebFetch
  - WebSearch
---

# Telegram Bot Skill

You are a Telegram marketing specialist. Your job is to help users send messages, media, polls,
and marketing content to Telegram channels and groups using the Telegram Bot API. You handle
formatting, inline keyboards, and content templates for effective channel management.

## Prerequisites

### Environment Variables

Check for required credentials before any API call:

```bash
source ~/.claude/.env.global 2>/dev/null
source .env 2>/dev/null
source .env.local 2>/dev/null

if [ -z "$TELEGRAM_BOT_TOKEN" ]; then
  echo "TELEGRAM_BOT_TOKEN is not set."
  echo "To create a bot and get a token:"
  echo "  1. Open Telegram and search for @BotFather"
  echo "  2. Send /newbot and follow the prompts"
  echo "  3. Copy the token and add it to your .env or ~/.claude/.env.global:"
  echo "     TELEGRAM_BOT_TOKEN=123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11"
  exit 1
else
  echo "TELEGRAM_BOT_TOKEN is configured."
fi

if [ -z "$TELEGRAM_CHAT_ID" ]; then
  echo "TELEGRAM_CHAT_ID is not set."
  echo "To find your channel/group chat ID:"
  echo "  1. Add your bot to the channel/group as an admin"
  echo "  2. Send a message in the channel/group"
  echo "  3. Run: curl -s https://api.telegram.org/bot\${TELEGRAM_BOT_TOKEN}/getUpdates | jq '.result[-1].message.chat.id'"
  echo "  4. For public channels, use the @channel_username format (e.g., @mychannel)"
  echo "  5. Add it to your .env or ~/.claude/.env.global:"
  echo "     TELEGRAM_CHAT_ID=-1001234567890"
else
  echo "TELEGRAM_CHAT_ID is configured: ${TELEGRAM_CHAT_ID}"
fi
```

### Creating a Bot via @BotFather

If the user does not have a bot yet, walk them through this process:

1. Open Telegram and search for **@BotFather** (the official bot creation tool).
2. Send `/newbot` to BotFather.
3. Choose a **display name** for the bot (e.g., "My Marketing Bot").
4. Choose a **username** ending in `bot` (e.g., `my_marketing_bot`).
5. BotFather replies with an **API token** like `123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11`.
6. Store the token as `TELEGRAM_BOT_TOKEN` in `.env` or `~/.claude/.env.global`.
7. **Add the bot as an admin** to the target channel or group.
8. Optionally, customize the bot with BotFather commands:
   - `/setdescription` - Set the bot's description
   - `/setabouttext` - Set the "About" section
   - `/setuserpic` - Upload a profile photo for the bot

### Finding the Chat ID

For **public channels**, use `@channel_username` as the chat ID.

For **private channels and groups**, retrieve the numeric chat ID:

```bash
source ~/.claude/.env.global 2>/dev/null
# Send a message in the channel/group first, then run:
curl -s "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/getUpdates" | \
  jq -r '.result[] | "\(.message.chat.id // .channel_post.chat.id) - \(.message.chat.title // .channel_post.chat.title)"' | \
  sort -u
```

Private channel and group IDs are negative numbers (e.g., `-1001234567890`).

## API Reference

All Telegram Bot API calls use this base URL:

```
https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/{method}
```

Always source environment variables before making API calls:

```bash
source ~/.claude/.env.global 2>/dev/null
source .env 2>/dev/null
source .env.local 2>/dev/null
```

### sendMessage - Text Messages

Send a text message to a channel or group:

```bash
curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
  -H "Content-Type: application/json" \
  -d '{
    "chat_id": "'"${TELEGRAM_CHAT_ID}"'",
    "text": "Your message text here",
    "parse_mode": "HTML"
  }'
```

**Response:** Returns a JSON object with `ok: true` and the sent `message` object on success. Check `ok` to confirm delivery. The `message.message_id` can be saved for later editing or deletion.

### sendPhoto - Images

Send a photo by URL or file ID:

```bash
# Send photo by URL
curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendPhoto" \
  -H "Content-Type: application/json" \
  -d '{
    "chat_id": "'"${TELEGRAM_CHAT_ID}"'",
    "photo": "https://example.com/image.jpg",
    "caption": "Image caption with <b>HTML</b> formatting",
    "parse_mode": "HTML"
  }'
```

```bash
# Send photo from local file
curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendPhoto" \
  -F "chat_id=${TELEGRAM_CHAT_ID}" \
  -F "photo=@/path/to/image.jpg" \
  -F "caption=Image caption here" \
  -F "parse_mode=HTML"
```

**Photo limits:** Maximum file size 10 MB. The photo will be compressed. For uncompressed images up to 50 MB, use `sendDocument` instead.

### sendDocument - Files and Documents

Send any file (PDF, ZIP, uncompressed images, etc.):

```bash
# Send document by URL
curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendDocument" \
  -H "Content-Type: application/json" \
  -d '{
    "chat_id": "'"${TELEGRAM_CHAT_ID}"'",
    "document": "https://example.com/report.pdf",
    "caption": "Download our latest report",
    "parse_mode": "HTML"
  }'
```

```bash
# Send document from local file
curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendDocument" \
  -F "chat_id=${TELEGRAM_CHAT_ID}" \
  -F "document=@/path/to/file.pdf" \
  -F "caption=Here is the document" \
  -F "parse_mode=HTML"
```

**Document limits:** Maximum file size 50 MB.

### sendPoll - Polls and Quizzes

Create interactive polls for engagement:

```bash
# Regular poll (multiple choice)
curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendPoll" \
  -H "Content-Type: application/json" \
  -d '{
    "chat_id": "'"${TELEGRAM_CHAT_ID}"'",
    "question": "What feature should we build next?",
    "options": ["Dark mode", "Mobile app", "API access", "Integrations"],
    "is_anonymous": false,
    "allows_multiple_answers": false
  }'
```

```bash
# Quiz mode (one correct answer)
curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendPoll" \
  -H "Content-Type: application/json" \
  -d '{
    "chat_id": "'"${TELEGRAM_CHAT_ID}"'",
    "question": "Which programming language was created first?",
    "options": ["Python", "JavaScript", "C", "Java"],
    "type": "quiz",
    "correct_option_id": 2,
    "explanation": "C was created by Dennis Ritchie in 1972, well before the others.",
    "explanation_parse_mode": "HTML"
  }'
```

**Poll limits:** Question text 1-300 characters. 2-10 options, each 1-100 characters. Explanation up to 200 characters.

### Inline Keyboard Buttons (CTAs)

Add clickable buttons below any message for calls-to-action:

```bash
curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
  -H "Content-Type: application/json" \
  -d '{
    "chat_id": "'"${TELEGRAM_CHAT_ID}"'",
    "text": "Check out our latest product!",
    "parse_mode": "HTML",
    "reply_markup": {
      "inline_keyboard": [
        [
          {"text": "Visit Website", "url": "https://example.com"},
          {"text": "View Demo", "url": "https://example.com/demo"}
        ],
        [
          {"text": "Read Blog Post", "url": "https://example.com/blog"}
        ]
      ]
    }
  }'
```

**Keyboard layout:** Each inner array is a row of buttons. Keep rows to 1-3 buttons for readability on mobile. Maximum 100 buttons total per message.

**Button types:**
- `url` - Opens a URL in the browser
- `callback_data` - Sends data back to the bot (requires a webhook to handle)
- `switch_inline_query` - Prompts the user to select a chat and send an inline query

### editMessageText - Edit Existing Messages

Update a previously sent message:

```bash
curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/editMessageText" \
  -H "Content-Type: application/json" \
  -d '{
    "chat_id": "'"${TELEGRAM_CHAT_ID}"'",
    "message_id": MESSAGE_ID_HERE,
    "text": "Updated message text",
    "parse_mode": "HTML"
  }'
```

### deleteMessage - Delete a Message

Remove a message from the channel:

```bash
curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/deleteMessage" \
  -H "Content-Type: application/json" \
  -d '{
    "chat_id": "'"${TELEGRAM_CHAT_ID}"'",
    "message_id": MESSAGE_ID_HERE
  }'
```

### pinChatMessage - Pin Important Messages

Pin a message to the top of the channel or group:

```bash
curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/pinChatMessage" \
  -H "Content-Type: application/json" \
  -d '{
    "chat_id": "'"${TELEGRAM_CHAT_ID}"'",
    "message_id": MESSAGE_ID_HERE,
    "disable_notification": true
  }'
```

## Message Formatting

### HTML Mode (Recommended)

Set `"parse_mode": "HTML"` and use these tags:

| Tag | Result | Example |
|-----|--------|---------|
| `<b>text</b>` | **Bold** | `<b>Important</b>` |
| `<i>text</i>` | *Italic* | `<i>Note:</i>` |
| `<u>text</u>` | Underline | `<u>highlight</u>` |
| `<s>text</s>` | ~~Strikethrough~~ | `<s>old price</s>` |
| `<code>text</code>` | `Monospace` | `<code>variable</code>` |
| `<pre>text</pre>` | Code block | `<pre>code block</pre>` |
| `<a href="url">text</a>` | Link | `<a href="https://example.com">Click here</a>` |
| `<tg-emoji emoji-id="ID">emoji</tg-emoji>` | Custom emoji | Premium feature |
| `<blockquote>text</blockquote>` | Block quote | `<blockquote>Quote</blockquote>` |
| `<tg-spoiler>text</tg-spoiler>` | Spoiler | `<tg-spoiler>Hidden</tg-spoiler>` |

**HTML escaping rules:** Replace `&` with `&amp;`, `<` with `&lt;`, `>` with `&gt;` in all text that is not part of an HTML tag. Unrecognized tags are stripped. Tags must be properly closed.

### MarkdownV2 Mode

Set `"parse_mode": "MarkdownV2"` and use this syntax:

| Syntax | Result |
|--------|--------|
| `*bold*` | **Bold** |
| `_italic_` | *Italic* |
| `__underline__` | Underline |
| `~strikethrough~` | ~~Strikethrough~~ |
| `` `code` `` | `Monospace` |
| ` ```code block``` ` | Code block |
| `[text](url)` | Link |
| `||spoiler||` | Spoiler |
| `>blockquote` | Block quote (start of line) |

**MarkdownV2 escaping rules:** These characters MUST be escaped with a preceding backslash outside of code blocks: `_ * [ ] ( ) ~ > # + - = | { } . !`. This makes MarkdownV2 error-prone. **HTML mode is recommended** for most use cases to avoid escaping issues.

### Formatting Tips

- Use blank lines (`\n\n`) to separate sections visually.
- Emoji work natively in message text. No special handling needed.
- Combine formatting: `<b><i>bold italic</i></b>` works in HTML mode.
- Links can be hidden behind text: `<a href="https://example.com">Click here</a>`.
- For silent messages (no notification), add `"disable_notification": true` to the request body.

## Marketing Content Templates

### Template 1: Product Announcement

```bash
curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
  -H "Content-Type: application/json" \
  -d '{
    "chat_id": "'"${TELEGRAM_CHAT_ID}"'",
    "parse_mode": "HTML",
    "text": "🚀 <b>Introducing [Product Name]</b>\n\n[One-sentence value proposition that answers: what is it and why should I care?]\n\n<b>What'"'"'s new:</b>\n✅ [Feature 1] — [Benefit in user terms]\n✅ [Feature 2] — [Benefit in user terms]\n✅ [Feature 3] — [Benefit in user terms]\n\n💡 <i>[Short sentence about who this is for or what problem it solves]</i>\n\n👉 <a href=\"https://example.com\">Try it now</a>",
    "reply_markup": {
      "inline_keyboard": [
        [
          {"text": "🔗 Try It Now", "url": "https://example.com"},
          {"text": "📖 Learn More", "url": "https://example.com/blog"}
        ]
      ]
    }
  }'
```

### Template 2: Blog Post Share

```bash
curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
  -H "Content-Type: application/json" \
  -d '{
    "chat_id": "'"${TELEGRAM_CHAT_ID}"'",
    "parse_mode": "HTML",
    "text": "📝 <b>New on the blog:</b> [Blog Post Title]\n\n[2-3 sentence summary that highlights the key takeaway and why the reader should care. Pull out the most surprising insight or actionable tip.]\n\n<b>Key takeaways:</b>\n🔹 [Takeaway 1]\n🔹 [Takeaway 2]\n🔹 [Takeaway 3]\n\n⏱ [X] min read",
    "reply_markup": {
      "inline_keyboard": [
        [
          {"text": "📖 Read the Full Post", "url": "https://example.com/blog/post-slug"}
        ]
      ]
    }
  }'
```

### Template 3: Community Update / Newsletter Digest

```bash
curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
  -H "Content-Type: application/json" \
  -d '{
    "chat_id": "'"${TELEGRAM_CHAT_ID}"'",
    "parse_mode": "HTML",
    "text": "📢 <b>[Brand] Weekly Update — [Date]</b>\n\nHey everyone! Here'"'"'s what happened this week:\n\n<b>🔧 Product</b>\n• [Update 1]\n• [Update 2]\n\n<b>📊 Metrics</b>\n• [Milestone or growth number]\n• [Community stat, e.g., new members]\n\n<b>📅 Coming Up</b>\n• [Upcoming event, release, or deadline]\n• [Upcoming event, release, or deadline]\n\n<b>🎯 Action Item</b>\n[One clear thing you want the community to do this week]\n\nQuestions? Drop them below 👇"
  }'
```

### Template 4: Product Launch with Image

```bash
# First, send the image with caption
curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendPhoto" \
  -H "Content-Type: application/json" \
  -d '{
    "chat_id": "'"${TELEGRAM_CHAT_ID}"'",
    "photo": "https://example.com/launch-banner.jpg",
    "caption": "🎉 <b>[Product Name] is LIVE!</b>\n\n[One powerful sentence about what this means for users]\n\n🏷 Launch offer: <b>[Discount/offer details]</b>\n⏰ Available until [date/time]\n\n👉 <a href=\"https://example.com\">Get it now</a>",
    "parse_mode": "HTML",
    "reply_markup": {
      "inline_keyboard": [
        [
          {"text": "🛒 Get It Now", "url": "https://example.com/buy"},
          {"text": "🎥 Watch Demo", "url": "https://example.com/demo"}
        ],
        [
          {"text": "💬 Join Discussion", "url": "https://t.me/community_group"}
        ]
      ]
    }
  }'
```

### Template 5: Engagement Poll

```bash
curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendPoll" \
  -H "Content-Type: application/json" \
  -d '{
    "chat_id": "'"${TELEGRAM_CHAT_ID}"'",
    "question": "What should we focus on next? 🗳",
    "options": [
      "Feature A — [short description]",
      "Feature B — [short description]",
      "Feature C — [short description]",
      "Something else (comment below!)"
    ],
    "is_anonymous": false,
    "allows_multiple_answers": false
  }'
```

### Template 6: Knowledge Quiz

```bash
curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendPoll" \
  -H "Content-Type: application/json" \
  -d '{
    "chat_id": "'"${TELEGRAM_CHAT_ID}"'",
    "question": "[Interesting question related to your niche]?",
    "options": [
      "[Option A]",
      "[Option B]",
      "[Option C]",
      "[Option D]"
    ],
    "type": "quiz",
    "correct_option_id": 0,
    "explanation": "[Brief explanation of why the correct answer is correct. Include a fun fact or link to learn more.]",
    "explanation_parse_mode": "HTML",
    "is_anonymous": false
  }'
```

### Template 7: Event / Webinar Announcement

```bash
curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
  -H "Content-Type: application/json" \
  -d '{
    "chat_id": "'"${TELEGRAM_CHAT_ID}"'",
    "parse_mode": "HTML",
    "text": "🎙 <b>Live Event: [Event Title]</b>\n\n📅 <b>Date:</b> [Day, Month Date, Year]\n🕐 <b>Time:</b> [Time + Timezone]\n📍 <b>Where:</b> [Platform/Location]\n🎤 <b>Speaker:</b> [Name, Title]\n\n<b>What you'"'"'ll learn:</b>\n1. [Topic 1]\n2. [Topic 2]\n3. [Topic 3]\n\n🎁 <i>Bonus: [Incentive for attending, e.g., free template, recording access]</i>\n\nSpots are limited — register now 👇",
    "reply_markup": {
      "inline_keyboard": [
        [
          {"text": "📝 Register Now", "url": "https://example.com/event"}
        ],
        [
          {"text": "📅 Add to Calendar", "url": "https://example.com/calendar-link"}
        ]
      ]
    }
  }'
```

## Content Scheduling Workflow

Telegram Bot API does not have a built-in scheduling feature. Use these approaches for scheduled content delivery.

### Approach 1: Delayed Send with `sleep` (Simple)

For one-off scheduled messages from the terminal:

```bash
# Send a message after a delay (e.g., 2 hours = 7200 seconds)
echo "Message scheduled. Will send at $(date -v+2H '+%Y-%m-%d %H:%M:%S' 2>/dev/null || date -d '+2 hours' '+%Y-%m-%d %H:%M:%S' 2>/dev/null)"
sleep 7200 && curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
  -H "Content-Type: application/json" \
  -d '{
    "chat_id": "'"${TELEGRAM_CHAT_ID}"'",
    "text": "Scheduled message content here",
    "parse_mode": "HTML"
  }'
```

### Approach 2: `at` Command (Specific Time)

Schedule a message for a specific date and time:

```bash
# Create the send script
cat > /tmp/telegram_scheduled.sh << 'SCRIPT'
source ~/.claude/.env.global 2>/dev/null
curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
  -H "Content-Type: application/json" \
  -d '{
    "chat_id": "'"${TELEGRAM_CHAT_ID}"'",
    "text": "Your scheduled message here",
    "parse_mode": "HTML"
  }'
SCRIPT
chmod +x /tmp/telegram_scheduled.sh

# Schedule it (macOS/Linux)
echo "bash /tmp/telegram_scheduled.sh" | at 09:00 AM tomorrow
```

### Approach 3: Cron Job (Recurring)

For recurring messages (daily tips, weekly digests):

```bash
# Edit crontab
# Example: Send every weekday at 9:00 AM
# 0 9 * * 1-5 bash /path/to/telegram_post.sh

crontab -l 2>/dev/null > /tmp/crontab_backup
echo "0 9 * * 1-5 source ~/.claude/.env.global && curl -s -X POST 'https://api.telegram.org/bot\${TELEGRAM_BOT_TOKEN}/sendMessage' -H 'Content-Type: application/json' -d '{\"chat_id\": \"\${TELEGRAM_CHAT_ID}\", \"text\": \"Good morning! Here is your daily tip.\", \"parse_mode\": \"HTML\"}'" >> /tmp/crontab_backup
crontab /tmp/crontab_backup
```

### Approach 4: Batch Content Queue

Prepare multiple messages and send them with delays between each:

```bash
# Create a batch of messages as a JSON array, then iterate
messages=(
  "Message 1: Monday motivation"
  "Message 2: Tuesday tip"
  "Message 3: Wednesday wisdom"
)

DELAY=86400  # 24 hours between messages

for i in "${!messages[@]}"; do
  if [ "$i" -gt 0 ]; then
    echo "Waiting ${DELAY}s before next message..."
    sleep ${DELAY}
  fi
  echo "Sending message $((i+1)) of ${#messages[@]}..."
  curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
    -H "Content-Type: application/json" \
    -d '{
      "chat_id": "'"${TELEGRAM_CHAT_ID}"'",
      "text": "'"${messages[$i]}"'",
      "parse_mode": "HTML"
    }'
  echo ""
done
```

## Sending to Multiple Channels

If the user manages multiple channels, accept a list of chat IDs and broadcast to all:

```bash
# Define target channels
CHANNELS=("-1001234567890" "-1009876543210" "@public_channel")

MESSAGE='<b>Announcement</b>\n\nThis message goes to all channels.'

for CHAT_ID in "${CHANNELS[@]}"; do
  echo "Sending to ${CHAT_ID}..."
  curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
    -H "Content-Type: application/json" \
    -d '{
      "chat_id": "'"${CHAT_ID}"'",
      "text": "'"${MESSAGE}"'",
      "parse_mode": "HTML"
    }'
  echo ""
  sleep 1  # Respect rate limits
done
```

## Channel Management

### Get Channel Info

```bash
curl -s "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/getChat?chat_id=${TELEGRAM_CHAT_ID}" | jq .
```

### Get Member Count

```bash
curl -s "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/getChatMemberCount?chat_id=${TELEGRAM_CHAT_ID}" | jq .
```

### Set Channel Description

```bash
curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/setChatDescription" \
  -H "Content-Type: application/json" \
  -d '{
    "chat_id": "'"${TELEGRAM_CHAT_ID}"'",
    "description": "Your channel description here (up to 255 characters)"
  }'
```

## Rate Limits and Best Practices

### Telegram API Rate Limits

- **Messages to the same chat:** ~30 messages per second (but keep well below this).
- **Messages to different chats:** ~30 messages per second total.
- **Bulk notifications:** If sending to many users, Telegram recommends no more than 30 messages per second. Add `sleep 1` between sends when broadcasting.
- **File uploads:** 50 MB max per file for documents, 10 MB for photos.

### Content Best Practices for Telegram Channels

| Practice | Details |
|----------|---------|
| Post frequency | 1-3 posts per day for active channels. More than 5 risks mute/unsubscribe. |
| Best times | 9-11 AM and 6-8 PM in your audience's primary timezone. |
| Message length | Keep under 1,000 characters for feed posts. Long-form is fine for articles. |
| Media | Posts with images get 2-3x more engagement than text-only. |
| Formatting | Use bold for key points, bullet lists for scannability, links at the end. |
| Engagement | Ask questions. Use polls weekly. Reply to comments promptly. |
| Silent posts | Use `disable_notification: true` for non-urgent updates to avoid annoying subscribers. |
| Pin messages | Pin important announcements. Unpin old ones to keep the pinned area relevant. |
| Link previews | Telegram auto-generates link previews. To disable, set `disable_web_page_preview: true`. |

### Publishing Workflow

When the user asks to post content to Telegram:

1. **Check credentials** - Verify `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` are set.
2. **Generate content** - Write the message using appropriate formatting and templates.
3. **Preview** - Show the user the exact message that will be sent, including:
   - Message text with formatting
   - Any inline keyboard buttons
   - Media attachments (URL or file path)
   - Target chat ID
4. **Confirm** - Ask the user to approve before sending.
5. **Send** - Execute the API call.
6. **Report** - Show the response, including `message_id` for future reference (editing, deleting, pinning).

**Never auto-post without explicit user confirmation.**

## Gathering Requirements

Before composing a Telegram message, collect these inputs:

1. **Message type** - Text, photo, document, poll, or quiz.
2. **Content** - What is the message about? Provide copy or topic for generation.
3. **Target** - Which channel or group? Use `TELEGRAM_CHAT_ID` or ask for a specific one.
4. **Formatting** - HTML or MarkdownV2. Default to HTML.
5. **Buttons** - Any CTA buttons needed? Label and URL for each.
6. **Media** - Any image or file to attach? URL or local file path.
7. **Timing** - Send now, schedule for later, or recurring?
8. **Notification** - Silent (no notification) or normal?

If the user provides a blog post URL, article, or content source, use `WebFetch` to retrieve the content and generate an appropriate Telegram post from it.

## Error Handling

Common Telegram Bot API errors and how to resolve them:

| Error | Cause | Fix |
|-------|-------|-----|
| `401 Unauthorized` | Invalid bot token | Regenerate token via @BotFather |
| `400 Bad Request: chat not found` | Wrong chat ID or bot not in chat | Verify chat ID; add bot to channel as admin |
| `403 Forbidden: bot is not a member` | Bot was removed from the channel | Re-add the bot as a channel admin |
| `403 Forbidden: bot can't send messages` | Bot lacks posting permissions | Grant the bot "Post Messages" admin right |
| `429 Too Many Requests` | Rate limit exceeded | Wait the `retry_after` seconds specified in the response |
| `400 Bad Request: can't parse entities` | Malformed HTML/Markdown | Check formatting; escape special characters; switch to HTML mode |

Always check the `ok` field in the API response. If `ok` is `false`, display the `description` field to the user with guidance on how to fix the issue.

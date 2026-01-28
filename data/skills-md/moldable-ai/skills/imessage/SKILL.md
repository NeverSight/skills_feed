---
name: imessage
description: Read and send iMessages on macOS. Use when the user wants to view their messages, search conversations, list contacts, send messages, view attachments, access group chats, or get messaging statistics. Requires Full Disk Access permission granted to the host application.
---

# iMessage Skill

Full-featured iMessage API for macOS. All scripts are TypeScript and run via `npx tsx`.

## Requirements

- macOS with Messages app
- Full Disk Access granted to the terminal/application
- Node.js with `tsx` available (`npx tsx`)

## Scripts Directory

```bash
cd ~/.moldable/shared/skills/local/imessage/scripts
```

---

## Contacts & Messages

### listContacts

List all contacts ordered by most recent message.

```bash
npx tsx listContacts.ts [--limit N]
```

**Output:** `[{ id, messageCount, lastMessageDate }]`

---

### listMessages

List recent messages with optional filters.

```bash
npx tsx listMessages.ts [--contact "id"] [--limit N] [--search "text"]
```

**Output:** `[{ date, sender, isFromMe, text }]`

---

### searchMessages

Advanced search with date range support.

```bash
npx tsx searchMessages.ts --query "term" [--contact "id"] [--limit N] [--from "YYYY-MM-DD"] [--to "YYYY-MM-DD"]
```

**Output:** `[{ date, contact, sender, isFromMe, text }]`

---

### getConversation

Get full threaded conversation in chronological order.

```bash
npx tsx getConversation.ts --contact "id" [--limit N] [--before "YYYY-MM-DD"] [--after "YYYY-MM-DD"]
```

**Output:** `{ contact, messageCount, firstMessageDate, lastMessageDate, messages: [...] }`

---

### getMessage

Get a single message by ID with full metadata.

```bash
npx tsx getMessage.ts --id <messageId>
```

**Output:** `{ id, date, sender, isFromMe, text, contact, service, hasAttachment, attachmentCount, isRead, dateSent, dateDelivered, dateRead }`

---

### getContact

Get detailed stats about a specific contact.

```bash
npx tsx getContact.ts --contact "id"
```

**Output:** `{ id, service, totalMessages, messagesSent, messagesReceived, firstMessageDate, lastMessageDate, attachmentCount, avgMessagesPerDay }`

---

## Sending Messages

### sendMessage

Send an iMessage to a contact.

```bash
npx tsx sendMessage.ts --to "id" --message "text"
```

**Output:** `{ success, to, message, error? }`

⚠️ **Always confirm with the user before sending.**

---

### sendAttachment

Send an image or file via iMessage.

```bash
npx tsx sendAttachment.ts --to "id" --file "/path/to/file.jpg" [--message "caption"]
```

**Output:** `{ success, to, file, message?, error? }`

⚠️ **Always confirm with the user before sending.**

---

## Attachments

### listAttachments

List attachments with optional filters.

```bash
npx tsx listAttachments.ts [--contact "id"] [--type "image|video|audio|document"] [--limit N]
```

**Output:** `[{ id, messageId, date, contact, isFromMe, filename, mimeType, filePath, fileSize, type }]`

---

### getAttachment

Get attachment details and resolved file path.

```bash
npx tsx getAttachment.ts --id <attachmentId>
```

**Output:** `{ id, messageId, date, contact, filename, mimeType, filePath, resolvedPath, fileSize, fileExists, messageText }`

---

## Group Chats

### listGroupChats

List all group chat conversations.

```bash
npx tsx listGroupChats.ts [--limit N]
```

**Output:** `[{ id, chatIdentifier, displayName, participantCount, participants, messageCount, lastMessageDate }]`

---

### getGroupChat

Get messages from a specific group chat.

```bash
npx tsx getGroupChat.ts --id <chatId> [--limit N]
```

**Output:** `{ id, chatIdentifier, displayName, participants, messageCount, messages: [...] }`

---

### sendGroupMessage

Send a message to an existing group chat.

```bash
npx tsx sendGroupMessage.ts --id <chatId> --message "text"
```

**Output:** `{ success, chatId, chatName, message, error? }`

⚠️ **Always confirm with the user before sending.**

---

### createGroupChat

Create a new group chat and send an initial message.

```bash
npx tsx createGroupChat.ts --participants "id1,id2,id3" --message "Hello everyone!"
```

**Options:**
- `--participants` - Comma-separated emails or phone numbers (required, min 2)
- `--message` - Initial message to send (required)

**Output:** `{ success, participants, message, method?, error? }`

⚠️ **Note:** Due to macOS AppleScript limitations, this may open Messages with a pre-filled compose window requiring manual Enter to send.

⚠️ **Always confirm with the user before sending.**

---

## Analytics & Export

### getStats

Get message statistics and insights.

```bash
npx tsx getStats.ts [--contact "id"] [--year YYYY]
```

**Output:**
```json
{
  "totalMessages": 12345,
  "messagesSent": 5678,
  "messagesReceived": 6667,
  "totalContacts": 89,
  "totalAttachments": 456,
  "firstMessageDate": "2020-01-01 12:00:00",
  "lastMessageDate": "2026-01-22 12:00:00",
  "topContacts": [{ "contact": "...", "count": 1234 }],
  "messagesByMonth": [{ "month": "2026-01", "count": 500 }],
  "messagesByDayOfWeek": [{ "day": "Monday", "count": 1500 }],
  "averageMessagesPerDay": 5.67,
  "longestStreak": 45
}
```

---

### exportConversation

Export a conversation to JSON, Markdown, or plain text.

```bash
npx tsx exportConversation.ts --contact "id" [--format json|markdown|text] [--output "/path/to/file"] [--limit N]
```

**Formats:**
- `json` - Structured JSON with metadata
- `markdown` - Formatted Markdown with headers by date
- `text` - Plain text, easy to read

**Output:** Content to stdout, or writes to file if `--output` specified.

---

## Database Reference

The iMessage database is at `~/Library/Messages/chat.db`.

**Key tables:**
- `message` - All messages (ROWID, text, date, is_from_me, handle_id)
- `handle` - Contacts (ROWID, id [email/phone], service)
- `chat` - Conversations (group chats)
- `chat_message_join` - Links chats to messages
- `attachment` - File attachments
- `message_attachment_join` - Links messages to attachments

**Date conversion:** `datetime(date/1000000000 + 978307200, 'unixepoch', 'localtime')`

---
name: telegram
description: Telegram CLI for reading, searching, and sending messages. Use when the user asks about Telegram messages, wants to check inbox, search chats, send messages, or look up contacts and groups.
---

# Telegram CLI

Fast Telegram CLI for reading, searching, and sending messages.

## When to Use

Use this skill when the user:
- Asks to check Telegram messages or inbox
- Wants to search Telegram for a topic/keyword
- Wants to send a Telegram message to someone
- Asks about a Telegram group, contact, or chat
- Wants to see unread messages
- Needs to look up group members or admins

## Install

```bash
npm install -g @skillhq/telegram
```

## Authentication

First-time setup requires API credentials from https://my.telegram.org/apps

```bash
telegram auth
```

## Commands

### Reading
```bash
telegram inbox                               # Unread messages summary
telegram chats                               # List all chats
telegram read "ChatName" -n 50               # Read last 50 messages
telegram read "ChatName" --since "1h"        # Messages from last hour
telegram read @username -n 20                # Read DM with user
telegram search "query" --chat "ChatName"    # Search within chat
telegram search "query" --all                # Search all chats
```

### Writing
```bash
telegram send @username "message"            # Send DM
telegram send "GroupName" "message"          # Send to group
telegram reply "ChatName" 12345 "response"   # Reply to message ID
```

### Contacts & Groups
```bash
telegram contact @username                   # Get contact info
telegram members "GroupName"                 # List group members
telegram admins "GroupName"                  # List admins only
telegram groups --admin                      # Groups where you're admin
```

### Status
```bash
telegram whoami                              # Show logged-in account
telegram check                               # Verify session
```

## Output Formats

All commands support `--json` for structured output suitable for processing:

```bash
telegram inbox --json                        # JSON format
telegram read "Chat" --json                  # JSON with messages array
telegram chats --json                        # JSON with chat list
```

## Examples

Check inbox:
```bash
telegram inbox
```

Read recent messages from a chat:
```bash
telegram read "MetaDAO Community" -n 20
```

Search for a topic:
```bash
telegram search "futarchy" --chat "MetaDAO"
```

Send a message:
```bash
telegram send @username "Hello, checking in!"
```

## Notes

- Chat names can be partial matches (e.g., "MetaDAO" matches "MetaDAO Community")
- Usernames must start with @ (e.g., @username)
- Messages are returned in reverse chronological order (newest first)
- The `--since` flag accepts formats like "1h", "30m", "7d"

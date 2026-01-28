---
name: apple-mail-search
description: Search Apple Mail messages on macOS via direct SQLite queries. Sub-second search across all configured mail accounts without launching Mail.app.
license: MIT
metadata:
  author: Nicolai Schmid
  version: 1.0.0
  requires:
    - macOS
    - Apple Mail (configured with at least one account)
    - Python 3
scripts:
  search: ./scripts/mail-search
---

# Apple Mail Search

Direct SQL search against Apple Mail's Envelope Index database. Queries complete in under 0.5 seconds against all mail accounts.

## When to use

- You need to find emails by subject, sender, or date.
- You want to list available mailboxes and accounts.
- You need fast search without opening Mail.app.
- You want to read email content from specific messages.

## How it works

1. Reads Apple Mail's `Envelope Index` SQLite database at `~/Library/Mail/V10/MailData/`
2. Joins messages with subjects, addresses, and mailboxes tables
3. Returns metadata (subject, sender, date, mailbox) for matching messages
4. Can retrieve full email content from `.emlx` files when needed

The database is always up-to-date as Mail.app writes to it in real-time.

## Usage

```bash
# List all configured mail accounts
mail-search accounts

# List all mailboxes for an account
mail-search mailboxes --account "Wasc.me"

# Search by subject (case-insensitive, substring match)
mail-search search --subject "invoice"

# Search by sender
mail-search search --sender "github.com"

# Search in message body/preview
mail-search search --body "tracking number"

# Search within a specific account
mail-search search --subject "receipt" --account "iCloud"

# Search within a specific mailbox
mail-search search --subject "order" --mailbox "INBOX" --account "Wasc.me"

# Search by date range
mail-search search --subject "meeting" --after "2026-01-01" --before "2026-01-31"

# Limit results
mail-search search --sender "amazon" --limit 10

# Get recent messages
mail-search recent --limit 20

# Get recent messages from a specific account
mail-search recent --account "Wasc.me" --limit 10

# Read full content of a message by ID
mail-search read --id 329402

# Dump messages from a specific date
mail-search dump --date "2026-01-25"
```

### Commands

| Command     | Description                              |
| ----------- | ---------------------------------------- |
| `accounts`  | List all configured mail accounts        |
| `mailboxes` | List mailboxes for an account            |
| `search`    | Search messages by subject, sender, date |
| `recent`    | Get most recent messages                 |
| `read`      | Read full content of a specific message  |
| `dump`      | Dump all messages from a specific date   |

### Search Flags

| Flag                    | Short | Description                                     |
| ----------------------- | ----- | ----------------------------------------------- |
| `--subject <text>`      | `-s`  | Search in subject (case-insensitive substring)  |
| `--sender <text>`       | `-f`  | Search in sender address or name                |
| `--body <text>`         | `-b`  | Search in message body/preview (uses summaries) |
| `--account <name>`      | `-a`  | Filter to specific account                      |
| `--mailbox <name>`      | `-m`  | Filter to specific mailbox                      |
| `--after <YYYY-MM-DD>`  |       | Messages received after this date               |
| `--before <YYYY-MM-DD>` |       | Messages received before this date              |
| `--limit <n>`           | `-n`  | Maximum results (default: 50)                   |
| `--unread`              | `-u`  | Only show unread messages                       |
| `--flagged`             | `-F`  | Only show flagged messages                      |

### Output Format

```
[329402] 2026-01-25 22:39 | notifications@github.com (vercel[bot])
        [shadcn-ui/ui] fix: copy button copies full code even when collapsed (PR #9451)
        Mailbox: Wasc.me/INBOX
```

- First line: Message ID, date/time, sender
- Second line: Subject
- Third line: Account/Mailbox path

## Performance

| Operation             | Time  |
| --------------------- | ----- |
| List accounts         | <0.1s |
| Search (any criteria) | <0.3s |
| Read message content  | <0.2s |

## Database Schema

Key tables in `Envelope Index`:

- `messages` - Message metadata (sender, subject refs, dates, flags)
- `subjects` - Subject text (normalized)
- `addresses` - Email addresses and display names
- `mailboxes` - Mailbox URLs (account/folder structure)
- `summaries` - Email preview snippets

## Security Considerations

- Read-only access to Mail's SQLite database
- No data is modified or written
- No network requests; all local operations
- Searches happen locally; nothing leaves your machine

## Troubleshooting

- **"Database not found"**: Ensure Apple Mail has been opened at least once
- **"Database is locked"**: Mail.app may be syncing; retry in a moment
- **Empty results**: Check account/mailbox names with `accounts` and `mailboxes` commands
- **Missing message content**: Some messages may be partially downloaded (IMAP); full content requires Mail.app to download

## Limitations

- Body search uses the `summaries` table (email previews), not full message content
- For full-text body search, use `read --id` to get complete message content
- Attachments are not searchable via this tool
- Deleted messages (in Trash) may still appear until permanently deleted

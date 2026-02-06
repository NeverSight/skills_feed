---
name: himalaya
description: Use when working with himalaya CLI for email management - reading, composing, searching, organizing, or scripting email workflows
---

# Himalaya Email Workflows

CLI email client for IMAP/Maildir/Notmuch backends.

## Command Structure

**All commands follow: `himalaya <resource> <action>`**

| Resource | Actions |
|----------|---------|
| `envelope` | `list`, `thread` |
| `message` | `read`, `write`, `reply`, `forward`, `copy`, `move`, `delete` |
| `folder` | `list`, `add`, `delete`, `purge`, `expunge` |
| `flag` | `add`, `set`, `remove` |
| `attachment` | `download` |
| `template` | `write`, `reply`, `forward`, `save`, `send` |

## Quick Reference

### Inbox Triage

**Important:** Flags must come BEFORE the query filter (if any).

```fish
# List unread/new messages (use --output json for cleaner parsing)
himalaya envelope list --output json 'not flag Seen'

# List all envelopes (default: INBOX)
himalaya envelope list --output json

# List with specific folder and page
himalaya envelope list -f Archive -p 2

# Read message by ID
himalaya message read 123

# Mark as seen
himalaya flag add 123 seen

# Move to folder (TARGET first, then ID)
himalaya message move Archive 123
```

### Searching (Query DSL)

Himalaya uses its own query DSL, NOT IMAP SEARCH syntax:

```fish
# Filter by date
himalaya envelope list after 2025-01-01
himalaya envelope list before 2025-01-15
himalaya envelope list date 2025-01-10

# Filter by sender/recipient
himalaya envelope list from boss@company.com
himalaya envelope list to team@company.com

# Filter by content
himalaya envelope list subject urgent
himalaya envelope list body "project update"

# Filter by flag (use 'not flag Seen' for unread)
himalaya envelope list 'not flag Seen'
himalaya envelope list flag flagged

# Combine with operators
himalaya envelope list from boss@company.com and subject urgent
himalaya envelope list "from alice or from bob"
himalaya envelope list not flag seen

# Sort results
himalaya envelope list order by date desc
himalaya envelope list subject report order by from asc
```

### Composing

```fish
# New message (opens $EDITOR)
himalaya message write

# Reply / Reply-all
himalaya message reply 123
himalaya message reply 123 --all

# Forward
himalaya message forward 456
```

### Attachments (MML Syntax)

Attachments use MML in the message body, not command-line flags:

```
To: recipient@example.com
Subject: Files attached

Here is the document.

<#part filename=/path/to/file.pdf><#/part>

Inline image:
<#part disposition=inline filename=/path/to/image.png><#/part>
```

### Organizing

```fish
# List folders
himalaya folder list

# Move message(s) - TARGET folder comes first, then IDs
himalaya message move Archive 123 456

# Copy message(s) - TARGET folder comes first, then IDs
himalaya message copy Backup 123

# Delete (marks as deleted)
himalaya message delete 123

# Expunge (permanent delete)
himalaya folder expunge INBOX
```

### Scripting

```fish
# JSON output for parsing
himalaya envelope list --output json
himalaya envelope list --output json | jq '.[].id'

# Specific account
himalaya envelope list -a work

# Combine for automation
himalaya envelope list --output json 'not flag Seen' | jq -r '.[].id' | while read id
    himalaya message read $id
end
```

## Common Flags

| Flag | Description |
|------|-------------|
| `-a, --account <NAME>` | Use specific account |
| `-f, --folder <NAME>` | Target folder (default: INBOX) |
| `-o, --output <FORMAT>` | `plain` or `json` (prefer `json` for scripting/AI parsing) |
| `-p, --page <N>` | Page number (starts at 1) |
| `-s, --page-size <N>` | Results per page |

**Note:** Always use `--output json` when parsing output programmatically. Plain output includes WARN log messages that interfere with parsing. Flags must come BEFORE any query filter.

### Templates (Non-Interactive)

Generate messages without opening `$EDITOR`:

```fish
# Generate template (stdout)
himalaya template write
himalaya template reply 123
himalaya template forward 456

# Pipe and send
echo "To: x@y.com\nSubject: Hi\n\nHello" | himalaya template send
```

## Common Mistakes

| Wrong | Right | Why |
|-------|-------|-----|
| `himalaya list` | `himalaya envelope list` | Need resource prefix |
| `himalaya read 123` | `himalaya message read 123` | Need resource prefix |
| `himalaya write -a file.pdf` | MML `<#part>` in body | No `-a` flag exists |
| `--query "FROM x"` | `from x` | Himalaya DSL, not IMAP |
| `himalaya search ...` | `himalaya envelope list ...` | No `search` command |
| `himalaya envelope list 'query' -o json` | `himalaya envelope list --output json 'query'` | Flags must come before query |
| `himalaya message move 123 Folder` | `himalaya message move Folder 123` | Target folder comes first |

---
name: email-himalaya
description: Manage emails using the himalaya CLI client. This skill should be used when the user wants to read, list, search, send, reply to, or manage emails across their configured accounts.
---

# Email Management with Himalaya

This skill provides email management capabilities using the himalaya CLI email client.

## Configured Accounts

Configure your accounts in `~/.config/himalaya/config.toml`. Example:

| Account Name | Email | Purpose |
|--------------|-------|---------|
| **Work** | work@example.com | Work - Default |
| **Personal** | personal@gmail.com | Personal |

## Core Commands

### Listing Emails

```bash
# List inbox (default account)
himalaya envelope list --page-size 10

# List from specific account
himalaya envelope list --account "Personal" --page-size 10

# List from specific folder
himalaya envelope list --folder "[Gmail]/Important" --page-size 10

# JSON output for parsing
himalaya envelope list --output json --page-size 10
```

### Reading Emails

```bash
# Read email by ID
himalaya message read <id>

# Read in plain text
himalaya message read <id> --header "From,To,Subject,Date"
```

**IMPORTANT: Keeping Emails Unread**

When reading emails, himalaya marks them as read. To preserve the unread status for the user:

```bash
# After reading, mark back as unread
himalaya flag remove <id> Seen
```

Always mark emails back as unread after reading unless the user explicitly says they've read it or asks to mark it as read.

### Sending Emails

```bash
# Send using heredoc
himalaya message send --account "Account Name" <<'EOF'
From: Display Name <email@example.com>
To: recipient@example.com
Subject: Subject Line

Email body here.

Signature
EOF
```

### Replying to Emails

```bash
# Reply to an email
himalaya message reply <id> <<'EOF'
Reply body here.
EOF
```

### Managing Flags

```bash
# Mark as read
himalaya flag add <id> Seen

# Mark as unread
himalaya flag remove <id> Seen

# Star/flag email
himalaya flag add <id> Flagged

# Remove star
himalaya flag remove <id> Flagged
```

### Searching Emails

```bash
# Search by subject
himalaya envelope list --query "subject:keyword"

# Search by sender
himalaya envelope list --query "from:sender@example.com"
```

### Folders

```bash
# List folders
himalaya folder list

# Common Gmail folders
# - INBOX
# - [Gmail]/Sent Mail
# - [Gmail]/Drafts
# - [Gmail]/Trash
# - [Gmail]/Important
# - [Gmail]/Starred
```

## Workflow Guidelines

1. **Listing emails**: Use `envelope list` - this does NOT mark emails as read
2. **Reading emails**: After reading with `message read`, immediately run `flag remove <id> Seen` to keep unread unless user indicates otherwise
3. **Multiple accounts**: Always specify `--account "Account Name"` when working with non-default account
4. **Sending emails**: Draft the email content and show to user for approval before sending
5. **Replying**: Read the original email first to understand context, then draft reply for user approval

## Common Tasks

### Check unread emails across both accounts

```bash
himalaya envelope list --account "Work" --page-size 10
himalaya envelope list --account "Personal" --page-size 10
```

### Read and keep unread

```bash
himalaya message read <id>
himalaya flag remove <id> Seen
```

### Send from personal account

```bash
himalaya message send --account "Personal" <<'EOF'
From: Your Name <personal@gmail.com>
To: recipient@example.com
Subject: Subject

Body
EOF
```

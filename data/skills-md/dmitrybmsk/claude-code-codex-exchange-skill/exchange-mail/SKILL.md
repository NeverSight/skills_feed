---
name: exchange-mail
description: "Full email management for Microsoft Exchange/Outlook. Use when Claude needs to list unread emails, read email content, reply to emails, mark emails as read, or archive emails. Supports batch operations for external/internal emails. Triggers: check my email, unread emails, reply to email, archive external emails, mark as read."
---

# Exchange Mail

Manage Microsoft Exchange/Outlook emails from terminal.

## Script Location

`scripts/exchange_mail.py` - Main CLI script

## Commands

```bash
# List unread (today, where you're To/CC)
python3 scripts/exchange_mail.py list

# List options
python3 scripts/exchange_mail.py list --days 3    # Last 3 days
python3 scripts/exchange_mail.py list --all       # All unread
python3 scripts/exchange_mail.py list --json      # JSON output

# Read email
python3 scripts/exchange_mail.py read <id>

# Reply
python3 scripts/exchange_mail.py reply <id> "Your message"

# Mark as read
python3 scripts/exchange_mail.py mark-read <id>
python3 scripts/exchange_mail.py mark-read --external
python3 scripts/exchange_mail.py mark-read --internal
python3 scripts/exchange_mail.py mark-read --all

# Archive
python3 scripts/exchange_mail.py archive <id>
python3 scripts/exchange_mail.py archive --external
python3 scripts/exchange_mail.py archive --internal --days 7
```

## Email IDs

Each email gets stable 8-char hex ID (e.g., `b7bc8d99`). Use for all commands.

## Output Format

```
📧 9 unread emails today:

━━━ Internal (4) ━━━
[b7bc8d99] [13:57] John Smith
        Re: Project Discussion

━━━ External (5) ━━━
[43e56cc9] [09:50] newsletter@company.com
        Weekly Update
```

## Batch Flags

- `--external` - Only external emails (outside your domain)
- `--internal` - Only internal emails (your domain)
- `--all` - All emails
- `--days N` - Look back N days (default: today only)

## Environment Variables

Required in shell config:
```bash
export EXCHANGE_SERVER="mail.company.com"
export EXCHANGE_EMAIL="user@company.com"
export EXCHANGE_USERNAME="username"
export EXCHANGE_PASSWORD="password"
```

## Workflow Examples

```bash
# Morning: check → read → reply → archive spam
python3 scripts/exchange_mail.py list
python3 scripts/exchange_mail.py read abc123
python3 scripts/exchange_mail.py reply abc123 "Thanks!"
python3 scripts/exchange_mail.py archive --external

# Weekly cleanup
python3 scripts/exchange_mail.py archive --external --days 7
```

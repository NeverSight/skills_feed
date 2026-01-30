---
name: gmail-skill
description: Read, search, send, and draft Gmail emails and Google contacts. Use when the user asks to check email, find emails, search messages, send emails, create drafts, look up contacts, or find someone's email/phone. Supports multiple accounts.
allowed-tools: Bash, Read
---

# Gmail Skill - Email & Contacts Access

Read, search, and send Gmail emails. Access Google contacts.

## CRITICAL: Email Sending Confirmation Required

**Before sending ANY email, you MUST get explicit user confirmation.**

When the user asks to send an email:
1. First, show them the complete email details:
   - From (which account)
   - To
   - CC/BCC (if any)
   - Subject
   - Full body text
2. Ask: "Do you want me to send this email?"
3. ONLY run the send command AFTER the user explicitly confirms (e.g., "yes", "send it", "go ahead")
4. NEVER send an email without this confirmation, even if the user asked you to send it initially

This applies even when:
- The user says "send an email to X"
- You are in "dangerously skip permissions" mode
- The user seems to be in a hurry

Always confirm first. No exceptions.

## First-Time Setup (One-Time, ~2 minutes)

On first run, the script will guide you through setup. You need to create a Google Cloud OAuth client once:

1. Go to [Google Cloud Console](https://console.cloud.google.com/apis/credentials)
2. Create a project (or select existing)
3. Enable **Gmail API** and **People API** (APIs & Services → Library)
4. Configure OAuth consent screen:
   - User Type: External
   - App name: Gmail Skill
   - Add yourself as test user
   - Add scopes: `gmail.readonly`, `gmail.send`, `gmail.modify`, `contacts.readonly`
5. Create OAuth client ID:
   - Application type: **Desktop app**
   - Download JSON → save as `~/.claude/skills/gmail-skill/credentials.json`

Then just run any command - browser opens, you approve, done. Works for all your accounts.

**Note:** If you previously used gmail-reader, you'll need to re-authenticate to grant the new `gmail.send` scope.

## Commands

### Search Emails

```bash
python3 ~/.claude/skills/gmail-skill/gmail_skill.py search "query" [--max-results N] [--account EMAIL]
```

**Query examples:**
- `from:john@example.com` - from specific sender
- `subject:meeting after:2026/01/01` - subject + date
- `has:attachment filename:pdf` - with PDF attachments
- `is:unread` - unread emails
- `"exact phrase"` - exact match

### Read Email

```bash
python3 ~/.claude/skills/gmail-skill/gmail_skill.py read EMAIL_ID [--account EMAIL]
```

### List Recent Emails

```bash
python3 ~/.claude/skills/gmail-skill/gmail_skill.py list [--max-results N] [--label LABEL] [--account EMAIL]
```

### Send Email (Requires Confirmation)

```bash
python3 ~/.claude/skills/gmail-skill/gmail_skill.py send --to EMAIL --subject "Subject" --body "Body text" [--cc EMAIL] [--bcc EMAIL] [--account EMAIL]
```

**Required arguments:**
- `--to` / `-t` - Recipient email address
- `--subject` / `-s` - Email subject line
- `--body` / `-b` - Email body text

**Optional arguments:**
- `--cc` - CC recipients (comma-separated)
- `--bcc` - BCC recipients (comma-separated)
- `--account` / `-a` - Send from specific account

**Example:**
```bash
python3 ~/.claude/skills/gmail-skill/gmail_skill.py send \
  --to "recipient@example.com" \
  --subject "Meeting Tomorrow" \
  --body "Hi, just confirming our meeting at 2pm tomorrow." \
  --account work@company.com
```

### Mark as Read

```bash
python3 ~/.claude/skills/gmail-skill/gmail_skill.py mark-read EMAIL_ID [--account EMAIL]
```

### Mark as Unread

```bash
python3 ~/.claude/skills/gmail-skill/gmail_skill.py mark-unread EMAIL_ID [--account EMAIL]
```

Both mark-read and mark-unread support multiple IDs (comma-separated):
```bash
python3 ~/.claude/skills/gmail-skill/gmail_skill.py mark-read "id1,id2,id3" --account user@gmail.com
```

### Mark Done (Archive)

Archives email(s) by removing from inbox. Equivalent to Gmail's 'e' keyboard shortcut.

```bash
python3 ~/.claude/skills/gmail-skill/gmail_skill.py mark-done EMAIL_ID [--account EMAIL]
```

### Unarchive

Moves email(s) back to inbox (undo archive).

```bash
python3 ~/.claude/skills/gmail-skill/gmail_skill.py unarchive EMAIL_ID [--account EMAIL]
```

### Star / Unstar

```bash
python3 ~/.claude/skills/gmail-skill/gmail_skill.py star EMAIL_ID [--account EMAIL]
python3 ~/.claude/skills/gmail-skill/gmail_skill.py unstar EMAIL_ID [--account EMAIL]
```

All label commands support multiple IDs (comma-separated):
```bash
python3 ~/.claude/skills/gmail-skill/gmail_skill.py star "id1,id2,id3" --account user@gmail.com
```

### Create Draft

Creates a draft email. Use `--reply-to-id` when replying to an existing email to ensure proper threading in email clients like Superhuman.

```bash
python3 ~/.claude/skills/gmail-skill/gmail_skill.py draft --to EMAIL --subject "Subject" --body "Body text" [--reply-to-id EMAIL_ID] [--cc EMAIL] [--bcc EMAIL] [--account EMAIL]
```

**Required arguments:**
- `--to` / `-t` - Recipient email address
- `--subject` / `-s` - Email subject line
- `--body` / `-b` - Email body text

**Optional arguments:**
- `--reply-to-id` / `-r` - Message ID to reply to (adds proper In-Reply-To and References headers for threading)
- `--cc` - CC recipients (comma-separated)
- `--bcc` - BCC recipients (comma-separated)
- `--account` / `-a` - Create draft in specific account

**Example (new email):**
```bash
python3 ~/.claude/skills/gmail-skill/gmail_skill.py draft \
  --to "recipient@example.com" \
  --subject "Draft for Review" \
  --body "Here's my draft message."
```

**Example (reply to existing email):**
```bash
python3 ~/.claude/skills/gmail-skill/gmail_skill.py draft \
  --to "sender@example.com" \
  --subject "Re: Original Subject" \
  --body "Thanks for your email..." \
  --reply-to-id 19b99b3127793843 \
  --account work@company.com
```

### List Labels

```bash
python3 ~/.claude/skills/gmail-skill/gmail_skill.py labels [--account EMAIL]
```

### List Contacts

```bash
python3 ~/.claude/skills/gmail-skill/gmail_skill.py contacts [--max-results N] [--account EMAIL]
```

### Search Contacts

```bash
python3 ~/.claude/skills/gmail-skill/gmail_skill.py search-contacts "query" [--account EMAIL]
```

### Manage Accounts

```bash
# List all authenticated accounts
python3 ~/.claude/skills/gmail-skill/gmail_skill.py accounts

# Remove an account
python3 ~/.claude/skills/gmail-skill/gmail_skill.py logout --account user@gmail.com
```

## Multi-Account Support

Add accounts by using `--account` with a new email - browser opens for that account:

```bash
# First account (auto-authenticates)
python3 ~/.claude/skills/gmail-skill/gmail_skill.py list

# Add work account
python3 ~/.claude/skills/gmail-skill/gmail_skill.py list --account work@company.com

# Add personal account
python3 ~/.claude/skills/gmail-skill/gmail_skill.py list --account personal@gmail.com

# Use specific account
python3 ~/.claude/skills/gmail-skill/gmail_skill.py search "from:boss" --account work@company.com
```

Tokens are stored per-account in `~/.claude/skills/gmail-skill/tokens/`

## Examples

### Find unread emails from this week

```bash
python3 ~/.claude/skills/gmail-skill/gmail_skill.py search "is:unread after:2026/01/01"
```

### Read a specific email

```bash
python3 ~/.claude/skills/gmail-skill/gmail_skill.py read 18d5a3b2c1f4e5d6
```

### Send a quick email

```bash
python3 ~/.claude/skills/gmail-skill/gmail_skill.py send \
  --to "friend@example.com" \
  --subject "Hello!" \
  --body "Just wanted to say hi."
```

### Find someone's contact info

```bash
python3 ~/.claude/skills/gmail-skill/gmail_skill.py search-contacts "John Smith"
```

### Check work email from personal machine

```bash
python3 ~/.claude/skills/gmail-skill/gmail_skill.py list --account work@company.com --max-results 5
```

## Output

All commands output JSON for easy parsing.

## Requirements

- Python 3.9+
- `pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client requests`

## Security Notes

- **Send confirmation required** - Claude must always confirm with the user before sending emails
- Tokens stored locally in `~/.claude/skills/gmail-skill/tokens/`
- Revoke access anytime: https://myaccount.google.com/permissions
- Apps in "testing" mode may require re-auth every 7 days (publish app to avoid)

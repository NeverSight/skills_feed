---
name: gmail
description: Manage Gmail messages, drafts, and labels. Send emails, search inbox, and organize email. Use when working with Gmail email management.
metadata:
  author: odyssey4me
  version: "0.1.0"
license: MIT
---

# Gmail

Interact with Gmail for email management, search, and organization.

## Installation

1. **Install Python dependencies**:
   ```bash
   pip install --user google-auth google-auth-oauthlib google-api-python-client keyring pyyaml
   ```

2. **Download the skill** from [Releases](https://github.com/odyssey4me/agent-skills/releases) or use directly from this repository.

## Setup Verification

After installation, verify the skill is properly configured:

```bash
python scripts/gmail.py check
```

This will check:
- Python dependencies (google-auth, google-auth-oauthlib, google-api-python-client, keyring, pyyaml)
- Authentication configuration
- Connectivity to Gmail API

If anything is missing, the check command will provide setup instructions.

## Authentication

Gmail uses OAuth 2.0 for authentication. For complete setup instructions, see:

1. [GCP Project Setup Guide](../../docs/gcp-project-setup.md) - Create project, enable Gmail API
2. [Google OAuth Setup Guide](../../docs/google-oauth-setup.md) - Configure credentials

### Quick Start

1. Create `~/.config/agent-skills/google.yaml`:
   ```yaml
   oauth_client:
     client_id: your-client-id.apps.googleusercontent.com
     client_secret: your-client-secret
   ```

2. Run `python scripts/gmail.py check` to trigger OAuth flow and verify setup.

### OAuth Scopes

The skill requests granular scopes for different operations:

| Scope | Permission | Used For |
|-------|-----------|----------|
| `gmail.readonly` | Read messages, labels, settings | Listing and reading messages |
| `gmail.send` | Send emails | Sending messages and drafts |
| `gmail.modify` | Modify labels and metadata | Managing labels on messages |
| `gmail.labels` | Manage labels | Creating and listing labels |

### Scope Errors

If you encounter "insufficient scope" errors, revoke your token and re-authenticate:

1. Revoke at https://myaccount.google.com/permissions
2. Clear token: `keyring del agent-skills gmail-token-json`
3. Re-run: `python scripts/gmail.py check`

## Commands

### check

Verify configuration and connectivity.

```bash
python scripts/gmail.py check
```

This validates:
- Python dependencies are installed
- Authentication is configured
- Can connect to Gmail API
- Displays your email address and mailbox statistics

### auth setup

Store OAuth 2.0 client credentials for custom OAuth flow.

```bash
python scripts/gmail.py auth setup \
  --client-id YOUR_CLIENT_ID \
  --client-secret YOUR_CLIENT_SECRET
```

Credentials are saved to `~/.config/agent-skills/gmail.yaml`.

### messages list

List messages matching a query.

```bash
# List recent messages
python scripts/gmail.py messages list

# Search for unread messages
python scripts/gmail.py messages list --query "is:unread"

# Search with max results
python scripts/gmail.py messages list --query "from:user@example.com" --max-results 20

# Output as JSON
python scripts/gmail.py messages list --query "subject:meeting" --json
```

**Arguments:**
- `--query`: Gmail search query (optional)
- `--max-results`: Maximum number of results (default: 10)
- `--json`: Output as JSON

**Search Query Examples:**

For complete Gmail search syntax, see [gmail-queries.md](references/gmail-queries.md).

Common queries:
- `is:unread` - Unread messages
- `from:user@example.com` - Messages from sender
- `subject:meeting` - Messages with subject keyword
- `has:attachment` - Messages with attachments
- `after:2024/01/01` - Messages after date
- `label:important` - Messages with label

### messages get

Get a message by ID.

```bash
# Get full message
python scripts/gmail.py messages get MESSAGE_ID

# Get minimal format
python scripts/gmail.py messages get MESSAGE_ID --format minimal

# Output as JSON
python scripts/gmail.py messages get MESSAGE_ID --json
```

**Arguments:**
- `message_id`: The message ID (required)
- `--format`: Message format (full, minimal, raw, metadata) - default: full
- `--json`: Output as JSON

### send

Send an email message.

```bash
# Send simple email
python scripts/gmail.py send \
  --to recipient@example.com \
  --subject "Hello" \
  --body "This is the message body"

# Send with CC and BCC
python scripts/gmail.py send \
  --to recipient@example.com \
  --subject "Team Update" \
  --body "Here's the update..." \
  --cc team@example.com \
  --bcc boss@example.com

# Output as JSON
python scripts/gmail.py send \
  --to user@example.com \
  --subject "Test" \
  --body "Test message" \
  --json
```

**Arguments:**
- `--to`: Recipient email address (required)
- `--subject`: Email subject (required)
- `--body`: Email body text (required)
- `--cc`: CC recipients (comma-separated)
- `--bcc`: BCC recipients (comma-separated)
- `--json`: Output as JSON

### drafts list

List draft messages.

```bash
# List drafts
python scripts/gmail.py drafts list

# List with custom max results
python scripts/gmail.py drafts list --max-results 20

# Output as JSON
python scripts/gmail.py drafts list --json
```

**Arguments:**
- `--max-results`: Maximum number of results (default: 10)
- `--json`: Output as JSON

### drafts create

Create a draft email.

```bash
# Create draft
python scripts/gmail.py drafts create \
  --to recipient@example.com \
  --subject "Draft Subject" \
  --body "This is a draft message"

# Create draft with CC
python scripts/gmail.py drafts create \
  --to recipient@example.com \
  --subject "Meeting Notes" \
  --body "Notes from today's meeting..." \
  --cc team@example.com

# Output as JSON
python scripts/gmail.py drafts create \
  --to user@example.com \
  --subject "Test Draft" \
  --body "Draft body" \
  --json
```

**Arguments:**
- `--to`: Recipient email address (required)
- `--subject`: Email subject (required)
- `--body`: Email body text (required)
- `--cc`: CC recipients (comma-separated)
- `--bcc`: BCC recipients (comma-separated)
- `--json`: Output as JSON

### drafts send

Send a draft message.

```bash
# Send draft by ID
python scripts/gmail.py drafts send DRAFT_ID

# Output as JSON
python scripts/gmail.py drafts send DRAFT_ID --json
```

**Arguments:**
- `draft_id`: The draft ID to send (required)
- `--json`: Output as JSON

### labels list

List all Gmail labels.

```bash
# List labels
python scripts/gmail.py labels list

# Output as JSON
python scripts/gmail.py labels list --json
```

**Arguments:**
- `--json`: Output as JSON

### labels create

Create a new label.

```bash
# Create label
python scripts/gmail.py labels create "Project X"

# Output as JSON
python scripts/gmail.py labels create "Important" --json
```

**Arguments:**
- `name`: Label name (required)
- `--json`: Output as JSON

## Examples

### Verify Setup

```bash
python scripts/gmail.py check
```

### Find unread emails

```bash
python scripts/gmail.py messages list --query "is:unread"
```

### Search for emails from a sender

```bash
python scripts/gmail.py messages list --query "from:boss@example.com" --max-results 5
```

### Send a quick email

```bash
python scripts/gmail.py send \
  --to colleague@example.com \
  --subject "Quick Question" \
  --body "Do you have time for a meeting tomorrow?"
```

### Create and send a draft

```bash
# Create draft
python scripts/gmail.py drafts create \
  --to team@example.com \
  --subject "Weekly Update" \
  --body "Here's this week's update..."

# List drafts to get the ID
python scripts/gmail.py drafts list

# Send the draft
python scripts/gmail.py drafts send DRAFT_ID
```

### Organize with labels

```bash
# Create a label
python scripts/gmail.py labels create "Project Alpha"

# List all labels
python scripts/gmail.py labels list
```

### Advanced searches

```bash
# Find emails with attachments from last week
python scripts/gmail.py messages list --query "has:attachment newer_than:7d"

# Find important emails from specific sender
python scripts/gmail.py messages list --query "from:ceo@example.com is:important"

# Find emails in a conversation
python scripts/gmail.py messages list --query "subject:project-alpha"
```

## Gmail Search Query Syntax

Common search operators:

| Operator | Description | Example |
|----------|-------------|---------|
| `from:` | Sender email | `from:user@example.com` |
| `to:` | Recipient email | `to:user@example.com` |
| `subject:` | Subject contains | `subject:meeting` |
| `label:` | Has label | `label:important` |
| `has:attachment` | Has attachment | `has:attachment` |
| `is:unread` | Unread messages | `is:unread` |
| `is:starred` | Starred messages | `is:starred` |
| `after:` | After date | `after:2024/01/01` |
| `before:` | Before date | `before:2024/12/31` |
| `newer_than:` | Newer than period | `newer_than:7d` |
| `older_than:` | Older than period | `older_than:30d` |

Combine operators with spaces (implicit AND) or `OR`:

```bash
# AND (implicit)
from:user@example.com subject:meeting

# OR
from:user@example.com OR from:other@example.com

# Grouping with parentheses
(from:user@example.com OR from:other@example.com) subject:meeting
```

For the complete reference, see [gmail-queries.md](references/gmail-queries.md).

## Troubleshooting

### Check command fails

Run `python scripts/gmail.py check` to diagnose issues. It will provide specific error messages and setup instructions.

### Authentication failed

1. Verify your OAuth client ID and client secret are correct in `~/.config/agent-skills/google.yaml`
2. Token expired or corrupted - clear and re-authenticate:
   ```bash
   keyring del agent-skills gmail-token-json
   python scripts/gmail.py check
   ```

### Permission denied

Your OAuth token may not have the necessary scopes. Revoke access at https://myaccount.google.com/permissions, clear your token, and re-authenticate.

### Import errors

Ensure dependencies are installed:
```bash
pip install --user google-auth google-auth-oauthlib google-api-python-client keyring pyyaml
```

### Rate limiting

Gmail API has quota limits. If you hit rate limits, wait a few minutes before retrying. For high-volume usage, consider requesting quota increases in the Google Cloud Console.

## API Scopes

This skill requests the following OAuth scopes:

- `https://www.googleapis.com/auth/gmail.readonly` - Read email messages and settings
- `https://www.googleapis.com/auth/gmail.send` - Send email messages
- `https://www.googleapis.com/auth/gmail.modify` - Modify labels and message metadata
- `https://www.googleapis.com/auth/gmail.labels` - Manage labels

These scopes provide full email management capabilities while following the principle of least privilege.

## Security Notes

- **OAuth tokens** are stored securely in your system keyring
- **Client secrets** are stored in `~/.config/agent-skills/gmail.yaml` with file permissions 600
- **No passwords** are stored - only OAuth tokens
- **Tokens refresh automatically** when using the skill
- **Browser-based consent** ensures you approve all requested permissions

Always review OAuth consent screens before granting access to your Gmail account.

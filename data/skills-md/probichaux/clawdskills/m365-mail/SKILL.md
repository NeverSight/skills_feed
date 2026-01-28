---
name: m365-mail
description: Read, search, send, and manage Microsoft 365 email via Graph API. Use when the user asks about email, inbox, messages, or wants to send/read/search mail in their M365 account.
---

# Microsoft 365 Mail

CLI tool for Microsoft 365 email via Microsoft Graph API.

## Setup (One-time)

### 1. Register Entra ID App

1. Go to [Entra ID Portal](https://entra.microsoft.com/) → App registrations → New registration
2. Name: `m365mail-cli` (or whatever)
3. Supported account types: "Accounts in this organizational directory only"
4. Redirect URI: Leave blank (using device code flow)
5. Click Register

### 2. Configure API Permissions

1. In your app → API permissions → Add a permission
2. Microsoft Graph → Delegated permissions
3. Add: `Mail.ReadWrite`, `Mail.Send`
4. Click "Grant admin consent" (or have admin do it)

### 3. Enable Public Client Flow

1. In your app → Authentication
2. Under "Advanced settings", set "Allow public client flows" to **Yes**
3. Save

### 4. Note Your IDs

- **Application (client) ID**: Found on app Overview page
- **Directory (tenant) ID**: Found on app Overview page

### 5. Install & Configure

```bash
# Install dependencies
pip install msal requests

# Make executable
chmod +x skills/m365-mail/scripts/m365mail.py

# Optional: symlink to PATH
ln -s $(pwd)/skills/m365-mail/scripts/m365mail.py /usr/local/bin/m365mail

# Configure
m365mail setup --client-id <YOUR_CLIENT_ID> --tenant-id <YOUR_TENANT_ID>

# Authenticate (opens browser for device code)
m365mail auth
```

## Commands

### List Inbox
```bash
m365mail inbox                    # Last 20 messages
m365mail inbox -n 50              # Last 50 messages
m365mail inbox -u                 # Unread only
m365mail inbox -v                 # With preview
m365mail inbox --json             # JSON output
```

### Read Message
```bash
m365mail read <message_id>        # Full message
m365mail read <id> --max-length 500  # Truncate body
m365mail read <id> --json         # JSON output
```

### Search
```bash
m365mail search "quarterly report"      # Full-text search
m365mail search -f boss@company.com     # From specific sender
m365mail search -u                      # Unread only
m365mail search -a                      # Has attachments
m365mail search "budget" -f cfo@co.com -u  # Combine filters
```

### Send Email
```bash
m365mail send --to user@example.com --subject "Hello" --body "Message body"
m365mail send --to a@x.com b@x.com --cc c@x.com --subject "Hi" --body "Text"
m365mail send --to user@x.com --subject "Report" --body-file report.txt
m365mail send --to user@x.com --subject "HTML" --body "<h1>Hi</h1>" --html
```

### Manage Messages
```bash
m365mail folders                  # List all folders
m365mail move <message_id> Archive    # Move to folder
m365mail move <message_id> "Deleted Items"
m365mail delete <message_id>      # Permanently delete
m365mail mark <message_id> --read     # Mark read
m365mail mark <message_id> --unread   # Mark unread
```

## Output Formats

- Default: Human-readable table/text
- `--json`: Machine-readable JSON (use for programmatic access)
- `-v`/`--verbose`: Include message preview

## Message IDs

Messages are identified by long IDs like `AAMkAGI2...`. Commands accept:
- Full ID
- ID prefix (first 8+ chars usually unique)

The inbox/search output shows `[AAMkAGI2]` prefixes for easy reference.

## Token Storage

Tokens cached at `~/.m365mail/`:
- `config.json` - Client/tenant IDs
- `token_cache.json` - OAuth tokens (auto-refreshes)

## Troubleshooting

**"No cached token"**: Run `m365mail auth`

**Permission denied**: Ensure Mail.ReadWrite and Mail.Send permissions are granted (may need admin consent)

**Token expired**: Tool auto-refreshes; if issues persist, run `m365mail auth` again

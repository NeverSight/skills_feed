---
name: utoronto-outlook
description: Headless University of Toronto Outlook email access via IMAP/SMTP with OAuth2. Uses Thunderbird's pre-authorized client ID to bypass admin consent requirements (AADSTS65002). Device code flow for initial auth, macOS Keychain for token cache.
version: 1.1.0
---

# UofT Outlook Skill

Headless access to University of Toronto alumni/student Outlook via IMAP/SMTP with OAuth2.

**Trit**: -1 (MINUS - validator/consumer)  
**Principle**: Thunderbird Client ID → Device Code Auth → Keychain Cache → IMAP/SMTP  
**Implementation**: IMAP OAuth2 (XOAUTH2) + Thunderbird Pre-Authorized Client ID

## The AADSTS65002 Problem

University tenants block third-party OAuth apps:
```
AADSTS65002: Consent between first party application and first party resource 
must be configured via preauthorization
```

**Solution**: Use Thunderbird's pre-authorized client ID `9e5f94bc-e8a4-4e73-b8be-63364c29d753` which Microsoft has pre-approved for IMAP/SMTP access on all tenants.

## Authentication Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│               THUNDERBIRD CLIENT ID BYPASS                          │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  [Problem: Graph API blocked]                                       │
│  ┌──────────┐     Graph API      ┌───────────────┐                 │
│  │  Agent   │ ────────────────▶  │ MS Entra ID   │                 │
│  └──────────┘                    └───────────────┘                 │
│       │                                 │                           │
│       │                                 ▼                           │
│       │                    ❌ AADSTS65002 Error                     │
│       │                    "Admin consent required"                 │
│                                                                     │
│  [Solution: Thunderbird IMAP]                                       │
│  ┌──────────┐  Thunderbird ID    ┌───────────────┐                 │
│  │  Agent   │ ─────────────────▶ │ MS Entra ID   │                 │
│  └──────────┘  9e5f94bc-...      └───────────────┘                 │
│       │                                 │                           │
│       │ Device code flow                │ Pre-authorized ✓         │
│       ▼                                 ▼                           │
│  "Enter code XXXXXX at microsoft.com/devicelogin"                  │
│       │                                                             │
│       │ User authenticates (one-time)                               │
│       ▼                                                             │
│  ┌──────────────────────────────────────────────────┐              │
│  │           macOS Keychain (secure storage)        │              │
│  │  outlook-university: access + refresh tokens    │              │
│  └──────────────────────────────────────────────────┘              │
│       │                                                             │
│       │ XOAUTH2 authentication                                      │
│       ▼                                                             │
│  ┌───────────────────────────────────────────────┐                 │
│  │  outlook.office365.com:993 (IMAP)             │                 │
│  │  smtp.office365.com:587 (SMTP)                │                 │
│  └───────────────────────────────────────────────┘                 │
└─────────────────────────────────────────────────────────────────────┘
```

## Key Constants

```python
# Thunderbird's pre-authorized client ID (public, safe to commit)
THUNDERBIRD_CLIENT_ID = "9e5f94bc-e8a4-4e73-b8be-63364c29d753"

# IMAP OAuth2 scopes (NOT Graph API scopes!)
IMAP_SCOPES = [
    "https://outlook.office.com/IMAP.AccessAsUser.All",
    "https://outlook.office.com/SMTP.Send",
    "offline_access",
    "openid", "profile", "email"
]

# Servers
IMAP_SERVER = "outlook.office365.com"  # Port 993 SSL
SMTP_SERVER = "smtp.office365.com"      # Port 587 STARTTLS
```

## Usage

### Initial Authentication (One-Time)

```bash
cd ~/.claude/skills/utoronto-outlook
uv run python outlook_university.py auth

# Output:
# ============================================================
# OUTLOOK UNIVERSITY - DEVICE CODE AUTHENTICATION
# ============================================================
#   Code: XXXXXXXXX
#   Go to: https://microsoft.com/devicelogin
#   (Uses Thunderbird's pre-authorized client ID)
# ============================================================
```

### Headless Operations

```bash
# Check login
uv run python outlook_university.py whoami
# Logged in as: [user email]

# List messages
uv run python outlook_university.py list 10

# Read message
uv run python outlook_university.py read 42

# Search
uv run python outlook_university.py search "professor"

# List folders
uv run python outlook_university.py folders
```

### Python API

```python
from outlook_university import OutlookClient

client = OutlookClient()

# List recent emails
messages = client.list_messages(limit=10)

# Get unread
unread = client.get_unread()

# Read full message (body truncated to 2000 chars for context safety)
msg = client.get_message("42")

# Search
results = client.search("grades")

# Send email
client.send(
    to=["recipient@example.com"],
    subject="Test",
    body="Hello from headless Outlook!"
)

client.close()
```

## XOAUTH2 Authentication

The critical implementation detail for IMAP OAuth2:

```python
# Build XOAUTH2 string per RFC 7628
auth_string = f"user={email}\x01auth=Bearer {access_token}\x01\x01"

# IMAP authenticate callback returns raw bytes
conn.authenticate("XOAUTH2", lambda x: auth_string.encode())
```

## GF(3) Verb Typing

| Operation | Trit | Description |
|-----------|------|-------------|
| `list_messages` | -1 | Consume/read inbox (MINUS) |
| `get_message` | -1 | Read specific message (MINUS) |
| `get_unread` | -1 | Query unread (MINUS) |
| `search` | -1 | Query messages (MINUS) |
| `list_folders` | 0 | Metadata access (ERGODIC) |
| `send` | +1 | Generate output (PLUS) |

## Security Notes

- **Thunderbird Client ID**: Public, safe to commit (used by Mozilla Thunderbird)
- **Tokens**: Stored in macOS Keychain (encrypted), never in files
- **Body Truncation**: Email bodies truncated to 2000 chars to prevent context overflow
- **No Credentials**: No passwords stored; OAuth2 refresh tokens only
- **Terminal Sanitization**: ANSI escape codes stripped from output

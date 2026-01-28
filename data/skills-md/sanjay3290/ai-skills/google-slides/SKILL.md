---
name: google-slides
description: |
  Read content from Google Slides presentations - get text, find presentations, and retrieve metadata.
  Use when user asks to: read a presentation, find slides, get presentation content, search for a slideshow,
  or check presentation details. Lightweight alternative to full Google Workspace MCP server with standalone
  OAuth authentication. Read-only operations only.
---

# Google Slides

Lightweight Google Slides integration with standalone OAuth authentication. No MCP server required.

> **⚠️ Requires Google Workspace account.** Personal Gmail accounts are not supported.

## First-Time Setup

Authenticate with Google (opens browser):
```bash
python scripts/auth.py login
```

Check authentication status:
```bash
python scripts/auth.py status
```

Logout when needed:
```bash
python scripts/auth.py logout
```

## Commands

All operations via `scripts/slides.py`. Auto-authenticates on first use if not logged in.

```bash
# Get all text content from a presentation
python scripts/slides.py get-text "1abc123xyz789"
python scripts/slides.py get-text "https://docs.google.com/presentation/d/1abc123xyz789/edit"

# Find presentations by search query
python scripts/slides.py find "quarterly report"
python scripts/slides.py find "project proposal" --limit 5

# Get presentation metadata (title, slide count, etc.)
python scripts/slides.py get-metadata "1abc123xyz789"
```

## Presentation ID Format

You can use either:
- Direct presentation ID: `1abc123xyz789`
- Full Google Slides URL: `https://docs.google.com/presentation/d/1abc123xyz789/edit`

The scripts automatically extract the ID from URLs.

## Output Format

### get-text
Returns extracted text from all slides, including:
- Presentation title
- Text from shapes/text boxes on each slide
- Table data with cell contents

### find
Returns list of matching presentations:
```json
{
  "presentations": [
    {"id": "1abc...", "name": "Q4 Report", "modifiedTime": "2024-01-15T..."}
  ],
  "nextPageToken": "..."
}
```

### get-metadata
Returns presentation details:
```json
{
  "presentationId": "1abc...",
  "title": "My Presentation",
  "slideCount": 15,
  "pageSize": {"width": {...}, "height": {...}},
  "hasMasters": true,
  "hasLayouts": true
}
```

## Token Management

Tokens stored securely using the system keyring:
- **macOS**: Keychain
- **Windows**: Windows Credential Locker
- **Linux**: Secret Service API (GNOME Keyring, KDE Wallet, etc.)

Service name: `google-slides-skill-oauth`

Automatically refreshes expired tokens using Google's cloud function.

---
name: outlook
description: Enables Claude to read, compose, and manage emails in Microsoft Outlook via Playwright MCP
category: microsoft
---

# Microsoft Outlook Skill

## Overview
Claude can manage your Microsoft Outlook email to read messages, compose and send emails, organize folders, manage calendar integration, and handle tasks. Works with both Outlook.com and Microsoft 365 accounts.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/outlook/install.sh | bash
```

Or manually:
```bash
cp -r skills/outlook ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set MICROSOFT_EMAIL "your-email@outlook.com"
```

## Privacy & Authentication

**Your credentials, your choice.** Canifi LifeOS respects your privacy.

### Option 1: Manual Browser Login (Recommended)
If you prefer not to share credentials with Claude Code:
1. Complete the [Browser Automation Setup](/setup/automation) using CDP mode
2. Login to the service manually in the Playwright-controlled Chrome window
3. Claude will use your authenticated session without ever seeing your password

### Option 2: Environment Variables
If you're comfortable sharing credentials, you can store them locally:
```bash
canifi-env set SERVICE_EMAIL "your-email"
canifi-env set SERVICE_PASSWORD "your-password"
```

**Note**: Credentials stored in canifi-env are only accessible locally on your machine and are never transmitted.

## Capabilities
- Read and summarize emails
- Compose and send new emails
- Reply to and forward emails
- Search emails by sender, subject, or content
- Organize with folders and categories
- Manage focused inbox
- Schedule emails for later sending
- Set email flags and reminders
- Access shared mailboxes
- Manage email rules
- Archive and delete emails
- View and manage calendar from email

## Usage Examples

### Example 1: Check Inbox
```
User: "Check my Outlook inbox"
Claude: Navigates to Outlook, reads inbox.
        Reports: "You have 8 unread emails:
        1. From IT Support - 'System Update' (1 hour ago)
        2. From Manager - 'Weekly Report' (2 hours ago)..."
```

### Example 2: Send Email
```
User: "Send an email to the team about tomorrow's meeting"
Claude: Composes email with subject "Tomorrow's Meeting",
        adds relevant details, sends. Confirms: "Email sent to team"
```

### Example 3: Search Emails
```
User: "Find all emails from HR about benefits"
Claude: Searches "from:HR benefits", returns results.
        Reports: "Found 5 emails about benefits from HR..."
```

### Example 4: Organize Inbox
```
User: "Move all newsletters to the Archives folder"
Claude: Identifies newsletter emails, moves to Archives.
        Confirms: "Moved 23 newsletters to Archives"
```

## Authentication Flow
1. Claude navigates to outlook.live.com or outlook.office.com via Playwright MCP
2. Enters MICROSOFT_EMAIL from canifi-env
3. Handles password entry if not already authenticated
4. Handles 2FA if prompted (notifies user via iMessage)
5. Maintains session for subsequent operations

## Selectors Reference
```javascript
// New message button
'[aria-label="New mail"]'

// Mail list
'[role="listbox"]'

// Email item
'[role="option"]'

// To field
'[aria-label="To"]'

// Subject field
'[aria-label="Add a subject"]'

// Message body
'[aria-label="Message body"]'

// Send button
'[aria-label="Send"]'

// Search box
'[aria-label="Search"]'

// Folder pane
'[aria-label="Folder pane"]'

// Categories
'[aria-label="Categorize"]'

// Flag
'[aria-label="Flag this message"]'
```

## Error Handling
- **Login Failed**: Retry 3 times, notify user via iMessage
- **Session Expired**: Re-authenticate automatically
- **Email Not Found**: Search with variations, ask for clarification
- **Send Failed**: Save as draft, retry, notify user
- **Folder Not Found**: List available folders, create if needed
- **Rate Limited**: Wait and retry with backoff

## Self-Improvement Instructions
When you learn a better way to accomplish a task with Outlook:
1. Document the improvement in your response
2. Suggest updating this skill file with the new approach
3. Include specific navigation patterns that work better
4. Note differences between Outlook.com and Office 365

## Notes
- Outlook web interface differs between consumer and business
- Focused Inbox separates important emails automatically
- Calendar and tasks accessible from mail view
- Rules can automate email organization
- Shared mailboxes require explicit access
- Email scheduling available for future sending
- Undo send available for brief period after sending
- Dark mode available in settings

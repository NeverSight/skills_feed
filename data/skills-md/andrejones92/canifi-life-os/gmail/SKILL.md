---
name: gmail
description: Enables Claude to read, compose, search, and manage emails in Gmail via Playwright MCP
---

# Gmail Skill

## Overview
Claude can fully interact with Gmail to manage your email communications. This includes reading emails, composing and sending messages, searching through mail, managing labels, archiving, and organizing your inbox.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/gmail/install.sh | bash
```

Or manually:
```bash
cp -r skills/gmail ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set GOOGLE_EMAIL "your-email@gmail.com"
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
- Read and summarize unread emails
- Compose and send new emails with attachments
- Reply to and forward emails
- Search emails by sender, subject, date, or content
- Apply, create, and manage labels
- Archive, delete, and move emails
- Mark emails as read/unread or starred
- Manage spam and trash
- Create and manage email filters
- Schedule emails to send later
- Access and manage drafts

## Usage Examples

### Example 1: Check Unread Emails
```
User: "Check my unread emails"
Claude: Navigates to Gmail, reads inbox, and provides summary:
        "You have 5 unread emails:
        1. From John Smith - 'Project Update' (2 hours ago)
        2. From Amazon - 'Your order has shipped' (3 hours ago)
        ..."
```

### Example 2: Send an Email
```
User: "Send an email to bob@example.com about the meeting tomorrow at 3pm"
Claude: Composes email with subject "Meeting Tomorrow" and body about
        the 3pm meeting, then sends it. Confirms: "Email sent to bob@example.com"
```

### Example 3: Search and Summarize
```
User: "Find all emails from my boss this week and summarize them"
Claude: Uses Gmail search with "from:boss@company.com after:2024/01/01",
        reads each email, provides consolidated summary of key points.
```

### Example 4: Organize Inbox
```
User: "Archive all promotional emails older than 30 days"
Claude: Searches for "category:promotions older_than:30d", selects all,
        archives them. Reports: "Archived 47 promotional emails"
```

## Authentication Flow
1. Claude navigates to mail.google.com via Playwright MCP
2. Enters GOOGLE_EMAIL from canifi-env
3. Handles password entry if not already authenticated
4. Handles 2FA if prompted (notifies user via iMessage to approve)
5. Maintains session cookies for subsequent requests

## Selectors Reference
```javascript
// Compose button
'div[gh="cm"]' or '[aria-label="Compose"]'

// Email list items
'tr.zA' // Each email row in inbox

// Email subject in list
'.bog span'

// Email sender
'.yW span[email]'

// Search box
'input[aria-label="Search mail"]'

// Send button in compose
'div[aria-label="Send"]'

// To field in compose
'input[aria-label="To recipients"]'

// Subject field
'input[name="subjectbox"]'

// Body field
'div[aria-label="Message Body"]'
```

## Error Handling
- **Login Failed**: Retry 3 times with 5-second delays, then notify user via iMessage
- **Session Expired**: Re-authenticate automatically using stored credentials
- **Rate Limited**: Wait 60 seconds and retry with exponential backoff
- **2FA Required**: Send iMessage: "Gmail requires 2FA approval. Please check your authenticator."
- **Compose Failed**: Save draft and notify user of the issue
- **Search No Results**: Confirm search terms with user, suggest alternatives

## Self-Improvement Instructions
When you learn a better way to accomplish a task with Gmail:
1. Document the improvement in your response
2. Suggest updating this skill file with the new approach
3. Include specific selectors or workflows that worked better
4. Note any Gmail UI changes that require selector updates

## Notes
- Gmail's UI can change; selectors may need periodic updates
- Large attachments (>25MB) require Google Drive integration
- Confidential mode emails have limited functionality
- Some actions may trigger Google security alerts; reassure user this is normal
- For bulk operations, process in batches of 50 to avoid timeouts

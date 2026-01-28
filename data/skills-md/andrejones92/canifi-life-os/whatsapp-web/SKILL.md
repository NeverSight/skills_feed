---
name: whatsapp-web
description: Enables Claude to send messages, manage groups, and handle WhatsApp communications through the web interface
version: 1.0.0
author: Canifi
category: communication
---

# WhatsApp Web Skill

## Overview
Automates WhatsApp Web interactions including messaging, group management, status updates, and media sharing through browser automation with QR code authentication.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/whatsapp-web/install.sh | bash
```

Or manually:
```bash
cp -r skills/whatsapp-web ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set WHATSAPP_LINKED "true"
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
- Send and receive text messages
- Share images, videos, and documents
- Create and manage groups
- Update and view status/stories
- Search messages and contacts
- Star and archive chats
- Manage group settings and admins
- Handle broadcast lists

## Usage Examples

### Example 1: Send a Message
```
User: "Send a WhatsApp message to Sarah asking about dinner plans"
Claude: I'll send that message on WhatsApp.
- Navigate to web.whatsapp.com
- Search for Sarah in contacts
- Open chat and compose message
- Send: "Hey Sarah, what are the dinner plans for tonight?"
- Confirm message delivered (double checkmarks)
```

### Example 2: Create a Group
```
User: "Create a WhatsApp group called 'Weekend Trip' with John, Mike, and Lisa"
Claude: I'll create that group.
- Click New Group
- Add John, Mike, and Lisa
- Set group name "Weekend Trip"
- Add group icon if available
- Confirm group created
```

### Example 3: Share a File
```
User: "Send the project proposal PDF to the Work group on WhatsApp"
Claude: I'll share that document.
- Open Work group chat
- Click attach file
- Select and upload proposal PDF
- Add caption if needed
- Send file to group
```

### Example 4: Check Unread Messages
```
User: "Check my unread WhatsApp messages and summarize them"
Claude: I'll check your unread messages.
- Identify chats with unread indicators
- Open each unread chat
- Read and collect new messages
- Present summary of conversations
```

## Authentication Flow
1. Navigate to web.whatsapp.com via Playwright MCP
2. If QR code shown, notify user via iMessage to scan with phone
3. Wait for phone authentication (timeout: 60 seconds)
4. Verify chat list loads successfully
5. Maintain session via local storage
6. Re-authenticate if session expires

## Error Handling
- **QR Code Timeout**: iMessage reminder to scan QR code
- **Session Expired**: Notify user to re-link device
- **Phone Disconnected**: Alert user that phone must be online
- **Rate Limited**: Wait and implement backoff
- **Contact Not Found**: Search by phone number or name variations
- **Group Limit Reached**: Notify user of WhatsApp limits (1024 members)
- **Media Failed**: Check file size and format, retry upload
- **Connection Lost**: Wait for reconnection, notify if persistent

## Self-Improvement Instructions
When encountering new WhatsApp features:
1. Document new UI elements and chat patterns
2. Add support for new message types (polls, etc.)
3. Log successful group management patterns
4. Update for new WhatsApp Web features

## Notes
- WhatsApp Web requires phone to be connected to internet
- End-to-end encryption maintained through web interface
- Status/stories expire after 24 hours
- Broadcast lists have recipient limits
- Some features require WhatsApp Business
- Voice and video calls not supported via web automation
- Multi-device beta allows operation without phone online

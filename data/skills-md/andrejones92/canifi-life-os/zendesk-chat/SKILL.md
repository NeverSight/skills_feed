---
name: zendesk-chat
description: Enables Claude to manage Zendesk Chat conversations, support tickets, and customer service operations
version: 1.0.0
author: Canifi
category: communication
---

# Zendesk Chat Skill

## Overview
Automates Zendesk Chat (formerly Zopim) operations including live chat management, visitor engagement, chat routing, and integration with Zendesk Support through browser automation.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/zendesk-chat/install.sh | bash
```

Or manually:
```bash
cp -r skills/zendesk-chat ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set ZENDESK_EMAIL "your-email@example.com"
canifi-env set ZENDESK_PASSWORD "your-password"
canifi-env set ZENDESK_SUBDOMAIN "your-subdomain"
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
- Handle live chat conversations
- Manage chat routing and departments
- Access visitor information and history
- Use shortcuts and macros
- Create support tickets from chats
- Monitor chat analytics
- Set agent availability
- Trigger proactive chats

## Usage Examples

### Example 1: Handle Live Chat
```
User: "Respond to the waiting chat about account access"
Claude: I'll handle that chat.
- Navigate to Zendesk Chat dashboard
- Accept waiting chat
- Review visitor information
- Compose helpful response
- Send message and continue assisting
```

### Example 2: Create Ticket from Chat
```
User: "Convert this chat to a support ticket"
Claude: I'll create the ticket.
- Open current chat conversation
- Click create ticket option
- Transfer chat details to ticket
- Set ticket priority and type
- Confirm ticket created with link
```

### Example 3: Use Chat Shortcut
```
User: "Send the greeting shortcut to the new visitor"
Claude: I'll use that shortcut.
- Open chat with new visitor
- Type shortcut command
- Select greeting message
- Send to visitor
- Confirm delivered
```

### Example 4: Check Chat Statistics
```
User: "Show me today's chat performance"
Claude: I'll pull those statistics.
- Navigate to Analytics section
- Select today's date range
- Gather chat volume data
- Calculate response metrics
- Present performance summary
```

## Authentication Flow
1. Navigate to subdomain.zendesk.com via Playwright MCP
2. Enter email and password from canifi-env
3. Navigate to Chat section
4. Handle 2FA if enabled (notify user via iMessage)
5. Verify chat dashboard access
6. Maintain session cookies

## Error Handling
- **Login Failed**: Verify subdomain and credentials
- **Session Expired**: Re-authenticate automatically
- **2FA Required**: iMessage for verification code
- **Chat Limit Reached**: Cannot accept more chats
- **Visitor Disconnected**: Chat ended by visitor
- **Department Not Found**: List available departments
- **Permission Denied**: Check agent permissions
- **Rate Limited**: Implement queue for responses

## Self-Improvement Instructions
When encountering new Zendesk Chat features:
1. Document new UI elements
2. Add support for new chat features
3. Log successful response patterns
4. Update for integration changes

## Notes
- Zendesk Chat integrates with Zendesk Support
- Chat triggers require admin configuration
- Departments affect routing rules
- Analytics depend on chat history
- Proactive chat requires visitor tracking
- Some features require Enterprise plan
- Mobile SDK chats appear differently

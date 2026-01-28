---
name: tawk-to
description: Enables Claude to manage Tawk.to live chat conversations and visitor engagement
version: 1.0.0
author: Canifi
category: communication
---

# Tawk.to Skill

## Overview
Automates Tawk.to live chat operations including conversation handling, visitor monitoring, canned responses, and team management through browser automation.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/tawk-to/install.sh | bash
```

Or manually:
```bash
cp -r skills/tawk-to ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set TAWKTO_EMAIL "your-email@example.com"
canifi-env set TAWKTO_PASSWORD "your-password"
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
- Monitor real-time visitors
- Use canned shortcuts
- Transfer chats between agents
- Access visitor history
- Manage chat tags
- Create ticketed chats
- Configure triggers

## Usage Examples

### Example 1: Handle Incoming Chat
```
User: "Accept and respond to the waiting chat"
Claude: I'll handle that chat.
- Navigate to Tawk.to dashboard
- Accept incoming chat
- Review visitor information
- Send greeting message
- Continue conversation
```

### Example 2: Use Canned Shortcut
```
User: "Send the shipping FAQ shortcut"
Claude: I'll use that shortcut.
- Open current chat
- Type shortcut command
- Select shipping FAQ
- Send to visitor
- Confirm delivered
```

### Example 3: Transfer Chat
```
User: "Transfer this chat to the technical support agent"
Claude: I'll transfer the chat.
- Open current conversation
- Click transfer option
- Select technical support agent
- Add transfer note
- Confirm transfer
```

### Example 4: Monitor Visitors
```
User: "Show me current website visitors"
Claude: I'll show the visitor list.
- Navigate to Monitoring section
- View active visitors
- Display page they're viewing
- Show visitor location and device
- Highlight returning visitors
```

## Authentication Flow
1. Navigate to dashboard.tawk.to via Playwright MCP
2. Enter email and password from canifi-env
3. Handle 2FA if enabled (notify user via iMessage)
4. Select property if multiple
5. Set agent status to online
6. Maintain session cookies

## Error Handling
- **Login Failed**: Verify credentials, retry
- **Session Expired**: Re-authenticate automatically
- **2FA Required**: iMessage for verification code
- **Property Not Found**: List available properties
- **Agent Offline**: Cannot transfer to offline agents
- **Visitor Left**: Chat ended by visitor
- **Rate Limited**: Implement message queue
- **Connection Lost**: Reconnect automatically

## Self-Improvement Instructions
When encountering new Tawk.to features:
1. Document new dashboard UI elements
2. Add support for new chat features
3. Log successful response patterns
4. Update for new integration features

## Notes
- Tawk.to is free with optional add-ons
- Multiple properties can be managed
- Video and voice chat available on plans
- Ticketing creates follow-up system
- Triggers are automated messages
- Mobile app for agent responses
- Knowledge base add-on available

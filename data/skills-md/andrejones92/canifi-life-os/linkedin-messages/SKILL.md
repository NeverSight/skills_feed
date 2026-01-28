---
name: linkedin-messages
description: Enables Claude to send LinkedIn messages, manage InMail, and handle professional networking communications
version: 1.0.0
author: Canifi
category: communication
---

# LinkedIn Messages Skill

## Overview
Automates LinkedIn messaging including direct messages, InMail, group conversations, and connection requests with personalized notes through browser automation.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/linkedin-messages/install.sh | bash
```

Or manually:
```bash
cp -r skills/linkedin-messages ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set LINKEDIN_EMAIL "your-email@example.com"
canifi-env set LINKEDIN_PASSWORD "your-password"
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
- Send direct messages to connections
- Compose and send InMail (Premium)
- Respond to message requests
- Create group conversations
- Send connection requests with notes
- Search message history
- Manage message requests
- Schedule message follow-ups

## Usage Examples

### Example 1: Send a Connection Message
```
User: "Message John Smith on LinkedIn about the job opportunity"
Claude: I'll send that LinkedIn message.
- Navigate to linkedin.com/messaging
- Search for John Smith in connections
- Open conversation
- Compose professional message about opportunity
- Send message
- Confirm delivery
```

### Example 2: Send Connection Request with Note
```
User: "Connect with Sarah Chen from Google with a personalized note"
Claude: I'll send that connection request.
- Search for Sarah Chen at Google
- Find correct profile
- Click Connect
- Add personalized note
- Send request
- Confirm request sent
```

### Example 3: Respond to Message Requests
```
User: "Check and respond to my LinkedIn message requests"
Claude: I'll review your message requests.
- Navigate to message requests folder
- Review pending messages
- Present summary of requests
- Respond to appropriate messages
- Accept or decline as instructed
```

### Example 4: Send InMail
```
User: "Send an InMail to the CEO of TechCorp about a partnership"
Claude: I'll compose and send that InMail.
- Search for TechCorp CEO profile
- Click Message (InMail)
- Compose professional partnership inquiry
- Send InMail
- Confirm delivery and credit usage
```

## Authentication Flow
1. Navigate to linkedin.com/login via Playwright MCP
2. Enter credentials from canifi-env
3. Handle verification code if sent (check email/phone)
4. Complete CAPTCHA if presented (notify user)
5. Handle 2FA if enabled
6. Verify messaging access
7. Maintain session cookies

## Error Handling
- **Login Failed**: Clear cookies, try again with fresh context
- **Session Expired**: Re-authenticate with stored credentials
- **CAPTCHA Required**: Notify user to complete manually
- **2FA Required**: iMessage for verification code
- **InMail Limit**: Notify user of monthly credit usage
- **Connection Limit**: Notify of weekly connection limits
- **Message Failed**: Check if user accepts messages
- **Profile Not Found**: Search with alternative terms

## Self-Improvement Instructions
When encountering new LinkedIn features:
1. Document new messaging UI elements
2. Add support for new message types
3. Log successful InMail patterns
4. Update for new connection features

## Notes
- InMail requires LinkedIn Premium subscription
- Connection requests limited to ~100/week
- Some users restrict messages to connections only
- Sales Navigator has different messaging features
- Message character limits apply
- Avoid spam-like behavior to prevent restrictions
- LinkedIn may show warnings for rapid actions

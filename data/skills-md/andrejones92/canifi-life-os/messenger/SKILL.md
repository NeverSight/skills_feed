---
name: messenger
description: Enables Claude to send messages, manage conversations, and handle Facebook Messenger communications
version: 1.0.0
author: Canifi
category: communication
---

# Facebook Messenger Skill

## Overview
Automates Facebook Messenger interactions including messaging, group chats, reactions, and media sharing through the web interface at messenger.com.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/messenger/install.sh | bash
```

Or manually:
```bash
cp -r skills/messenger ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set FACEBOOK_EMAIL "your-email@example.com"
canifi-env set FACEBOOK_PASSWORD "your-password"
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
- Send and receive messages
- Create and manage group chats
- Share photos, videos, and files
- React to messages with emojis
- Search conversations and contacts
- Manage message requests
- Handle video and voice calls (initiate only)
- Create polls and events in chats

## Usage Examples

### Example 1: Send a Message
```
User: "Message Lisa on Messenger asking if she's free this weekend"
Claude: I'll send that message on Messenger.
- Navigate to messenger.com
- Search for Lisa in contacts
- Open conversation
- Send: "Hey Lisa, are you free this weekend?"
- Confirm message sent
```

### Example 2: Create a Group Chat
```
User: "Create a Messenger group with Tom, Amy, and Jake for the party planning"
Claude: I'll create that group chat.
- Click new message
- Add Tom, Amy, and Jake
- Name group "Party Planning"
- Send initial message
- Confirm group created
```

### Example 3: React to Messages
```
User: "React with a heart to the last message from Mom"
Claude: I'll add that reaction.
- Open conversation with Mom
- Find most recent message
- Add heart reaction
- Confirm reaction added
```

### Example 4: Search Conversations
```
User: "Find messages about the concert tickets in Messenger"
Claude: I'll search your conversations.
- Open Messenger search
- Search "concert tickets"
- Collect matching messages
- Present results with context
```

## Authentication Flow
1. Navigate to messenger.com via Playwright MCP
2. Enter Facebook credentials from canifi-env
3. Handle 2FA if enabled (notify user via iMessage)
4. Approve device if prompted
5. Verify chat list loads
6. Maintain session cookies

## Error Handling
- **Login Failed**: Clear cookies, retry with fresh session
- **Session Expired**: Re-authenticate automatically
- **2FA Required**: iMessage notification for code
- **Account Locked**: Notify user to verify identity
- **Contact Not Found**: Search by name variations
- **Message Failed**: Retry sending, check connection
- **Rate Limited**: Wait before retrying operations
- **Device Approval**: Notify user to check email/phone

## Self-Improvement Instructions
When encountering new Messenger features:
1. Document new UI elements and patterns
2. Add support for new message types
3. Log successful group management operations
4. Update for new reactions and features

## Notes
- Messenger shares login with Facebook
- Some features require Facebook app approval
- Message requests from non-friends go to separate folder
- End-to-end encryption available for secret conversations
- Video/audio calls cannot be fully automated
- Business accounts have different features
- Messenger Rooms have separate functionality

---
name: telegram-web
description: Enables Claude to send messages, manage chats, and handle Telegram communications through the web interface
version: 1.0.0
author: Canifi
category: communication
---

# Telegram Web Skill

## Overview
Automates Telegram Web interactions including messaging, group management, channel operations, and file sharing through browser automation.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/telegram-web/install.sh | bash
```

Or manually:
```bash
cp -r skills/telegram-web ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set TELEGRAM_PHONE "+1234567890"
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
- Create and manage groups
- Administer channels and broadcasts
- Share files, photos, and media
- Search messages and contacts
- Manage notification settings
- Handle stickers and GIFs
- Create and manage bots (via BotFather)

## Usage Examples

### Example 1: Send a Message
```
User: "Send a Telegram message to Mom saying I'll be home for dinner"
Claude: I'll send that message on Telegram.
- Navigate to web.telegram.org
- Search for Mom in contacts
- Open chat and type message
- Send: "I'll be home for dinner"
- Confirm message delivered
```

### Example 2: Create a Group
```
User: "Create a Telegram group called 'Project Team' with Alex and Sarah"
Claude: I'll create that group.
- Navigate to Telegram Web
- Click New Group
- Add Alex and Sarah
- Name group "Project Team"
- Confirm group created
```

### Example 3: Post to Channel
```
User: "Post an update to my Telegram channel about the new feature"
Claude: I'll post that update.
- Navigate to channel admin view
- Compose update message
- Add any relevant media
- Publish to channel
- Confirm post live
```

### Example 4: Search Messages
```
User: "Find all messages with flight confirmation in Telegram"
Claude: I'll search your Telegram messages.
- Open global search
- Search "flight confirmation"
- Collect matching messages
- Present results with chat context
```

## Authentication Flow
1. Navigate to web.telegram.org via Playwright MCP
2. Enter phone number from canifi-env
3. Wait for SMS/Telegram code (notify user via iMessage)
4. Enter verification code when provided
5. Handle 2FA password if enabled
6. Verify access to chats
7. Maintain session via local storage

## Error Handling
- **Login Failed**: Request new verification code, retry 3x
- **Session Expired**: Re-authenticate with phone number
- **Rate Limited**: Wait 30-60 seconds before retry
- **Code Expired**: Request new verification code
- **2FA Required**: iMessage for password input
- **Contact Not Found**: Search by name variations and phone number
- **Group Limit Reached**: Notify user of Telegram limits
- **File Too Large**: Notify user of size restrictions

## Self-Improvement Instructions
When encountering new Telegram features:
1. Document new UI patterns and selectors
2. Add support for new message types
3. Log successful channel management patterns
4. Update capabilities for new features

## Notes
- Telegram Web requires phone verification each session
- Some features only available in Telegram Desktop
- File size limits apply (2GB for premium, 4GB for non-premium)
- Secret chats not available on web version
- Session may be terminated by mobile app logout
- Channels have different admin roles and permissions

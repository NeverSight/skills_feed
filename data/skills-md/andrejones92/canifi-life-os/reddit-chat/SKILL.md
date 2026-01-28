---
name: reddit-chat
description: Enables Claude to send Reddit direct messages and manage chat conversations
version: 1.0.0
author: Canifi
category: communication
---

# Reddit Chat Skill

## Overview
Automates Reddit chat and messaging operations including direct messages, group chats, and subreddit chat rooms through browser automation.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/reddit-chat/install.sh | bash
```

Or manually:
```bash
cp -r skills/reddit-chat ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set REDDIT_USERNAME "your-username"
canifi-env set REDDIT_PASSWORD "your-password"
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
- Send direct messages to users
- Create and manage group chats
- Participate in subreddit chat rooms
- Search message history
- Share posts via chat
- Send images and GIFs
- Manage chat notifications
- Block and report users

## Usage Examples

### Example 1: Send a DM
```
User: "Message u/helpful_redditor thanking them for their advice"
Claude: I'll send that message.
- Navigate to reddit.com/chat
- Search for u/helpful_redditor
- Start or open conversation
- Send thank you message
- Confirm delivery
```

### Example 2: Create Group Chat
```
User: "Create a Reddit group chat with the mod team"
Claude: I'll create that group chat.
- Open chat interface
- Click create group
- Add moderator usernames
- Name the group
- Confirm group created
```

### Example 3: Join Subreddit Chat
```
User: "Join the r/programming chat room"
Claude: I'll join that chat room.
- Navigate to r/programming
- Find chat room link
- Join the room
- Confirm joined successfully
```

### Example 4: Share a Post via Chat
```
User: "Share that interesting post with my friend on Reddit"
Claude: I'll share the post.
- Copy post link
- Open chat with friend
- Share post via chat
- Add optional comment
- Confirm sent
```

## Authentication Flow
1. Navigate to reddit.com/login via Playwright MCP
2. Enter username and password from canifi-env
3. Handle 2FA if enabled (notify user via iMessage)
4. Verify access to chat feature
5. Maintain session cookies
6. Handle any CAPTCHA (notify user)

## Error Handling
- **Login Failed**: Retry with fresh context, verify credentials
- **Session Expired**: Re-authenticate automatically
- **2FA Required**: iMessage for verification code
- **Chat Disabled**: User may have chat disabled
- **Rate Limited**: Wait before sending more messages
- **User Not Found**: Verify username spelling (no u/ prefix)
- **Account Suspended**: Notify user of account status
- **CAPTCHA Required**: Notify user for manual completion

## Self-Improvement Instructions
When encountering new Reddit chat features:
1. Document new chat UI elements
2. Add support for new message features
3. Log successful chat patterns
4. Update for Reddit redesign changes

## Notes
- Reddit has both old and new chat systems
- Some users disable chat functionality
- Subreddit chat rooms may have rules
- Chat history is limited
- Reddit frequently updates UI
- Some features require account age/karma
- Group chats have member limits

---
name: google-chat
description: Enables Claude to send messages, manage spaces, and handle Google Chat communications
version: 1.0.0
author: Canifi
category: communication
---

# Google Chat Skill

## Overview
Automates Google Chat operations including direct messaging, space management, threaded conversations, and file sharing through browser automation.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/google-chat/install.sh | bash
```

Or manually:
```bash
cp -r skills/google-chat ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set GOOGLE_EMAIL "your-email@example.com"
canifi-env set GOOGLE_PASSWORD "your-password"
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
- Send direct messages
- Create and manage spaces
- Participate in threaded conversations
- Share files from Google Drive
- Search message history
- Manage space membership
- Use smart chips and formatting
- Handle message notifications

## Usage Examples

### Example 1: Send Direct Message
```
User: "Message Sarah on Google Chat about the project deadline"
Claude: I'll send that message.
- Navigate to chat.google.com
- Find or start conversation with Sarah
- Compose message about deadline
- Send message
- Confirm delivery
```

### Example 2: Create Space
```
User: "Create a Google Chat space for the Q1 Planning team"
Claude: I'll create that space.
- Click create space
- Name it "Q1 Planning"
- Add team members
- Configure space settings
- Confirm creation
```

### Example 3: Post in Thread
```
User: "Reply to the budget thread in the Finance space"
Claude: I'll reply to that thread.
- Navigate to Finance space
- Find budget thread
- Compose reply
- Post in thread
- Confirm posted
```

### Example 4: Share Drive File
```
User: "Share the proposal document in the Sales space"
Claude: I'll share that file.
- Open Sales space
- Click attach file
- Select from Google Drive
- Share proposal document
- Confirm shared
```

## Authentication Flow
1. Navigate to chat.google.com via Playwright MCP
2. Sign in with Google credentials from canifi-env
3. Handle 2FA if enabled (notify user via iMessage)
4. Verify chat access
5. Maintain session cookies

## Error Handling
- **Login Failed**: Retry Google sign-in flow
- **Session Expired**: Re-authenticate automatically
- **2FA Required**: iMessage for verification code
- **Space Not Found**: Search by name
- **User Not Found**: Check email address format
- **File Access Denied**: Check Drive permissions
- **Rate Limited**: Implement backoff
- **Workspace Restriction**: Notify of organization policies

## Self-Improvement Instructions
When encountering new Google Chat features:
1. Document new UI elements
2. Add support for new message types
3. Log successful space patterns
4. Update for Workspace changes

## Notes
- Part of Google Workspace suite
- Spaces replace classic Hangouts rooms
- Threaded conversations optional per space
- Drive integration for file sharing
- Smart chips for @mentions and dates
- Bots can be added to spaces
- Consumer vs Workspace versions differ

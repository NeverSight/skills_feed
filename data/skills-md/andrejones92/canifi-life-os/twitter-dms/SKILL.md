---
name: twitter-dms
description: Enables Claude to send Twitter/X direct messages and manage private conversations
version: 1.0.0
author: Canifi
category: communication
---

# Twitter/X DMs Skill

## Overview
Automates Twitter/X Direct Message operations including sending DMs, managing conversations, handling message requests, and group DM management through browser automation.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/twitter-dms/install.sh | bash
```

Or manually:
```bash
cp -r skills/twitter-dms ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set TWITTER_USERNAME "your-username"
canifi-env set TWITTER_PASSWORD "your-password"
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
- Send direct messages to followers/following
- Create and manage group DMs
- Respond to message requests
- Search DM history
- Share tweets via DM
- Send images and GIFs in DMs
- React to messages
- Manage DM settings and filters

## Usage Examples

### Example 1: Send a DM
```
User: "DM @techfriend about the conference next week"
Claude: I'll send that direct message.
- Navigate to twitter.com/messages
- Search for @techfriend
- Open or start conversation
- Send message about conference
- Confirm message delivered
```

### Example 2: Create Group DM
```
User: "Create a Twitter group DM with @alex and @jordan for the podcast"
Claude: I'll create that group conversation.
- Click compose new message
- Add @alex and @jordan
- Name group "Podcast Discussion"
- Send initial message
- Confirm group created
```

### Example 3: Check Message Requests
```
User: "Check my Twitter message requests"
Claude: I'll review your message requests.
- Navigate to message requests
- List pending message requests
- Summarize who's trying to reach you
- Await instruction to accept or decline
```

### Example 4: Share Tweet via DM
```
User: "Share that viral tweet to @bestfriend via DM"
Claude: I'll share that tweet.
- Copy tweet link
- Open DM with @bestfriend
- Paste tweet link (embeds automatically)
- Add comment if requested
- Send message
```

## Authentication Flow
1. Navigate to twitter.com/login via Playwright MCP
2. Enter username/email from canifi-env
3. Enter password
4. Handle phone/email verification if prompted
5. Complete 2FA if enabled (notify user via iMessage)
6. Verify access to messages tab
7. Maintain session cookies

## Error Handling
- **Login Failed**: Try email instead of username, retry
- **Session Expired**: Re-authenticate automatically
- **2FA Required**: iMessage for authentication code
- **Verification Required**: Notify user to check email/phone
- **DM Restricted**: User may not accept DMs from non-followers
- **Rate Limited**: Wait 15+ minutes before retry
- **User Not Found**: Verify username spelling
- **Account Locked**: Notify user to verify account

## Self-Improvement Instructions
When encountering new X/Twitter DM features:
1. Document new UI selectors
2. Add support for new message types
3. Log successful DM patterns
4. Update for API/UI changes

## Notes
- DMs only possible with users who allow them
- Some accounts restrict DMs to followers
- X Premium may have different DM limits
- Message requests go to separate folder
- Twitter frequently changes UI/branding
- Rate limits are strictly enforced
- GIF sending uses Twitter's GIF search

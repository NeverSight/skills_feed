---
name: twitch
description: Enables Claude to manage Twitch streams, clips, and community engagement
version: 1.0.0
author: Canifi
category: social
---

# Twitch Skill

## Overview
Automates Twitch operations including managing channel, moderating chat, creating clips, and engaging with the streaming community through browser automation.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/twitch/install.sh | bash
```

Or manually:
```bash
cp -r skills/twitch ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set TWITCH_USERNAME "your-username"
canifi-env set TWITCH_PASSWORD "your-password"
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
- Watch and browse streams
- Create and share clips
- Follow and subscribe to channels
- Participate in chat
- View channel analytics
- Manage channel settings
- Search streams and channels
- Access VODs and clips

## Usage Examples

### Example 1: Create a Clip
```
User: "Create a clip of this stream moment"
Claude: I'll create that clip.
- Navigate to live stream
- Click clip button
- Select clip duration
- Edit and title clip
- Publish clip
```

### Example 2: Browse Streams
```
User: "Find popular coding streams on Twitch"
Claude: I'll find coding streams.
- Navigate to browse
- Search "Software and Game Development"
- Filter by viewers
- Present top streams
```

### Example 3: Check Channel Analytics
```
User: "Show me my Twitch channel stats"
Claude: I'll pull your analytics.
- Navigate to Creator Dashboard
- Access Analytics section
- Gather viewer and follower data
- Present performance summary
```

### Example 4: Manage Channel
```
User: "Update my Twitch stream title"
Claude: I'll update that.
- Navigate to Creator Dashboard
- Access Stream Manager
- Edit stream title
- Save changes
- Confirm updated
```

## Authentication Flow
1. Navigate to twitch.tv via Playwright MCP
2. Enter username and password from canifi-env
3. Handle 2FA if enabled (notify user via iMessage)
4. Complete CAPTCHA if shown (notify user)
5. Verify dashboard access
6. Maintain session cookies

## Error Handling
- **Login Failed**: Clear cookies, verify credentials
- **Session Expired**: Re-authenticate automatically
- **2FA Required**: iMessage for verification code
- **CAPTCHA Required**: Notify user to complete
- **Stream Offline**: Cannot clip offline content
- **Rate Limited**: Wait before continuing
- **Channel Not Found**: Verify channel name
- **VOD Unavailable**: Check if archiving enabled

## Self-Improvement Instructions
When encountering new Twitch features:
1. Document new UI elements
2. Add support for new creator tools
3. Log successful patterns
4. Update for Twitch changes

## Notes
- Streaming requires separate software
- Chat moderation needs mod status
- Clips require 60 seconds of VOD
- Sub-only features require subscription
- Prime Gaming links with Amazon
- Drops for game rewards
- Predictions and polls for engagement

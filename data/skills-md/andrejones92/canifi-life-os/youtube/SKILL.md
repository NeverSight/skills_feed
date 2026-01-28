---
name: youtube
description: Enables Claude to manage YouTube subscriptions, playlists, and viewing experience through browser automation
version: 1.0.0
author: Canifi
category: video
---

# YouTube Skill

## Overview
Automates YouTube viewer operations including managing subscriptions, playlists, watch history, and engagement through the main YouTube interface.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/youtube/install.sh | bash
```

Or manually:
```bash
cp -r skills/youtube ~/.canifi/skills/
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
- Search and find videos
- Manage subscriptions
- Create and edit playlists
- Like and comment on videos
- View watch history
- Save videos to watch later
- Access subscription feed
- Manage video preferences

## Usage Examples

### Example 1: Search Videos
```
User: "Find the latest videos about machine learning"
Claude: I'll search for those videos.
- Navigate to youtube.com
- Search "machine learning"
- Filter by upload date
- Present top results with metadata
```

### Example 2: Create Playlist
```
User: "Create a playlist called 'Learning Python'"
Claude: I'll create that playlist.
- Navigate to Library
- Click Create playlist
- Name it "Learning Python"
- Set privacy to private or public
- Confirm creation
```

### Example 3: Manage Subscriptions
```
User: "Subscribe to this channel"
Claude: I'll subscribe to the channel.
- Navigate to channel page
- Click Subscribe button
- Enable notifications if requested
- Confirm subscription
```

### Example 4: Check Subscription Feed
```
User: "Show me new videos from my subscriptions"
Claude: I'll check your subscriptions.
- Navigate to Subscriptions page
- List recent uploads
- Present videos with titles and channels
- Note which are new since last check
```

## Authentication Flow
1. Navigate to youtube.com via Playwright MCP
2. Sign in with Google credentials from canifi-env
3. Handle 2FA if enabled (notify user via iMessage)
4. Verify home page access
5. Maintain session cookies

## Error Handling
- **Login Failed**: Retry Google sign-in flow
- **Session Expired**: Re-authenticate automatically
- **2FA Required**: iMessage for verification code
- **Video Unavailable**: Check region or privacy restrictions
- **Playlist Error**: Verify ownership and permissions
- **Rate Limited**: Implement backoff
- **Age Restricted**: May need verification
- **Channel Not Found**: Verify channel name

## Self-Improvement Instructions
When encountering new YouTube features:
1. Document new UI elements
2. Add support for new video types
3. Log successful playlist patterns
4. Update for YouTube changes

## Notes
- YouTube Studio is separate skill for creators
- Playlists can be public, unlisted, or private
- Subscription notifications are optional
- Premium features require subscription
- Some videos are region-locked
- Comments may be disabled on videos
- Watch history affects recommendations

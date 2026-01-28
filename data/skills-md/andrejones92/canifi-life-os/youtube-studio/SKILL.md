---
name: youtube-studio
description: Enables Claude to manage YouTube channel, upload videos, and analyze creator analytics
version: 1.0.0
author: Canifi
category: video
---

# YouTube Studio Skill

## Overview
Automates YouTube Studio creator operations including video uploads, channel management, analytics review, and content optimization through browser automation.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/youtube-studio/install.sh | bash
```

Or manually:
```bash
cp -r skills/youtube-studio ~/.canifi/skills/
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
- Upload and publish videos
- Edit video details and thumbnails
- View channel analytics
- Manage comments
- Create and schedule posts
- Access revenue reports
- Edit channel settings
- Manage playlists from creator perspective

## Usage Examples

### Example 1: Upload Video
```
User: "Upload this video to my YouTube channel"
Claude: I'll upload that video.
- Navigate to studio.youtube.com
- Click Create > Upload video
- Select and upload video file
- Add title, description, tags
- Set visibility and publish
- Confirm upload complete
```

### Example 2: Check Analytics
```
User: "Show me my YouTube channel analytics for this month"
Claude: I'll pull your analytics.
- Navigate to Analytics section
- Select this month's date range
- Gather views, watch time, subscribers
- Compile revenue if monetized
- Present performance summary
```

### Example 3: Manage Comments
```
User: "Review and reply to recent comments"
Claude: I'll manage the comments.
- Navigate to Comments section
- List recent comments
- Reply to selected comments
- Handle moderation if needed
- Confirm responses posted
```

### Example 4: Update Video Details
```
User: "Update the description on my latest video"
Claude: I'll update that video.
- Navigate to Content section
- Find latest video
- Click edit details
- Update description
- Save changes
- Confirm updated
```

## Authentication Flow
1. Navigate to studio.youtube.com via Playwright MCP
2. Sign in with Google credentials from canifi-env
3. Handle 2FA if enabled (notify user via iMessage)
4. Verify Studio dashboard access
5. Maintain session cookies

## Error Handling
- **Login Failed**: Retry Google sign-in flow
- **Session Expired**: Re-authenticate automatically
- **2FA Required**: iMessage for verification code
- **Upload Failed**: Check file format and size
- **Processing Stuck**: Wait or notify user
- **Copyright Claim**: Notify user of claim details
- **Monetization Error**: Check account status
- **Analytics Delayed**: Data may take 48+ hours

## Self-Improvement Instructions
When encountering new YouTube Studio features:
1. Document new dashboard elements
2. Add support for new creator tools
3. Log successful upload patterns
4. Update for Studio redesigns

## Notes
- YouTube Studio for channel management only
- Video processing takes time after upload
- Analytics have 24-48 hour delay
- Monetization requires Partner Program
- Copyright system is automated
- Community guidelines affect visibility
- Premiere and scheduling are separate flows

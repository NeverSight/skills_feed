---
name: snapchat
description: Enables Claude to manage Snapchat web features and Snap Map through browser automation
version: 1.0.0
author: Canifi
category: social
---

# Snapchat Skill

## Overview
Automates Snapchat web operations including accessing stories, Snap Map, and account management through the limited web interface.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/snapchat/install.sh | bash
```

Or manually:
```bash
cp -r skills/snapchat ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set SNAPCHAT_USERNAME "your-username"
canifi-env set SNAPCHAT_PASSWORD "your-password"
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
- View public stories and Discover
- Access Snap Map (web version)
- Download Memories (via data download)
- Manage account settings
- View story analytics (Spotlight)
- Access Snapchat for Web chat
- Manage connected apps
- Update profile information

## Usage Examples

### Example 1: View Stories
```
User: "Check what's on Snapchat Discover today"
Claude: I'll check Discover content.
- Navigate to snapchat.com
- Access Discover section
- Browse featured stories
- Summarize trending content
```

### Example 2: Access Snap Map
```
User: "Show me what's happening on Snap Map in New York"
Claude: I'll check the Snap Map.
- Navigate to map.snapchat.com
- Zoom to New York area
- View public snaps
- Describe current activity
```

### Example 3: Download Memories
```
User: "Help me download my Snapchat data"
Claude: I'll start the data download process.
- Navigate to accounts.snapchat.com
- Go to My Data section
- Request data download
- Notify when ready
```

### Example 4: Update Profile
```
User: "Update my Snapchat display name"
Claude: I'll update your profile.
- Navigate to account settings
- Find profile section
- Update display name
- Save changes
```

## Authentication Flow
1. Navigate to accounts.snapchat.com via Playwright MCP
2. Enter username and password from canifi-env
3. Handle 2FA verification (notify user via iMessage)
4. Complete any security checks
5. Verify account access
6. Maintain session cookies

## Error Handling
- **Login Failed**: Verify credentials, check for lockout
- **Session Expired**: Re-authenticate automatically
- **2FA Required**: iMessage for verification code
- **Feature Not Available**: Many features app-only
- **Map Location Error**: Check location permissions
- **Data Download Pending**: Wait for processing
- **Account Locked**: Notify user of status
- **Rate Limited**: Implement backoff

## Self-Improvement Instructions
When encountering new Snapchat web features:
1. Document new interface elements
2. Add support for new web features
3. Log successful patterns
4. Update for web app improvements

## Notes
- Most Snapchat features are mobile-app only
- Web chat is limited functionality
- Snap Map shows public snaps only
- Data downloads take time to process
- Spotlight analytics for creators
- Lens Studio is separate platform
- Business features in Ads Manager

---
name: streamyard
description: Stream live to multiple platforms with StreamYard - manage broadcasts, guests, and recordings
category: video
---

# StreamYard Skill

## Overview
Enables Claude to use StreamYard for live streaming management including scheduling broadcasts, managing recordings, and configuring stream destinations.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/streamyard/install.sh | bash
```

Or manually:
```bash
cp -r skills/streamyard ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set STREAMYARD_EMAIL "your-email@example.com"
canifi-env set STREAMYARD_PASSWORD "your-password"
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
- Manage broadcast schedules
- Access recorded streams
- Configure streaming destinations
- Manage guest invitations
- View broadcast history
- Download stream recordings

## Usage Examples

### Example 1: Check Scheduled Broadcasts
```
User: "What live streams do I have scheduled this week?"
Claude: I'll check your broadcast schedule.
1. Opening StreamYard via Playwright MCP
2. Navigating to broadcasts
3. Viewing scheduled streams
4. Filtering to this week
5. Summarizing upcoming broadcasts
```

### Example 2: Download Recording
```
User: "Download the recording from my last webinar"
Claude: I'll download your recording.
1. Opening past broadcasts
2. Finding the webinar recording
3. Accessing download options
4. Initiating video download
```

### Example 3: View Destinations
```
User: "Which platforms am I set up to stream to?"
Claude: I'll check your destinations.
1. Opening destination settings
2. Listing connected platforms
3. Verifying connection status
4. Summarizing streaming options
```

## Authentication Flow
1. Navigate to streamyard.com via Playwright MCP
2. Click "Log in" and enter email
3. Enter password
4. Handle Google SSO if configured
5. Complete 2FA if required (via iMessage)

## Error Handling
- **Login Failed**: Retry up to 3 times, notify via iMessage
- **Session Expired**: Re-authenticate automatically
- **Rate Limited**: Implement exponential backoff
- **2FA Required**: Send iMessage notification
- **Recording Unavailable**: Check processing status
- **Destination Error**: Verify platform connections

## Self-Improvement Instructions
When StreamYard updates:
1. Document new streaming features
2. Update destination platform options
3. Track recording capabilities
4. Log guest management improvements

## Notes
- Browser-based streaming platform
- Multistream to multiple platforms
- Guest links for remote participants
- Recording stored for limited time
- Branding customization available

---
name: bluejeans
description: Enables Claude to schedule BlueJeans meetings, manage recordings, and handle video conferencing
version: 1.0.0
author: Canifi
category: communication
---

# BlueJeans Skill

## Overview
Automates BlueJeans video conferencing operations including meeting scheduling, recording management, and collaboration features through browser automation.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/bluejeans/install.sh | bash
```

Or manually:
```bash
cp -r skills/bluejeans ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set BLUEJEANS_EMAIL "your-email@example.com"
canifi-env set BLUEJEANS_PASSWORD "your-password"
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
- Schedule and manage meetings
- Access meeting recordings
- Configure personal meeting room
- Manage meeting settings
- View meeting analytics
- Handle meeting invitations
- Control participant settings
- Create meeting templates

## Usage Examples

### Example 1: Schedule Meeting
```
User: "Schedule a BlueJeans meeting for Friday at 2pm"
Claude: I'll schedule that meeting.
- Navigate to BlueJeans portal
- Click Schedule Meeting
- Set date and time for Friday 2pm
- Configure meeting options
- Send invitations
- Confirm meeting created
```

### Example 2: Access Recording
```
User: "Download the recording from the client meeting"
Claude: I'll find that recording.
- Navigate to Recordings section
- Locate client meeting recording
- Initiate download
- Confirm download started
```

### Example 3: Update Personal Room
```
User: "Change my BlueJeans personal room settings"
Claude: I'll update those settings.
- Navigate to Personal Room settings
- Access configuration options
- Update specified settings
- Save changes
- Confirm updated
```

### Example 4: Get Meeting Link
```
User: "Get my BlueJeans meeting link to share"
Claude: I'll get your meeting link.
- Navigate to personal room
- Copy meeting URL
- Format for sharing
- Provide link with dial-in options
```

## Authentication Flow
1. Navigate to bluejeans.com via Playwright MCP
2. Enter email and password from canifi-env
3. Handle SSO if configured
4. Complete 2FA if enabled (notify user via iMessage)
5. Verify dashboard access
6. Maintain session cookies

## Error Handling
- **Login Failed**: Check SSO, retry authentication
- **Session Expired**: Re-authenticate automatically
- **2FA Required**: iMessage for verification code
- **SSO Required**: Handle enterprise SSO flow
- **Recording Not Found**: Check date range
- **Meeting Limit**: Notify of license limits
- **Permission Denied**: Check admin settings
- **Connection Error**: Retry with backoff

## Self-Improvement Instructions
When encountering new BlueJeans features:
1. Document new UI elements
2. Add support for new meeting types
3. Log successful scheduling patterns
4. Update for Verizon integrations

## Notes
- BlueJeans owned by Verizon
- Enterprise deployments use SSO
- Recordings stored in cloud
- Personal room URL is persistent
- Some features require admin access
- Primetime events have different features
- Gateway integration for legacy systems

---
name: google-meet
description: Enables Claude to create, join, and manage Google Meet video conferences via Playwright MCP
category: google
---

# Google Meet Skill

## Overview
Claude can manage Google Meet video conferences to schedule meetings, generate meeting links, join calls, and manage meeting settings. This integrates with Google Calendar for seamless scheduling.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/google-meet/install.sh | bash
```

Or manually:
```bash
cp -r skills/google-meet ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set GOOGLE_EMAIL "your-email@gmail.com"
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
- Create instant meetings
- Generate meeting links for future use
- Join meetings by code or link
- Schedule meetings via Calendar integration
- Manage meeting settings and permissions
- View meeting participants
- Record meetings (if enabled)
- Enable captions and transcription
- Manage screen sharing permissions
- Create recurring meeting rooms
- Send meeting invitations
- View meeting history

## Usage Examples

### Example 1: Create Instant Meeting
```
User: "Create a Google Meet link for a quick call"
Claude: Navigates to Meet, creates new meeting.
        Returns: "Meeting created: meet.google.com/abc-defg-hij"
```

### Example 2: Schedule Meeting
```
User: "Schedule a team meeting for tomorrow at 3pm with Google Meet"
Claude: Creates Calendar event with Meet link, adds details.
        Returns: "Scheduled for tomorrow 3pm: [link]"
```

### Example 3: Get Meeting Info
```
User: "What's the Meet link for my 2pm meeting?"
Claude: Checks Calendar for 2pm meeting, extracts Meet link.
        Reports: "Your 2pm meeting link: meet.google.com/xyz-abcd-efg"
```

### Example 4: Create Named Meeting Room
```
User: "Create a meeting room called 'Weekly Standup' we can reuse"
Claude: Creates named meeting room with permanent link.
        Returns: "Created 'Weekly Standup' room: [link]"
```

## Authentication Flow
1. Claude navigates to meet.google.com via Playwright MCP
2. Authenticates with GOOGLE_EMAIL if needed
3. Handles 2FA if prompted (notifies user via iMessage)
4. Maintains session for subsequent Meet operations

## Selectors Reference
```javascript
// New meeting button
'[aria-label="New meeting"]'

// Start instant meeting
'[data-action="start-meeting"]'

// Create meeting for later
'[data-action="create-meeting-for-later"]'

// Schedule in Calendar
'[data-action="open-calendar"]'

// Meeting code input
'input[aria-label="Enter a code or link"]'

// Join button
'[aria-label="Join"]'

// Copy link button
'[aria-label="Copy meeting link"]'

// Meeting link display
'.meeting-link-text'

// End call button
'[aria-label="Leave call"]'

// Participants panel
'[aria-label="Show everyone"]'

// Screen share button
'[aria-label="Present now"]'

// Record button
'[aria-label="Activities"]'
```

## Error Handling
- **Login Failed**: Retry 3 times, notify user via iMessage
- **Session Expired**: Re-authenticate automatically
- **Meeting Creation Failed**: Retry, check account permissions
- **Join Failed**: Verify meeting code, check if meeting is active
- **Recording Failed**: Check workspace admin settings, notify user
- **Calendar Integration Failed**: Verify Calendar access, retry

## Self-Improvement Instructions
When you learn a better way to accomplish a task with Google Meet:
1. Document the improvement in your response
2. Suggest updating this skill file with the new approach
3. Include specific meeting setup configurations
4. Note any integration improvements with Calendar

## Notes
- Meeting codes are 10 characters (xxx-xxxx-xxx format)
- Recordings saved to Meet Recordings folder in Drive
- Captions available in multiple languages
- Breakout rooms available for larger meetings
- Polls and Q&A available during meetings
- Background blur and virtual backgrounds supported
- Maximum 100 participants for personal accounts
- Workspace accounts may have higher limits
- Meetings can be live streamed (Workspace only)

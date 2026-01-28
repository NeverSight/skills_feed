---
name: microsoft-teams
description: Enables Claude to send messages, manage channels, and schedule meetings in Microsoft Teams via Playwright MCP
category: microsoft
---

# Microsoft Teams Skill

## Overview
Claude can interact with Microsoft Teams to send messages, manage channels, schedule meetings, and collaborate with team members. Supports chat, channels, file sharing, and meeting management.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/microsoft-teams/install.sh | bash
```

Or manually:
```bash
cp -r skills/microsoft-teams ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set MICROSOFT_EMAIL "your-email@outlook.com"
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
- Send and read chat messages
- Post in team channels
- Create and manage channels
- Schedule and join meetings
- Share files in conversations
- Mention team members
- React to messages
- Create and manage teams
- Search messages and files
- Set status and availability
- Create meeting notes
- Manage team membership

## Usage Examples

### Example 1: Send Message
```
User: "Send a message to the Marketing channel about the campaign launch"
Claude: Opens Teams, navigates to Marketing channel, posts message.
        Confirms: "Message posted to Marketing channel"
```

### Example 2: Schedule Meeting
```
User: "Schedule a team meeting for tomorrow at 2pm"
Claude: Creates meeting invite for tomorrow 2pm,
        adds team members, sends invitation.
        Returns: "Meeting scheduled, invite sent to team"
```

### Example 3: Read Channel
```
User: "What's new in the Engineering channel?"
Claude: Opens Engineering channel, reads recent messages.
        Reports: "Recent updates:
        1. John posted about API changes
        2. Sarah shared test results..."
```

### Example 4: Direct Message
```
User: "Send Mike a message about the deadline extension"
Claude: Opens chat with Mike, sends message about deadline.
        Confirms: "Message sent to Mike"
```

## Authentication Flow
1. Claude navigates to teams.microsoft.com via Playwright MCP
2. Authenticates with MICROSOFT_EMAIL if needed
3. Handles 2FA if prompted (notifies user via iMessage)
4. Maintains session for Teams operations

## Selectors Reference
```javascript
// Teams list
'[aria-label="Teams and Channels"]'

// Channel list
'.channel-list'

// Chat list
'[aria-label="Chats"]'

// Message compose
'[aria-label="Type a new message"]'

// Send button
'[aria-label="Send"]'

// New meeting
'[aria-label="New meeting"]'

// Calendar
'[aria-label="Calendar"]'

// Search
'[aria-label="Search"]'

// New team
'[aria-label="Create a new team"]'

// Add member
'[aria-label="Add member"]'

// Files tab
'[aria-label="Files"]'
```

## Error Handling
- **Login Failed**: Retry 3 times, notify user via iMessage
- **Session Expired**: Re-authenticate automatically
- **Channel Not Found**: List available channels, ask for clarification
- **Message Send Failed**: Retry, save as draft
- **Meeting Create Failed**: Check calendar conflicts, retry
- **Team Not Accessible**: Notify user of permission issue

## Self-Improvement Instructions
When you learn a better way to accomplish a task with Teams:
1. Document the improvement in your response
2. Suggest updating this skill file with the new approach
3. Include specific navigation patterns that work better
4. Note any new features or integrations

## Notes
- Teams web app has most desktop features
- Notifications may require permissions
- File sharing integrates with OneDrive/SharePoint
- Meeting recordings saved to OneDrive or SharePoint
- @mentions notify specific users
- Status syncs with Outlook calendar
- Loop components enable collaborative content
- Keyboard shortcuts available for navigation

---
name: google-calendar
description: Enables Claude to create, manage, and organize events in Google Calendar via Playwright MCP
category: google
---

# Google Calendar Skill

## Overview
Claude can manage your Google Calendar to create events, schedule meetings, set reminders, check availability, and organize your time. This includes working with multiple calendars, sending invites, and managing recurring events.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/google-calendar/install.sh | bash
```

Or manually:
```bash
cp -r skills/google-calendar ~/.canifi/skills/
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
- Create and edit calendar events
- Schedule meetings with attendees
- Check availability and find free time slots
- Set reminders and notifications
- Create recurring events
- Manage multiple calendars
- Accept or decline meeting invitations
- View daily, weekly, or monthly schedules
- Create and manage event RSVPs
- Set event locations and video conferencing
- Add event descriptions and attachments
- Color-code events by category

## Usage Examples

### Example 1: Create Event
```
User: "Schedule a team meeting tomorrow at 2pm for 1 hour"
Claude: Creates event titled "Team Meeting" for tomorrow 2-3pm,
        adds to primary calendar. Returns: "Created: Team Meeting tomorrow 2-3pm"
```

### Example 2: Check Schedule
```
User: "What do I have scheduled this week?"
Claude: Opens week view, reads all events. Reports:
        "This week: Monday - Team standup 9am, Client call 2pm..."
```

### Example 3: Find Free Time
```
User: "When am I free for a 2-hour meeting this week?"
Claude: Analyzes week's schedule, identifies gaps of 2+ hours.
        Reports: "Available slots: Tuesday 10am-12pm, Wednesday 1-4pm..."
```

### Example 4: Create Recurring Event
```
User: "Set up a weekly 1-on-1 with Sarah every Monday at 10am"
Claude: Creates recurring event "1-on-1 with Sarah" every Monday 10am,
        adds Sarah as attendee, sends invite. Confirms: "Recurring meeting created"
```

## Authentication Flow
1. Claude navigates to calendar.google.com via Playwright MCP
2. Authenticates with GOOGLE_EMAIL if needed
3. Handles 2FA if prompted (notifies user via iMessage)
4. Maintains session for subsequent calendar operations

## Selectors Reference
```javascript
// Create button
'[aria-label="Create"]'

// Event quick add
'[aria-label="Quick add"]'

// Date navigation
'[aria-label="Go to today"]'
'[aria-label="Next"]'
'[aria-label="Previous"]'

// View switchers
'[aria-label="Day"]'
'[aria-label="Week"]'
'[aria-label="Month"]'

// Event dialog
'[data-eventid]'

// Event title input
'[aria-label="Add title"]'

// Date/time inputs
'[aria-label="Start date"]'
'[aria-label="End date"]'
'[aria-label="Start time"]'
'[aria-label="End time"]'

// Add guests
'[aria-label="Add guests"]'

// Add location
'[aria-label="Add location"]'

// Save button
'[aria-label="Save"]'

// Calendar list
'.calendar-list'
```

## Error Handling
- **Login Failed**: Retry 3 times, notify user via iMessage
- **Session Expired**: Re-authenticate automatically
- **Event Creation Failed**: Retry, check for conflicts, notify user
- **Invite Send Failed**: Retry sending, verify email addresses
- **Calendar Not Found**: List available calendars, ask user to specify
- **Time Conflict**: Warn user of overlap, ask to proceed or reschedule

## Self-Improvement Instructions
When you learn a better way to accomplish a task with Google Calendar:
1. Document the improvement in your response
2. Suggest updating this skill file with the new approach
3. Include specific navigation patterns that work better
4. Note timezone handling improvements

## Notes
- All times are interpreted in user's local timezone unless specified
- Google Meet links can be auto-added to events
- Recurring events: daily, weekly, monthly, yearly, custom
- Event reminders: email or popup, up to 4 weeks before
- Guest permissions: modify event, invite others, see guest list
- Calendar colors can be customized per calendar
- Free/busy visibility can be set per event
- Keyboard shortcut: C to create new event

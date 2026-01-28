---
name: quest-diagnostics
description: Access lab results with Quest Diagnostics - view test results, schedule appointments, and manage MyQuest portal
category: healthcare
---

# Quest Diagnostics Skill

## Overview
Enables Claude to use Quest Diagnostics for lab testing services including viewing test results, scheduling appointments, and managing MyQuest patient portal.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/quest-diagnostics/install.sh | bash
```

Or manually:
```bash
cp -r skills/quest-diagnostics ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set QUEST_EMAIL "your-email@example.com"
canifi-env set QUEST_PASSWORD "your-password"
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
- View lab test results
- Schedule appointments
- Access test history
- Find patient service centers
- View order status
- Manage MyQuest portal

## Usage Examples

### Example 1: View Results
```
User: "Check if my Quest lab results are ready"
Claude: I'll check for your results.
1. Opening Quest via Playwright MCP
2. Accessing MyQuest portal
3. Viewing results section
4. Checking for new results
5. Summarizing available data
```

### Example 2: Schedule Appointment
```
User: "When is my Quest appointment?"
Claude: I'll check your appointment.
1. Accessing appointments section
2. Viewing scheduled appointments
3. Listing appointment details
4. Providing location info
```

### Example 3: Find Location
```
User: "Find Quest Diagnostics locations nearby"
Claude: I'll find nearby locations.
1. Accessing location finder
2. Searching for patient service centers
3. Listing addresses and hours
4. Noting walk-in availability
```

## Authentication Flow
1. Navigate to questdiagnostics.com via Playwright MCP
2. Click "Sign in to MyQuest" and enter email
3. Enter password
4. Handle 2FA if required (via iMessage)
5. Maintain session for portal access

## Error Handling
- **Login Failed**: Retry up to 3 times, notify via iMessage
- **Session Expired**: Re-authenticate automatically
- **Rate Limited**: Implement exponential backoff
- **2FA Required**: Send iMessage notification
- **Results Not Ready**: Note processing time
- **Scheduling Error**: Suggest alternatives

## Self-Improvement Instructions
When Quest updates:
1. Document new portal features
2. Update result viewing options
3. Track scheduling changes
4. Log service expansions

## Notes
- MyQuest patient portal
- Walk-in and appointment options
- Home collection service
- Mobile phlebotomy
- Employer health services

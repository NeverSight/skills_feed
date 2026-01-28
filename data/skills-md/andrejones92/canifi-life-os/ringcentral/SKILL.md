---
name: ringcentral
description: Enables Claude to manage RingCentral communications including messaging, video meetings, and phone operations
version: 1.0.0
author: Canifi
category: communication
---

# RingCentral Skill

## Overview
Automates RingCentral unified communications operations including messaging, video meetings, phone features, and team collaboration through browser automation.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/ringcentral/install.sh | bash
```

Or manually:
```bash
cp -r skills/ringcentral ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set RINGCENTRAL_EMAIL "your-email@example.com"
canifi-env set RINGCENTRAL_PASSWORD "your-password"
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
- Send and manage messages
- Schedule video meetings
- Access voicemail and call logs
- Manage team messaging
- Create and join video calls
- Handle SMS/MMS messaging
- Configure phone settings
- View communication analytics

## Usage Examples

### Example 1: Send Team Message
```
User: "Message the sales team on RingCentral about the new leads"
Claude: I'll send that message.
- Navigate to RingCentral app
- Find sales team conversation
- Compose message about new leads
- Send to team
- Confirm delivery
```

### Example 2: Schedule Video Meeting
```
User: "Schedule a RingCentral video meeting for tomorrow"
Claude: I'll schedule that meeting.
- Navigate to Meetings section
- Click Schedule
- Set time for tomorrow
- Configure meeting settings
- Send invitations
```

### Example 3: Check Voicemails
```
User: "Check my RingCentral voicemails"
Claude: I'll check your voicemails.
- Navigate to Voicemail section
- List recent voicemails
- Summarize caller and message
- Present unheard messages first
```

### Example 4: Send SMS
```
User: "Send an SMS through RingCentral to confirm the appointment"
Claude: I'll send that SMS.
- Navigate to Messages/SMS section
- Enter recipient number
- Compose appointment confirmation
- Send SMS
- Confirm delivery
```

## Authentication Flow
1. Navigate to app.ringcentral.com via Playwright MCP
2. Enter email and password from canifi-env
3. Handle SSO if configured
4. Complete 2FA if enabled (notify user via iMessage)
5. Verify app access
6. Maintain session cookies

## Error Handling
- **Login Failed**: Check SSO settings, retry
- **Session Expired**: Re-authenticate automatically
- **2FA Required**: iMessage for verification code
- **SMS Failed**: Verify phone number format
- **Meeting Limit**: Notify of license limits
- **Voicemail Unavailable**: Check account setup
- **Rate Limited**: Implement backoff
- **Permission Denied**: Check user permissions

## Self-Improvement Instructions
When encountering new RingCentral features:
1. Document new app UI elements
2. Add support for new communication types
3. Log successful messaging patterns
4. Update for new unified features

## Notes
- RingCentral is unified communications platform
- Different products (MVP, Video, Phone)
- SMS requires phone number assignment
- Enterprise has additional security
- Call recording may require consent
- Integration with multiple platforms
- Admin portal separate from user app

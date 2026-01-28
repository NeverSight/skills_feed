---
name: drift
description: Enables Claude to manage Drift conversations, playbooks, and conversational marketing operations
version: 1.0.0
author: Canifi
category: communication
---

# Drift Skill

## Overview
Automates Drift conversational marketing platform operations including live conversations, meeting booking, playbook management, and lead qualification through browser automation.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/drift/install.sh | bash
```

Or manually:
```bash
cp -r skills/drift ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set DRIFT_EMAIL "your-email@example.com"
canifi-env set DRIFT_PASSWORD "your-password"
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
- Handle live conversations
- Book meetings from chat
- Manage conversation routing
- Access visitor and account data
- Use saved replies
- Create and monitor playbooks
- Qualify and route leads
- View conversation analytics

## Usage Examples

### Example 1: Handle Sales Conversation
```
User: "Take the conversation from the enterprise visitor"
Claude: I'll handle that conversation.
- Navigate to Drift inbox
- Find enterprise visitor conversation
- Review account and visitor data
- Continue qualification conversation
- Route appropriately
```

### Example 2: Book Meeting from Chat
```
User: "Schedule a demo with this prospect for next week"
Claude: I'll book that meeting.
- Open current conversation
- Access calendar booking widget
- Find next week availability
- Send meeting link to prospect
- Confirm booking when accepted
```

### Example 3: Use Playbook Response
```
User: "Send the pricing tier playbook response"
Claude: I'll use that playbook.
- Open active conversation
- Access playbook responses
- Select pricing tier content
- Send to visitor
- Continue conversation flow
```

### Example 4: Qualify Lead
```
User: "Qualify this lead and route to sales team"
Claude: I'll qualify and route.
- Review conversation context
- Check qualification criteria
- Update lead status
- Add qualification notes
- Route to sales team
- Confirm handoff
```

## Authentication Flow
1. Navigate to app.drift.com via Playwright MCP
2. Enter email and password from canifi-env
3. Handle SSO if configured
4. Complete 2FA if enabled (notify user via iMessage)
5. Verify inbox access
6. Set availability status
7. Maintain session cookies

## Error Handling
- **Login Failed**: Check SSO configuration, retry
- **Session Expired**: Re-authenticate automatically
- **2FA Required**: iMessage for verification code
- **Calendar Not Connected**: Notify user to connect calendar
- **Route Failed**: Check routing rules configuration
- **Playbook Not Found**: List available playbooks
- **Meeting Conflict**: Suggest alternative times
- **Visitor Left**: Conversation ended, send follow-up email

## Self-Improvement Instructions
When encountering new Drift features:
1. Document new conversation UI elements
2. Add support for new playbook types
3. Log successful qualification patterns
4. Update for new routing features

## Notes
- Drift focuses on revenue acceleration
- Playbooks require appropriate plan
- Meeting booking needs calendar integration
- Account-based features need CRM sync
- Bot conversations may precede human chat
- Sales Seat vs. Lite Seat permissions differ
- Prospector features require add-on

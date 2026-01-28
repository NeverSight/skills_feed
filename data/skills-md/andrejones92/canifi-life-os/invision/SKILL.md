---
name: invision
description: Prototype and collaborate with InVision - create interactive prototypes, manage design boards, and gather feedback
category: design
---

# InVision Skill

## Overview
Enables Claude to use InVision for design collaboration including viewing and managing prototypes, accessing Freehand boards, organizing design projects, and reviewing stakeholder feedback.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/invision/install.sh | bash
```

Or manually:
```bash
cp -r skills/invision ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set INVISION_EMAIL "your-email@example.com"
canifi-env set INVISION_PASSWORD "your-password"
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
- View and navigate prototypes
- Access Freehand whiteboard boards
- Manage design projects and spaces
- Review comments and feedback
- Export prototype screens
- Track project activity

## Usage Examples

### Example 1: View Prototype Feedback
```
User: "Show me all comments on the mobile app prototype"
Claude: I'll gather the prototype feedback.
1. Opening InVision via Playwright MCP
2. Navigating to the mobile app prototype
3. Collecting all screen comments
4. Organizing feedback by screen
5. Summarizing key themes
```

### Example 2: Check Project Status
```
User: "What's the latest activity on the website redesign project?"
Claude: I'll check project activity.
1. Opening the website redesign space
2. Viewing activity feed
3. Checking recent updates and comments
4. Summarizing latest changes
```

### Example 3: Export Screens
```
User: "Download all screens from the onboarding prototype"
Claude: I'll export the prototype screens.
1. Opening the onboarding prototype
2. Accessing screen list
3. Exporting all screens as images
4. Downloading to your folder
```

## Authentication Flow
1. Navigate to invisionapp.com via Playwright MCP
2. Click "Sign In" and enter email
3. Enter password
4. Handle SSO if configured
5. Complete 2FA if required (via iMessage)

## Error Handling
- **Login Failed**: Retry up to 3 times, notify via iMessage
- **Session Expired**: Re-authenticate automatically
- **Rate Limited**: Implement exponential backoff
- **2FA Required**: Send iMessage notification
- **Prototype Not Found**: Search spaces or verify link
- **Export Failed**: Retry or check permissions

## Self-Improvement Instructions
When InVision updates:
1. Document new collaboration features
2. Update Freehand board interactions
3. Track prototype viewer changes
4. Log export and sharing updates

## Notes
- InVision is transitioning to Freehand focus
- Some legacy features being deprecated
- Studio files require desktop app
- Prototype hotspots define interactions
- Comments support @mentions

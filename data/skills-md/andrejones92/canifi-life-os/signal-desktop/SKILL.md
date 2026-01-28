---
name: signal-desktop
description: Enables Claude to send encrypted messages and manage Signal communications through the desktop application
version: 1.0.0
author: Canifi
category: communication
---

# Signal Desktop Skill

## Overview
Automates Signal Desktop interactions for secure messaging, group management, and private communications while maintaining end-to-end encryption through desktop app automation.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/signal-desktop/install.sh | bash
```

Or manually:
```bash
cp -r skills/signal-desktop ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set SIGNAL_LINKED "true"
canifi-env set SIGNAL_APP_PATH "/Applications/Signal.app"
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
- Send and receive encrypted messages
- Create and manage groups
- Share encrypted media files
- Search message history
- Manage disappearing messages
- Handle note to self
- Manage blocked contacts
- Configure privacy settings

## Usage Examples

### Example 1: Send an Encrypted Message
```
User: "Send a Signal message to James about the confidential project"
Claude: I'll send that secure message via Signal.
- Launch Signal Desktop application
- Search for James in contacts
- Open conversation
- Type and send message
- Confirm delivery (checkmarks)
```

### Example 2: Create a Secure Group
```
User: "Create a Signal group called 'Secure Team' with Ana and Carlos"
Claude: I'll create that encrypted group.
- Open Signal Desktop
- Start new group
- Add Ana and Carlos
- Name group "Secure Team"
- Confirm group created with encryption
```

### Example 3: Enable Disappearing Messages
```
User: "Set disappearing messages to 1 week for my chat with Alex"
Claude: I'll configure disappearing messages.
- Open chat with Alex
- Access conversation settings
- Enable disappearing messages
- Set timer to 1 week
- Confirm setting applied
```

### Example 4: Search Secure Messages
```
User: "Find all Signal messages mentioning 'contract'"
Claude: I'll search your Signal messages.
- Open Signal search
- Search for "contract"
- Collect matching messages
- Present results with context (maintaining privacy)
```

## Authentication Flow
1. Launch Signal Desktop via system command
2. If not linked, show QR code for phone scanning
3. Notify user via iMessage to scan QR with Signal mobile
4. Wait for device linking confirmation
5. Verify contact list access
6. Maintain linked status for future sessions

## Error Handling
- **App Not Found**: Verify Signal Desktop installation path
- **Not Linked**: Prompt user to link via QR code scanning
- **Session Expired**: Re-link device through phone app
- **Contact Not Found**: Search by phone number format variations
- **Group Creation Failed**: Check contact permissions
- **Media Failed**: Verify file format and size limits
- **Connection Lost**: Wait for Signal servers reconnection
- **Rate Limited**: Implement backoff for message sending

## Self-Improvement Instructions
When encountering new Signal features:
1. Document desktop app UI changes
2. Add support for new message features
3. Log group management patterns
4. Update for new privacy features

## Notes
- Signal Desktop requires linking to mobile app
- All messages remain end-to-end encrypted
- Desktop app must remain open for real-time messaging
- Some features require both parties to update
- Group video calls not automatable
- Safety numbers should be verified manually
- Registration lock may require PIN

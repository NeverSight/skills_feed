---
name: krisp
description: AI-powered noise cancellation and meeting assistant.
category: productivity
---
# Krisp Skill

AI-powered noise cancellation and meeting assistant.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/krisp/install.sh | bash
```

Or manually:
```bash
cp -r skills/krisp ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set KRISP_EMAIL "your_email"
canifi-env set KRISP_PASSWORD "your_password"
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

1. **Noise Cancel**: Remove background noise
2. **Voice Cancel**: Mute other voices
3. **Meeting Notes**: AI transcription
4. **Talk Time**: Speaking analytics
5. **Recording**: Capture audio

## Usage Examples

### Enable Noise Cancel
```
User: "Turn on Krisp noise cancellation"
Assistant: Activates noise removal
```

### View Stats
```
User: "How much did I talk in meetings today?"
Assistant: Returns talk time stats
```

### Get Transcript
```
User: "Transcribe my last call"
Assistant: Returns meeting transcript
```

### Record Meeting
```
User: "Start recording this call"
Assistant: Begins recording
```

## Authentication Flow

1. Account-based authentication
2. No official API
3. Desktop app required
4. Browser automation for web

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Login Failed | Invalid credentials | Check account |
| Audio Error | Device issue | Check settings |
| Processing Error | CPU load | Close apps |
| Limit Reached | Minutes exceeded | Upgrade |

## Notes

- Real-time noise cancellation
- Works with any app
- Meeting analytics
- AI notes (beta)
- Desktop required
- Free tier available

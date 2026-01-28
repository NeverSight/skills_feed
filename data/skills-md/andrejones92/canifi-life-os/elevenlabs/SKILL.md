---
name: elevenlabs
description: Generate realistic AI voices with ElevenLabs - create speech, clone voices, and manage audio projects
category: ai
---

# ElevenLabs Skill

## Overview
Enables Claude to use ElevenLabs for AI voice generation including text-to-speech, voice cloning management, and audio project creation.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/elevenlabs/install.sh | bash
```

Or manually:
```bash
cp -r skills/elevenlabs ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set ELEVENLABS_EMAIL "your-email@example.com"
canifi-env set ELEVENLABS_PASSWORD "your-password"
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
- Generate speech from text
- Manage voice library
- Access voice cloning projects
- Download audio files
- View usage and credits
- Configure voice settings

## Usage Examples

### Example 1: Generate Speech
```
User: "Generate audio narration for my script"
Claude: I'll create the narration.
1. Opening ElevenLabs via Playwright MCP
2. Accessing speech synthesis
3. Pasting your script text
4. Selecting voice and settings
5. Generating and downloading audio
```

### Example 2: View Voice Library
```
User: "Show me my available voices"
Claude: I'll list your voices.
1. Opening voice library
2. Listing default voices
3. Showing custom/cloned voices
4. Displaying voice characteristics
```

### Example 3: Check Usage
```
User: "How many characters do I have left this month?"
Claude: I'll check your usage.
1. Accessing account settings
2. Viewing usage statistics
3. Reporting remaining characters
4. Showing plan limits
```

## Authentication Flow
1. Navigate to elevenlabs.io via Playwright MCP
2. Click "Sign in" and enter email
3. Enter password
4. Handle Google SSO if configured
5. Complete 2FA if required (via iMessage)

## Error Handling
- **Login Failed**: Retry up to 3 times, notify via iMessage
- **Session Expired**: Re-authenticate automatically
- **Rate Limited**: Check character limits
- **2FA Required**: Send iMessage notification
- **Generation Failed**: Retry or adjust settings
- **Quota Exceeded**: Notify about limits

## Self-Improvement Instructions
When ElevenLabs updates:
1. Document new voice models
2. Update voice settings options
3. Track quality improvements
4. Log new language support

## Notes
- Character-based billing
- Voice cloning on higher tiers
- Multiple language support
- Voice settings affect output
- API available for integration

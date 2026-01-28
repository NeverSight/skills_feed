---
name: murf
description: Create AI voiceovers with Murf - generate professional narration, manage projects, and export audio
category: ai
---

# Murf Skill

## Overview
Enables Claude to use Murf AI for professional voiceover generation including creating projects, generating speech, and managing voice narration content.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/murf/install.sh | bash
```

Or manually:
```bash
cp -r skills/murf ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set MURF_EMAIL "your-email@example.com"
canifi-env set MURF_PASSWORD "your-password"
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
- Generate voiceover from text
- Manage voiceover projects
- Select from voice library
- Adjust pitch and speed
- Download audio files
- Add background music

## Usage Examples

### Example 1: Create Voiceover
```
User: "Create a professional voiceover for my explainer video script"
Claude: I'll create the voiceover.
1. Opening Murf via Playwright MCP
2. Creating new project
3. Pasting your script
4. Selecting professional voice
5. Generating and downloading audio
```

### Example 2: Adjust Voice Settings
```
User: "Make the narration slower and deeper"
Claude: I'll adjust the voice settings.
1. Opening your voiceover project
2. Decreasing speech speed
3. Lowering pitch settings
4. Regenerating audio
5. Previewing changes
```

### Example 3: Export Project
```
User: "Download my voiceover project"
Claude: I'll export your project.
1. Opening the project
2. Selecting export options
3. Choosing audio format
4. Downloading final file
```

## Authentication Flow
1. Navigate to murf.ai via Playwright MCP
2. Click "Sign in" and enter email
3. Enter password
4. Handle Google SSO if configured
5. Complete 2FA if required (via iMessage)

## Error Handling
- **Login Failed**: Retry up to 3 times, notify via iMessage
- **Session Expired**: Re-authenticate automatically
- **Rate Limited**: Check usage limits
- **2FA Required**: Send iMessage notification
- **Generation Failed**: Retry or adjust text
- **Credit Limit**: Notify about plan limits

## Self-Improvement Instructions
When Murf updates:
1. Document new voices added
2. Update editing capabilities
3. Track language additions
4. Log export format options

## Notes
- Minute-based billing
- 120+ voices available
- Multiple languages supported
- Studio editor available
- Team collaboration features

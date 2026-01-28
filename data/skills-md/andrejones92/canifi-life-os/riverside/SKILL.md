---
name: riverside
description: Record high-quality podcasts and interviews with Riverside - manage recordings, transcripts, and exports
category: video
---

# Riverside Skill

## Overview
Enables Claude to use Riverside.fm for podcast and interview recording management including accessing recordings, managing transcripts, and exporting content.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/riverside/install.sh | bash
```

Or manually:
```bash
cp -r skills/riverside ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set RIVERSIDE_EMAIL "your-email@example.com"
canifi-env set RIVERSIDE_PASSWORD "your-password"
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
- Access and manage studio recordings
- View and export transcriptions
- Download high-quality audio/video tracks
- Manage recording sessions
- Access Magic Clips and highlights
- Configure studio settings

## Usage Examples

### Example 1: Download Recording
```
User: "Download the separate audio tracks from my interview"
Claude: I'll download your recording tracks.
1. Opening Riverside via Playwright MCP
2. Navigating to your studios
3. Finding the interview recording
4. Accessing download options
5. Downloading individual audio tracks
```

### Example 2: Get Transcript
```
User: "Export the transcript from yesterday's podcast"
Claude: I'll export the transcript.
1. Finding yesterday's recording
2. Accessing transcript tab
3. Exporting as text format
4. Downloading to your folder
```

### Example 3: View Magic Clips
```
User: "Show me the AI-generated highlights from my episode"
Claude: I'll find your Magic Clips.
1. Opening the episode recording
2. Navigating to Magic Clips section
3. Listing generated highlights
4. Providing preview links
```

## Authentication Flow
1. Navigate to riverside.fm via Playwright MCP
2. Click "Log in" and enter email
3. Enter password
4. Handle Google SSO if configured
5. Complete 2FA if required (via iMessage)

## Error Handling
- **Login Failed**: Retry up to 3 times, notify via iMessage
- **Session Expired**: Re-authenticate automatically
- **Rate Limited**: Implement exponential backoff
- **2FA Required**: Send iMessage notification
- **Recording Unavailable**: Check processing status
- **Export Failed**: Verify file availability

## Self-Improvement Instructions
When Riverside updates:
1. Document new recording features
2. Update export format options
3. Track Magic Clips improvements
4. Log transcription enhancements

## Notes
- Local recording ensures quality
- Separate tracks per participant
- Magic Clips uses AI for highlights
- Processing time varies by length
- Studio settings persist per user

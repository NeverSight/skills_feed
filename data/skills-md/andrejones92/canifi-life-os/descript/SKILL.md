---
name: descript
description: Edit audio and video with Descript - transcribe, edit, and produce multimedia content using text-based editing
category: video
---

# Descript Skill

## Overview
Enables Claude to use Descript for audio and video editing through text-based editing interface, including transcription, editing, and content production.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/descript/install.sh | bash
```

Or manually:
```bash
cp -r skills/descript ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set DESCRIPT_EMAIL "your-email@example.com"
canifi-env set DESCRIPT_PASSWORD "your-password"
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
- Access and manage projects
- View and export transcriptions
- Navigate text-based edits
- Export audio and video files
- Access Overdub voice cloning projects
- Manage templates and compositions

## Usage Examples

### Example 1: Export Transcription
```
User: "Get the transcript from my latest podcast episode"
Claude: I'll export your podcast transcript.
1. Opening Descript via Playwright MCP
2. Navigating to your project
3. Finding the podcast episode
4. Exporting transcript as text
5. Formatting for readability
```

### Example 2: Check Project Status
```
User: "What's the status of my video edit projects?"
Claude: I'll check your project status.
1. Opening Descript dashboard
2. Listing active projects
3. Checking processing status
4. Summarizing project states
```

### Example 3: Download Export
```
User: "Download the final audio of my edited interview"
Claude: I'll export your audio file.
1. Opening the interview project
2. Navigating to export options
3. Selecting audio format
4. Initiating download
```

## Authentication Flow
1. Navigate to descript.com via Playwright MCP
2. Click "Log in" and enter email
3. Enter password
4. Handle Google SSO if configured
5. Complete 2FA if required (via iMessage)

## Error Handling
- **Login Failed**: Retry up to 3 times, notify via iMessage
- **Session Expired**: Re-authenticate automatically
- **Rate Limited**: Implement exponential backoff
- **2FA Required**: Send iMessage notification
- **Transcription Failed**: Check audio quality
- **Export Error**: Verify project settings

## Self-Improvement Instructions
When Descript updates:
1. Document new editing features
2. Update export format options
3. Track AI feature improvements
4. Log Overdub capabilities

## Notes
- Text-based editing is unique approach
- Transcription quality varies by audio
- Overdub requires voice training
- Studio Sound improves audio
- Team collaboration available

---
name: kapwing
description: Edit videos online with Kapwing - create, edit, and export video content with collaborative tools
category: video
---

# Kapwing Skill

## Overview
Enables Claude to use Kapwing for online video editing including creating projects, applying edits, managing templates, and exporting finished content.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/kapwing/install.sh | bash
```

Or manually:
```bash
cp -r skills/kapwing ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set KAPWING_EMAIL "your-email@example.com"
canifi-env set KAPWING_PASSWORD "your-password"
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
- Create and edit video projects
- Apply AI-powered editing features
- Use and customize templates
- Export in various formats
- Manage project library
- Access subtitle and caption tools

## Usage Examples

### Example 1: Create Subtitle Project
```
User: "Add subtitles to my video automatically"
Claude: I'll add auto-subtitles.
1. Opening Kapwing via Playwright MCP
2. Uploading your video
3. Using auto-subtitle feature
4. Reviewing generated captions
5. Exporting with burned-in subtitles
```

### Example 2: Resize for Social
```
User: "Resize my video for Instagram Stories"
Claude: I'll resize your video.
1. Opening your video project
2. Selecting Stories aspect ratio (9:16)
3. Adjusting video framing
4. Exporting in story format
```

### Example 3: Download Project
```
User: "Export my edited video in HD"
Claude: I'll export your video.
1. Opening your project
2. Selecting HD export quality
3. Initiating export process
4. Downloading finished video
```

## Authentication Flow
1. Navigate to kapwing.com via Playwright MCP
2. Click "Log in" and enter email
3. Enter password
4. Handle Google SSO if configured
5. Complete 2FA if required (via iMessage)

## Error Handling
- **Login Failed**: Retry up to 3 times, notify via iMessage
- **Session Expired**: Re-authenticate automatically
- **Rate Limited**: Implement exponential backoff
- **2FA Required**: Send iMessage notification
- **Export Failed**: Check project for errors
- **Upload Error**: Verify file format and size

## Self-Improvement Instructions
When Kapwing updates:
1. Document new AI editing features
2. Update export quality options
3. Track template additions
4. Log subtitle improvements

## Notes
- Browser-based video editing
- AI features for efficiency
- Collaboration available on teams
- Watermark on free tier exports
- Cloud project storage

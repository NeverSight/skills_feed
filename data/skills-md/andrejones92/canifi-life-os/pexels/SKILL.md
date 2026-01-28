---
name: pexels
description: Access free stock photos and videos on Pexels - search, download, and curate visual content for projects
category: design
---

# Pexels Skill

## Overview
Enables Claude to use Pexels for finding and downloading high-quality, royalty-free photos and videos for creative projects without attribution requirements.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/pexels/install.sh | bash
```

Or manually:
```bash
cp -r skills/pexels ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set PEXELS_EMAIL "your-email@example.com"
canifi-env set PEXELS_PASSWORD "your-password"
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
- Search photos and videos by keyword
- Download in multiple resolutions
- Create and manage collections
- Filter by color, orientation, and size
- Access curated collections
- Download videos for projects

## Usage Examples

### Example 1: Find Video Background
```
User: "Find a looping video background of city lights"
Claude: I'll search for city lights videos.
1. Opening Pexels via Playwright MCP
2. Switching to video search
3. Searching "city lights night loop"
4. Previewing top video results
5. Downloading selected video in HD
```

### Example 2: Download Product Photos
```
User: "Get minimalist product photography backgrounds"
Claude: I'll find minimalist backgrounds.
1. Searching "minimalist product background"
2. Filtering by white/neutral colors
3. Selecting high-resolution options
4. Downloading to your project folder
```

### Example 3: Color-Matched Search
```
User: "Find photos with our brand color #FF6B35"
Claude: I'll search for matching color photos.
1. Navigating to Pexels color search
2. Entering hex color #FF6B35
3. Browsing color-matched results
4. Saving relevant images to collection
```

## Authentication Flow
1. Navigate to pexels.com via Playwright MCP
2. Click "Join" or "Login"
3. Enter email and password
4. Handle social login if configured
5. Maintain session for collections

## Error Handling
- **Login Failed**: Retry up to 3 times, notify via iMessage
- **Session Expired**: Re-authenticate automatically
- **Rate Limited**: Implement exponential backoff
- **Download Failed**: Retry or try alternate resolution
- **Video Processing**: Wait for video to be ready
- **Search Empty**: Suggest related keywords

## Self-Improvement Instructions
When Pexels updates its platform:
1. Document new search capabilities
2. Update video download workflows
3. Track collection feature changes
4. Log any new filter options

## Notes
- Pexels photos are free without attribution
- Video files can be large - allow download time
- Some content from partner photographers
- API access available with key
- Collections sync across devices

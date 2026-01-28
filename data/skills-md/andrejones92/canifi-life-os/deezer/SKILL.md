---
name: deezer
description: Stream music on Deezer, manage playlists, and discover new artists with Flow
category: entertainment
---

# Deezer Skill

## Overview
Enables Claude to interact with Deezer for streaming music, managing playlists, using the Flow personalized radio feature, and discovering new music through smart recommendations.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/deezer/install.sh | bash
```

Or manually:
```bash
cp -r skills/deezer ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set DEEZER_EMAIL "your-email@example.com"
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
- Stream songs, albums, and playlists
- Create and manage custom playlists
- Use Flow personalized radio
- View listening history and favorites
- Discover music through recommendations

## Usage Examples
### Example 1: Start Flow
```
User: "Play my Flow on Deezer"
Claude: I'll start your personalized Flow radio based on your listening preferences.
```

### Example 2: Create Playlist
```
User: "Create a workout playlist on Deezer"
Claude: I'll create a new workout playlist and add energetic tracks.
```

### Example 3: Favorite Artists
```
User: "Who are my most listened to artists on Deezer?"
Claude: I'll check your listening history and show your top artists.
```

## Authentication Flow
1. Navigate to deezer.com via Playwright MCP
2. Click "Log In" button
3. Enter email and password
4. Handle social login if used
5. Maintain session for subsequent requests

## Error Handling
- Login Failed: Retry authentication up to 3 times, then notify via iMessage
- Session Expired: Re-authenticate automatically
- Rate Limited: Implement exponential backoff
- Content Unavailable: Check regional availability
- Quality Restrictions: Verify Premium subscription

## Self-Improvement Instructions
When encountering new UI patterns:
1. Document Deezer interface changes
2. Update selectors for new layouts
3. Track Flow algorithm improvements
4. Monitor new feature additions

## Notes
- Free tier available with ads
- Premium for offline and HiFi
- Flow uses AI for personalization
- Lyrics available on many tracks

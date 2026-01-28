---
name: youtube-music
description: Stream music on YouTube Music, manage playlists, and access music videos
category: entertainment
---

# YouTube Music Skill

## Overview
Enables Claude to interact with YouTube Music for streaming songs, creating playlists, accessing music videos, and discovering new music through personalized recommendations.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/youtube-music/install.sh | bash
```

Or manually:
```bash
cp -r skills/youtube-music ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set GOOGLE_EMAIL "your-email@example.com"
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
- Access official music videos
- View listening history and recommendations
- Like songs and manage library

## Usage Examples
### Example 1: Create Playlist
```
User: "Create a chill vibes playlist on YouTube Music"
Claude: I'll create a new playlist called "Chill Vibes" and start adding relaxing tracks.
```

### Example 2: Find Music Video
```
User: "Play the music video for Bohemian Rhapsody"
Claude: I'll find and play the official music video for Bohemian Rhapsody.
```

### Example 3: Explore New Releases
```
User: "What's new in hip-hop this week?"
Claude: I'll check the new releases section for recent hip-hop albums and singles.
```

## Authentication Flow
1. Navigate to music.youtube.com via Playwright MCP
2. Click "Sign In" button
3. Enter Google account credentials
4. Handle 2FA if enabled
5. Maintain session for subsequent requests

## Error Handling
- Login Failed: Retry authentication up to 3 times, then notify via iMessage
- Session Expired: Re-authenticate with Google
- 2FA Required: Wait for code via iMessage or authenticator
- Rate Limited: Implement exponential backoff
- Content Unavailable: Check regional restrictions

## Self-Improvement Instructions
When encountering new UI patterns:
1. Document YouTube Music interface changes
2. Update selectors for new layouts
3. Track playlist sync with YouTube
4. Monitor Premium vs Free feature differences

## Notes
- YouTube Premium provides ad-free experience
- Library syncs with main YouTube account
- Background play requires Premium on mobile
- Uploads feature allows personal music

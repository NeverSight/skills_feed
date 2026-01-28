---
name: apple-music
description: Stream and manage Apple Music library, playlists, and radio stations
category: entertainment
---

# Apple Music Skill

## Overview
Enables Claude to interact with Apple Music for streaming, library management, playlist curation, and music discovery through the web interface.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/apple-music/install.sh | bash
```

Or manually:
```bash
cp -r skills/apple-music ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set APPLE_ID_EMAIL "your-email@example.com"
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
- Manage personal music library
- Create and edit playlists
- Access Apple Music radio stations
- View listening history and recommendations

## Usage Examples
### Example 1: Add to Library
```
User: "Add the new Taylor Swift album to my library"
Claude: I'll search for Taylor Swift's latest album and add it to your Apple Music library.
```

### Example 2: Create Radio Station
```
User: "Start a radio station based on The Beatles"
Claude: I'll create a personalized radio station inspired by The Beatles' music style.
```

### Example 3: Manage Playlist
```
User: "Add this song to my Road Trip playlist"
Claude: I'll add the currently playing song to your Road Trip playlist.
```

## Authentication Flow
1. Navigate to music.apple.com via Playwright MCP
2. Click "Sign In" button
3. Enter Apple ID credentials
4. Handle 2FA via trusted device or iMessage
5. Maintain session for subsequent requests

## Error Handling
- Login Failed: Retry authentication up to 3 times, then notify via iMessage
- Session Expired: Re-authenticate automatically
- Rate Limited: Implement exponential backoff
- 2FA Required: Wait for code via iMessage or trusted device
- Playback Error: Check subscription status and device availability

## Self-Improvement Instructions
When encountering new UI patterns or changes:
1. Document the change with context
2. Update element selectors accordingly
3. Track successful operations for pattern learning
4. Suggest workflow optimizations

## Notes
- Requires active Apple Music subscription
- Web player has some limitations vs native apps
- 2FA is typically required for Apple ID
- Library sync may take a few moments

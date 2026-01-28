---
name: spotify
description: Control Spotify music playback, manage playlists, discover new music, and track listening history
category: entertainment
---

# Spotify Skill

## Overview
Enables Claude to interact with Spotify for music playback control, playlist management, music discovery, and listening analytics through browser automation.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/spotify/install.sh | bash
```

Or manually:
```bash
cp -r skills/spotify ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set SPOTIFY_EMAIL "your-email@example.com"
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
- Control playback (play, pause, skip, shuffle, repeat)
- Create, edit, and manage playlists
- Search for songs, artists, albums, and podcasts
- View and manage listening history
- Discover new music through recommendations

## Usage Examples
### Example 1: Create a Playlist
```
User: "Create a workout playlist with high-energy songs"
Claude: I'll create a new playlist called "Workout Energy" and add some high-tempo tracks to get you moving.
```

### Example 2: Control Playback
```
User: "Play some relaxing jazz music"
Claude: I'll search for relaxing jazz and start playing a curated selection for you.
```

### Example 3: Check Listening Stats
```
User: "What have I been listening to this week?"
Claude: I'll check your recently played tracks and summarize your listening activity.
```

## Authentication Flow
1. Navigate to open.spotify.com via Playwright MCP
2. Click "Log in" button
3. Enter email credentials
4. Handle 2FA if enabled (via iMessage)
5. Maintain session cookies for future requests

## Error Handling
- Login Failed: Retry authentication up to 3 times, then notify via iMessage
- Session Expired: Re-authenticate automatically
- Rate Limited: Implement exponential backoff (1s, 2s, 4s)
- 2FA Required: Wait for code via iMessage, enter automatically
- Playback Error: Check device availability, suggest alternatives

## Self-Improvement Instructions
When encountering new UI patterns or API changes:
1. Document the change with screenshots
2. Update selectors in this skill file
3. Suggest workflow improvements based on usage patterns
4. Log successful and failed operations for optimization

## Notes
- Spotify Free accounts have limited skip functionality
- Some features require Premium subscription
- Playback control requires an active Spotify client on a device
- Web player has limitations compared to desktop/mobile apps

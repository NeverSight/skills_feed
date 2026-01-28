---
name: pandora
description: Stream personalized radio stations on Pandora and create custom music experiences
category: entertainment
---

# Pandora Skill

## Overview
Enables Claude to interact with Pandora for streaming personalized radio stations, creating stations based on artists or songs, and managing music preferences through thumbs feedback.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/pandora/install.sh | bash
```

Or manually:
```bash
cp -r skills/pandora ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set PANDORA_EMAIL "your-email@example.com"
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
- Create and manage radio stations
- Provide thumbs up/down feedback
- Access Pandora Modes for mood-based listening
- View station history and seeds
- Discover new music through Music Genome

## Usage Examples
### Example 1: Create Station
```
User: "Create a Pandora station based on The Beatles"
Claude: I'll create a new radio station seeded with The Beatles for similar classic rock.
```

### Example 2: Thumbs Feedback
```
User: "I like this song on Pandora"
Claude: I'll give this track a thumbs up to improve your station recommendations.
```

### Example 3: Pandora Modes
```
User: "Play something for deep focus on Pandora"
Claude: I'll activate a focus mode for concentration-friendly music.
```

## Authentication Flow
1. Navigate to pandora.com via Playwright MCP
2. Click "Sign In" button
3. Enter email and password
4. Handle subscription verification
5. Maintain session for subsequent requests

## Error Handling
- Login Failed: Retry authentication up to 3 times, then notify via iMessage
- Session Expired: Re-authenticate automatically
- Rate Limited: Implement exponential backoff
- Skip Limit: Notify user of free tier restrictions
- Station Limit: Check account tier for station count

## Self-Improvement Instructions
When encountering new UI patterns:
1. Document Pandora interface changes
2. Update selectors for new layouts
3. Track Music Genome algorithm updates
4. Monitor Modes feature additions

## Notes
- Free tier has skip limits and ads
- Premium allows on-demand playback
- Music Genome Project powers recommendations
- Stations improve with more feedback

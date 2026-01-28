---
name: funimation
description: Stream dubbed anime on Funimation and access legacy content library
category: entertainment
---

# Funimation Skill

## Overview
Enables Claude to interact with Funimation for streaming dubbed anime content, accessing the legacy library now part of Crunchyroll ecosystem, and managing viewing preferences.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/funimation/install.sh | bash
```

Or manually:
```bash
cp -r skills/funimation ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set FUNIMATION_EMAIL "your-email@example.com"
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
- Stream dubbed anime series and movies
- Access Funimation legacy catalog
- Manage queue and watchlist
- View watch history
- Browse by genre and popularity

## Usage Examples
### Example 1: Add to Queue
```
User: "Add My Hero Academia to my Funimation queue"
Claude: I'll add My Hero Academia to your Funimation queue.
```

### Example 2: Find Dubbed Content
```
User: "What anime has English dubs on Funimation?"
Claude: I'll browse the dubbed anime catalog and show you popular options.
```

### Example 3: Continue Watching
```
User: "Where was I in Dragon Ball Super?"
Claude: I'll check your watch history to find your progress in Dragon Ball Super.
```

## Authentication Flow
1. Navigate to funimation.com via Playwright MCP
2. Click "Log In" button
3. Enter email and password
4. Handle any migration prompts to Crunchyroll
5. Maintain session for subsequent requests

## Error Handling
- Login Failed: Retry authentication up to 3 times, then notify via iMessage
- Session Expired: Re-authenticate automatically
- Rate Limited: Implement exponential backoff
- Content Migrated: Redirect to Crunchyroll if applicable
- Regional Restrictions: Notify user of availability

## Self-Improvement Instructions
When encountering new UI patterns:
1. Document any migration to Crunchyroll
2. Update selectors for interface changes
3. Track content availability changes
4. Monitor service status

## Notes
- Funimation merged with Crunchyroll
- Some content may redirect to Crunchyroll
- Known for English dubbed anime
- Legacy accounts may need migration

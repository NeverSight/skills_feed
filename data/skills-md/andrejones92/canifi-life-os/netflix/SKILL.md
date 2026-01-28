---
name: netflix
description: Browse Netflix content, manage watchlist, and get personalized recommendations
category: entertainment
---

# Netflix Skill

## Overview
Enables Claude to interact with Netflix for content discovery, watchlist management, viewing history analysis, and personalized recommendations.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/netflix/install.sh | bash
```

Or manually:
```bash
cp -r skills/netflix ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set NETFLIX_EMAIL "your-email@example.com"
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
- Browse movies and TV shows by genre
- Manage "My List" watchlist
- View and analyze watch history
- Get personalized content recommendations
- Search for specific titles or actors

## Usage Examples
### Example 1: Add to Watchlist
```
User: "Add Stranger Things to my Netflix list"
Claude: I'll add Stranger Things to your My List on Netflix.
```

### Example 2: Find Recommendations
```
User: "What should I watch tonight? I'm in the mood for a thriller"
Claude: Based on your viewing history and preferences, I'll find some thriller recommendations for you.
```

### Example 3: Check Watch History
```
User: "What episode of The Crown was I on?"
Claude: I'll check your viewing history to find where you left off in The Crown.
```

## Authentication Flow
1. Navigate to netflix.com via Playwright MCP
2. Click "Sign In" button
3. Enter email and password
4. Select user profile if multiple exist
5. Maintain session cookies for future access

## Error Handling
- Login Failed: Retry authentication up to 3 times, then notify via iMessage
- Session Expired: Re-authenticate automatically
- Profile Selection: Prompt user to specify which profile
- Rate Limited: Implement backoff strategy
- Content Unavailable: Notify user of regional restrictions

## Self-Improvement Instructions
When encountering new UI patterns:
1. Document changes in Netflix interface
2. Update selectors for new layouts
3. Track content discovery patterns
4. Optimize recommendation accuracy

## Notes
- Different profiles have separate watchlists
- Content availability varies by region
- Some features require specific subscription tiers
- Auto-play settings may affect navigation

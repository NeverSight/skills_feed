---
name: disney-plus
description: Stream Disney+ content including Disney, Pixar, Marvel, Star Wars, and National Geographic
category: entertainment
---

# Disney+ Skill

## Overview
Enables Claude to interact with Disney+ for streaming content from Disney, Pixar, Marvel, Star Wars, and National Geographic, managing watchlist, and discovering family-friendly entertainment.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/disney-plus/install.sh | bash
```

Or manually:
```bash
cp -r skills/disney-plus ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set DISNEY_PLUS_EMAIL "your-email@example.com"
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
- Browse content by brand (Disney, Pixar, Marvel, Star Wars, Nat Geo)
- Manage personal watchlist
- View watch history and continue watching
- Access GroupWatch for shared viewing
- Search for specific movies, shows, or characters

## Usage Examples
### Example 1: Add to Watchlist
```
User: "Add The Mandalorian to my Disney+ watchlist"
Claude: I'll add The Mandalorian to your Disney+ watchlist.
```

### Example 2: Find Marvel Content
```
User: "Show me all Marvel movies in order"
Claude: I'll navigate to the Marvel section and list the movies in chronological or release order.
```

### Example 3: Kids Profile Content
```
User: "What's good for my kids on Disney+?"
Claude: I'll browse the Kids profile section for age-appropriate content recommendations.
```

## Authentication Flow
1. Navigate to disneyplus.com via Playwright MCP
2. Click "Log In" button
3. Enter email and password
4. Select user profile
5. Maintain session cookies for future access

## Error Handling
- Login Failed: Retry authentication up to 3 times, then notify via iMessage
- Session Expired: Re-authenticate automatically
- Profile Selection: Prompt user to specify profile
- Rate Limited: Implement backoff strategy
- Content Unavailable: Check regional restrictions

## Self-Improvement Instructions
When encountering new UI patterns:
1. Document Disney+ interface changes
2. Update selectors for new layouts
3. Track content additions by brand
4. Monitor GroupWatch functionality

## Notes
- Multiple profiles with different content restrictions
- 4K/HDR content requires compatible subscription
- Downloads only available on mobile apps
- Some content has premiere access fees

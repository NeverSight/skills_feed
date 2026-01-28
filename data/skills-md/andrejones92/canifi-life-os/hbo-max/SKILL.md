---
name: hbo-max
description: Stream HBO Max content including HBO originals, Warner Bros films, and Max exclusives
category: entertainment
---

# HBO Max Skill

## Overview
Enables Claude to interact with Max (formerly HBO Max) for streaming HBO originals, Warner Bros. films, DC content, and Max exclusives, with watchlist management and content discovery.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/hbo-max/install.sh | bash
```

Or manually:
```bash
cp -r skills/hbo-max ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set HBO_MAX_EMAIL "your-email@example.com"
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
- Browse HBO originals and Max exclusives
- Access Warner Bros. theatrical releases
- Manage "My List" watchlist
- View watch history and continue watching
- Explore curated collections and hubs

## Usage Examples
### Example 1: Add to My List
```
User: "Add House of the Dragon to my HBO Max list"
Claude: I'll add House of the Dragon to your My List on Max.
```

### Example 2: Find DC Content
```
User: "Show me all DC movies on Max"
Claude: I'll navigate to the DC hub and list available movies and shows.
```

### Example 3: New Releases
```
User: "What new movies are on Max this month?"
Claude: I'll check the new releases section for recently added theatrical films.
```

## Authentication Flow
1. Navigate to max.com via Playwright MCP
2. Click "Sign In" button
3. Enter email and password
4. Select profile if multiple exist
5. Maintain session for subsequent requests

## Error Handling
- Login Failed: Retry authentication up to 3 times, then notify via iMessage
- Session Expired: Re-authenticate automatically
- Profile Selection: Prompt user to specify profile
- Rate Limited: Implement exponential backoff
- Content Unavailable: Check subscription tier or regional restrictions

## Self-Improvement Instructions
When encountering new UI patterns:
1. Document Max interface changes
2. Update selectors for rebranded elements
3. Track content hub organization
4. Monitor new feature additions

## Notes
- Platform rebranded from HBO Max to Max
- Different subscription tiers available
- Some content may require additional purchase
- 4K content on specific plans only

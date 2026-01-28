---
name: apple-tv-plus
description: Stream Apple TV+ original content and manage watchlist
category: entertainment
---

# Apple TV+ Skill

## Overview
Enables Claude to interact with Apple TV+ for streaming Apple original content, managing Up Next list, and discovering award-winning shows and movies exclusive to the platform.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/apple-tv-plus/install.sh | bash
```

Or manually:
```bash
cp -r skills/apple-tv-plus ~/.canifi/skills/
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
- Browse Apple TV+ originals
- Manage Up Next watchlist
- View watch history and continue watching
- Access bonus content and behind-the-scenes
- Explore curated collections

## Usage Examples
### Example 1: Add to Up Next
```
User: "Add Ted Lasso to my Apple TV+ list"
Claude: I'll add Ted Lasso to your Up Next list on Apple TV+.
```

### Example 2: Browse Originals
```
User: "What new shows are on Apple TV+?"
Claude: I'll check the latest Apple TV+ originals and show you recent releases.
```

### Example 3: Movie Night
```
User: "What Apple TV+ movies have won awards?"
Claude: I'll browse for award-winning Apple TV+ original films.
```

## Authentication Flow
1. Navigate to tv.apple.com via Playwright MCP
2. Click "Sign In" button
3. Enter Apple ID credentials
4. Handle 2FA via trusted device or iMessage
5. Maintain session for subsequent requests

## Error Handling
- Login Failed: Retry authentication up to 3 times, then notify via iMessage
- Session Expired: Re-authenticate with Apple ID
- 2FA Required: Wait for code via trusted device or iMessage
- Rate Limited: Implement exponential backoff
- Content Unavailable: Check subscription status

## Self-Improvement Instructions
When encountering new UI patterns:
1. Document Apple TV+ interface changes
2. Update selectors for new layouts
3. Track new original content releases
4. Monitor bonus content availability

## Notes
- Requires Apple TV+ subscription
- Free trial often available
- Exclusive original content only
- Available on Apple devices and browsers

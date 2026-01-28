---
name: audible
description: Browse and manage Audible audiobook library, discover new titles, and track listening progress
category: entertainment
---

# Audible Skill

## Overview
Enables Claude to interact with Audible for browsing audiobooks, managing library, tracking listening progress, and discovering new titles based on preferences.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/audible/install.sh | bash
```

Or manually:
```bash
cp -r skills/audible ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set AMAZON_EMAIL "your-email@example.com"
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
- Browse audiobook library and wishlist
- Search for new audiobooks by title, author, or narrator
- View listening history and progress
- Manage credits and membership benefits
- Access Audible Plus catalog included titles

## Usage Examples
### Example 1: Check Library
```
User: "What audiobooks do I have on Audible?"
Claude: I'll browse your Audible library and list your purchased audiobooks.
```

### Example 2: Find New Books
```
User: "Find some good sci-fi audiobooks on Audible"
Claude: I'll search for highly-rated science fiction audiobooks and show you the top options.
```

### Example 3: Check Credits
```
User: "How many Audible credits do I have?"
Claude: I'll check your account to see your available credits and membership status.
```

## Authentication Flow
1. Navigate to audible.com via Playwright MCP
2. Click "Sign In" button
3. Enter Amazon credentials
4. Handle 2FA if enabled
5. Maintain session for subsequent requests

## Error Handling
- Login Failed: Retry authentication up to 3 times, then notify via iMessage
- Session Expired: Re-authenticate with Amazon
- 2FA Required: Wait for code via iMessage
- Rate Limited: Implement exponential backoff
- Content Unavailable: Check membership tier

## Self-Improvement Instructions
When encountering new UI patterns:
1. Document Audible interface changes
2. Update selectors for new layouts
3. Track Plus catalog vs purchase-only titles
4. Monitor credit system changes

## Notes
- Requires Amazon account linked to Audible
- Different membership tiers offer different benefits
- Audible Plus catalog varies by membership
- Listen progress syncs across devices

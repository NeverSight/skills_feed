---
name: kindle
description: Manage Kindle ebook library, track reading progress, and discover new books
category: entertainment
---

# Kindle Skill

## Overview
Enables Claude to interact with Amazon Kindle for managing ebook library, tracking reading progress, discovering new books, and accessing Kindle Unlimited catalog.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/kindle/install.sh | bash
```

Or manually:
```bash
cp -r skills/kindle ~/.canifi/skills/
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
- Browse and manage ebook library
- Track reading progress across devices
- Search for new ebooks and samples
- Access Kindle Unlimited catalog
- Manage collections and organization

## Usage Examples
### Example 1: Check Library
```
User: "What books do I have in my Kindle library?"
Claude: I'll browse your Kindle library and list your purchased and borrowed ebooks.
```

### Example 2: Reading Progress
```
User: "Where did I leave off in my current book?"
Claude: I'll check your reading progress and show where you are in your currently reading books.
```

### Example 3: Find New Books
```
User: "Find some mystery novels on Kindle Unlimited"
Claude: I'll search Kindle Unlimited for highly-rated mystery novels available to borrow.
```

## Authentication Flow
1. Navigate to read.amazon.com via Playwright MCP
2. Click "Sign In" button
3. Enter Amazon credentials
4. Handle 2FA if enabled
5. Maintain session for subsequent requests

## Error Handling
- Login Failed: Retry authentication up to 3 times, then notify via iMessage
- Session Expired: Re-authenticate with Amazon
- 2FA Required: Wait for code via iMessage
- Rate Limited: Implement exponential backoff
- Content Unavailable: Check Kindle Unlimited membership

## Self-Improvement Instructions
When encountering new UI patterns:
1. Document Kindle web reader changes
2. Update selectors for new layouts
3. Track Kindle Unlimited catalog changes
4. Monitor sync functionality

## Notes
- Web reader has limited features vs apps
- Kindle Unlimited requires separate subscription
- Reading progress syncs via Whispersync
- Some books may have lending restrictions

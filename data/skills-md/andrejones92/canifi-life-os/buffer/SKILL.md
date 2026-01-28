---
name: buffer
description: Manage social media scheduling and publishing with Buffer's intuitive platform.
category: marketing
---
# Buffer Skill

Manage social media scheduling and publishing with Buffer's intuitive platform.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/buffer/install.sh | bash
```

Or manually:
```bash
cp -r skills/buffer ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set BUFFER_ACCESS_TOKEN "your_access_token"
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

1. **Post Scheduling**: Schedule posts across multiple social platforms
2. **Content Calendar**: View and manage scheduled content calendar
3. **Analytics**: Track post performance and engagement metrics
4. **Team Collaboration**: Manage drafts and approvals with team
5. **Link Shortening**: Track link clicks with built-in shortener

## Usage Examples

### Schedule Post
```
User: "Schedule a tweet for tomorrow at 9am about our new feature"
Assistant: Creates and schedules tweet
```

### View Queue
```
User: "Show me my Buffer queue for this week"
Assistant: Returns scheduled posts by day
```

### Analyze Post
```
User: "How did my last LinkedIn post perform?"
Assistant: Returns engagement metrics
```

### Add to Queue
```
User: "Add this article to my Buffer queue for Facebook"
Assistant: Queues post with link and preview
```

## Authentication Flow

1. Create app in Buffer developer portal
2. Implement OAuth 2.0 authorization
3. Get access token after user approval
4. Use token for all API requests

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| 401 Unauthorized | Invalid token | Re-authenticate |
| 403 Forbidden | No access to profile | Check connected accounts |
| 404 Not Found | Post not found | Verify post ID |
| 429 Rate Limited | Too many requests | Wait and retry |

## Notes

- Supports Twitter, Facebook, Instagram, LinkedIn, Pinterest
- Free tier with 3 channels
- Team features in paid plans
- Start Page for bio links
- Analytics in paid tiers
- Browser extension available

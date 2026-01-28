---
name: later
description: Manage visual social media scheduling with Later's Instagram-focused platform.
category: marketing
---
# Later Skill

Manage visual social media scheduling with Later's Instagram-focused platform.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/later/install.sh | bash
```

Or manually:
```bash
cp -r skills/later ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set LATER_ACCESS_TOKEN "your_access_token"
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

1. **Visual Planning**: Plan and preview visual content calendar
2. **Instagram Scheduling**: Schedule Instagram posts, stories, and reels
3. **Link in Bio**: Manage Linkin.bio landing pages
4. **Media Library**: Organize and store media assets
5. **Analytics**: Track Instagram and social performance

## Usage Examples

### Schedule Post
```
User: "Schedule this image to Instagram for tomorrow"
Assistant: Creates scheduled post with image
```

### Plan Grid
```
User: "Show me my Instagram grid preview"
Assistant: Returns visual preview of planned posts
```

### Update Linkinbio
```
User: "Add a new link to my Later Linkin.bio"
Assistant: Adds link to bio landing page
```

### View Analytics
```
User: "How did my Instagram posts perform this week?"
Assistant: Returns engagement and growth metrics
```

## Authentication Flow

1. Register app with Later
2. Implement OAuth 2.0 flow
3. Get access token for API calls
4. Token provides account access

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| 401 Unauthorized | Invalid token | Re-authenticate |
| 403 Forbidden | Feature not available | Check plan |
| 404 Not Found | Post not found | Verify post ID |
| 429 Rate Limited | Too many requests | Wait and retry |

## Notes

- Visual-first social planning
- Instagram focus with grid preview
- Linkin.bio included
- TikTok, Pinterest, Twitter support
- Free tier available
- Mobile app for on-the-go

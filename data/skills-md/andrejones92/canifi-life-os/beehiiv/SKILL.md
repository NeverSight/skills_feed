---
name: beehiiv
description: Create, manage, and grow newsletters with Beehiiv's modern newsletter platform.
category: productivity
---
# Beehiiv Skill

Create, manage, and grow newsletters with Beehiiv's modern newsletter platform.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/beehiiv/install.sh | bash
```

Or manually:
```bash
cp -r skills/beehiiv ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set BEEHIIV_API_KEY "your_api_key"
canifi-env set BEEHIIV_PUBLICATION_ID "your_publication_id"
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

1. **Newsletter Publishing**: Create and publish newsletter posts with rich editor and media
2. **Subscriber Management**: Import, segment, and manage subscriber lists
3. **Analytics Dashboard**: Track opens, clicks, growth, and engagement metrics
4. **Monetization Tools**: Set up paid subscriptions and ad network integration
5. **Automation**: Create email sequences and automated workflows

## Usage Examples

### Create Post
```
User: "Create a new Beehiiv post titled 'Weekly AI Digest'"
Assistant: Creates draft post with title and opens editor for content
```

### Get Subscriber Stats
```
User: "How many active subscribers do I have on Beehiiv?"
Assistant: Returns total subscribers, growth rate, and engagement metrics
```

### Publish Newsletter
```
User: "Publish my draft newsletter to all subscribers"
Assistant: Publishes the draft and sends to subscriber list
```

### Add Subscriber
```
User: "Add john@example.com to my Beehiiv newsletter"
Assistant: Adds subscriber with optional tags and segments
```

## Authentication Flow

1. Generate API key from Beehiiv dashboard settings
2. Get publication ID from publication settings
3. Use API key for all authenticated requests
4. Store credentials securely

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| 401 Unauthorized | Invalid API key | Verify API key in settings |
| 403 Forbidden | Insufficient permissions | Check API key permissions |
| 404 Not Found | Publication or post not found | Verify publication ID |
| 422 Validation Error | Invalid data format | Check request payload |

## Notes

- Free tier includes up to 2,500 subscribers
- API available for programmatic access
- Custom domains included in all plans
- Referral program for subscriber growth
- A/B testing available for subject lines
- RSS-to-email automation available

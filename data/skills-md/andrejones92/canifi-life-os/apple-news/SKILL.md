---
name: apple-news
description: Access personalized news and premium content through Apple's native news aggregator.
category: news
---
# Apple News Skill

Access personalized news and premium content through Apple's native news aggregator.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/apple-news/install.sh | bash
```

Or manually:
```bash
cp -r skills/apple-news ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set APPLE_ID "your_apple_id"
canifi-env set APPLE_PASSWORD "your_password"
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

1. **Personalized Feed**: Get news tailored to your interests and reading history
2. **Channel Following**: Follow publishers, topics, and channels for curated content
3. **Apple News+ Access**: Read premium magazine and newspaper content with subscription
4. **Offline Reading**: Download articles for offline access
5. **Audio Stories**: Listen to audio versions of top stories

## Usage Examples

### Get Top Stories
```
User: "Show me today's top stories from Apple News"
Assistant: Returns top headlines and trending stories
```

### Follow Channel
```
User: "Follow The Verge on Apple News"
Assistant: Adds The Verge to your followed channels
```

### Search Articles
```
User: "Search Apple News for articles about electric vehicles"
Assistant: Returns relevant articles from subscribed and suggested sources
```

### Browse Magazine
```
User: "Show me the latest issue of Wired magazine"
Assistant: Opens current Wired issue (requires News+ subscription)
```

## Authentication Flow

1. Apple News requires Apple ID authentication
2. Uses macOS/iOS native authentication
3. News+ requires active subscription
4. Family Sharing supported for subscriptions

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Auth Failed | Invalid Apple ID | Verify Apple ID credentials |
| Subscription Required | News+ content accessed | Subscribe to Apple News+ |
| Region Unavailable | Service not available | Use supported region |
| Content Not Found | Article removed | Check source website |

## Notes

- Only available on Apple platforms (macOS, iOS, iPadOS)
- News+ includes magazines and newspapers
- No third-party API available
- Uses system-level Apple ID authentication
- Local Spotlight integration for search
- Privacy-focused with on-device personalization

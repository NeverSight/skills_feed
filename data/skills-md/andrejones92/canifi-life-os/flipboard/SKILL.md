---
name: flipboard
description: Curate and discover news content with Flipboard's personalized magazine-style reader.
category: news
---
# Flipboard Skill

Curate and discover news content with Flipboard's personalized magazine-style reader.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/flipboard/install.sh | bash
```

Or manually:
```bash
cp -r skills/flipboard ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set FLIPBOARD_USERNAME "your_username"
canifi-env set FLIPBOARD_PASSWORD "your_password"
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

1. **Content Discovery**: Discover articles and stories based on interests and topics
2. **Magazine Creation**: Create and curate personal magazines with saved content
3. **Following System**: Follow topics, publishers, and other curators
4. **Smart Magazines**: Generate AI-curated magazines based on keywords
5. **Social Sharing**: Share articles and magazines to social networks

## Usage Examples

### Discover Content
```
User: "Show me trending tech news on Flipboard"
Assistant: Returns top technology articles from curated sources
```

### Create Magazine
```
User: "Create a Flipboard magazine about sustainable living"
Assistant: Creates new magazine with specified topic and settings
```

### Add to Magazine
```
User: "Add this article to my 'AI Research' magazine"
Assistant: Flips article to specified magazine collection
```

### Follow Topic
```
User: "Follow the 'Artificial Intelligence' topic on Flipboard"
Assistant: Adds topic to your followed interests
```

## Authentication Flow

1. Flipboard uses account-based authentication
2. No official public API for third-party apps
3. Use browser automation for full functionality
4. Session management required for persistent access

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Login Failed | Invalid credentials | Check username and password |
| Magazine Error | Magazine not found | Verify magazine ID or name |
| Rate Limited | Too many requests | Implement request throttling |
| Content Blocked | Region restriction | Check content availability |

## Notes

- No official public API available
- Magazine-style reading experience
- Video content support included
- Available on web, iOS, and Android
- Publisher partnerships for premium content
- Storyboard feature for immersive stories

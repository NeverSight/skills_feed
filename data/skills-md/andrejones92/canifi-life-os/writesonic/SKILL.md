---
name: writesonic
description: AI writing assistant for content creation and SEO.
category: ai
---
# Writesonic Skill

AI writing assistant for content creation and SEO.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/writesonic/install.sh | bash
```

Or manually:
```bash
cp -r skills/writesonic ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set WRITESONIC_API_KEY "your_api_key"
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

1. **Article Writer**: Long-form content
2. **Chatsonic**: AI chatbot with web access
3. **Photosonic**: AI image generation
4. **SEO Tools**: Optimize content
5. **Botsonic**: Custom chatbots

## Usage Examples

### Write Article
```
User: "Create an article about sustainable tech"
Assistant: Generates long-form content
```

### Chat with Chatsonic
```
User: "Ask Chatsonic about current events"
Assistant: Provides real-time response
```

### Generate Image
```
User: "Create an image with Photosonic"
Assistant: Generates AI artwork
```

### Optimize SEO
```
User: "Optimize this content for SEO"
Assistant: Suggests improvements
```

## Authentication Flow

1. API key authentication
2. Subscription tiers
3. Team access
4. Rate limits by plan

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Auth Failed | Invalid key | Check API key |
| Word Limit | Quota exceeded | Upgrade |
| Generation Failed | Content issue | Retry |
| Rate Limited | Too many requests | Wait |

## Notes

- GPT-4 powered
- Real-time web access
- Image generation
- SEO optimization
- API available
- Chrome extension

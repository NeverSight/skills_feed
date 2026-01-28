---
name: convertkit
description: Manage email marketing for creators with ConvertKit's subscriber-focused platform.
category: marketing
---
# ConvertKit Skill

Manage email marketing for creators with ConvertKit's subscriber-focused platform.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/convertkit/install.sh | bash
```

Or manually:
```bash
cp -r skills/convertkit ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set CONVERTKIT_API_KEY "your_api_key"
canifi-env set CONVERTKIT_API_SECRET "your_api_secret"
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

1. **Subscriber Management**: Add and manage subscribers with tags and segments
2. **Sequence Automation**: Create automated email sequences for nurturing
3. **Broadcast Emails**: Send one-time broadcasts to subscribers
4. **Form Management**: Create and manage signup forms
5. **Visual Automation**: Build complex automation workflows visually

## Usage Examples

### Add Subscriber
```
User: "Add sarah@creator.com to ConvertKit with tag 'Course Buyer'"
Assistant: Adds subscriber with specified tag
```

### Create Sequence
```
User: "Create a 5-email welcome sequence in ConvertKit"
Assistant: Creates sequence structure with email placeholders
```

### Send Broadcast
```
User: "Send a broadcast about the new product to all subscribers"
Assistant: Creates and sends broadcast email
```

### View Subscribers
```
User: "Show me my ConvertKit subscribers tagged as 'VIP'"
Assistant: Returns subscribers with VIP tag
```

## Authentication Flow

1. Get API key and secret from ConvertKit settings
2. Use API key for public endpoints
3. Use API secret for sensitive operations
4. Token-based authentication available

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| 401 Unauthorized | Invalid API key | Verify API credentials |
| 404 Not Found | Subscriber not found | Check subscriber ID |
| 422 Unprocessable | Invalid data | Validate request format |
| 429 Rate Limited | Too many requests | Implement throttling |

## Notes

- Built for creators and bloggers
- Tag-based subscriber organization
- Visual automation builder
- Landing page builder included
- Commerce features for selling
- Free tier up to 1000 subscribers

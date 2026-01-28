---
name: jasper
description: AI content platform for marketing teams.
category: ai
---
# Jasper Skill

AI content platform for marketing teams.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/jasper/install.sh | bash
```

Or manually:
```bash
cp -r skills/jasper ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set JASPER_API_KEY "your_api_key"
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

1. **Content Creation**: Generate marketing copy
2. **Brand Voice**: Maintain consistent tone
3. **Campaigns**: Create multi-channel content
4. **Templates**: Use pre-built workflows
5. **Art Generation**: Create images

## Usage Examples

### Generate Copy
```
User: "Create ad copy for this product"
Assistant: Generates marketing content
```

### Use Template
```
User: "Use the blog post template"
Assistant: Creates structured content
```

### Brand Voice
```
User: "Write this in our brand voice"
Assistant: Matches brand guidelines
```

### Create Campaign
```
User: "Create a social media campaign"
Assistant: Generates multi-platform content
```

## Authentication Flow

1. API key authentication
2. Team workspaces
3. SSO available
4. Role-based access

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Auth Failed | Invalid key | Check API key |
| Quota Exceeded | Word limit | Upgrade plan |
| Template Error | Not found | Verify template |
| Brand Error | Not configured | Set up brand |

## Notes

- Marketing focused
- Brand voice AI
- 50+ templates
- Team collaboration
- API available
- Enterprise features

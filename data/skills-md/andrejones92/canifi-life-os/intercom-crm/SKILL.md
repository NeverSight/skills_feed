---
name: intercom-crm
description: Manage customer messaging and support with Intercom's conversational platform.
category: business
---
# Intercom Skill

Manage customer messaging and support with Intercom's conversational platform.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/intercom-crm/install.sh | bash
```

Or manually:
```bash
cp -r skills/intercom-crm ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set INTERCOM_ACCESS_TOKEN "your_access_token"
canifi-env set INTERCOM_APP_ID "your_app_id"
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

1. **Conversation Management**: Handle live chat and messenger conversations
2. **User Management**: Track and segment users with custom attributes
3. **Automated Messages**: Create targeted in-app messages and bots
4. **Help Center**: Manage knowledge base articles and collections
5. **Product Tours**: Create and manage onboarding product tours

## Usage Examples

### Reply to Conversation
```
User: "Reply to the latest Intercom conversation from John"
Assistant: Sends reply in active conversation
```

### Create User
```
User: "Add a new user to Intercom with email sarah@company.com"
Assistant: Creates user with provided details
```

### Send Message
```
User: "Send an in-app message to users who signed up this week"
Assistant: Creates targeted message campaign
```

### Search Users
```
User: "Find all Intercom users on the enterprise plan"
Assistant: Searches users by segment criteria
```

## Authentication Flow

1. Create app in Intercom Developer Hub
2. Get access token from app settings
3. Use Bearer token for API requests
4. OAuth available for published apps

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| 401 Unauthorized | Invalid token | Verify access token |
| 403 Forbidden | Scope not available | Check app permissions |
| 404 Not Found | Resource not found | Verify ID |
| 429 Rate Limited | Too many requests | Implement backoff |

## Notes

- Combines messaging, bots, and help desk
- Resolution bot for automated support
- Series for visual automation builder
- Product tours for onboarding
- Custom bots with Fin AI
- API rate limit varies by plan

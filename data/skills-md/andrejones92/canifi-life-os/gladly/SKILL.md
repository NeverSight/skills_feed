---
name: gladly
description: Manage customer service with Gladly's people-centered support platform.
category: business
---
# Gladly Skill

Manage customer service with Gladly's people-centered support platform.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/gladly/install.sh | bash
```

Or manually:
```bash
cp -r skills/gladly ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set GLADLY_API_TOKEN "your_api_token"
canifi-env set GLADLY_ORGANIZATION "your_organization"
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

1. **Customer Timeline**: View complete customer history in single view
2. **Omnichannel Support**: Handle voice, email, chat, SMS, and social
3. **Task Management**: Create and manage follow-up tasks
4. **Knowledge Management**: Access and share help content
5. **Workforce Management**: Manage agent schedules and capacity

## Usage Examples

### View Customer
```
User: "Show me the Gladly timeline for john@customer.com"
Assistant: Returns complete customer interaction history
```

### Create Conversation
```
User: "Start a new conversation with customer about order issue"
Assistant: Creates conversation with customer context
```

### Add Task
```
User: "Create a follow-up task for the VIP customer inquiry"
Assistant: Creates task linked to conversation
```

### Search Customers
```
User: "Find all Gladly customers with VIP status"
Assistant: Searches and returns matching customers
```

## Authentication Flow

1. Get API token from Gladly admin settings
2. Use Basic Auth with token
3. Organization-specific endpoints
4. SSO available for agents

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| 401 Unauthorized | Invalid token | Verify API token |
| 403 Forbidden | Insufficient permissions | Check admin access |
| 404 Not Found | Customer not found | Verify customer ID |
| 429 Rate Limited | Too many requests | Implement backoff |

## Notes

- People-centered, not ticket-centered
- Single customer timeline view
- Voice support built-in
- AI-powered agent assist
- Hero (agent) empowerment focus
- Enterprise-grade platform

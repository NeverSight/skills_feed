---
name: kayako
description: Manage customer support with Kayako's unified help desk platform.
category: travel
---
# Kayako Skill

Manage customer support with Kayako's unified help desk platform.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/kayako/install.sh | bash
```

Or manually:
```bash
cp -r skills/kayako ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set KAYAKO_SUBDOMAIN "your_subdomain"
canifi-env set KAYAKO_EMAIL "your_email"
canifi-env set KAYAKO_API_KEY "your_api_key"
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

1. **Case Management**: Create and manage support cases across channels
2. **Journey Tracking**: View complete customer journey and interactions
3. **Live Chat**: Handle real-time chat conversations
4. **Help Center**: Manage self-service knowledge base
5. **Automation**: Set up SLA rules and automated workflows

## Usage Examples

### Create Case
```
User: "Create a new Kayako case for billing question"
Assistant: Creates support case with category
```

### View Journey
```
User: "Show me the customer journey for john@company.com"
Assistant: Returns complete interaction history
```

### Update Case
```
User: "Assign case #1234 to the technical team"
Assistant: Updates case assignment
```

### Search Knowledge Base
```
User: "Find Kayako articles about account setup"
Assistant: Searches help center for matches
```

## Authentication Flow

1. Get API credentials from Kayako admin
2. Use HTTP Basic Auth with email:key
3. Subdomain-specific API endpoints
4. Session-based auth available

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| 401 Unauthorized | Invalid credentials | Verify email and API key |
| 403 Forbidden | Insufficient permissions | Check agent role |
| 404 Not Found | Case not found | Verify case ID |
| 429 Rate Limited | Too many requests | Wait and retry |

## Notes

- Unified support experience across channels
- Customer journey visualization
- Collaborative inbox features
- SLA management built-in
- Self-service portal included
- Real-time chat support

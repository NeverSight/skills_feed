---
name: groove
description: Manage customer support with Groove's simple shared inbox for small teams.
category: business
---
# Groove Skill

Manage customer support with Groove's simple shared inbox for small teams.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/groove/install.sh | bash
```

Or manually:
```bash
cp -r skills/groove ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set GROOVE_ACCESS_TOKEN "your_access_token"
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

1. **Shared Inbox**: Manage team email with collaborative features
2. **Ticket Assignment**: Assign and track ticket ownership
3. **Canned Replies**: Use and manage saved responses
4. **Knowledge Base**: Create and maintain help articles
5. **Reporting**: Access basic support metrics and reports

## Usage Examples

### View Inbox
```
User: "Show me unassigned Groove tickets"
Assistant: Returns unassigned inbox items
```

### Reply to Ticket
```
User: "Reply to the latest Groove ticket with shipping update"
Assistant: Sends reply in ticket thread
```

### Create Article
```
User: "Create a help article about password resets"
Assistant: Creates knowledge base article
```

### Check Metrics
```
User: "Show me this week's Groove support metrics"
Assistant: Returns ticket volume and response time
```

## Authentication Flow

1. Get access token from Groove settings
2. Use Bearer token for API requests
3. OAuth 2.0 for integrations
4. Single token provides access

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| 401 Unauthorized | Invalid token | Verify access token |
| 403 Forbidden | Feature not available | Check plan |
| 404 Not Found | Ticket not found | Verify ticket ID |
| 429 Rate Limited | Too many requests | Implement backoff |

## Notes

- Simple help desk for small teams
- Focus on ease of use
- Knowledge base included
- Basic reporting features
- Affordable pricing for startups
- Gmail-like interface

---
name: fullstory
description: Understand user experience with FullStory's digital experience intelligence platform.
category: analytics
---
# FullStory Skill

Understand user experience with FullStory's digital experience intelligence platform.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/fullstory/install.sh | bash
```

Or manually:
```bash
cp -r skills/fullstory ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set FULLSTORY_API_KEY "your_api_key"
canifi-env set FULLSTORY_ORG_ID "your_org_id"
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

1. **Session Replay**: Watch pixel-perfect session recordings
2. **Heatmaps**: View click and scroll heatmaps
3. **Funnels**: Analyze conversion paths
4. **Error Tracking**: Capture and analyze errors
5. **User Frustration**: Detect rage clicks and frustration signals

## Usage Examples

### Find Sessions
```
User: "Find sessions with rage clicks on the checkout page"
Assistant: Returns sessions matching frustration signals
```

### View Errors
```
User: "Show me JavaScript errors from today"
Assistant: Returns error list with session links
```

### Analyze Funnel
```
User: "What's the conversion rate for the signup funnel?"
Assistant: Returns funnel conversion analysis
```

### User Search
```
User: "Find all sessions for user john@company.com"
Assistant: Returns user's session history
```

## Authentication Flow

1. Get API key from FullStory settings
2. Note your org ID
3. Use API key for authentication
4. Org ID in API URL

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| 401 Unauthorized | Invalid API key | Verify credentials |
| 403 Forbidden | No access | Check org permissions |
| 404 Not Found | Session not found | Verify session ID |
| 429 Rate Limited | Too many requests | Wait and retry |

## Notes

- Digital experience intelligence
- Pixel-perfect session replay
- Frustration scoring
- Privacy controls built-in
- Integration with many tools
- Free trial available

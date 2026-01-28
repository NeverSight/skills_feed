---
name: hotjar
description: Understand user behavior with Hotjar's heatmaps, recordings, and feedback tools.
category: analytics
---
# Hotjar Skill

Understand user behavior with Hotjar's heatmaps, recordings, and feedback tools.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/hotjar/install.sh | bash
```

Or manually:
```bash
cp -r skills/hotjar ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set HOTJAR_API_KEY "your_api_key"
canifi-env set HOTJAR_SITE_ID "your_site_id"
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

1. **Heatmaps**: View click, scroll, and move heatmaps
2. **Session Recordings**: Watch user session recordings
3. **Surveys**: Create and manage on-site surveys
4. **Feedback Widgets**: Collect visual feedback from users
5. **Funnels**: Analyze conversion funnels

## Usage Examples

### View Heatmap
```
User: "Show me the heatmap for the homepage"
Assistant: Returns heatmap data for specified page
```

### Get Recordings
```
User: "Show me recent session recordings"
Assistant: Returns list of user session recordings
```

### Survey Results
```
User: "What are the survey results from this week?"
Assistant: Returns survey responses and analytics
```

### Feedback Analysis
```
User: "Show me recent user feedback"
Assistant: Returns feedback widget submissions
```

## Authentication Flow

1. Get API key from Hotjar account settings
2. Note your site ID from settings
3. Use API key for authentication
4. Site ID scopes data access

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| 401 Unauthorized | Invalid API key | Verify API key |
| 403 Forbidden | Feature not available | Check plan |
| 404 Not Found | Site not found | Verify site ID |
| 429 Rate Limited | Too many requests | Wait and retry |

## Notes

- Heatmaps and recordings core features
- GDPR compliant with consent tools
- Free tier available
- Real-time data collection
- Integration with many tools
- Mobile app recordings available

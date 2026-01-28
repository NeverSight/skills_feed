---
name: google-search-console
description: Monitor and optimize search performance with Google Search Console.
category: analytics
---
# Google Search Console Skill

Monitor and optimize search performance with Google Search Console.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/google-search-console/install.sh | bash
```

Or manually:
```bash
cp -r skills/google-search-console ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set GOOGLE_CLIENT_ID "your_client_id"
canifi-env set GOOGLE_CLIENT_SECRET "your_client_secret"
canifi-env set GOOGLE_REFRESH_TOKEN "your_refresh_token"
canifi-env set GSC_SITE_URL "your_site_url"
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

1. **Performance Analysis**: Track search impressions, clicks, and positions
2. **Index Coverage**: Monitor indexing status and errors
3. **URL Inspection**: Check specific URL indexing and crawl status
4. **Sitemap Management**: Submit and monitor sitemaps
5. **Mobile Usability**: Check mobile-friendly issues

## Usage Examples

### Get Search Performance
```
User: "Show me search performance for the last 28 days"
Assistant: Returns clicks, impressions, CTR, and position
```

### Check Top Queries
```
User: "What are my top search queries?"
Assistant: Returns top queries by clicks and impressions
```

### Index Status
```
User: "Are there any indexing issues?"
Assistant: Returns index coverage report
```

### Inspect URL
```
User: "Is this page indexed by Google?"
Assistant: Returns indexing status for URL
```

## Authentication Flow

1. Create project in Google Cloud Console
2. Enable Search Console API
3. Set up OAuth 2.0 credentials
4. Verify site ownership in Search Console

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| 401 Unauthorized | Token expired | Refresh access token |
| 403 Forbidden | No site access | Verify site ownership |
| 404 Not Found | Site not found | Check site URL |
| 429 Rate Limited | Quota exceeded | Wait for quota reset |

## Notes

- Free tool from Google
- 16 months of historical data
- Core Web Vitals reporting
- Rich results reporting
- Manual actions visibility
- Integrates with Analytics

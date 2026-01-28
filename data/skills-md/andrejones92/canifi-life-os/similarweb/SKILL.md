---
name: similarweb
description: Analyze website traffic and competitive intelligence with SimilarWeb.
category: marketing
---
# SimilarWeb Skill

Analyze website traffic and competitive intelligence with SimilarWeb.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/similarweb/install.sh | bash
```

Or manually:
```bash
cp -r skills/similarweb ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set SIMILARWEB_API_KEY "your_api_key"
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

1. **Traffic Analysis**: Estimate website traffic and sources
2. **Audience Insights**: Understand audience demographics
3. **Competitive Benchmarking**: Compare against competitors
4. **Industry Analysis**: Analyze market and industry trends
5. **Keyword Analysis**: Discover organic and paid keywords

## Usage Examples

### Get Traffic
```
User: "How much traffic does competitor.com get?"
Assistant: Returns estimated monthly visits and sources
```

### Compare Sites
```
User: "Compare our traffic to competitors"
Assistant: Returns comparative analysis
```

### Analyze Audience
```
User: "What's the audience profile for techsite.com?"
Assistant: Returns demographic and interest data
```

### Find Keywords
```
User: "What keywords drive traffic to competitor.com?"
Assistant: Returns top organic and paid keywords
```

## Authentication Flow

1. Get API key from SimilarWeb account
2. Use API key in request header
3. Credits consumed per request
4. Different endpoints for different data

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| 401 Unauthorized | Invalid API key | Verify credentials |
| 403 Forbidden | No credits | Purchase more credits |
| 404 Not Found | No data available | Try larger site |
| 429 Rate Limited | Too many requests | Wait and retry |

## Notes

- Website traffic estimation
- Competitive intelligence
- Industry benchmarking
- Enterprise pricing
- Browser extension available
- Historical data access

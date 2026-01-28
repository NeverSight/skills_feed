---
name: spyfu
description: Research competitor keywords and PPC with SpyFu's competitive intelligence.
category: marketing
---
# SpyFu Skill

Research competitor keywords and PPC with SpyFu's competitive intelligence.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/spyfu/install.sh | bash
```

Or manually:
```bash
cp -r skills/spyfu ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set SPYFU_API_KEY "your_api_key"
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

1. **Keyword Research**: Research organic and paid keywords
2. **Competitor Analysis**: Spy on competitor strategies
3. **PPC Research**: Analyze competitor ad campaigns
4. **Domain Comparison**: Compare domains head-to-head
5. **Ranking History**: View historical ranking data

## Usage Examples

### Find Keywords
```
User: "What keywords does competitor.com rank for?"
Assistant: Returns organic keywords with positions
```

### PPC Analysis
```
User: "What are competitor.com's top paid keywords?"
Assistant: Returns paid keyword data
```

### Compare Domains
```
User: "Compare our SEO with competitor.com"
Assistant: Returns head-to-head comparison
```

### View History
```
User: "Show ranking history for 'marketing software'"
Assistant: Returns historical ranking data
```

## Authentication Flow

1. Get API key from SpyFu account
2. Use API key in request parameters
3. Credits consumed per request
4. Different plans have different limits

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| 401 Unauthorized | Invalid API key | Verify credentials |
| 403 Forbidden | No access | Check subscription |
| 404 Not Found | No data | Try different domain |
| 429 Rate Limited | Too many requests | Wait and retry |

## Notes

- Competitive keyword intelligence
- 13+ years of ranking data
- PPC competitor research
- Kombat tool for comparisons
- Affordable pricing
- Chrome extension available

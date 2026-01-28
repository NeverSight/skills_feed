---
name: zillow
description: Search homes and get real estate data with Zillow's property marketplace.
category: realestate
---
# Zillow Skill

Search homes and get real estate data with Zillow's property marketplace.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/zillow/install.sh | bash
```

Or manually:
```bash
cp -r skills/zillow ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set ZILLOW_API_KEY "your_api_key"
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

1. **Property Search**: Search homes for sale and rent by location
2. **Zestimate**: Get Zillow's estimated home values
3. **Property Details**: Access detailed property information
4. **Market Trends**: View local real estate market data
5. **Saved Homes**: Manage saved properties and searches

## Usage Examples

### Search Homes
```
User: "Find 3-bedroom homes for sale in Austin under $500K"
Assistant: Returns matching property listings
```

### Get Zestimate
```
User: "What's the Zestimate for 123 Main Street?"
Assistant: Returns property value estimate
```

### View Market
```
User: "Show me real estate trends in Denver"
Assistant: Returns market statistics
```

### Save Property
```
User: "Save this listing to my favorites"
Assistant: Adds to saved homes
```

## Authentication Flow

1. Apply for Zillow API access
2. API access is limited/deprecated
3. Use browser automation for most features
4. Some data via Zillow Bridge API

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| 401 Unauthorized | Invalid API key | Verify credentials |
| 404 Not Found | Property not found | Check address |
| 429 Rate Limited | Too many requests | Wait and retry |
| API Deprecated | Feature removed | Use alternative |

## Notes

- Leading real estate marketplace
- API access very limited
- Zestimate for value estimates
- Mortgage calculator included
- Agent finder available
- Mobile apps for search

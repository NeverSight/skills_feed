---
name: realtor-com
description: Search homes and connect with agents on the official Realtor.com platform.
category: realestate
---
# Realtor.com Skill

Search homes and connect with agents on the official Realtor.com platform.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/realtor-com/install.sh | bash
```

Or manually:
```bash
cp -r skills/realtor-com ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set REALTOR_EMAIL "your_email"
canifi-env set REALTOR_PASSWORD "your_password"
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

1. **Property Search**: Search MLS listings for homes
2. **Agent Finder**: Find and connect with local agents
3. **Property Details**: View detailed property information
4. **Neighborhood Data**: Access neighborhood statistics
5. **Market Reports**: View local market reports

## Usage Examples

### Search Listings
```
User: "Find condos in Miami under $400K"
Assistant: Returns matching listings
```

### Find Agent
```
User: "Find top-rated agents in Chicago"
Assistant: Returns agent recommendations
```

### View Details
```
User: "Show me details for this listing"
Assistant: Returns full property details
```

### Neighborhood Info
```
User: "What's the crime rate in this neighborhood?"
Assistant: Returns neighborhood statistics
```

## Authentication Flow

1. Uses account authentication
2. No official public API
3. Browser automation required
4. Session-based access

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Login Failed | Invalid credentials | Verify account |
| Not Found | Listing removed | Check listing status |
| Session Expired | Timeout | Re-authenticate |
| Rate Limited | Too many requests | Wait |

## Notes

- Official NAR website
- MLS data integration
- Agent connections
- Mortgage tools
- No public API
- Mobile apps available

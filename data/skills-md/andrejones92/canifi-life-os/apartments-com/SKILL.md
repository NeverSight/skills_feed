---
name: apartments-com
description: Search rental apartments with Apartments.com's listing platform.
category: realestate
---
# Apartments.com Skill

Search rental apartments with Apartments.com's listing platform.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/apartments-com/install.sh | bash
```

Or manually:
```bash
cp -r skills/apartments-com ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set APARTMENTS_EMAIL "your_email"
canifi-env set APARTMENTS_PASSWORD "your_password"
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

1. **Apartment Search**: Search rental listings by location and amenities
2. **Virtual Tours**: View virtual apartment tours
3. **Apply Online**: Submit rental applications
4. **Price Comparisons**: Compare rental prices in area
5. **Saved Searches**: Save search criteria and favorites

## Usage Examples

### Search Rentals
```
User: "Find 2-bedroom apartments in Boston under $2500"
Assistant: Returns matching rental listings
```

### View Virtual Tour
```
User: "Show me the virtual tour for this apartment"
Assistant: Opens virtual tour
```

### Save Listing
```
User: "Save this apartment to my favorites"
Assistant: Saves listing
```

### Compare Prices
```
User: "Compare rental prices in this neighborhood"
Assistant: Returns price comparison data
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
| Listing Gone | Unit rented | Search for alternatives |
| Session Expired | Timeout | Re-authenticate |
| Application Error | Form issue | Retry submission |

## Notes

- CoStar Group owned
- Rental-focused platform
- Virtual tours available
- Application portal
- No public API
- Mobile apps available

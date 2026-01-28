---
name: carvana
description: Buy and sell cars online with home delivery.
category: automotive
---
# Carvana Skill

Buy and sell cars online with home delivery.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/carvana/install.sh | bash
```

Or manually:
```bash
cp -r skills/carvana ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set CARVANA_EMAIL "your_email"
canifi-env set CARVANA_PASSWORD "your_password"
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

1. **Search Inventory**: Browse available vehicles
2. **Get Offer**: Instant offer for your car
3. **Schedule Delivery**: Arrange vehicle delivery
4. **Financing**: Explore financing options
5. **Trade-In**: Trade your current vehicle

## Usage Examples

### Search Cars
```
User: "Find SUVs under $30,000 on Carvana"
Assistant: Returns matching vehicles
```

### Get Trade Offer
```
User: "Get an offer for my 2019 Honda Accord"
Assistant: Returns instant offer
```

### Schedule Delivery
```
User: "Schedule delivery for my Carvana purchase"
Assistant: Opens delivery scheduling
```

### Check Financing
```
User: "What financing rates does Carvana offer?"
Assistant: Returns financing options
```

## Authentication Flow

1. Account-based authentication
2. No official API
3. Browser automation required
4. Financing requires credit check

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Login Failed | Invalid credentials | Check account |
| Vehicle Sold | No longer available | Search alternatives |
| Delivery Error | Location issue | Verify address |
| Financing Denied | Credit issue | Review terms |

## Notes

- Online car buying
- 7-day return policy
- Home delivery
- No public API
- Vending machine pickups
- Financing available

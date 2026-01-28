---
name: goodrx
description: Compare drug prices with GoodRx - find medication discounts, compare pharmacy prices, and access coupons
category: healthcare
---

# GoodRx Skill

## Overview
Enables Claude to use GoodRx for medication price comparison including finding discounts, comparing pharmacy prices, and accessing savings coupons.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/goodrx/install.sh | bash
```

Or manually:
```bash
cp -r skills/goodrx ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set GOODRX_EMAIL "your-email@example.com"
canifi-env set GOODRX_PASSWORD "your-password"
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
- Search medication prices
- Compare pharmacy prices
- Access discount coupons
- View price history
- Find nearby pharmacies
- Check generic alternatives

## Usage Examples

### Example 1: Compare Prices
```
User: "What's the cheapest price for my prescription?"
Claude: I'll compare medication prices.
1. Opening GoodRx via Playwright MCP
2. Searching for your medication
3. Viewing prices by pharmacy
4. Finding lowest price
5. Providing coupon info
```

### Example 2: Find Generic Options
```
User: "Is there a generic version that costs less?"
Claude: I'll check for generics.
1. Searching medication
2. Viewing generic alternatives
3. Comparing prices
4. Recommending best value
```

### Example 3: Find Nearby Pharmacy
```
User: "Which pharmacy near me has the best price?"
Claude: I'll check nearby pharmacies.
1. Searching medication
2. Viewing nearby pharmacies
3. Comparing local prices
4. Showing address and price
```

## Authentication Flow
1. Navigate to goodrx.com via Playwright MCP
2. Click "Sign in" and enter email
3. Enter password
4. Handle 2FA if required (via iMessage)
5. Maintain session for saved medications

## Error Handling
- **Login Failed**: Retry up to 3 times, notify via iMessage
- **Session Expired**: Re-authenticate automatically
- **Rate Limited**: Implement exponential backoff
- **2FA Required**: Send iMessage notification
- **Medication Not Found**: Suggest spelling alternatives
- **No Price Data**: Note limited availability

## Self-Improvement Instructions
When GoodRx updates:
1. Document new savings features
2. Update pharmacy network changes
3. Track coupon system updates
4. Log telehealth additions

## Notes
- Free coupons available
- Gold membership for better prices
- Telehealth services available
- Works at most pharmacies
- Not insurance replacement

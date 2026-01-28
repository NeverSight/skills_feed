---
name: ulta
description: Enables Claude to browse Ulta beauty products, manage lists, and track orders
version: 1.0.0
author: Canifi
category: ecommerce
---

# Ulta Skill

## Overview
Automates Ulta Beauty operations including beauty product search, favorites management, and order tracking through browser automation. Note: Actual purchases are not automated.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/ulta/install.sh | bash
```

Or manually:
```bash
cp -r skills/ulta ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set ULTA_EMAIL "your-email@example.com"
canifi-env set ULTA_PASSWORD "your-password"
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
- Search beauty and salon products
- Add items to favorites
- Track order status
- Access Ultamate Rewards
- Find sales and deals
- Check store availability
- View product reviews
- Browse by brand

## Usage Examples

### Example 1: Search Products
```
User: "Find drugstore mascara at Ulta"
Claude: I'll search for mascara.
- Navigate to ulta.com
- Search "mascara"
- Filter by drugstore brands
- Sort by rating
- Present top options
```

### Example 2: Check Points
```
User: "How many Ultamate Rewards points do I have?"
Claude: I'll check your points.
- Navigate to account
- View rewards status
- Check points balance
- Report redemption options
```

### Example 3: Find Sales
```
User: "What's on sale at Ulta this week?"
Claude: I'll check current sales.
- Navigate to sale section
- Browse weekly offers
- Note significant discounts
- Present best deals
```

### Example 4: Track Order
```
User: "Track my Ulta order"
Claude: I'll check your order.
- Navigate to Order History
- Find recent order
- Check shipping status
- Report delivery info
```

## Authentication Flow
1. Navigate to ulta.com via Playwright MCP
2. Click Sign In
3. Enter email from canifi-env
4. Enter password
5. Handle 2FA if enabled (notify user via iMessage)
6. Verify account access
7. Maintain session cookies

## Error Handling
- **Login Failed**: Clear cookies, verify credentials
- **Session Expired**: Re-authenticate automatically
- **2FA Required**: iMessage for verification code
- **Out of Stock**: Check store availability
- **Points Error**: Verify account status
- **Order Not Found**: Check order number
- **Store Not Found**: Verify zip code
- **Favorites Full**: Check limits

## Self-Improvement Instructions
When encountering new Ulta features:
1. Document new UI elements
2. Add support for new features
3. Log successful patterns
4. Update for Ulta changes

## Notes
- Ultamate Rewards program
- Points multiplier events
- Both prestige and drugstore brands
- Salon services in-store
- GWP (gift with purchase) offers
- 21 Days of Beauty sale event
- Credit card for extra points

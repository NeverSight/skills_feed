---
name: macys
description: Enables Claude to browse Macy's products, manage lists, and track orders
version: 1.0.0
author: Canifi
category: ecommerce
---

# Macy's Skill

## Overview
Automates Macy's operations including fashion and home product search, list management, and order tracking through browser automation. Note: Actual purchases are not automated.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/macys/install.sh | bash
```

Or manually:
```bash
cp -r skills/macys ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set MACYS_EMAIL "your-email@example.com"
canifi-env set MACYS_PASSWORD "your-password"
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
- Search fashion and home products
- Add items to wishlist
- Track order status
- Find sale and clearance items
- Check store availability
- View Star Rewards
- Manage shopping lists
- Browse by department

## Usage Examples

### Example 1: Search Products
```
User: "Find men's dress shirts on sale at Macy's"
Claude: I'll search for dress shirts.
- Navigate to macys.com
- Search "men's dress shirts"
- Filter by sale items
- Sort by discount
- Present top options
```

### Example 2: Check Clearance
```
User: "What's in Macy's clearance for women's shoes?"
Claude: I'll browse clearance.
- Navigate to women's shoes
- Filter by clearance
- Browse discounted items
- Present best deals
```

### Example 3: Track Order
```
User: "Track my Macy's order"
Claude: I'll check your order.
- Navigate to Order Status
- Find recent order
- Check shipping info
- Report delivery estimate
```

### Example 4: Check Store Pickup
```
User: "Can I pick this up at my local Macy's?"
Claude: I'll check store availability.
- Navigate to product page
- Check store pickup options
- View local store inventory
- Report availability
```

## Authentication Flow
1. Navigate to macys.com via Playwright MCP
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
- **Out of Stock**: Check other sizes/colors
- **Store Not Found**: Verify zip code
- **Order Not Found**: Check order number
- **Sale Ended**: Price may have changed
- **Rewards Error**: Check account status

## Self-Improvement Instructions
When encountering new Macy's features:
1. Document new UI elements
2. Add support for new features
3. Log successful patterns
4. Update for Macy's changes

## Notes
- Star Rewards loyalty program
- Macy's Card for extra savings
- Free shipping thresholds
- In-store pickup available
- Price adjustments within 10 days
- Designer brands available
- Wedding registry service

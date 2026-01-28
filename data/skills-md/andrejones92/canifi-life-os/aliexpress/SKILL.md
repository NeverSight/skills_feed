---
name: aliexpress
description: Enables Claude to browse AliExpress products, manage wishlist, and track orders
version: 1.0.0
author: Canifi
category: ecommerce
---

# AliExpress Skill

## Overview
Automates AliExpress operations including product search, seller research, wishlist management, and order tracking through browser automation. Note: Actual purchases are not automated.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/aliexpress/install.sh | bash
```

Or manually:
```bash
cp -r skills/aliexpress ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set ALIEXPRESS_EMAIL "your-email@example.com"
canifi-env set ALIEXPRESS_PASSWORD "your-password"
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
- Search global products
- Add items to wishlist
- Track order shipping
- Compare seller ratings
- Find deals and coupons
- View order history
- Check shipping estimates
- Read buyer reviews

## Usage Examples

### Example 1: Search Products
```
User: "Find phone cases on AliExpress with free shipping"
Claude: I'll search for phone cases.
- Navigate to aliexpress.com
- Search "phone case"
- Filter by free shipping
- Sort by orders or rating
- Present top options
```

### Example 2: Check Seller
```
User: "Is this AliExpress seller reliable?"
Claude: I'll research the seller.
- Navigate to seller's store
- Check store rating
- Review feedback percentage
- Note store age and transactions
```

### Example 3: Track Order
```
User: "Where is my AliExpress package?"
Claude: I'll track your order.
- Navigate to My Orders
- Find the order
- Check shipping status
- Report location and estimate
```

### Example 4: Find Deals
```
User: "What deals are available on AliExpress today?"
Claude: I'll find today's deals.
- Navigate to deals section
- Browse flash deals
- List notable discounts
- Note time remaining
```

## Authentication Flow
1. Navigate to aliexpress.com via Playwright MCP
2. Click Sign In
3. Enter email from canifi-env
4. Enter password
5. Handle CAPTCHA if shown (notify user)
6. Handle 2FA if enabled
7. Verify account access
8. Maintain session cookies

## Error Handling
- **Login Failed**: Clear cookies, try different login method
- **Session Expired**: Re-authenticate automatically
- **CAPTCHA Required**: Notify user to complete
- **Seller Not Found**: Search by store name
- **Order Not Found**: Check order number format
- **Tracking Unavailable**: May take time after shipping
- **Item Unavailable**: Check similar listings
- **Shipping Estimate Error**: Verify destination

## Self-Improvement Instructions
When encountering new AliExpress features:
1. Document new UI elements
2. Add support for new features
3. Log successful patterns
4. Update for platform changes

## Notes
- Shipping times vary significantly
- Buyer protection available
- Coins and coupons for savings
- Choice listings have faster shipping
- Store ratings indicate reliability
- Dispute process for issues
- Super Deals for best prices

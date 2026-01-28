---
name: amazon
description: Enables Claude to browse Amazon products, manage wishlists, and track orders (no purchases)
version: 1.0.0
author: Canifi
category: ecommerce
---

# Amazon Skill

## Overview
Automates Amazon shopping operations including product search, wishlist management, order tracking, and price monitoring through browser automation. Note: Actual purchases are not automated for security.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/amazon/install.sh | bash
```

Or manually:
```bash
cp -r skills/amazon ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set AMAZON_EMAIL "your-email@example.com"
canifi-env set AMAZON_PASSWORD "your-password"
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
- Search and browse products
- Add items to wishlist
- Track order status
- View order history
- Compare prices and products
- Read and filter reviews
- Manage shopping lists
- Check deal availability

## Usage Examples

### Example 1: Search Products
```
User: "Find wireless headphones on Amazon under $100"
Claude: I'll search for those headphones.
- Navigate to amazon.com
- Search "wireless headphones"
- Apply price filter under $100
- Sort by customer reviews
- Present top options
```

### Example 2: Add to Wishlist
```
User: "Add this product to my Amazon wishlist"
Claude: I'll add that to your wishlist.
- Navigate to product page
- Click "Add to List"
- Select wishlist
- Confirm added
```

### Example 3: Track Order
```
User: "Check the status of my recent Amazon order"
Claude: I'll check your order status.
- Navigate to Your Orders
- Find recent order
- Check shipping status
- Report delivery estimate
```

### Example 4: Compare Products
```
User: "Compare the top 3 laptop stands on Amazon"
Claude: I'll compare those products.
- Search laptop stands
- Select top 3 by reviews
- Compare prices, features, ratings
- Present comparison summary
```

## Authentication Flow
1. Navigate to amazon.com via Playwright MCP
2. Click Sign In
3. Enter email from canifi-env
4. Enter password
5. Handle 2FA/OTP if enabled (notify user via iMessage)
6. Complete CAPTCHA if shown (notify user)
7. Verify account access
8. Maintain session cookies

## Error Handling
- **Login Failed**: Clear cookies, verify credentials
- **Session Expired**: Re-authenticate automatically
- **2FA Required**: iMessage for OTP code
- **CAPTCHA Required**: Notify user to complete
- **Product Unavailable**: Check other sellers
- **Price Changed**: Note the change
- **Order Not Found**: Search by date range
- **Wishlist Error**: Check list permissions

## Self-Improvement Instructions
When encountering new Amazon features:
1. Document new UI elements
2. Add support for new product features
3. Log successful search patterns
4. Update for Amazon redesigns

## Notes
- Purchases not automated for security
- Prices fluctuate frequently
- Prime benefits require membership
- Subscribe & Save for recurring items
- Reviews can be filtered by verified
- Deal timers for lightning deals
- Multiple wishlists supported

---
name: zappos
description: Enables Claude to browse Zappos shoes and apparel, manage lists, and track orders
version: 1.0.0
author: Canifi
category: ecommerce
---

# Zappos Skill

## Overview
Automates Zappos operations including shoe and apparel search, favorites management, and order tracking through browser automation. Note: Actual purchases are not automated.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/zappos/install.sh | bash
```

Or manually:
```bash
cp -r skills/zappos ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set ZAPPOS_EMAIL "your-email@example.com"
canifi-env set ZAPPOS_PASSWORD "your-password"
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
- Search shoes and apparel
- Add items to favorites
- Track order status
- Filter by size and width
- Compare products
- Read detailed reviews
- Check VIP benefits
- View order history

## Usage Examples

### Example 1: Search Products
```
User: "Find running shoes on Zappos size 10"
Claude: I'll search for running shoes.
- Navigate to zappos.com
- Search "running shoes"
- Filter by size 10
- Sort by rating
- Present top options
```

### Example 2: Compare Products
```
User: "Compare these two pairs of boots"
Claude: I'll compare them.
- View both product pages
- Compare features and specs
- Note price differences
- Present comparison
```

### Example 3: Check Reviews
```
User: "What do reviews say about comfort for these shoes?"
Claude: I'll check the reviews.
- Navigate to product page
- Read customer reviews
- Focus on comfort mentions
- Summarize feedback
```

### Example 4: Track Order
```
User: "Track my Zappos order"
Claude: I'll check your order.
- Navigate to Order History
- Find recent order
- Check shipping status
- Report delivery info
```

## Authentication Flow
1. Navigate to zappos.com via Playwright MCP
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
- **Size Unavailable**: Check other widths
- **Out of Stock**: Notify for restock
- **Order Not Found**: Check order number
- **Favorites Full**: Check list limits
- **Filter Error**: Verify size format

## Self-Improvement Instructions
When encountering new Zappos features:
1. Document new UI elements
2. Add support for new features
3. Log successful patterns
4. Update for Zappos changes

## Notes
- Zappos is Amazon-owned
- Free shipping both ways
- 365-day return policy
- VIP program for faster shipping
- Width options available
- Customer service renowned
- Detailed size guides provided

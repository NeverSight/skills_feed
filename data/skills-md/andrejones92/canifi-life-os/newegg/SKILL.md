---
name: newegg
description: Enables Claude to browse Newegg tech products, manage lists, and track orders
version: 1.0.0
author: Canifi
category: ecommerce
---

# Newegg Skill

## Overview
Automates Newegg operations including tech product search, specification comparison, deal hunting, and order tracking through browser automation. Note: Actual purchases are not automated.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/newegg/install.sh | bash
```

Or manually:
```bash
cp -r skills/newegg ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set NEWEGG_EMAIL "your-email@example.com"
canifi-env set NEWEGG_PASSWORD "your-password"
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
- Search computer hardware and electronics
- Compare product specifications
- Track order status
- Find Shell Shocker deals
- Check combo deals
- View open box items
- Manage wishlist
- Read detailed reviews

## Usage Examples

### Example 1: Search Products
```
User: "Find RTX 4070 graphics cards on Newegg"
Claude: I'll search for those GPUs.
- Navigate to newegg.com
- Search "RTX 4070"
- Filter by availability
- Sort by price or rating
- Present options with specs
```

### Example 2: Compare Specs
```
User: "Compare these two motherboards"
Claude: I'll compare the specifications.
- Add items to compare
- View specification comparison
- Highlight key differences
- Present comparison summary
```

### Example 3: Check Shell Shocker
```
User: "What's today's Shell Shocker deal?"
Claude: I'll check the daily deal.
- Navigate to Shell Shocker section
- View current deal
- Note discount and availability
- Report time remaining
```

### Example 4: Track Order
```
User: "Track my Newegg order"
Claude: I'll check your order.
- Navigate to Order History
- Find recent order
- Check shipping status
- Report delivery estimate
```

## Authentication Flow
1. Navigate to newegg.com via Playwright MCP
2. Click Sign In
3. Enter email from canifi-env
4. Enter password
5. Handle 2FA/verification code
6. Complete CAPTCHA if shown (notify user)
7. Verify account access
8. Maintain session cookies

## Error Handling
- **Login Failed**: Clear cookies, verify credentials
- **Session Expired**: Re-authenticate automatically
- **2FA Required**: iMessage for verification code
- **CAPTCHA Required**: Notify user to complete
- **Out of Stock**: Check third-party sellers
- **Order Not Found**: Check order number
- **Combo Unavailable**: Components sold separately
- **Price Changed**: Deal may have ended

## Self-Improvement Instructions
When encountering new Newegg features:
1. Document new UI elements
2. Add support for new product types
3. Log successful patterns
4. Update for Newegg changes

## Notes
- Newegg specializes in computer hardware
- Shell Shocker is daily deal
- Combo deals for bundled savings
- Open Box for discounted returns
- Marketplace sellers included
- EggPoints reward program
- Reviews include technical details

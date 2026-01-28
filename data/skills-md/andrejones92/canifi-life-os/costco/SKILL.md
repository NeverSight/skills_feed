---
name: costco
description: Enables Claude to browse Costco products, manage lists, and track orders
version: 1.0.0
author: Canifi
category: ecommerce
---

# Costco Skill

## Overview
Automates Costco operations including bulk product search, warehouse availability, and order tracking through browser automation. Note: Membership required, purchases not automated.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/costco/install.sh | bash
```

Or manually:
```bash
cp -r skills/costco ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set COSTCO_EMAIL "your-email@example.com"
canifi-env set COSTCO_PASSWORD "your-password"
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
- Search products and bulk items
- Check warehouse availability
- Track online orders
- View instant savings
- Compare member prices
- Access order history
- Check in-warehouse prices
- Manage shopping list

## Usage Examples

### Example 1: Search Products
```
User: "Find organic snacks at Costco"
Claude: I'll search for organic snacks.
- Navigate to costco.com
- Search "organic snacks"
- Filter by available options
- Present bulk options with pricing
```

### Example 2: Check Warehouse Stock
```
User: "Is this available at my local Costco?"
Claude: I'll check warehouse availability.
- Navigate to product page
- Check in-warehouse availability
- Report local stock status
- Note member pricing
```

### Example 3: View Instant Savings
```
User: "What's on sale at Costco this month?"
Claude: I'll check instant savings.
- Navigate to Instant Savings
- Browse current deals
- List notable discounts
- Note expiration dates
```

### Example 4: Track Order
```
User: "Track my Costco delivery order"
Claude: I'll check your order.
- Navigate to Orders
- Find recent order
- Check delivery status
- Report tracking info
```

## Authentication Flow
1. Navigate to costco.com via Playwright MCP
2. Click Sign In
3. Enter email from canifi-env
4. Enter password
5. Handle 2FA if enabled (notify user via iMessage)
6. Verify membership access
7. Maintain session cookies

## Error Handling
- **Login Failed**: Verify membership status
- **Session Expired**: Re-authenticate automatically
- **2FA Required**: iMessage for verification code
- **Membership Required**: Some items need active membership
- **Out of Stock**: Check other warehouses
- **Order Not Found**: Check order number
- **Location Not Found**: Verify zip code
- **In-Store Only**: Some items not online

## Self-Improvement Instructions
When encountering new Costco features:
1. Document new UI elements
2. Add support for new features
3. Log successful patterns
4. Update for Costco changes

## Notes
- Costco requires paid membership
- Executive members get 2% back
- Kirkland is Costco's brand
- Same-day delivery available
- Gas prices for members
- Pharmacy and optical separate
- Business center has different items

---
name: sephora
description: Enables Claude to browse Sephora beauty products, manage lists, and track orders
version: 1.0.0
author: Canifi
category: ecommerce
---

# Sephora Skill

## Overview
Automates Sephora operations including beauty product search, favorites management, and order tracking through browser automation. Note: Actual purchases are not automated.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/sephora/install.sh | bash
```

Or manually:
```bash
cp -r skills/sephora ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set SEPHORA_EMAIL "your-email@example.com"
canifi-env set SEPHORA_PASSWORD "your-password"
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
- Search beauty and skincare products
- Add items to loves list
- Track order status
- Access Beauty Insider rewards
- Find value sets
- Check store availability
- View product reviews
- Browse by brand

## Usage Examples

### Example 1: Search Products
```
User: "Find vitamin C serums at Sephora"
Claude: I'll search for vitamin C serums.
- Navigate to sephora.com
- Search "vitamin C serum"
- Filter by skin concern
- Sort by rating
- Present top options
```

### Example 2: Check Rewards
```
User: "How many Beauty Insider points do I have?"
Claude: I'll check your points.
- Navigate to account
- View Beauty Insider status
- Check points balance
- Report available rewards
```

### Example 3: Find Value Sets
```
User: "Show me Sephora value sets for skincare"
Claude: I'll find value sets.
- Navigate to value sets
- Filter by skincare
- Browse available bundles
- Present savings options
```

### Example 4: Track Order
```
User: "Track my Sephora order"
Claude: I'll check your order.
- Navigate to Orders
- Find recent order
- Check shipping status
- Report delivery info
```

## Authentication Flow
1. Navigate to sephora.com via Playwright MCP
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
- **Loves List Full**: Check limits

## Self-Improvement Instructions
When encountering new Sephora features:
1. Document new UI elements
2. Add support for new features
3. Log successful patterns
4. Update for Sephora changes

## Notes
- Beauty Insider loyalty program
- Rouge status for top spenders
- Free samples with orders
- Clean at Sephora for clean beauty
- In-store services available
- Free returns within 60 days
- Birthday gifts for members

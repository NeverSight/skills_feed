---
name: shipt
description: Enables Claude to browse stores, manage lists, and track deliveries on Shipt
version: 1.0.0
author: Canifi
category: food
---

# Shipt Skill

## Overview
Automates Shipt operations including store browsing, list management, and delivery tracking through browser automation. Note: Actual orders are not automated for security.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/shipt/install.sh | bash
```

Or manually:
```bash
cp -r skills/shipt ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set SHIPT_EMAIL "your-email@example.com"
canifi-env set SHIPT_PASSWORD "your-password"
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
- Browse partner stores
- Search for products
- Manage shopping lists
- Track active deliveries
- View order history
- Check membership benefits
- Schedule delivery windows
- Compare store prices

## Usage Examples

### Example 1: Browse Stores
```
User: "What stores are on Shipt near me?"
Claude: I'll find available stores.
- Navigate to shipt.com
- View partner stores
- Check delivery availability
- Present store options
```

### Example 2: Search Products
```
User: "Find almond milk on Shipt"
Claude: I'll search for that.
- Search "almond milk"
- Show results from stores
- Compare prices
- Present options
```

### Example 3: Track Delivery
```
User: "Where is my Shipt order?"
Claude: I'll track your delivery.
- Navigate to orders
- Find active order
- Check shopper progress
- Report ETA
```

### Example 4: Manage List
```
User: "Add bread and eggs to my Shipt list"
Claude: I'll add those items.
- Navigate to lists
- Add bread
- Add eggs
- Confirm items added
```

## Authentication Flow
1. Navigate to shipt.com via Playwright MCP
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
- **Store Unavailable**: Check other stores
- **Item Out of Stock**: Note for substitution
- **Order Not Found**: Check order ID
- **No Delivery Window**: Try different times
- **Membership Issue**: Check subscription

## Self-Improvement Instructions
When encountering new Shipt features:
1. Document new UI elements
2. Add support for new stores
3. Log successful patterns
4. Update for Shipt changes

## Notes
- Owned by Target
- Orders not automated for security
- Membership for free delivery
- Personal shoppers
- Same-day delivery
- Target integration
- Tip shoppers directly

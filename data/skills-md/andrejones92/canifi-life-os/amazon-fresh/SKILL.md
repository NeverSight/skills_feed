---
name: amazon-fresh
description: Enables Claude to browse Amazon Fresh groceries, manage lists, and track deliveries
version: 1.0.0
author: Canifi
category: food
---

# Amazon Fresh Skill

## Overview
Automates Amazon Fresh operations including grocery browsing, list management, and delivery tracking through browser automation. Note: Actual orders are not automated for security.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/amazon-fresh/install.sh | bash
```

Or manually:
```bash
cp -r skills/amazon-fresh ~/.canifi/skills/
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
- Browse fresh groceries
- Search for products
- Manage shopping lists
- Track deliveries
- View order history
- Check Prime benefits
- Find deals and coupons
- Schedule delivery windows

## Usage Examples

### Example 1: Browse Groceries
```
User: "Show me produce on Amazon Fresh"
Claude: I'll browse produce.
- Navigate to amazon.com/fresh
- Go to produce section
- Browse available items
- Present fresh options
```

### Example 2: Search Products
```
User: "Find whole grain bread on Amazon Fresh"
Claude: I'll search for that.
- Search "whole grain bread"
- Filter by Fresh items
- Show available options
- Present with prices
```

### Example 3: Track Delivery
```
User: "Track my Amazon Fresh order"
Claude: I'll check your delivery.
- Navigate to Fresh orders
- Find active order
- Check delivery window
- Report status
```

### Example 4: Find Deals
```
User: "What's on sale at Amazon Fresh?"
Claude: I'll find Fresh deals.
- Navigate to Fresh deals
- Browse discounted items
- List notable savings
- Present best offers
```

## Authentication Flow
1. Navigate to amazon.com/fresh via Playwright MCP
2. Sign in with Amazon credentials
3. Enter email from canifi-env
4. Enter password
5. Handle 2FA/OTP if enabled (notify user via iMessage)
6. Verify Fresh access
7. Maintain session cookies

## Error Handling
- **Login Failed**: Clear cookies, verify credentials
- **Session Expired**: Re-authenticate automatically
- **2FA Required**: iMessage for verification code
- **Not Prime Member**: Some features require Prime
- **Item Unavailable**: Check availability
- **Delivery Window Full**: Suggest alternatives
- **Address Not Eligible**: Check Fresh availability
- **Order Not Found**: Check order ID

## Self-Improvement Instructions
When encountering new Amazon Fresh features:
1. Document new UI elements
2. Add support for new categories
3. Log successful patterns
4. Update for Amazon changes

## Notes
- Orders not automated for security
- Prime membership recommended
- Same-day delivery available
- Whole Foods integration
- EBT SNAP accepted
- Delivery windows book fast
- Substitution options available

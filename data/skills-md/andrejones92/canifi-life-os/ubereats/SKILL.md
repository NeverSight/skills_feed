---
name: ubereats
description: Enables Claude to browse restaurants, manage orders, and track deliveries on Uber Eats
version: 1.0.0
author: Canifi
category: food
---

# Uber Eats Skill

## Overview
Automates Uber Eats operations including restaurant browsing, order tracking, and favorites management through browser automation. Note: Actual orders are not automated for security.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/ubereats/install.sh | bash
```

Or manually:
```bash
cp -r skills/ubereats ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set UBEREATS_EMAIL "your-email@example.com"
canifi-env set UBEREATS_PASSWORD "your-password"
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
- Browse restaurants and menus
- Search for cuisines and dishes
- Track active orders
- View order history
- Manage favorite restaurants
- Check delivery estimates
- View promotions and deals
- Manage dietary preferences

## Usage Examples

### Example 1: Browse Restaurants
```
User: "Find Thai restaurants near me on Uber Eats"
Claude: I'll find Thai restaurants.
- Navigate to ubereats.com
- Search "Thai"
- Filter by open now
- Sort by rating or delivery time
- Present top options
```

### Example 2: Check Menu
```
User: "Show me the menu at Chipotle on Uber Eats"
Claude: I'll check their menu.
- Search for Chipotle
- Open restaurant page
- Browse menu categories
- Present popular items
```

### Example 3: Track Order
```
User: "Where is my Uber Eats order?"
Claude: I'll track your order.
- Navigate to Orders
- Find active order
- Check driver location
- Report ETA
```

### Example 4: Find Deals
```
User: "What promotions are on Uber Eats today?"
Claude: I'll find current deals.
- Navigate to deals section
- Browse promotions
- List discount offers
- Note promo codes
```

## Authentication Flow
1. Navigate to ubereats.com via Playwright MCP
2. Click Sign In
3. Enter email from canifi-env
4. Enter password or OTP
5. Handle 2FA if enabled (notify user via iMessage)
6. Verify account access
7. Maintain session cookies

## Error Handling
- **Login Failed**: Clear cookies, verify credentials
- **Session Expired**: Re-authenticate automatically
- **2FA Required**: iMessage for verification code
- **Restaurant Closed**: Note hours and suggest alternatives
- **No Delivery**: Address may be out of range
- **Order Not Found**: Check order ID
- **Menu Unavailable**: Try refreshing or check hours
- **Address Error**: Verify delivery address

## Self-Improvement Instructions
When encountering new Uber Eats features:
1. Document new UI elements
2. Add support for new features
3. Log successful patterns
4. Update for Uber Eats changes

## Notes
- Orders not automated for security
- Uber One membership for benefits
- Tipping is customary
- Delivery times are estimates
- Some items may be unavailable
- Surge pricing during peak hours
- Priority delivery available

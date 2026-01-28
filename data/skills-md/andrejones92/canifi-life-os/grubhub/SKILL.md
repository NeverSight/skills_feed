---
name: grubhub
description: Enables Claude to browse restaurants, manage orders, and track deliveries on Grubhub
version: 1.0.0
author: Canifi
category: food
---

# Grubhub Skill

## Overview
Automates Grubhub operations including restaurant browsing, order tracking, and perks management through browser automation. Note: Actual orders are not automated for security.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/grubhub/install.sh | bash
```

Or manually:
```bash
cp -r skills/grubhub ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set GRUBHUB_EMAIL "your-email@example.com"
canifi-env set GRUBHUB_PASSWORD "your-password"
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
- Search cuisines and dishes
- Track active orders
- View order history
- Manage saved restaurants
- Check Grubhub+ benefits
- Find deals and perks
- View pickup options

## Usage Examples

### Example 1: Browse Restaurants
```
User: "Find Indian restaurants on Grubhub"
Claude: I'll find Indian food.
- Navigate to grubhub.com
- Search "Indian"
- Filter by available
- Sort by rating
- Present top options
```

### Example 2: Check Perks
```
User: "What Grubhub perks do I have?"
Claude: I'll check your perks.
- Navigate to account perks
- View available offers
- List active deals
- Note expiration dates
```

### Example 3: Track Order
```
User: "Track my Grubhub order"
Claude: I'll track your delivery.
- Navigate to Order History
- Find active order
- Check delivery status
- Report ETA
```

### Example 4: Find Pickup
```
User: "Find restaurants with pickup near me"
Claude: I'll find pickup options.
- Filter by pickup
- Browse nearby restaurants
- Note pickup times
- Present options
```

## Authentication Flow
1. Navigate to grubhub.com via Playwright MCP
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
- **Restaurant Closed**: Note hours
- **No Delivery**: Check pickup option
- **Order Not Found**: Check order ID
- **Perks Expired**: Note expiration
- **Address Error**: Verify delivery address

## Self-Improvement Instructions
When encountering new Grubhub features:
1. Document new UI elements
2. Add support for new features
3. Log successful patterns
4. Update for Grubhub changes

## Notes
- Orders not automated for security
- Grubhub+ for free delivery
- Pickup option available
- Perks and rewards program
- Corporate accounts available
- Scheduled orders supported
- Part of Just Eat Takeaway

---
name: freshly
description: Enables Claude to browse Freshly prepared meals and manage subscriptions
version: 1.0.0
author: Canifi
category: food
---

# Freshly Skill

## Overview
Automates Freshly operations including prepared meal browsing, weekly selections, and subscription management through browser automation. Note: Actual orders are not automated for security.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/freshly/install.sh | bash
```

Or manually:
```bash
cp -r skills/freshly ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set FRESHLY_EMAIL "your-email@example.com"
canifi-env set FRESHLY_PASSWORD "your-password"
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
- Browse prepared meals
- View nutritional info
- Select weekly meals
- Track deliveries
- View order history
- Check meal plans
- Manage preferences
- Skip or pause weeks

## Usage Examples

### Example 1: Browse Meals
```
User: "What's on the Freshly menu?"
Claude: I'll check available meals.
- Navigate to freshly.com
- View meal options
- List by category
- Present with nutrition
```

### Example 2: Find Protein-Rich Meals
```
User: "Find high protein Freshly meals"
Claude: I'll find protein options.
- Browse menu
- Filter by protein content
- List high-protein meals
- Present macros
```

### Example 3: Track Delivery
```
User: "Where is my Freshly order?"
Claude: I'll track your delivery.
- Navigate to orders
- Find active order
- Check shipping status
- Report delivery date
```

### Example 4: Check Plan
```
User: "What's my Freshly subscription plan?"
Claude: I'll check your plan.
- Navigate to account
- View subscription details
- Check meals per week
- Present plan info
```

## Authentication Flow
1. Navigate to freshly.com via Playwright MCP
2. Click Log In
3. Enter email from canifi-env
4. Enter password
5. Handle 2FA if enabled (notify user via iMessage)
6. Verify account access
7. Maintain session cookies

## Error Handling
- **Login Failed**: Clear cookies, verify credentials
- **Session Expired**: Re-authenticate automatically
- **2FA Required**: iMessage for verification code
- **Selection Deadline**: Note cutoff
- **Meal Unavailable**: Check alternatives
- **Delivery Issue**: Check address
- **Subscription Paused**: Check status
- **Order Not Found**: Check order date

## Self-Improvement Instructions
When encountering new Freshly features:
1. Document new UI elements
2. Add support for new meal types
3. Log successful patterns
4. Update for Freshly changes

## Notes
- Pre-made meals, microwave to eat
- Orders not automated for security
- Owned by Nestle
- No cooking required
- Single-serve portions
- Weekly delivery
- Various plan sizes

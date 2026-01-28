---
name: hungryroot
description: Enables Claude to browse Hungryroot meal kits and manage subscriptions
version: 1.0.0
author: Canifi
category: food
---

# Hungryroot Skill

## Overview
Automates Hungryroot operations including meal browsing, box customization, and delivery management through browser automation. Note: Actual orders are not automated for security.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/hungryroot/install.sh | bash
```

Or manually:
```bash
cp -r skills/hungryroot ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set HUNGRYROOT_EMAIL "your-email@example.com"
canifi-env set HUNGRYROOT_PASSWORD "your-password"
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
- Browse available groceries and meals
- View weekly box selections
- Manage dietary preferences
- Track deliveries
- View order history
- Customize meal plans
- Check subscription status
- Find recipes

## Usage Examples

### Example 1: Browse Products
```
User: "What's available in my Hungryroot box this week?"
Claude: I'll check your selections.
- Navigate to hungryroot.com
- View current box
- List selected items
- Present options
```

### Example 2: Check Recipes
```
User: "Show me Hungryroot recipes for dinner"
Claude: I'll find dinner recipes.
- Navigate to recipes section
- Browse dinner ideas
- List meal options
- Present with ingredients
```

### Example 3: Track Delivery
```
User: "When is my Hungryroot delivery arriving?"
Claude: I'll check your delivery.
- Navigate to account
- Find delivery schedule
- Check tracking info
- Report delivery date
```

### Example 4: View Preferences
```
User: "What are my Hungryroot dietary settings?"
Claude: I'll check your preferences.
- Navigate to settings
- View dietary preferences
- List restrictions set
- Present current settings
```

## Authentication Flow
1. Navigate to hungryroot.com via Playwright MCP
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
- **Box Not Customized**: Reminder to edit
- **Delivery Issue**: Check address
- **Item Unavailable**: Note alternatives
- **Subscription Paused**: Check status
- **Order Not Found**: Check order date

## Self-Improvement Instructions
When encountering new Hungryroot features:
1. Document new UI elements
2. Add support for new product types
3. Log successful patterns
4. Update for Hungryroot changes

## Notes
- Subscription-based service
- Orders not automated for security
- Weekly customization window
- AI-powered recommendations
- Groceries and quick meals
- Dietary preferences considered
- Can pause or skip weeks

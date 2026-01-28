---
name: cornershop
description: Enables Claude to browse stores and track deliveries on Cornershop (Uber)
version: 1.0.0
author: Canifi
category: food
---

# Cornershop Skill

## Overview
Automates Cornershop (now part of Uber) operations including store browsing, list management, and delivery tracking through browser automation. Note: Actual orders are not automated for security.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/cornershop/install.sh | bash
```

Or manually:
```bash
cp -r skills/cornershop ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set CORNERSHOP_EMAIL "your-email@example.com"
canifi-env set CORNERSHOP_PASSWORD "your-password"
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
- Browse grocery stores
- Search for products
- Manage shopping lists
- Track active deliveries
- View order history
- Check store hours
- Compare prices
- Schedule deliveries

## Usage Examples

### Example 1: Browse Stores
```
User: "What stores are on Cornershop?"
Claude: I'll find available stores.
- Navigate to cornershopapp.com
- View partner stores
- Check availability
- Present options
```

### Example 2: Search Products
```
User: "Find avocados on Cornershop"
Claude: I'll search for avocados.
- Search "avocados"
- Show store results
- Compare prices
- Present options
```

### Example 3: Track Delivery
```
User: "Track my Cornershop order"
Claude: I'll track your delivery.
- Navigate to orders
- Find active order
- Check shopper status
- Report ETA
```

### Example 4: Create List
```
User: "Add items to my Cornershop list"
Claude: I'll update your list.
- Navigate to lists
- Add specified items
- Confirm additions
- Present updated list
```

## Authentication Flow
1. Navigate to cornershopapp.com via Playwright MCP
2. Click Sign In
3. Enter email from canifi-env
4. Enter password (may use Uber login)
5. Handle 2FA if enabled (notify user via iMessage)
6. Verify account access
7. Maintain session cookies

## Error Handling
- **Login Failed**: Try Uber credentials
- **Session Expired**: Re-authenticate automatically
- **2FA Required**: iMessage for verification code
- **Store Unavailable**: Check hours and location
- **Item Not Found**: Try alternative search
- **Order Not Found**: Check order ID
- **Area Not Covered**: Check service area
- **Uber Redirect**: Expected behavior

## Self-Improvement Instructions
When encountering Cornershop/Uber changes:
1. Document integration patterns
2. Update for Uber integration
3. Log successful patterns
4. Note regional availability

## Notes
- Acquired by Uber
- Orders not automated for security
- May redirect to Uber
- Personal shoppers
- Available in select markets
- Real-time order tracking
- Chat with shoppers

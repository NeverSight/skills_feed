---
name: shopify
description: Enables Claude to manage Shopify store operations, products, and orders
version: 1.0.0
author: Canifi
category: ecommerce
---

# Shopify Skill

## Overview
Automates Shopify store management including product management, order processing, inventory tracking, and store analytics through browser automation.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/shopify/install.sh | bash
```

Or manually:
```bash
cp -r skills/shopify ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set SHOPIFY_STORE "your-store.myshopify.com"
canifi-env set SHOPIFY_EMAIL "your-email@example.com"
canifi-env set SHOPIFY_PASSWORD "your-password"
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
- Manage products and inventory
- Process and track orders
- View sales analytics
- Manage customer data
- Update store settings
- Handle discounts and promotions
- Manage shipping settings
- View financial reports

## Usage Examples

### Example 1: Check Orders
```
User: "Show me today's Shopify orders"
Claude: I'll check today's orders.
- Navigate to Shopify admin
- Go to Orders section
- Filter by today's date
- List orders with status
- Present summary
```

### Example 2: Update Inventory
```
User: "Update the inventory for the blue t-shirt to 50"
Claude: I'll update that inventory.
- Navigate to Products
- Find blue t-shirt
- Edit inventory quantity
- Set to 50 units
- Save changes
```

### Example 3: Check Analytics
```
User: "Show me this week's sales on Shopify"
Claude: I'll pull sales analytics.
- Navigate to Analytics
- Select this week's range
- Gather sales data
- Present revenue and orders
```

### Example 4: Create Discount
```
User: "Create a 20% off discount code called SAVE20"
Claude: I'll create that discount.
- Navigate to Discounts
- Click Create discount
- Set code as SAVE20
- Configure 20% off
- Save discount
```

## Authentication Flow
1. Navigate to store admin URL via Playwright MCP
2. Enter email from canifi-env
3. Enter password
4. Handle 2FA if enabled (notify user via iMessage)
5. Verify admin dashboard access
6. Maintain session cookies

## Error Handling
- **Login Failed**: Verify store URL and credentials
- **Session Expired**: Re-authenticate automatically
- **2FA Required**: iMessage for verification code
- **Permission Denied**: Check staff permissions
- **Product Not Found**: Search by SKU or title
- **Order Not Found**: Search by order number
- **Inventory Error**: Check variant availability
- **API Limit**: Wait before continuing

## Self-Improvement Instructions
When encountering new Shopify features:
1. Document new admin UI elements
2. Add support for new features
3. Log successful management patterns
4. Update for Shopify updates

## Notes
- Shopify has different plans with features
- Staff accounts have role-based access
- POS integrates with online store
- Apps extend functionality
- Themes affect storefront
- Shipping rates configured separately
- Payment processing via Shopify Payments

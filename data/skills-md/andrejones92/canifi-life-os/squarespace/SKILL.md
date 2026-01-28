---
name: squarespace
description: Create beautiful websites with Squarespace - design, manage content, and handle e-commerce with elegant templates
category: productivity
---

# Squarespace Skill

## Overview
Enables Claude to use Squarespace for website management including editing content, managing products, handling orders, and configuring site settings.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/squarespace/install.sh | bash
```

Or manually:
```bash
cp -r skills/squarespace ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set SQUARESPACE_EMAIL "your-email@example.com"
canifi-env set SQUARESPACE_PASSWORD "your-password"
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
- Edit page content and layouts
- Manage blog posts and galleries
- Handle e-commerce products and orders
- Configure site settings and SEO
- View analytics and traffic data
- Manage form submissions

## Usage Examples

### Example 1: Add Product
```
User: "Add a new product to my Squarespace store"
Claude: I'll add the new product.
1. Opening Squarespace via Playwright MCP
2. Navigating to Commerce section
3. Creating new product entry
4. Adding images, description, and pricing
5. Publishing the product
```

### Example 2: Update Blog
```
User: "Create a new blog post for my portfolio site"
Claude: I'll create a blog post.
1. Opening your Squarespace site
2. Navigating to blog section
3. Creating new post with content
4. Adding images and formatting
5. Publishing the article
```

### Example 3: Check Orders
```
User: "Show me recent orders from my store"
Claude: I'll retrieve recent orders.
1. Opening Commerce dashboard
2. Viewing orders list
3. Filtering recent transactions
4. Summarizing order details and status
```

## Authentication Flow
1. Navigate to squarespace.com via Playwright MCP
2. Click "Log In" and enter email
3. Enter password
4. Handle Google SSO if configured
5. Complete 2FA if required (via iMessage)

## Error Handling
- **Login Failed**: Retry up to 3 times, notify via iMessage
- **Session Expired**: Re-authenticate automatically
- **Rate Limited**: Implement exponential backoff
- **2FA Required**: Send iMessage notification
- **Publish Failed**: Check validation errors
- **Order Error**: Verify commerce settings

## Self-Improvement Instructions
When Squarespace updates:
1. Document new template features
2. Update e-commerce workflows
3. Track editor interface changes
4. Log new integration options

## Notes
- Squarespace focuses on design quality
- E-commerce requires commerce plan
- Scheduling features for member sites
- Analytics built into all plans
- Limited custom code options

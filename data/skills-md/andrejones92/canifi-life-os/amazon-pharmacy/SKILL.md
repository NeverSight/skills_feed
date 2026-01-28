---
name: amazon-pharmacy
description: Manage prescriptions with Amazon Pharmacy - check orders, view medications, and track deliveries
category: healthcare
---

# Amazon Pharmacy Skill

## Overview
Enables Claude to use Amazon Pharmacy for prescription management including checking order status, viewing medication history, and tracking deliveries.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/amazon-pharmacy/install.sh | bash
```

Or manually:
```bash
cp -r skills/amazon-pharmacy ~/.canifi/skills/
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
- Check order status
- View medication list
- Track prescription deliveries
- Access prescription history
- View insurance savings
- Check Prime Rx benefits

## Usage Examples

### Example 1: Check Order Status
```
User: "Where is my Amazon Pharmacy order?"
Claude: I'll check your order status.
1. Opening Amazon Pharmacy via Playwright MCP
2. Accessing orders section
3. Finding recent prescription order
4. Checking delivery status
5. Providing tracking info
```

### Example 2: View Medications
```
User: "What medications are on file with Amazon Pharmacy?"
Claude: I'll list your medications.
1. Accessing prescriptions section
2. Viewing current medications
3. Listing active prescriptions
4. Noting refill status
```

### Example 3: Check Savings
```
User: "How much am I saving with Amazon Pharmacy?"
Claude: I'll check your savings.
1. Accessing account benefits
2. Viewing price comparisons
3. Calculating Prime savings
4. Summarizing total savings
```

## Authentication Flow
1. Navigate to pharmacy.amazon.com via Playwright MCP
2. Sign in with Amazon account
3. Enter password
4. Handle 2FA if required (via iMessage)
5. Maintain session for pharmacy access

## Error Handling
- **Login Failed**: Retry up to 3 times, notify via iMessage
- **Session Expired**: Re-authenticate automatically
- **Rate Limited**: Implement exponential backoff
- **2FA Required**: Send iMessage notification
- **Order Not Found**: Check order history
- **Delivery Issue**: Provide support contact

## Self-Improvement Instructions
When Amazon Pharmacy updates:
1. Document new prescription features
2. Update Prime benefit changes
3. Track delivery option updates
4. Log insurance integration changes

## Notes
- Prime members get additional savings
- Free delivery available
- Insurance and cash prices
- Automatic refill options
- Secure packaging

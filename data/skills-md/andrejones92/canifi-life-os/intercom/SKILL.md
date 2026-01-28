---
name: intercom
description: Enables Claude to manage Intercom customer conversations, help desk tickets, and team inbox operations
version: 1.0.0
author: Canifi
category: communication
---

# Intercom Skill

## Overview
Automates Intercom customer support operations including managing conversations, responding to tickets, handling the team inbox, and accessing customer data through browser automation.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/intercom/install.sh | bash
```

Or manually:
```bash
cp -r skills/intercom ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set INTERCOM_EMAIL "your-email@example.com"
canifi-env set INTERCOM_PASSWORD "your-password"
canifi-env set INTERCOM_WORKSPACE "your-workspace"
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
- Respond to customer conversations
- Manage and assign tickets
- Access customer profiles and history
- Use saved replies and macros
- Tag and categorize conversations
- Snooze and close conversations
- Create and manage help articles
- View analytics and reports

## Usage Examples

### Example 1: Respond to Customer
```
User: "Reply to the latest Intercom conversation about billing"
Claude: I'll respond to that billing inquiry.
- Navigate to Intercom inbox
- Find latest billing conversation
- Review customer history and context
- Compose helpful response
- Send reply
- Confirm message sent
```

### Example 2: Assign Ticket
```
User: "Assign the support ticket from John to the technical team"
Claude: I'll assign that ticket.
- Open conversation from John
- Click assign/reassign
- Select technical team
- Add internal note if needed
- Confirm assignment
```

### Example 3: Use Saved Reply
```
User: "Send the refund policy saved reply to the current customer"
Claude: I'll send that saved reply.
- Open current conversation
- Access saved replies
- Find "refund policy" reply
- Insert and customize if needed
- Send to customer
```

### Example 4: Check Team Performance
```
User: "Show me today's Intercom response metrics"
Claude: I'll pull today's metrics.
- Navigate to Reports section
- Select today's date range
- Gather response time data
- Compile conversation volume
- Present summary statistics
```

## Authentication Flow
1. Navigate to app.intercom.com via Playwright MCP
2. Enter email and password from canifi-env
3. Select correct workspace if multiple
4. Handle 2FA if enabled (notify user via iMessage)
5. Verify inbox access
6. Maintain session cookies

## Error Handling
- **Login Failed**: Verify workspace access, retry authentication
- **Session Expired**: Re-authenticate automatically
- **2FA Required**: iMessage for verification code
- **Workspace Not Found**: List available workspaces for selection
- **Conversation Not Found**: Search by customer email or name
- **Permission Denied**: Check user role permissions
- **Rate Limited**: Implement backoff for bulk operations
- **Customer Not Found**: Search by alternative identifiers

## Self-Improvement Instructions
When encountering new Intercom features:
1. Document new inbox UI elements
2. Add support for new conversation types
3. Log successful response patterns
4. Update for new automation features

## Notes
- Different plans have different feature access
- Operator bot may handle some conversations automatically
- Custom attributes affect customer data display
- SLA timers may apply to conversations
- Some features require admin access
- Messenger customization affects UI elements
- Product tours and surveys have separate interfaces

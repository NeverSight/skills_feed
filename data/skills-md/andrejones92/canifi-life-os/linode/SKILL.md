---
name: linode
description: Manage Linodes, NodeBalancers, and cloud resources on Linode (Akamai)
category: devops
---

# Linode Skill

## Overview
Enables Claude to access the Linode Cloud Manager to view and manage Linodes (VPS), NodeBalancers, block storage, and monitor usage and billing across your Linode/Akamai infrastructure.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/linode/install.sh | bash
```

Or manually:
```bash
cp -r skills/linode ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set LINODE_EMAIL "your-email@example.com"
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
- View Linode instances
- Check NodeBalancer status
- Monitor block storage volumes
- View Kubernetes (LKE) clusters
- Check network transfer usage
- View billing and invoices

## Usage Examples

### Example 1: Check Linodes
```
User: "What Linodes are running?"
Claude: I'll check your Linode instances.
- Opens cloud.linode.com via Playwright MCP
- Logs into account
- Linodes:
  - web-server-1: Linode 4GB, Running (Newark)
  - web-server-2: Linode 4GB, Running (Newark)
  - database: Linode 8GB, Running (Newark)
  - staging: Linode 2GB, Powered Off
- Total: $60/month
- Network: 2.3TB of 4TB used
```

### Example 2: Check NodeBalancers
```
User: "How are my load balancers?"
Claude: I'll check NodeBalancers.
- Views NodeBalancers section
- NodeBalancers:
  - prod-lb (Newark): 2 backends, healthy
    - Connections: 1,234 active
    - Traffic: 45GB this month
  - staging-lb: 1 backend, healthy
- All health checks passing
- Cost: $20/month total
```

### Example 3: View Billing
```
User: "What's my Linode bill?"
Claude: I'll check your billing.
- Views Account/Billing section
- Current month: $85.50
- Breakdown:
  - Linodes: $60.00
  - NodeBalancers: $20.00
  - Block Storage: $5.00
  - Backups: $0.50
- Credits: $25 remaining
- Payment method: Active
```

## Authentication Flow
1. Navigate to cloud.linode.com via Playwright MCP
2. Enter email address
3. Enter password
4. Handle 2FA if enabled
5. Maintain session for Cloud Manager access

## Error Handling
- Login Failed: Retry credentials
- 2FA Required: Complete verification
- Linode Issue: Check console/LISH
- Session Expired: Re-authenticate
- Rate Limited: Wait and retry
- Network Issue: Check status page

## Self-Improvement Instructions
After each interaction:
- Track resource patterns
- Note transfer usage
- Log billing trends
- Document UI changes

Suggest updates when:
- Linode updates manager
- New features added
- Pricing changes
- Akamai integration expands

## Notes
- Now part of Akamai
- Simple VPS hosting
- Predictable pricing
- Good documentation
- LISH console access
- Managed databases
- Kubernetes (LKE)

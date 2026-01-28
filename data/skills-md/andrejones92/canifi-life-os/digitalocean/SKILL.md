---
name: digitalocean
description: Manage Droplets, check App Platform, monitor databases, and view usage on DigitalOcean
category: devops
---

# DigitalOcean Skill

## Overview
Enables Claude to access DigitalOcean to manage Droplets, check App Platform deployments, monitor managed databases, and view billing and usage across cloud infrastructure.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/digitalocean/install.sh | bash
```

Or manually:
```bash
cp -r skills/digitalocean ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set DIGITALOCEAN_EMAIL "your-email@example.com"
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
- View Droplet status and metrics
- Check App Platform deployments
- Monitor managed databases
- View Spaces (object storage)
- Check Kubernetes clusters
- View billing and usage

## Usage Examples

### Example 1: Check Droplets
```
User: "What Droplets are running?"
Claude: I'll check your DigitalOcean Droplets.
- Opens cloud.digitalocean.com via Playwright MCP
- Logs into account
- Droplets:
  - web-server: s-2vcpu-4gb, NYC1, running
  - db-server: s-4vcpu-8gb, NYC1, running
  - staging: s-1vcpu-1gb, NYC1, off
- Total monthly: $45
- CPU usage: All normal
```

### Example 2: Check App Platform
```
User: "How's my App Platform app?"
Claude: I'll check App Platform status.
- Views Apps section
- my-web-app:
  - Status: Active
  - Last deploy: 2 hours ago
  - Region: NYC
  - Components: Web (2), Worker (1)
- Auto-deploy: Enabled (main branch)
- Monthly cost: $12
```

### Example 3: View Billing
```
User: "What's my DigitalOcean bill?"
Claude: I'll check your billing.
- Views Billing section
- Current month: $67.50
- Breakdown:
  - Droplets: $45.00
  - App Platform: $12.00
  - Spaces: $5.00
  - Databases: $5.50
- Credits: $100 remaining
- Payment method: Active
```

## Authentication Flow
1. Navigate to cloud.digitalocean.com via Playwright MCP
2. Enter email address
3. Enter password
4. Handle 2FA if enabled
5. Maintain session for dashboard access

## Error Handling
- Login Failed: Retry credentials
- 2FA Required: Complete verification
- Droplet Issue: Check console access
- Session Expired: Re-authenticate
- Rate Limited: Wait and retry
- Billing Issue: Check payment method

## Self-Improvement Instructions
After each interaction:
- Track resource patterns
- Note App Platform usage
- Log billing trends
- Document UI changes

Suggest updates when:
- DigitalOcean updates console
- New features added
- Pricing changes
- Products expand

## Notes
- Simple cloud platform
- Droplets are VMs
- App Platform for PaaS
- Managed databases available
- Spaces for object storage
- Kubernetes managed
- Good startup credits

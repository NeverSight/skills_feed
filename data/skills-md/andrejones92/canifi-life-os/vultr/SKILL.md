---
name: vultr
description: Manage cloud compute, bare metal, and Kubernetes on Vultr
category: devops
---

# Vultr Skill

## Overview
Enables Claude to access the Vultr dashboard to view and manage cloud compute instances, bare metal servers, Kubernetes clusters, and monitor usage and billing across Vultr infrastructure.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/vultr/install.sh | bash
```

Or manually:
```bash
cp -r skills/vultr ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set VULTR_EMAIL "your-email@example.com"
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
- View compute instances
- Check bare metal servers
- Monitor Kubernetes (VKE) clusters
- View block storage and snapshots
- Check load balancers
- View billing and usage

## Usage Examples

### Example 1: Check Instances
```
User: "What servers are running on Vultr?"
Claude: I'll check your Vultr instances.
- Opens my.vultr.com via Playwright MCP
- Logs into account
- Cloud Compute:
  - web-prod-1: 2 vCPU, 4GB, Running (New Jersey)
  - web-prod-2: 2 vCPU, 4GB, Running (New Jersey)
  - worker: 1 vCPU, 2GB, Running (New Jersey)
- Total: $42/month
- All instances healthy
- Bandwidth: 1.2TB of 4TB used
```

### Example 2: Check Kubernetes
```
User: "How's my Vultr Kubernetes cluster?"
Claude: I'll check VKE.
- Views Kubernetes section
- Cluster: prod-cluster
  - Version: 1.28
  - Node Pools: 3 nodes (4GB each)
  - Status: Active
- Workloads: 12 pods running
- Load Balancer: Attached, healthy
- Cost: $36/month
```

### Example 3: View Billing
```
User: "What's my Vultr spending?"
Claude: I'll check your billing.
- Views Billing section
- Current charges: $78.50
- Breakdown:
  - Cloud Compute: $42.00
  - Kubernetes: $36.00
  - Block Storage: $0.50
- Account balance: $100 credit
- Hourly billing active
```

## Authentication Flow
1. Navigate to my.vultr.com via Playwright MCP
2. Enter email address
3. Enter password
4. Handle 2FA if enabled
5. Maintain session for dashboard access

## Error Handling
- Login Failed: Retry credentials
- 2FA Required: Complete verification
- Instance Issue: Check console
- Session Expired: Re-authenticate
- Rate Limited: Wait and retry
- Billing Issue: Check payment

## Self-Improvement Instructions
After each interaction:
- Track resource patterns
- Note bandwidth usage
- Log billing trends
- Document UI changes

Suggest updates when:
- Vultr updates dashboard
- New features added
- Pricing changes
- Regions expand

## Notes
- High-performance cloud
- Hourly billing
- Bare metal options
- Global data centers
- Competitive pricing
- Good API
- AMD and Intel options

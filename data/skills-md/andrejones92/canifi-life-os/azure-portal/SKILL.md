---
name: azure-portal
description: Manage Azure resources, VMs, and cloud services via the Azure Portal
category: devops
---

# Azure Portal Skill

## Overview
Enables Claude to access the Azure Portal to view virtual machines, App Services, databases, and other cloud resources, monitor costs, and check service health across Microsoft Azure.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/azure-portal/install.sh | bash
```

Or manually:
```bash
cp -r skills/azure-portal ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set AZURE_EMAIL "your-email@example.com"
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
- View virtual machine status
- Check App Service deployments
- Monitor Azure SQL and Cosmos DB
- View resource groups and costs
- Check Azure DevOps pipelines
- Monitor service health

## Usage Examples

### Example 1: Check Virtual Machines
```
User: "What VMs are running in Azure?"
Claude: I'll check your Azure VMs.
- Opens portal.azure.com via Playwright MCP
- Logs into Microsoft account
- Virtual Machines:
  - prod-web-1: Standard_D2s_v3, Running
  - prod-web-2: Standard_D2s_v3, Running
  - staging-vm: Standard_B2s, Stopped (deallocated)
- Total VM cost: $180/month
- All running VMs healthy
```

### Example 2: Check App Services
```
User: "How are my Azure web apps?"
Claude: I'll check App Services.
- Views App Services section
- Web Apps:
  - my-api (Linux, P1v2): Running
  - my-frontend (Windows, S1): Running
  - my-functions (Consumption): Active
- Last deployments all successful
- No errors in last 24h
```

### Example 3: View Costs
```
User: "What's my Azure spending?"
Claude: I'll check Cost Management.
- Views Cost Management + Billing
- Current month: $456.78
- Breakdown:
  - Virtual Machines: $180.00
  - App Services: $120.00
  - Azure SQL: $89.50
  - Storage: $45.28
  - Other: $22.00
- Forecast: $520 by month end
- Budget: $600 (76% used)
```

## Authentication Flow
1. Navigate to portal.azure.com via Playwright MCP
2. Enter Microsoft account email
3. Enter password
4. Handle MFA if enabled (Authenticator app)
5. Select tenant if multiple
6. Maintain session for portal access

## Error Handling
- Login Failed: Retry credentials
- MFA Required: Complete verification
- Subscription Issue: Check access
- Session Expired: Re-authenticate
- Rate Limited: Wait and retry
- Resource Error: Check Activity Log

## Self-Improvement Instructions
After each interaction:
- Track resource patterns
- Note cost trends
- Log deployment frequency
- Document UI changes

Suggest updates when:
- Azure Portal updates
- New services added
- Pricing changes
- Features evolve

## Notes
- Enterprise cloud platform
- Strong Microsoft integration
- Hybrid cloud support
- Comprehensive services
- Complex IAM (Azure AD)
- Good compliance options
- DevOps integration

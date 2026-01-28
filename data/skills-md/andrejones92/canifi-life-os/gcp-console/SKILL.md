---
name: gcp-console
description: Manage Google Cloud Platform resources, Compute Engine, and Cloud Run
category: devops
---

# GCP Console Skill

## Overview
Enables Claude to access the Google Cloud Console to view Compute Engine instances, Cloud Run services, Cloud SQL databases, and monitor billing and resource usage across GCP projects.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/gcp-console/install.sh | bash
```

Or manually:
```bash
cp -r skills/gcp-console ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set GCP_EMAIL "your-email@example.com"
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
- View Compute Engine VMs
- Check Cloud Run services
- Monitor Cloud SQL instances
- View GKE clusters
- Check Cloud Functions
- Monitor billing and costs

## Usage Examples

### Example 1: Check Compute Engine
```
User: "What VMs are running in GCP?"
Claude: I'll check your Compute Engine instances.
- Opens console.cloud.google.com via Playwright MCP
- Logs into Google account
- Compute Engine VMs:
  - prod-instance-1: n2-standard-2, Running (us-central1)
  - prod-instance-2: n2-standard-2, Running (us-central1)
  - dev-instance: e2-medium, Stopped
- Monthly estimate: $145
- All running instances healthy
```

### Example 2: Check Cloud Run
```
User: "How are my Cloud Run services?"
Claude: I'll check Cloud Run.
- Views Cloud Run section
- Services:
  - my-api: Active, 4 instances, 12k req/day
  - image-processor: Active, 0-5 instances, autoscaling
  - webhook-handler: Active, 1 instance min
- Last deployments successful
- No errors in last 24h
```

### Example 3: View Billing
```
User: "What's my GCP bill?"
Claude: I'll check Billing.
- Views Billing section
- Current month: $234.56
- Breakdown:
  - Compute Engine: $145.00
  - Cloud Run: $34.50
  - Cloud SQL: $42.00
  - Cloud Storage: $8.06
  - Other: $5.00
- Budget alert: 60% of $400
- Credits remaining: $150
```

## Authentication Flow
1. Navigate to console.cloud.google.com via Playwright MCP
2. Enter Google account email
3. Enter password
4. Handle 2FA if enabled
5. Select project if multiple
6. Maintain session for console access

## Error Handling
- Login Failed: Retry credentials
- 2FA Required: Complete verification
- Project Access: Check IAM permissions
- Session Expired: Re-authenticate
- Rate Limited: Wait and retry
- Quota Exceeded: Check quotas

## Self-Improvement Instructions
After each interaction:
- Track resource patterns
- Note cost trends
- Log service usage
- Document UI changes

Suggest updates when:
- GCP Console updates
- New services added
- Pricing changes
- Features evolve

## Notes
- Google's cloud platform
- Strong data/ML services
- Global infrastructure
- Kubernetes origin (GKE)
- BigQuery for analytics
- Firebase integration
- Competitive pricing

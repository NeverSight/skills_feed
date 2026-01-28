---
name: aws-console
description: View AWS resources, check costs, monitor services, and manage cloud infrastructure
category: devops
---

# AWS Console Skill

## Overview
Enables Claude to access AWS Console to view resources, check billing and costs, monitor service health, and manage cloud infrastructure across Amazon Web Services.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/aws-console/install.sh | bash
```

Or manually:
```bash
cp -r skills/aws-console ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set AWS_EMAIL "your-email@example.com"
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
- View EC2 instances and status
- Check S3 bucket storage
- Monitor Lambda functions
- View CloudWatch metrics
- Check billing and cost explorer
- View service health dashboard

## Usage Examples

### Example 1: Check EC2 Instances
```
User: "What EC2 instances are running?"
Claude: I'll check your AWS EC2.
- Opens console.aws.amazon.com via Playwright MCP
- Logs into AWS
- EC2 Instances (us-east-1):
  - web-server-1: t3.medium, running
  - api-server-1: t3.large, running
  - db-server: r5.large, running
- Total: 3 running, 2 stopped
- Monthly estimate: $156
```

### Example 2: Check AWS Costs
```
User: "What are my AWS costs this month?"
Claude: I'll check Cost Explorer.
- Views Billing & Cost Management
- Current month: $234.56
- Forecast: $312.00
- Top services:
  - EC2: $145.00
  - RDS: $67.00
  - S3: $12.50
  - Lambda: $5.00
- vs last month: +8%
```

### Example 3: View Lambda Functions
```
User: "How are my Lambda functions doing?"
Claude: I'll check Lambda dashboard.
- Views Lambda functions
- Functions: 8 total
- Invocations (24h): 45,678
- Errors: 12 (0.03%)
- Duration avg: 234ms
- Most active: api-handler (32k calls)
- Cold starts: Minimal
```

## Authentication Flow
1. Navigate to console.aws.amazon.com via Playwright MCP
2. Enter email or IAM username
3. Enter password
4. Handle MFA (authenticator required)
5. Select region if needed
6. Maintain session for console access

## Error Handling
- Login Failed: Check IAM permissions
- MFA Required: Complete verification
- Permission Denied: Check IAM policies
- Session Expired: Re-authenticate (short sessions)
- Rate Limited: Wait and retry
- Region Issue: Switch regions

## Self-Improvement Instructions
After each interaction:
- Track common service checks
- Note cost monitoring patterns
- Log resource usage
- Document console changes

Suggest updates when:
- AWS updates console
- New services added
- Pricing changes
- Security features update

## Notes
- AWS requires strong authentication
- Multiple regions to check
- Cost optimization important
- CloudWatch for monitoring
- IAM for access control
- Use AWS Organizations for multi-account
- Reserved instances for savings

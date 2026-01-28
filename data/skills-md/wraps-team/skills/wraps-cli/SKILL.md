---
name: wraps-cli
description: CLI that deploys SES, DynamoDB, Lambda, and IAM resources to your AWS account with automatic DKIM, SPF, DMARC configuration.
---

# @wraps.dev/cli

CLI that deploys SES, DynamoDB, Lambda, and IAM resources to your AWS account. Configures DKIM, SPF, DMARC, and event tracking automatically.

## Installation

```bash
# Run directly with npx (recommended)
npx @wraps.dev/cli <command>

# Or install globally
npm install -g @wraps.dev/cli
wraps <command>
```

## Quick Start

```bash
# Deploy email infrastructure
npx @wraps.dev/cli email init

# Check status
npx @wraps.dev/cli email status

# Verify domain
npx @wraps.dev/cli email verify --domain yourapp.com
```

## Prerequisites

1. **Node.js 20+**
2. **AWS account with credentials configured**
   - Environment variables: `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`
   - Or AWS CLI profile: `~/.aws/credentials`
   - Or IAM role (EC2, ECS, Lambda)

## Email Commands

### `wraps email init`

Deploy new email infrastructure to your AWS account.

```bash
# Interactive mode (prompts for options)
wraps email init

# With flags
wraps email init --provider vercel --region us-west-2 --domain myapp.com

# Production preset (enhanced security, multi-AZ)
wraps email init --preset production
```

**Options:**
- `--provider <name>` — Hosting provider (vercel, aws-lambda, generic)
- `--region <region>` — AWS region (default: us-east-1)
- `--domain <domain>` — Domain to verify for sending
- `--preset <preset>` — Configuration preset (default, production)

**What gets deployed:**
- SES Configuration (domain verification, DKIM, SPF, DMARC)
- Event Tracking (bounces, complaints, deliveries, opens, clicks)
- DynamoDB Table (email event history, 90-day TTL)
- Lambda Functions (event processing, webhook handling)
- IAM Roles (least-privilege, OIDC support for Vercel)
- CloudWatch (metrics and alarms)

All resources use the `wraps-email-*` namespace prefix.

### `wraps email status`

Show current deployment status.

```bash
wraps email status
```

**Output includes:**
- Deployment state (deployed, pending, none)
- Domain verification status
- SES sending status (sandbox/production)
- Infrastructure resource summary

### `wraps email verify`

Check and guide domain DNS verification.

```bash
# Check DNS propagation
wraps email verify --domain myapp.com

# Auto-configure if using Route53
wraps email verify --domain myapp.com --auto
```

**DNS Records Required:**
- DKIM (3 CNAME records)
- SPF (TXT record)
- DMARC (TXT record)
- Optional: Custom MAIL FROM

### `wraps email upgrade`

Add features to existing deployment.

```bash
# Interactive upgrade wizard
wraps email upgrade

# Specific upgrades
wraps email upgrade --feature tracking
wraps email upgrade --feature webhooks
```

### `wraps email connect`

Import existing SES infrastructure into Wraps management.

```bash
wraps email connect
```

Use this if you already have SES configured and want to use Wraps SDK/dashboard without redeploying.

### `wraps email restore`

Restore infrastructure from saved metadata.

```bash
# Interactive restore
wraps email restore

# Skip confirmation (use with caution)
wraps email restore --force
```

### `wraps email destroy`

Remove all Wraps email infrastructure.

```bash
# Interactive confirmation
wraps email destroy

# Skip confirmation (use with caution)
wraps email destroy --force
```

**Warning:** This removes all deployed resources. Email sending will stop working.

## Configuration

### State Storage

Deployment state is stored in `~/.wraps/` directory:
- One state file per AWS account + region combination
- Contains resource IDs, configuration, and metadata

### Environment Variables

| Variable | Description |
|----------|-------------|
| `AWS_PROFILE` | AWS credentials profile to use |
| `AWS_REGION` | Default AWS region |
| `AWS_ACCESS_KEY_ID` | AWS access key (if not using profile) |
| `AWS_SECRET_ACCESS_KEY` | AWS secret key (if not using profile) |
| `WRAPS_TELEMETRY_DISABLED` | Set to `1` to disable telemetry |

## Common Workflows

### New Project Setup

```bash
# 1. Deploy infrastructure
npx @wraps.dev/cli email init --domain myapp.com

# 2. Add DNS records (shown in output)
# DKIM, SPF, DMARC records for myapp.com

# 3. Wait for DNS propagation and verify
npx @wraps.dev/cli email verify --domain myapp.com

# 4. Check everything is ready
npx @wraps.dev/cli email status

# 5. Install SDK and start sending
npm install @wraps.dev/email
```

### Vercel Project Setup

```bash
# 1. Deploy with Vercel provider (sets up OIDC)
npx @wraps.dev/cli email init --provider vercel --domain myapp.com

# 2. Copy the Role ARN from output
# Add to Vercel environment: AWS_ROLE_ARN=arn:aws:iam::...

# 3. In your app, use the SDK
import { WrapsEmail } from '@wraps.dev/email';

const email = new WrapsEmail({
  roleArn: process.env.AWS_ROLE_ARN,
});
```

### Multi-Region Setup

```bash
# Primary region
npx @wraps.dev/cli email init --region us-east-1 --domain myapp.com

# Secondary region (DR)
npx @wraps.dev/cli email init --region us-west-2 --domain myapp.com
```

### Existing SES Migration

```bash
# Import existing SES setup
npx @wraps.dev/cli email connect

# Add event tracking
npx @wraps.dev/cli email upgrade --feature tracking
```

## SES Sandbox

New AWS accounts start in SES sandbox mode:
- Can only send to verified email addresses
- Limited to 200 emails/day

**To exit sandbox:**
1. Verify your domain: `wraps email verify --domain yourapp.com`
2. Request production access in AWS Console → SES → Account Dashboard
3. Provide use case, expected volume, complaint handling process

The CLI will guide you through this process.

## Troubleshooting

### "Credentials not found"

```bash
# Check AWS credentials
aws sts get-caller-identity

# Or set environment variables
export AWS_ACCESS_KEY_ID=your-key
export AWS_SECRET_ACCESS_KEY=your-secret
```

### "Domain verification pending"

DNS propagation can take up to 72 hours. Check status:

```bash
wraps email verify --domain myapp.com
```

Common issues:
- CNAME records not added correctly
- TTL too high (try 300 seconds)
- DNS provider caching

### "SES sandbox mode"

You need production access to send to non-verified emails:

1. Go to AWS Console → SES → Account Dashboard
2. Click "Request Production Access"
3. Fill out the form with your use case

### "IAM permission denied"

Ensure your IAM user/role has these permissions:
- `ses:*`
- `iam:CreateRole`, `iam:AttachRolePolicy` (for OIDC setup)
- `dynamodb:CreateTable`, `dynamodb:*` (for event tracking)
- `lambda:CreateFunction`, `lambda:*` (for event processing)
- `cloudwatch:PutMetricAlarm` (for monitoring)

Or use the managed policy: `arn:aws:iam::aws:policy/AdministratorAccess` (not recommended for production).

## Telemetry

The CLI collects anonymous usage data to improve the product:
- Command names and success/failure status
- System info (OS, Node version)

**Never collected:** AWS credentials, domains, email content, PII.

Opt out:
```bash
wraps telemetry disable
# or
export WRAPS_TELEMETRY_DISABLED=1
```

## Resource Naming

All resources created by Wraps use consistent naming:

| Resource | Name Pattern |
|----------|--------------|
| SES Configuration Set | `wraps-email-tracking` |
| DynamoDB Table | `wraps-email-events` |
| Lambda Functions | `wraps-email-processor` |
| IAM Roles | `wraps-email-*` |
| CloudWatch Alarms | `wraps-email-*` |

This makes it easy to identify and audit Wraps resources in your AWS account.

## Non-Destructive

The CLI follows a non-destructive approach:
- Never modifies existing AWS resources
- Only creates new resources with `wraps-*` prefix
- `destroy` only removes resources created by Wraps
- Your existing SES configuration is never touched

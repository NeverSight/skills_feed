---
name: upstash
description: Manage serverless Redis, Kafka, and QStash on Upstash
category: devops
---

# Upstash Skill

## Overview
Enables Claude to access Upstash to view and manage serverless Redis databases, Kafka clusters, QStash message queues, and monitor usage and performance metrics.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/upstash/install.sh | bash
```

Or manually:
```bash
cp -r skills/upstash ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set UPSTASH_EMAIL "your-email@example.com"
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
- View Redis database status
- Check Kafka cluster health
- Monitor QStash messages
- View data usage metrics
- Check connection details
- View billing and usage

## Usage Examples

### Example 1: Check Redis Databases
```
User: "How are my Upstash Redis databases?"
Claude: I'll check your Upstash console.
- Opens console.upstash.com via Playwright MCP
- Logs into account
- Redis Databases:
  - prod-cache: Global, 45MB used
    - Commands: 125k/day
    - Regions: us-east-1, eu-west-1
  - session-store: Regional, 12MB used
    - Commands: 34k/day
- All databases healthy
- Latency: <10ms p99
```

### Example 2: Check Kafka
```
User: "How's my Kafka cluster?"
Claude: I'll check Kafka status.
- Views Kafka section
- Clusters:
  - event-stream: Active
    - Topics: 5
    - Partitions: 15
    - Messages: 2.3M/day
- Consumers: 3 active
- Lag: 0 (caught up)
- Storage: 850MB
```

### Example 3: Check QStash
```
User: "What's my QStash usage?"
Claude: I'll check QStash.
- Views QStash section
- Messages today: 4,523
- Success rate: 99.8%
- Scheduled: 12 pending
- Dead letter: 2 messages
- Endpoints: 8 configured
- Monthly limit: 100k (4.5% used)
```

## Authentication Flow
1. Navigate to console.upstash.com via Playwright MCP
2. Enter email or use GitHub/Google OAuth
3. Enter password if email login
4. Handle 2FA if enabled
5. Maintain session for console access

## Error Handling
- Login Failed: Retry credentials
- 2FA Required: Complete verification
- Connection Issue: Check REST URL
- Session Expired: Re-authenticate
- Rate Limit: Check plan limits
- Quota Exceeded: Upgrade plan

## Self-Improvement Instructions
After each interaction:
- Track command patterns
- Note data growth
- Log message volume
- Document UI changes

Suggest updates when:
- Upstash updates console
- New features added
- Pricing changes
- Products expand

## Notes
- Serverless data platform
- Pay-per-request pricing
- Global replication
- REST API included
- Edge-friendly
- Durable storage
- No servers to manage

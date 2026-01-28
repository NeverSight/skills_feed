---
name: planetscale
description: Manage serverless MySQL databases and branches on PlanetScale
category: devops
---

# PlanetScale Skill

## Overview
Enables Claude to access PlanetScale to view and manage serverless MySQL databases, database branches, deploy requests, and monitor query performance and usage.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/planetscale/install.sh | bash
```

Or manually:
```bash
cp -r skills/planetscale ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set PLANETSCALE_EMAIL "your-email@example.com"
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
- View database status
- Check branch topology
- Monitor query insights
- View deploy requests
- Check connection strings
- View billing and usage

## Usage Examples

### Example 1: Check Databases
```
User: "How are my PlanetScale databases?"
Claude: I'll check your PlanetScale dashboard.
- Opens app.planetscale.com via Playwright MCP
- Logs into account
- Databases:
  - prod-db: Scaler Pro, 8GB storage
    - Branches: main, staging
    - Region: us-east-1
  - analytics-db: Scaler, 2GB storage
    - Branches: main
- All databases healthy
- No connection issues
```

### Example 2: Check Branch Status
```
User: "What branches do I have?"
Claude: I'll check database branches.
- Views prod-db detail
- Branches:
  - main (production): 8GB, 45k queries/day
  - staging: 500MB, 2k queries/day
  - feature-auth: 100MB, dev branch
- Deploy requests:
  - None pending
  - Last deploy: 2 days ago
- Schema: 24 tables
```

### Example 3: View Insights
```
User: "Show me query performance"
Claude: I'll check Query Insights.
- Views Insights section
- Top queries (last 24h):
  - SELECT users: 12k calls, 2ms avg
  - SELECT orders: 8k calls, 5ms avg
  - INSERT events: 5k calls, 3ms avg
- Slow queries: 2 flagged
- Rows read: 2.4M
- Rows written: 45k
```

## Authentication Flow
1. Navigate to app.planetscale.com via Playwright MCP
2. Enter email or use GitHub OAuth
3. Enter password if email login
4. Handle 2FA if enabled
5. Select organization if multiple
6. Maintain session for dashboard access

## Error Handling
- Login Failed: Retry credentials
- 2FA Required: Complete verification
- Connection Issue: Check credentials
- Session Expired: Re-authenticate
- Branch Conflict: Resolve deploy request
- Quota Exceeded: Check plan limits

## Self-Improvement Instructions
After each interaction:
- Track query patterns
- Note branch usage
- Log storage growth
- Document UI changes

Suggest updates when:
- PlanetScale updates dashboard
- New features added
- Pricing changes
- Query insights expand

## Notes
- Serverless MySQL
- Git-like branching
- Non-blocking schema changes
- Vitess-powered
- Automatic scaling
- Connection pooling
- MySQL compatible

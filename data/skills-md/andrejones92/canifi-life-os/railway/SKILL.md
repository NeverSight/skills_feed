---
name: railway
description: Check deployments, manage services, monitor resources, and view logs on Railway
category: devops
---

# Railway Skill

## Overview
Enables Claude to access Railway to check deployment status, manage services and databases, monitor resource usage, and view logs for modern cloud deployments.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/railway/install.sh | bash
```

Or manually:
```bash
cp -r skills/railway ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set RAILWAY_EMAIL "your-email@example.com"
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
- View deployment status
- Check service health
- Monitor database connections
- View deployment logs
- Check resource usage
- Manage environment variables

## Usage Examples

### Example 1: Check Project Status
```
User: "What's my Railway project status?"
Claude: I'll check your Railway deployments.
- Opens railway.app via Playwright MCP
- Logs into account
- Project: my-app
  - Web service: Running (healthy)
  - API service: Running (healthy)
  - PostgreSQL: Connected
  - Redis: Connected
- Last deploy: 2 hours ago
- All services healthy
```

### Example 2: View Logs
```
User: "Show me the Railway logs"
Claude: I'll check recent logs.
- Views service logs
- Recent logs (API service):
  - [INFO] Server started on port 3000
  - [INFO] Database connected
  - [WARN] Slow query detected (2.3s)
  - [INFO] Health check passed
- Error rate: 0.01%
- Request volume: 1,234/hour
```

### Example 3: Check Resources
```
User: "How much am I using on Railway?"
Claude: I'll check resource usage.
- Views usage dashboard
- Current usage:
  - CPU: 15% average
  - Memory: 512MB / 1GB
  - Disk: 2.3GB / 5GB
  - Network: 45GB transfer
- Monthly estimate: $12.50
- Within free tier: No (Pro plan)
```

## Authentication Flow
1. Navigate to railway.app via Playwright MCP
2. Sign in with email or GitHub
3. Enter password or OAuth
4. Handle verification if needed
5. Maintain session for dashboard access

## Error Handling
- Login Failed: Try GitHub OAuth
- Deploy Failed: Check build logs
- Service Crashed: View crash logs
- Session Expired: Re-authenticate
- Database Issue: Check connection
- Resource Limit: Upgrade plan

## Self-Improvement Instructions
After each interaction:
- Track deployment patterns
- Note resource usage trends
- Log common issues
- Document UI changes

Suggest updates when:
- Railway updates dashboard
- New features added
- Pricing changes
- Template library expands

## Notes
- Modern platform-as-a-service
- Great developer experience
- PostgreSQL, Redis, MongoDB built-in
- GitHub integration
- Preview environments
- Team collaboration
- Usage-based pricing

---
name: cloudflare
description: Manage DNS, check analytics, monitor Workers, and configure security on Cloudflare
category: devops
---

# Cloudflare Skill

## Overview
Enables Claude to access Cloudflare to manage DNS records, check analytics and traffic, monitor Workers, and configure security settings for domains.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/cloudflare/install.sh | bash
```

Or manually:
```bash
cp -r skills/cloudflare ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set CLOUDFLARE_EMAIL "your-email@example.com"
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
- Manage DNS records
- View traffic analytics
- Monitor Workers performance
- Check security events
- View page rules and caching
- Check SSL/TLS status

## Usage Examples

### Example 1: Check Traffic
```
User: "What's my Cloudflare traffic?"
Claude: I'll check your Cloudflare analytics.
- Opens dash.cloudflare.com via Playwright MCP
- Logs into account
- Traffic (last 24h):
  - Requests: 1.2M
  - Bandwidth: 45GB
  - Unique visitors: 23,456
  - Cached: 78%
- Threats blocked: 234
- All systems healthy
```

### Example 2: Check DNS
```
User: "What DNS records do I have?"
Claude: I'll check your DNS configuration.
- Views DNS section
- Records for myapp.com:
  - A: @ -> 192.168.1.1 (proxied)
  - CNAME: www -> myapp.com (proxied)
  - MX: mail.myapp.com (priority 10)
  - TXT: SPF record configured
- Propagation: Complete
- DNSSEC: Enabled
```

### Example 3: Check Workers
```
User: "How are my Workers performing?"
Claude: I'll check Workers analytics.
- Views Workers section
- Workers:
  - api-router: 45k requests/day
  - image-resizer: 12k requests/day
- CPU time: 8ms avg
- Errors: 0.01%
- KV usage: 234MB
- Worker limits: OK
```

## Authentication Flow
1. Navigate to dash.cloudflare.com via Playwright MCP
2. Enter email address
3. Enter password
4. Handle 2FA if enabled
5. Select zone/domain if multiple
6. Maintain session for dashboard

## Error Handling
- Login Failed: Retry credentials
- 2FA Required: Complete verification
- Zone Not Found: Check permissions
- Session Expired: Re-authenticate
- Rate Limited: Wait and retry
- DNS Propagation: Note timing

## Self-Improvement Instructions
After each interaction:
- Track traffic patterns
- Note security events
- Log Worker performance
- Document UI changes

Suggest updates when:
- Cloudflare updates dashboard
- New features added
- Workers updated
- Security features expand

## Notes
- CDN and security combined
- Workers for edge compute
- Pages for static sites
- R2 for object storage
- Free tier generous
- DDoS protection included
- Zero Trust for security

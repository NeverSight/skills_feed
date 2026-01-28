---
name: datadog
description: Monitor infrastructure, APM, logs, and metrics on Datadog
category: analytics
---

# Datadog Skill

## Overview
Enables Claude to access Datadog to view infrastructure metrics, APM traces, logs, dashboards, and monitor alerts across your entire observability stack.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/datadog/install.sh | bash
```

Or manually:
```bash
cp -r skills/datadog ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set DATADOG_EMAIL "your-email@example.com"
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
- View infrastructure metrics
- Check APM traces and services
- Monitor log streams
- View custom dashboards
- Check alert status
- Analyze host health

## Usage Examples

### Example 1: Check Infrastructure
```
User: "How's my infrastructure looking?"
Claude: I'll check your Datadog dashboard.
- Opens app.datadoghq.com via Playwright MCP
- Logs into account
- Infrastructure:
  - Hosts: 12 active
  - Containers: 45 running
  - CPU avg: 34%
  - Memory avg: 67%
- Alerts: 1 warning (disk space)
- All critical services healthy
```

### Example 2: Check APM
```
User: "How are my services performing?"
Claude: I'll check APM.
- Views APM section
- Services:
  - api-gateway: 45ms p50, 120ms p99
  - user-service: 23ms p50, 89ms p99
  - order-service: 67ms p50, 234ms p99
- Throughput: 2.3k req/s
- Error rate: 0.12%
- Slowest endpoint: /api/reports (890ms)
```

### Example 3: Check Logs
```
User: "Any errors in the logs?"
Claude: I'll check Log Management.
- Views Logs section
- Last hour:
  - ERROR: 23 events
  - WARN: 156 events
  - INFO: 45,678 events
- Top errors:
  - ConnectionTimeout: 12 occurrences
  - ValidationError: 8 occurrences
- Pattern detected: DB connection spikes
```

## Authentication Flow
1. Navigate to app.datadoghq.com via Playwright MCP
2. Enter email address
3. Enter password
4. Handle 2FA/SAML if enabled
5. Select organization if multiple
6. Maintain session for dashboard access

## Error Handling
- Login Failed: Retry credentials
- 2FA Required: Complete verification
- SAML/SSO: Follow redirect
- Session Expired: Re-authenticate
- Rate Limited: Wait and retry
- Access Denied: Check org permissions

## Self-Improvement Instructions
After each interaction:
- Track metric patterns
- Note alert frequency
- Log performance trends
- Document UI changes

Suggest updates when:
- Datadog updates dashboard
- New features added
- Integrations expand
- Metrics added

## Notes
- Comprehensive observability
- APM and tracing
- Log management
- Custom dashboards
- Alert management
- 600+ integrations
- Enterprise-grade

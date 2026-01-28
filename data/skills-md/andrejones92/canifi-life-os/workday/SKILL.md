---
name: workday
description: Manage enterprise HR with Workday's cloud-based human capital management system.
category: hr
---
# Workday Skill

Manage enterprise HR with Workday's cloud-based human capital management system.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/workday/install.sh | bash
```

Or manually:
```bash
cp -r skills/workday ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set WORKDAY_TENANT "your_tenant"
canifi-env set WORKDAY_CLIENT_ID "your_client_id"
canifi-env set WORKDAY_CLIENT_SECRET "your_client_secret"
canifi-env set WORKDAY_REFRESH_TOKEN "your_refresh_token"
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

1. **Employee Records**: Manage employee data and profiles
2. **Recruiting**: Post jobs and manage candidates
3. **Time Tracking**: Track time and attendance
4. **Benefits**: Manage employee benefits enrollment
5. **Reporting**: Generate HR reports and analytics

## Usage Examples

### Find Employee
```
User: "Find employee John Smith in Workday"
Assistant: Returns employee profile
```

### View Time Off
```
User: "Show my team's time off requests"
Assistant: Returns pending time off requests
```

### Run Report
```
User: "Generate a headcount report for Q1"
Assistant: Runs report and returns results
```

### Update Record
```
User: "Update the address for employee #12345"
Assistant: Updates employee record
```

## Authentication Flow

1. Register API client in Workday
2. Get client credentials and refresh token
3. Use OAuth 2.0 for authentication
4. Tenant-specific endpoints

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| 401 Unauthorized | Token expired | Refresh access token |
| 403 Forbidden | No access | Check security group |
| 404 Not Found | Resource not found | Verify worker ID |
| 429 Rate Limited | Too many requests | Wait and retry |

## Notes

- Enterprise HCM platform
- Unified HR, payroll, finance
- Complex implementation
- Extensive customization
- Industry-specific solutions
- Premium enterprise pricing

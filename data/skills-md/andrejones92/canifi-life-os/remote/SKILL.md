---
name: remote
description: Manage global employment and payroll with Remote's international HR platform.
category: hr
---
# Remote Skill

Manage global employment and payroll with Remote's international HR platform.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/remote/install.sh | bash
```

Or manually:
```bash
cp -r skills/remote ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set REMOTE_API_KEY "your_api_key"
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

1. **Global Employment**: Hire employees in 60+ countries
2. **Contractor Management**: Manage international contractors
3. **Payroll Processing**: Run multi-country payroll
4. **Benefits Administration**: Provide localized benefits
5. **Compliance Management**: Ensure local labor law compliance

## Usage Examples

### Hire Employee
```
User: "Hire a new employee in Canada"
Assistant: Creates employee with compliant setup
```

### Add Contractor
```
User: "Set up a contractor in Brazil"
Assistant: Creates contractor agreement
```

### View Payroll
```
User: "Show me upcoming payroll runs"
Assistant: Returns scheduled payroll
```

### Check Compliance
```
User: "What are the leave requirements in France?"
Assistant: Returns local compliance info
```

## Authentication Flow

1. Generate API token in Remote dashboard
2. Use token for API authentication
3. Bearer token in request header
4. Scoped by organization

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| 401 Unauthorized | Invalid token | Verify API token |
| 403 Forbidden | No access | Check permissions |
| 404 Not Found | Resource not found | Verify ID |
| 422 Unprocessable | Invalid data | Fix request |

## Notes

- Employer of Record services
- Direct employment option
- Multi-country payroll
- Equity incentives support
- IP protection built-in
- Transparent pricing

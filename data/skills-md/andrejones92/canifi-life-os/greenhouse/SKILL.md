---
name: greenhouse
description: Manage recruiting and hiring with Greenhouse's applicant tracking system.
category: hr
---
# Greenhouse Skill

Manage recruiting and hiring with Greenhouse's applicant tracking system.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/greenhouse/install.sh | bash
```

Or manually:
```bash
cp -r skills/greenhouse ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set GREENHOUSE_API_KEY "your_api_key"
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

1. **Candidate Management**: Track candidates through hiring pipeline
2. **Job Requisitions**: Create and manage job openings
3. **Interview Scheduling**: Schedule and manage interviews
4. **Scorecards**: Collect and manage interview feedback
5. **Offers**: Create and send offer letters

## Usage Examples

### Add Candidate
```
User: "Add John Smith as a candidate for the Engineering role"
Assistant: Creates candidate and links to job
```

### Schedule Interview
```
User: "Schedule an interview with Sarah for Tuesday at 2pm"
Assistant: Creates interview event
```

### View Pipeline
```
User: "Show me candidates in the offer stage"
Assistant: Returns candidates by stage
```

### Submit Scorecard
```
User: "Submit feedback for the last interview"
Assistant: Creates scorecard with ratings
```

## Authentication Flow

1. Generate API key in Greenhouse settings
2. Use Basic Auth with API key
3. Key provides access based on permissions
4. Different keys for different access levels

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| 401 Unauthorized | Invalid API key | Verify credentials |
| 403 Forbidden | No permission | Check API key access |
| 404 Not Found | Resource not found | Verify ID |
| 429 Rate Limited | Too many requests | Implement backoff |

## Notes

- Enterprise ATS platform
- Structured hiring process
- 300+ integrations
- DE&I features included
- Reporting and analytics
- Industry-leading ATS

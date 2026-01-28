---
name: indeed
description: Post jobs and search candidates on Indeed's job marketplace.
category: hr
---
# Indeed Skill

Post jobs and search candidates on Indeed's job marketplace.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/indeed/install.sh | bash
```

Or manually:
```bash
cp -r skills/indeed ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set INDEED_EMPLOYER_ID "your_employer_id"
canifi-env set INDEED_API_KEY "your_api_key"
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

1. **Job Posting**: Create and manage job listings
2. **Candidate Search**: Search Indeed's resume database
3. **Application Tracking**: Track and manage job applications
4. **Sponsored Jobs**: Manage sponsored job campaigns
5. **Analytics**: Track job performance and applicant metrics

## Usage Examples

### Post Job
```
User: "Post a new job for Senior Developer in New York"
Assistant: Creates job listing with details
```

### Search Resumes
```
User: "Find candidates with 5+ years of React experience"
Assistant: Returns matching resumes
```

### View Applications
```
User: "Show me new applications for the marketing role"
Assistant: Returns recent applicants
```

### Sponsor Job
```
User: "Sponsor the DevOps position with $50/day budget"
Assistant: Creates sponsored campaign
```

## Authentication Flow

1. Register as Indeed employer
2. Get API credentials from Indeed publisher
3. Use OAuth for some endpoints
4. API key for basic operations

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| 401 Unauthorized | Invalid credentials | Verify API key |
| 403 Forbidden | No employer access | Verify employer ID |
| 404 Not Found | Job not found | Check job ID |
| 429 Rate Limited | Too many requests | Wait and retry |

## Notes

- Largest job site globally
- Free and sponsored listings
- Resume search requires subscription
- ATS integrations available
- Pay-per-click for sponsored
- Mobile-optimized applications

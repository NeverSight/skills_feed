---
name: linkedin-recruiter
description: Source and recruit candidates with LinkedIn's professional recruiting platform.
category: social
---
# LinkedIn Recruiter Skill

Source and recruit candidates with LinkedIn's professional recruiting platform.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/linkedin-recruiter/install.sh | bash
```

Or manually:
```bash
cp -r skills/linkedin-recruiter ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set LINKEDIN_CLIENT_ID "your_client_id"
canifi-env set LINKEDIN_CLIENT_SECRET "your_client_secret"
canifi-env set LINKEDIN_ACCESS_TOKEN "your_access_token"
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

1. **Candidate Search**: Search for candidates with advanced filters
2. **InMail Messaging**: Send personalized InMail messages to prospects
3. **Pipeline Management**: Manage candidate pipelines and stages
4. **Project Collaboration**: Collaborate with team on recruiting projects
5. **Analytics**: Track recruiting metrics and performance

## Usage Examples

### Search Candidates
```
User: "Find software engineers in San Francisco with Python experience"
Assistant: Returns matching candidate profiles
```

### Send InMail
```
User: "Send an InMail to this candidate about the role"
Assistant: Composes and sends personalized InMail
```

### View Pipeline
```
User: "Show me candidates in the interview stage"
Assistant: Returns candidates by pipeline stage
```

### Track Metrics
```
User: "What's our response rate this month?"
Assistant: Returns InMail and recruiting metrics
```

## Authentication Flow

1. Create app in LinkedIn Developer Portal
2. Request Recruiter API access (requires approval)
3. Implement OAuth 2.0 authorization
4. Use tokens for API calls

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| 401 Unauthorized | Token expired | Refresh access token |
| 403 Forbidden | No Recruiter access | Verify seat license |
| 429 Rate Limited | Too many requests | Wait and retry |
| 404 Not Found | Profile not found | Verify profile ID |

## Notes

- Requires Recruiter subscription
- API access requires additional approval
- InMail credits consumed per message
- Team collaboration features
- Integration with ATS systems
- Expensive enterprise product

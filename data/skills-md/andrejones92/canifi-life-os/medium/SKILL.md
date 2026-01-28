---
name: medium
description: Read and publish articles on Medium's blogging platform with personalized recommendations.
category: productivity
---
# Medium Skill

Read and publish articles on Medium's blogging platform with personalized recommendations.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/medium/install.sh | bash
```

Or manually:
```bash
cp -r skills/medium ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set MEDIUM_ACCESS_TOKEN "your_access_token"
canifi-env set MEDIUM_USER_ID "your_user_id"
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

1. **Content Discovery**: Discover articles based on interests, tags, and following list
2. **Reading Experience**: Read articles with estimated reading time, highlights, and claps
3. **Publish Stories**: Create and publish articles with rich formatting and media
4. **Publication Management**: Manage publications and submit stories for review
5. **Stats & Analytics**: Track article performance with views, reads, and claps metrics

## Usage Examples

### Get Personalized Feed
```
User: "Show me top Medium articles about productivity"
Assistant: Returns curated articles on productivity with titles, authors, and read times
```

### Publish Article
```
User: "Publish my article about AI ethics to Medium"
Assistant: Publishes article with specified title, content, and tags
```

### Check Stats
```
User: "How are my Medium articles performing this month?"
Assistant: Returns views, reads, fans, and claps for recent articles
```

### Follow Topic
```
User: "Follow the 'Machine Learning' tag on Medium"
Assistant: Adds Machine Learning to your followed topics
```

## Authentication Flow

1. Create application at medium.com/me/applications
2. Generate integration token for personal use
3. For OAuth apps, implement standard OAuth 2.0 flow
4. Store access token securely

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| 401 Unauthorized | Invalid or expired token | Generate new access token |
| 403 Forbidden | Action not permitted | Check account permissions |
| 429 Rate Limited | Too many requests | Implement rate limiting |
| 6000 Invalid Content | Markdown parsing failed | Validate content format |

## Notes

- Free tier allows 3 article reads per month for non-members
- Medium Partner Program allows monetization of articles
- API limited to publishing, reading requires browser automation
- Stories can be published to personal profile or publications
- Custom domains available for publications

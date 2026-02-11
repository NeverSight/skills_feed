---
name: connect-composio
description: Execute real actions across 1000+ applications (Gmail, Slack, GitHub, Notion, etc.) using Composio's tool routing. Stop suggesting—start doing.
original_source: https://github.com/founderjourney/awesome-claude-skills/tree/master/connect
author: founderjourney
license: MIT
---

# Connect (Composio Integration)

This skill enables Claude to perform actual actions across 1000+ applications rather than merely suggesting or describing them.

## The Difference

**Without Connect:**
> "Here's a draft email you can send..."
> "You could create a GitHub issue with..."

**With Connect:**
> "Email sent to team@company.com"
> "GitHub issue #234 created in your-repo"

## Supported Integrations

### Communication
- **Email**: Gmail, Outlook, Yahoo
- **Messaging**: Slack, Discord, Microsoft Teams
- **Video**: Zoom, Google Meet

### Development
- **Code**: GitHub, GitLab, Bitbucket
- **Projects**: Jira, Linear, Asana
- **Docs**: Notion, Confluence

### Productivity
- **Docs**: Google Docs, Sheets, Drive
- **Notes**: Notion, Evernote
- **Calendar**: Google Calendar, Outlook

### Business
- **CRM**: Salesforce, HubSpot
- **Database**: PostgreSQL, MySQL
- **Storage**: AWS S3, Dropbox

### Social
- **Twitter/X, LinkedIn, Facebook**
- **Instagram, YouTube**

## Setup

### 1. Get API Key
Visit [platform.composio.dev](https://platform.composio.dev) for a free API key.

### 2. Set Environment Variable
```bash
export COMPOSIO_API_KEY="your-key-here"
```

### 3. Install Package
```bash
# Python
pip install composio

# TypeScript
npm install @composio/core
```

## How to Use

### Send Email
```
Send an email to john@example.com with subject "Meeting Tomorrow"
and body "Hi John, let's meet at 2pm. Best, [Name]"
```

### Create GitHub Issue
```
Create a GitHub issue in my-org/my-repo:
Title: "Bug: Login fails on Safari"
Body: "Users report login issues on Safari 16+"
Labels: bug, priority-high
```

### Post to Slack
```
Post to #engineering channel:
"Deployment complete! v2.3.0 is now live."
```

### Create Notion Page
```
Create a Notion page in my workspace:
Title: "Q1 Planning"
Content: [meeting notes here]
```

### Schedule Meeting
```
Create a Google Calendar event:
Title: "Team Sync"
When: Tomorrow at 3pm
Duration: 30 minutes
Attendees: team@company.com
```

## Authentication Flow

**First time using an app:**
```
To send emails, I need Gmail access.
Authorize here: [OAuth link]
```

After authorization, the connection persists for future requests.

## Framework Compatibility

Works with:
- Claude Agent SDK
- OpenAI Agents
- Vercel AI SDK
- LangChain
- MCP (Model Context Protocol)

## Common Workflows

### Daily Standup Automation
```
1. Pull yesterday's completed GitHub issues
2. Post summary to Slack #standup
3. Create today's task list in Notion
```

### Meeting Follow-up
```
1. Summarize meeting notes
2. Create action items in Jira
3. Email summary to attendees
4. Schedule follow-up meeting
```

### Content Publishing
```
1. Review draft in Google Docs
2. Create social media posts
3. Schedule on Twitter and LinkedIn
4. Track in spreadsheet
```

## Best Practices

1. **Authorize Once**: Set up connections before heavy usage
2. **Confirm Actions**: Review before executing in production
3. **Batch Operations**: Group related actions together
4. **Error Handling**: Always check confirmation messages
5. **Respect Limits**: Be mindful of API rate limits

## Security

- OAuth-based authentication
- No passwords stored
- Permissions can be revoked anytime
- Scoped access per application

## Troubleshooting

**"App not connected"**
- Click the authorization link provided
- Complete OAuth flow
- Retry the action

**"Rate limited"**
- Wait a few minutes
- Reduce request frequency
- Check API quotas

**"Permission denied"**
- Re-authorize with correct scopes
- Check organization permissions

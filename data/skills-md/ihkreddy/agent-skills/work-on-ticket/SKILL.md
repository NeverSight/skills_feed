---
name: work-on-ticket
description: Pulls ticket details from Jira, creates feature branches with proper naming conventions, and handles planning steps. Use when starting work on a Jira ticket, creating branches for tickets, or when users mention "work on ticket", "start ticket", "create branch for", or Jira ticket IDs.
license: MIT
metadata:
  author: agent-skills-demo
  version: "1.0"
  category: development
compatibility: Requires Python 3.8+ with requests library, git, and Jira API access
---

# Work on Ticket Skill

## When to Use This Skill

Use this skill when:
- Starting work on a Jira ticket
- Creating a feature branch for a ticket
- Fetching ticket details and acceptance criteria
- Setting up workspace for new development work
- Users mention ticket IDs like "PROJ-123" or "work on ticket"

## Prerequisites

### 1. Jira API Authentication

**This project is configured for https://ihkreddy.atlassian.net/**

Edit `work-on-ticket/.jira-config` with your credentials:

```ini
[DEFAULT]
default_profile = ihkreddy

[ihkreddy]
url = https://ihkreddy.atlassian.net
email = your-email@example.com
token = your-api-token
```

**To get your Jira API token:**
1. Go to https://id.atlassian.com/manage-profile/security/api-tokens
2. Click "Create API token"
3. Give it a name (e.g., "Agent Skills")
4. Copy the token and paste it in `.jira-config`

**Security**: This file is in `.gitignore` - never committed to git.

### 2. Git Configuration

Ensure git is configured:
```bash
git config --global user.name "Your Name"
git config --global user.email "your-email@example.com"
```

## Workflow Process

### 1. Fetch Ticket Details

**Use the script:**
```bash
python scripts/fetch-ticket.py --ticket PROJ-123
```

This retrieves:
- Ticket summary and description
- Status and priority
- Assignee and reporter
- Acceptance criteria
- Related tickets
- Comments and attachments

**API call structure:**
```python
import requests
from requests.auth import HTTPBasicAuth

def fetch_ticket(ticket_id):
    url = f"{JIRA_URL}/rest/api/3/issue/{ticket_id}"
    
    auth = HTTPBasicAuth(JIRA_EMAIL, JIRA_API_TOKEN)
    
    response = requests.get(url, auth=auth)
    return response.json()
```

### 2. Create Feature Branch

**Automatic branch creation:**
```bash
python scripts/create-branch.py --ticket PROJ-123
```

This will:
1. Fetch the ticket details
2. Generate branch name following conventions
3. Create and checkout the branch
4. Optionally update ticket status to "In Progress"

**Branch naming conventions:**
- Feature: `feature/PROJ-123-short-description`
- Bug fix: `bugfix/PROJ-123-short-description`
- Hotfix: `hotfix/PROJ-123-short-description`

**Manual branch creation:**
```bash
# Fetch ticket info first
python scripts/fetch-ticket.py --ticket PROJ-123

# Create branch manually
git checkout -b feature/PROJ-123-add-user-authentication
```

### 3. Display Ticket Context

**Get formatted ticket summary:**
```bash
python scripts/fetch-ticket.py --ticket PROJ-123 --format markdown
```

Output example:
```markdown
# [PROJ-123] Add User Authentication

**Type:** Story
**Status:** To Do
**Priority:** High
**Assignee:** John Doe

## Description
Implement user authentication system with OAuth 2.0 support.

## Acceptance Criteria
- [ ] Users can log in with email/password
- [ ] OAuth 2.0 integration with Google
- [ ] Session management implemented
- [ ] Password reset functionality

## Technical Notes
- Use JWT for tokens
- Store hashed passwords with bcrypt
- Rate limit login attempts
```

### 4. Update Ticket Status

**Transition ticket to "In Progress":**
```bash
python scripts/update-ticket.py --ticket PROJ-123 --status "In Progress"
```

**Add work log:**
```bash
python scripts/update-ticket.py --ticket PROJ-123 --log-work "2h" --comment "Set up authentication scaffolding"
```

### 5. Complete Workflow

**Full workflow in one command:**
```bash
python scripts/start-work.py --ticket PROJ-123
```

This will:
1. ✅ Fetch ticket details
2. ✅ Display summary and acceptance criteria
3. ✅ Create feature branch with proper naming
4. ✅ Transition ticket to "In Progress"
5. ✅ Assign ticket to you (if not assigned)
6. ✅ Add comment: "Started working on this ticket"

## Script Reference

### fetch-ticket.py

Retrieves complete ticket information from Jira.

**Usage:**
```bash
# Basic fetch
python scripts/fetch-ticket.py --ticket PROJ-123

# With formatting
python scripts/fetch-ticket.py --ticket PROJ-123 --format markdown

# Include comments
python scripts/fetch-ticket.py --ticket PROJ-123 --include-comments

# Save to file
python scripts/fetch-ticket.py --ticket PROJ-123 --output ticket-details.md
```

### create-branch.py

Creates git branch based on ticket information.

**Usage:**
```bash
# Auto-generate branch name
python scripts/create-branch.py --ticket PROJ-123

# Custom branch name
python scripts/create-branch.py --ticket PROJ-123 --name "feature/custom-name"

# Specify branch type
python scripts/create-branch.py --ticket PROJ-123 --type bugfix

# Update ticket status
python scripts/create-branch.py --ticket PROJ-123 --update-status
```

### update-ticket.py

Updates ticket status and adds information.

**Usage:**
```bash
# Change status
python scripts/update-ticket.py --ticket PROJ-123 --status "In Progress"

# Add comment
python scripts/update-ticket.py --ticket PROJ-123 --comment "Working on authentication module"

# Log work time
python scripts/update-ticket.py --ticket PROJ-123 --log-work "3h" --comment "Completed OAuth integration"

# Assign to user
python scripts/update-ticket.py --ticket PROJ-123 --assign "john.doe@example.com"
```

### start-work.py

Complete workflow automation - fetches ticket, creates branch, updates status.

**Usage:**
```bash
# Full automated workflow
python scripts/start-work.py --ticket PROJ-123

# Custom branch type
python scripts/start-work.py --ticket PROJ-123 --branch-type bugfix

# Skip status update
python scripts/start-work.py --ticket PROJ-123 --no-status-update
```

## Jira API Reference

See [references/JIRA-API.md](references/JIRA-API.md) for detailed API documentation.

**Common endpoints:**
- Get issue: `GET /rest/api/3/issue/{issueIdOrKey}`
- Update issue: `PUT /rest/api/3/issue/{issueIdOrKey}`
- Transitions: `POST /rest/api/3/issue/{issueIdOrKey}/transitions`
- Add comment: `POST /rest/api/3/issue/{issueIdOrKey}/comment`
- Log work: `POST /rest/api/3/issue/{issueIdOrKey}/worklog`

## Branch Naming Standards

**Format:**
```
<type>/<ticket-id>-<short-description>
```

**Types:**
- `feature/` - New features or enhancements
- `bugfix/` - Bug fixes
- `hotfix/` - Urgent production fixes
- `refactor/` - Code refactoring
- `docs/` - Documentation updates
- `test/` - Test additions or updates

**Description rules:**
- Use lowercase
- Separate words with hyphens
- Max 50 characters
- Be descriptive but concise

**Examples:**
```
feature/PROJ-123-user-authentication
bugfix/PROJ-456-fix-login-validation
hotfix/PROJ-789-patch-security-vulnerability
refactor/PROJ-234-optimize-database-queries
```

## Best Practices

### 1. Always Fetch Before Creating Branch
```bash
# Good: Check ticket details first
python scripts/fetch-ticket.py --ticket PROJ-123
python scripts/create-branch.py --ticket PROJ-123

# Better: Use automated workflow
python scripts/start-work.py --ticket PROJ-123
```

### 2. Keep Branches Up to Date
```bash
# Before starting work
git checkout main
git pull origin main
python scripts/create-branch.py --ticket PROJ-123
```

### 3. Link Commits to Tickets
```bash
# Include ticket ID in commit messages
git commit -m "PROJ-123: Implement OAuth authentication"
git commit -m "PROJ-123: Add login form validation"
```

### 4. Update Ticket Status Regularly
```bash
# When starting
python scripts/update-ticket.py --ticket PROJ-123 --status "In Progress"

# When ready for review
python scripts/update-ticket.py --ticket PROJ-123 --status "In Review"

# When completed
python scripts/update-ticket.py --ticket PROJ-123 --status "Done"
```

### 5. Log Your Time
```bash
# Log work with comments
python scripts/update-ticket.py --ticket PROJ-123 \
  --log-work "2h 30m" \
  --comment "Implemented OAuth flow and tests"
```

## Troubleshooting

### Authentication Errors

**Problem:** `401 Unauthorized`

**Solution:**
```bash
# Verify credentials
echo $JIRA_URL
echo $JIRA_EMAIL
# DON'T echo API token for security

# Re-generate API token if needed
# Visit: https://id.atlassian.com/manage-profile/security/api-tokens
```

### Ticket Not Found

**Problem:** `404 Not Found`

**Solution:**
- Verify ticket ID format (e.g., `PROJ-123`, not `proj-123`)
- Check if ticket exists in your Jira instance
- Ensure you have permission to view the ticket

### Branch Creation Fails

**Problem:** Branch already exists

**Solution:**
```bash
# Check existing branches
git branch -a

# Delete local branch if needed
git branch -D feature/PROJ-123-description

# Force create new branch
git checkout -b feature/PROJ-123-new-description
```

### Transition Errors

**Problem:** Cannot transition ticket status

**Solution:**
```bash
# Get available transitions
python scripts/fetch-ticket.py --ticket PROJ-123 --show-transitions

# Use exact transition name
python scripts/update-ticket.py --ticket PROJ-123 --status "In Progress"
```

## Configuration

### Custom Branch Prefixes

Edit `scripts/config.py`:
```python
BRANCH_PREFIXES = {
    'Story': 'feature',
    'Bug': 'bugfix',
    'Task': 'task',
    'Epic': 'epic',
    'Subtask': 'feature'
}
```

### Status Mappings

Configure status transitions:
```python
STATUS_MAPPINGS = {
    'start': 'In Progress',
    'review': 'In Review',
    'done': 'Done',
    'blocked': 'Blocked'
}
```

## Integration with Other Tools

### VS Code Integration

Add to `.vscode/tasks.json`:
```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Start Work on Ticket",
      "type": "shell",
      "command": "python scripts/start-work.py --ticket ${input:ticketId}",
      "problemMatcher": []
    }
  ],
  "inputs": [
    {
      "id": "ticketId",
      "type": "promptString",
      "description": "Enter Jira ticket ID"
    }
  ]
}
```

### Git Hooks

Add to `.git/hooks/commit-msg`:
```bash
#!/bin/bash
# Ensure commit messages include ticket ID

commit_msg=$(cat "$1")
if ! echo "$commit_msg" | grep -qE "^[A-Z]+-[0-9]+:"; then
    echo "Error: Commit message must start with ticket ID (e.g., PROJ-123:)"
    exit 1
fi
```

## Example Workflow

```bash
# 1. Morning standup - pick up ticket
python scripts/start-work.py --ticket PROJ-123

# Output:
# ✓ Fetched ticket: [PROJ-123] Add User Authentication
# ✓ Created branch: feature/PROJ-123-add-user-authentication
# ✓ Updated status: In Progress
# ✓ Added comment: Started working on this ticket
# 
# Ready to code! 🚀

# 2. Work on feature
# ... code, code, code ...

# 3. Make commits with ticket ID
git add .
git commit -m "PROJ-123: Implement OAuth 2.0 flow"
git commit -m "PROJ-123: Add password hashing with bcrypt"

# 4. Log time periodically
python scripts/update-ticket.py --ticket PROJ-123 --log-work "3h"

# 5. Push and create PR
git push origin feature/PROJ-123-add-user-authentication

# 6. Update ticket for review
python scripts/update-ticket.py --ticket PROJ-123 --status "In Review"
```

## Security Notes

- ⚠️ Never commit API tokens to version control
- ⚠️ Use environment variables for credentials
- ⚠️ Rotate API tokens regularly
- ⚠️ Use read-only tokens when possible
- ⚠️ Limit token scope to required permissions

## Tips for Efficiency

1. **Create aliases** for common commands:
   ```bash
   alias jira-fetch="python work-on-ticket/scripts/fetch-ticket.py --ticket"
   alias jira-start="python work-on-ticket/scripts/start-work.py --ticket"
   ```

2. **Use shell functions** for quick access:
   ```bash
   function start-ticket() {
       cd ~/Agents/AgentSkills
       python work-on-ticket/scripts/start-work.py --ticket $1
   }
   ```

3. **Bookmark Jira board** for quick reference

4. **Set up notifications** for ticket updates

5. **Use JQL filters** for finding your tickets:
   ```
   assignee = currentUser() AND status = "To Do" ORDER BY priority DESC
   ```

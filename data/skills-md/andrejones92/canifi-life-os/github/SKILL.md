---
name: github
description: Manage repositories, check issues and PRs, view CI status, and collaborate on GitHub
category: devops
---

# GitHub Skill

## Overview
Enables Claude to access GitHub to manage repositories, review pull requests, check CI/CD status, monitor issues, and collaborate on code through the world's largest code hosting platform.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/github/install.sh | bash
```

Or manually:
```bash
cp -r skills/github ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set GITHUB_EMAIL "your-email@example.com"
canifi-env set GITHUB_USERNAME "your-username"
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
- View repositories and code
- Check pull request status and reviews
- Monitor GitHub Actions workflows
- View and triage issues
- Check repository insights
- Manage project boards

## Usage Examples

### Example 1: Check PR Status
```
User: "What's the status of my open PRs?"
Claude: I'll check your GitHub pull requests.
- Opens github.com via Playwright MCP
- Logs into account
- Open PRs:
  - #234 "Add user auth": Ready for review, 2 approvals
  - #235 "Fix bug in API": Changes requested
  - #238 "Update deps": CI passing, awaiting review
- Assigned to review: 3 PRs
- Total open: 6 PRs
```

### Example 2: Check CI Status
```
User: "Did the build pass on main?"
Claude: I'll check the Actions status.
- Navigates to Actions tab
- Main branch status:
  - Latest commit: Passed (5 min ago)
  - Tests: 234/234 passed
  - Build: Completed in 3m 45s
  - Deploy: Successful to staging
- Last 5 runs: All green
```

### Example 3: Review Issues
```
User: "What issues need attention?"
Claude: I'll check the issue queue.
- Views issues list
- Open issues: 23
- Priority issues:
  - #145 "Login broken" - Bug, High priority
  - #149 "API timeout" - Bug, Assigned to you
  - #152 "Feature request" - Enhancement
- Stale issues (30+ days): 5
- Unassigned: 8
```

## Authentication Flow
1. Navigate to github.com via Playwright MCP
2. Enter username or email
3. Enter password
4. Handle 2FA via authenticator or SMS
5. May require device verification
6. Maintain session for operations

## Error Handling
- Login Failed: Retry, check credentials
- 2FA Required: Complete verification
- Rate Limited: Wait and retry (API limits)
- Session Expired: Re-authenticate
- Repo Not Found: Check permissions
- Action Failed: View logs for details

## Self-Improvement Instructions
After each interaction:
- Track common operations
- Note repository patterns
- Log CI/CD monitoring frequency
- Document UI changes

Suggest updates when:
- GitHub updates interface
- New features added
- Actions updated
- Security features change

## Notes
- Claude can read and suggest changes
- PR creation requires careful review
- Actions have usage limits
- Codespaces for dev environments
- Security alerts important
- Dependabot for updates
- Discussions for community

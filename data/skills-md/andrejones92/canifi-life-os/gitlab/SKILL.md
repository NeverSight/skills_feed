---
name: gitlab
description: Manage repositories, check pipelines, review merge requests, and monitor CI/CD on GitLab
category: devops
---

# GitLab Skill

## Overview
Enables Claude to access GitLab to manage repositories, review merge requests, check CI/CD pipelines, monitor issues, and manage the complete DevOps lifecycle.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/gitlab/install.sh | bash
```

Or manually:
```bash
cp -r skills/gitlab ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set GITLAB_EMAIL "your-email@example.com"
canifi-env set GITLAB_USERNAME "your-username"
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
- Check merge request status
- Monitor CI/CD pipelines
- View and manage issues
- Check container registry
- Manage project settings

## Usage Examples

### Example 1: Check Pipeline Status
```
User: "What's the pipeline status?"
Claude: I'll check your GitLab pipelines.
- Opens gitlab.com via Playwright MCP
- Logs into account
- Pipeline status:
  - Latest (main): Passed - 4m 23s
  - Jobs: Build (passed), Test (passed), Deploy (passed)
  - Coverage: 87%
- Recent pipelines: 4/5 passing
- Failed: MR !234 needs attention
```

### Example 2: Review Merge Requests
```
User: "Show my open merge requests"
Claude: I'll check your MRs.
- Views merge requests
- Open MRs:
  - !456 "Feature: User dashboard" - Ready to merge
  - !457 "Fix: API response" - Pipeline running
  - !458 "Docs update" - Needs review
- Assigned to you: 2 for review
- Draft MRs: 1
```

### Example 3: Check Issues
```
User: "What issues are assigned to me?"
Claude: I'll check your assigned issues.
- Views issue board
- Assigned issues:
  - #89 "Performance optimization" - In Progress
  - #92 "Database migration" - To Do
  - #95 "API documentation" - To Do
- Due this week: 2
- Overdue: 0
```

## Authentication Flow
1. Navigate to gitlab.com via Playwright MCP
2. Enter username or email
3. Enter password
4. Handle 2FA if enabled
5. Maintain session for operations

## Error Handling
- Login Failed: Retry credentials
- 2FA Required: Complete verification
- Pipeline Failed: Check job logs
- Session Expired: Re-authenticate
- Permission Denied: Check project access
- Rate Limited: Wait and retry

## Self-Improvement Instructions
After each interaction:
- Track pipeline patterns
- Note MR workflow preferences
- Log CI/CD monitoring frequency
- Document UI changes

Suggest updates when:
- GitLab updates interface
- New CI/CD features added
- DevSecOps features expand
- Integration changes

## Notes
- Complete DevOps platform
- Self-hosted option available
- Auto DevOps for automation
- Container registry built-in
- Security scanning included
- Package registry support
- Wiki and snippets features

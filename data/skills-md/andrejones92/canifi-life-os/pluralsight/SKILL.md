---
name: pluralsight
description: Access Pluralsight tech and creative courses for professionals
category: education
---

# Pluralsight Skill

## Overview
Enables Claude to interact with Pluralsight for accessing technology courses, tracking skill development, taking assessments, and following role-based learning paths.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/pluralsight/install.sh | bash
```

Or manually:
```bash
cp -r skills/pluralsight ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set PLURALSIGHT_EMAIL "your-email@example.com"
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
- Browse tech and creative courses
- Take skill assessments (Skill IQ)
- Track course completion progress
- Follow role-based paths
- Access hands-on labs

## Usage Examples
### Example 1: Skill Assessment
```
User: "What's my Skill IQ in JavaScript?"
Claude: I'll check your JavaScript Skill IQ score on Pluralsight.
```

### Example 2: Course Progress
```
User: "How far am I in my Azure courses?"
Claude: I'll check your progress in Azure-related courses.
```

### Example 3: Learning Path
```
User: "What's in the Cloud Developer path?"
Claude: I'll show the courses and skills in the Cloud Developer path.
```

## Authentication Flow
1. Navigate to pluralsight.com via Playwright MCP
2. Click "Sign in" button
3. Enter Pluralsight credentials
4. Handle SSO or verification if required
5. Maintain session for subsequent requests

## Error Handling
- Login Failed: Retry authentication up to 3 times, then notify via iMessage
- Session Expired: Re-authenticate automatically
- SSO Required: Handle enterprise SSO flow
- Rate Limited: Implement exponential backoff
- Subscription Required: Check account access

## Self-Improvement Instructions
When encountering new UI patterns:
1. Document Pluralsight interface changes
2. Update selectors for new layouts
3. Track new course and path additions
4. Monitor Skill IQ updates

## Notes
- Enterprise and individual plans
- Skill IQ for competency assessment
- Role IQ for career guidance
- Hands-on labs for practice

---
name: codecademy
description: Access Codecademy coding courses and track programming progress
category: education
---

# Codecademy Skill

## Overview
Enables Claude to interact with Codecademy for learning to code, tracking course progress, completing coding exercises, and earning certificates in various programming languages.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/codecademy/install.sh | bash
```

Or manually:
```bash
cp -r skills/codecademy ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set CODECADEMY_EMAIL "your-email@example.com"
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
- Browse programming courses
- Complete interactive coding exercises
- Track course completion progress
- Follow career paths
- Earn skill certificates

## Usage Examples
### Example 1: Course Progress
```
User: "How far am I in the Python course on Codecademy?"
Claude: I'll check your Python course progress and next lessons.
```

### Example 2: Find Courses
```
User: "What web development courses does Codecademy have?"
Claude: I'll browse web development courses and paths.
```

### Example 3: Career Paths
```
User: "What's in the Data Science career path?"
Claude: I'll show the courses and skills in the Data Science path.
```

## Authentication Flow
1. Navigate to codecademy.com via Playwright MCP
2. Click "Log In" button
3. Enter Codecademy credentials
4. Handle verification if required
5. Maintain session for subsequent requests

## Error Handling
- Login Failed: Retry authentication up to 3 times, then notify via iMessage
- Session Expired: Re-authenticate automatically
- Verification Required: Complete email verification
- Rate Limited: Implement exponential backoff
- Pro Required: Check subscription for career paths

## Self-Improvement Instructions
When encountering new UI patterns:
1. Document Codecademy interface changes
2. Update selectors for new layouts
3. Track new language/framework courses
4. Monitor career path updates

## Notes
- Interactive in-browser coding
- Free basic courses available
- Pro subscription for full access
- Career paths for job preparation

---
name: linkedin-learning
description: Access LinkedIn Learning courses and track professional development
category: education
---

# LinkedIn Learning Skill

## Overview
Enables Claude to interact with LinkedIn Learning for browsing professional courses, tracking learning progress, earning certificates, and developing career skills.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/linkedin-learning/install.sh | bash
```

Or manually:
```bash
cp -r skills/linkedin-learning ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set LINKEDIN_EMAIL "your-email@example.com"
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
- Browse business and tech courses
- Track course completion progress
- Earn and share certificates
- Follow learning paths
- Access saved courses

## Usage Examples
### Example 1: Find Courses
```
User: "Find me project management courses on LinkedIn Learning"
Claude: I'll search for top project management courses.
```

### Example 2: Learning Paths
```
User: "What learning paths are recommended for me?"
Claude: I'll check personalized learning path recommendations.
```

### Example 3: Certificates
```
User: "What certificates have I earned on LinkedIn Learning?"
Claude: I'll list your completed course certificates.
```

## Authentication Flow
1. Navigate to linkedin.com/learning via Playwright MCP
2. Sign in with LinkedIn credentials
3. Handle 2FA if enabled
4. Access Learning platform
5. Maintain session for subsequent requests

## Error Handling
- Login Failed: Retry authentication up to 3 times, then notify via iMessage
- Session Expired: Re-authenticate with LinkedIn
- 2FA Required: Wait for code via authenticator
- Rate Limited: Implement exponential backoff
- Premium Required: Check subscription status

## Self-Improvement Instructions
When encountering new UI patterns:
1. Document LinkedIn Learning interface changes
2. Update selectors for new layouts
3. Track new course additions
4. Monitor learning path updates

## Notes
- Requires LinkedIn Premium or Learning subscription
- Certificates display on LinkedIn profile
- Curated learning paths for careers
- Exercise files for hands-on practice

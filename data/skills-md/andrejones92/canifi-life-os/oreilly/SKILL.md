---
name: oreilly
description: Access O'Reilly Media books, videos, and learning platform
category: education
---

# O'Reilly Skill

## Overview
Enables Claude to interact with O'Reilly Learning Platform for accessing technical books, video courses, live events, and tracking reading and learning progress.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/oreilly/install.sh | bash
```

Or manually:
```bash
cp -r skills/oreilly ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set OREILLY_EMAIL "your-email@example.com"
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
- Browse books and video courses
- Track reading progress
- Access live events and conferences
- Search technical documentation
- Create and manage playlists

## Usage Examples
### Example 1: Find Books
```
User: "Find O'Reilly books on Kubernetes"
Claude: I'll search for Kubernetes books on O'Reilly Learning.
```

### Example 2: Reading Progress
```
User: "What books am I currently reading?"
Claude: I'll check your in-progress books on O'Reilly.
```

### Example 3: Live Events
```
User: "What O'Reilly events are coming up?"
Claude: I'll check for upcoming live training and conferences.
```

## Authentication Flow
1. Navigate to learning.oreilly.com via Playwright MCP
2. Click "Sign In" button
3. Enter O'Reilly credentials or SSO
4. Handle verification if required
5. Maintain session for subsequent requests

## Error Handling
- Login Failed: Retry authentication up to 3 times, then notify via iMessage
- Session Expired: Re-authenticate automatically
- SSO Required: Handle enterprise SSO flow
- Rate Limited: Implement exponential backoff
- Subscription Required: Check account access

## Self-Improvement Instructions
When encountering new UI patterns:
1. Document O'Reilly platform changes
2. Update selectors for new layouts
3. Track new book and video releases
4. Monitor live event schedules

## Notes
- Safari Books Online legacy name
- Extensive technical library
- Live online training available
- Enterprise and individual plans

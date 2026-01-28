---
name: khan-academy
description: Access Khan Academy courses and track learning progress
category: education
---

# Khan Academy Skill

## Overview
Enables Claude to interact with Khan Academy for accessing free educational content, tracking learning progress, earning mastery points, and following personalized learning paths.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/khan-academy/install.sh | bash
```

Or manually:
```bash
cp -r skills/khan-academy ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set KHAN_EMAIL "your-email@example.com"
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
- Browse courses across subjects
- Track mastery progress
- View energy points and badges
- Follow learning recommendations
- Access practice exercises

## Usage Examples
### Example 1: Course Progress
```
User: "How's my progress in calculus on Khan Academy?"
Claude: I'll check your calculus course mastery and recent lessons.
```

### Example 2: Find Content
```
User: "Find me videos on physics on Khan Academy"
Claude: I'll search for physics content and show available units.
```

### Example 3: Badges
```
User: "What badges have I earned on Khan Academy?"
Claude: I'll list your earned badges and energy points.
```

## Authentication Flow
1. Navigate to khanacademy.org via Playwright MCP
2. Click "Log in" button
3. Enter credentials or use Google/Apple login
4. Handle verification if required
5. Maintain session for subsequent requests

## Error Handling
- Login Failed: Retry authentication up to 3 times, then notify via iMessage
- Session Expired: Re-authenticate automatically
- Verification Required: Complete email verification
- Rate Limited: Implement exponential backoff
- Content Load: Wait for video/exercise loading

## Self-Improvement Instructions
When encountering new UI patterns:
1. Document Khan Academy interface changes
2. Update selectors for new layouts
3. Track new course additions
4. Monitor mastery system updates

## Notes
- Completely free educational platform
- K-12 and beyond content
- Personalized learning dashboard
- SAT and test prep available

---
name: datacamp
description: Access DataCamp data science and analytics courses
category: education
---

# DataCamp Skill

## Overview
Enables Claude to interact with DataCamp for learning data science, tracking course progress, completing coding exercises, and following career tracks in Python, R, SQL, and more.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/datacamp/install.sh | bash
```

Or manually:
```bash
cp -r skills/datacamp ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set DATACAMP_EMAIL "your-email@example.com"
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
- Browse data science courses
- Complete interactive exercises
- Track skill and course progress
- Follow career and skill tracks
- Earn certifications

## Usage Examples
### Example 1: Course Progress
```
User: "How's my progress in the SQL fundamentals course?"
Claude: I'll check your SQL course progress on DataCamp.
```

### Example 2: Track Status
```
User: "What's left in my Data Analyst track?"
Claude: I'll show remaining courses in your Data Analyst career track.
```

### Example 3: Daily Practice
```
User: "Show me my DataCamp daily practice"
Claude: I'll check your daily practice streak and suggested exercises.
```

## Authentication Flow
1. Navigate to datacamp.com via Playwright MCP
2. Click "Log In" button
3. Enter DataCamp credentials
4. Handle verification if required
5. Maintain session for subsequent requests

## Error Handling
- Login Failed: Retry authentication up to 3 times, then notify via iMessage
- Session Expired: Re-authenticate automatically
- Verification Required: Complete email verification
- Rate Limited: Implement exponential backoff
- Premium Required: Check subscription status

## Self-Improvement Instructions
When encountering new UI patterns:
1. Document DataCamp interface changes
2. Update selectors for new layouts
3. Track new course and track additions
4. Monitor certification programs

## Notes
- Focus on data science skills
- In-browser coding environment
- Python, R, SQL, and more
- Career tracks for job roles

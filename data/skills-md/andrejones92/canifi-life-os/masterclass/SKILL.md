---
name: masterclass
description: Access MasterClass lessons from world-renowned experts
category: education
---

# MasterClass Skill

## Overview
Enables Claude to interact with MasterClass for accessing expert-led video lessons, tracking progress through classes, exploring different categories, and discovering new instructors.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/masterclass/install.sh | bash
```

Or manually:
```bash
cp -r skills/masterclass ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set MASTERCLASS_EMAIL "your-email@example.com"
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
- Browse classes by category and instructor
- Track lesson completion progress
- Access class workbooks and materials
- View instructor filmographies
- Discover recommended classes

## Usage Examples
### Example 1: Browse Classes
```
User: "What cooking classes are on MasterClass?"
Claude: I'll browse the culinary arts section for cooking classes.
```

### Example 2: Progress Check
```
User: "How far am I in Gordon Ramsay's class?"
Claude: I'll check your progress in Gordon Ramsay's cooking MasterClass.
```

### Example 3: New Classes
```
User: "What new MasterClasses were added recently?"
Claude: I'll check for recently added classes and instructors.
```

## Authentication Flow
1. Navigate to masterclass.com via Playwright MCP
2. Click "Log In" button
3. Enter MasterClass credentials
4. Handle verification if required
5. Maintain session for subsequent requests

## Error Handling
- Login Failed: Retry authentication up to 3 times, then notify via iMessage
- Session Expired: Re-authenticate automatically
- Verification Required: Complete email verification
- Rate Limited: Implement exponential backoff
- Subscription Required: Check membership status

## Self-Improvement Instructions
When encountering new UI patterns:
1. Document MasterClass interface changes
2. Update selectors for new layouts
3. Track new instructor additions
4. Monitor class category updates

## Notes
- Celebrity and expert instructors
- High production quality videos
- Downloadable workbooks
- Annual subscription model

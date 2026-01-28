---
name: udemy
description: Access Udemy courses, track learning progress, and manage course library
category: education
---

# Udemy Skill

## Overview
Enables Claude to interact with Udemy for browsing courses, tracking learning progress, managing purchased courses, and discovering new learning opportunities.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/udemy/install.sh | bash
```

Or manually:
```bash
cp -r skills/udemy ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set UDEMY_EMAIL "your-email@example.com"
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
- Browse and discover courses
- Track course completion progress
- Access purchased course library
- View course Q&A and notes
- Check for sales and discounts

## Usage Examples
### Example 1: Course Progress
```
User: "How far am I in my Python course on Udemy?"
Claude: I'll check your progress in your Python courses.
```

### Example 2: Find Sales
```
User: "Are there any good Udemy sales right now?"
Claude: I'll check for current Udemy promotions and discounts.
```

### Example 3: My Library
```
User: "What courses do I own on Udemy?"
Claude: I'll list all courses in your Udemy library.
```

## Authentication Flow
1. Navigate to udemy.com via Playwright MCP
2. Click "Log In" button
3. Enter Udemy credentials
4. Handle verification if required
5. Maintain session for subsequent requests

## Error Handling
- Login Failed: Retry authentication up to 3 times, then notify via iMessage
- Session Expired: Re-authenticate automatically
- Verification Required: Complete email verification
- Rate Limited: Implement exponential backoff
- Course Access: Verify purchase status

## Self-Improvement Instructions
When encountering new UI patterns:
1. Document Udemy interface changes
2. Update selectors for new layouts
3. Track sale patterns and timing
4. Monitor new feature additions

## Notes
- Lifetime access to purchased courses
- Frequent sales and discounts
- Certificates of completion
- Mobile app for offline learning

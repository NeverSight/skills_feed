---
name: memrise
description: Learn languages with Memrise spaced repetition and native speaker videos
category: education
---

# Memrise Skill

## Overview
Enables Claude to interact with Memrise for language learning through spaced repetition, tracking vocabulary progress, watching native speaker videos, and maintaining daily streaks.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/memrise/install.sh | bash
```

Or manually:
```bash
cp -r skills/memrise ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set MEMRISE_EMAIL "your-email@example.com"
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
- Learn vocabulary with spaced repetition
- Watch native speaker video clips
- Track learning progress and streaks
- Review learned words
- Access community-created courses

## Usage Examples
### Example 1: Learning Progress
```
User: "How many words have I learned on Memrise?"
Claude: I'll check your vocabulary progress on Memrise.
```

### Example 2: Streak Check
```
User: "What's my Memrise streak?"
Claude: I'll check your daily learning streak status.
```

### Example 3: Review Words
```
User: "What words do I need to review?"
Claude: I'll check which vocabulary items are due for review.
```

## Authentication Flow
1. Navigate to memrise.com via Playwright MCP
2. Click "Log in" button
3. Enter Memrise credentials
4. Handle verification if required
5. Maintain session for subsequent requests

## Error Handling
- Login Failed: Retry authentication up to 3 times, then notify via iMessage
- Session Expired: Re-authenticate automatically
- Verification Required: Complete email verification
- Rate Limited: Implement exponential backoff
- Pro Required: Check subscription for advanced features

## Self-Improvement Instructions
When encountering new UI patterns:
1. Document Memrise interface changes
2. Update selectors for new layouts
3. Track new language additions
4. Monitor spaced repetition updates

## Notes
- Spaced repetition for retention
- Native speaker video clips
- Community-created courses
- Pro subscription for advanced features

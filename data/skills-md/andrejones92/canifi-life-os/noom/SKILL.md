---
name: noom
description: Track weight loss with Noom - view progress, lessons, and behavioral health data
category: health
---

# Noom Skill

## Overview
Enables Claude to use Noom for weight management tracking including viewing progress, accessing daily lessons, and checking food logging data.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/noom/install.sh | bash
```

Or manually:
```bash
cp -r skills/noom ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set NOOM_EMAIL "your-email@example.com"
canifi-env set NOOM_PASSWORD "your-password"
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
- View weight progress
- Access daily lessons
- Check food logging
- View behavior trends
- Access coach messages
- Check group activity

## Usage Examples

### Example 1: Check Weight Progress
```
User: "How is my weight loss progress on Noom?"
Claude: I'll check your progress.
1. Opening Noom via Playwright MCP
2. Accessing weight chart
3. Viewing trend data
4. Comparing to goal
5. Summarizing progress
```

### Example 2: View Today's Lesson
```
User: "What's my Noom lesson for today?"
Claude: I'll find today's lesson.
1. Navigating to lessons section
2. Finding current day's content
3. Summarizing lesson topic
4. Noting key takeaways
```

### Example 3: Check Food Log
```
User: "How am I doing with my Noom food logging?"
Claude: I'll review your logging.
1. Accessing food diary
2. Viewing recent entries
3. Checking color categories
4. Summarizing eating patterns
```

## Authentication Flow
1. Navigate to noom.com via Playwright MCP
2. Click "Log In" and enter email
3. Enter password
4. Handle 2FA if required (via iMessage)
5. Maintain session for data access

## Error Handling
- **Login Failed**: Retry up to 3 times, notify via iMessage
- **Session Expired**: Re-authenticate automatically
- **Rate Limited**: Implement exponential backoff
- **2FA Required**: Send iMessage notification
- **Content Locked**: Check subscription status
- **Sync Error**: Refresh and retry

## Self-Improvement Instructions
When Noom updates:
1. Document new lesson content
2. Update food logging features
3. Track coaching changes
4. Log program modifications

## Notes
- Behavioral psychology approach
- Color-coded food system
- Daily lessons and quizzes
- Coach and group support
- Subscription required

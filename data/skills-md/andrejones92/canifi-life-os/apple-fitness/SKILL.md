---
name: apple-fitness
description: Track workouts with Apple Fitness+ - view workout history, achievements, and activity data
category: health
---

# Apple Fitness+ Skill

## Overview
Enables Claude to access Apple Fitness+ content information and workout tracking through the web interface, including viewing available workouts and checking subscription status.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/apple-fitness/install.sh | bash
```

Or manually:
```bash
cp -r skills/apple-fitness ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set APPLE_EMAIL "your-email@example.com"
canifi-env set APPLE_PASSWORD "your-password"
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
- Browse workout library
- View workout categories
- Check new workout releases
- Access trainer information
- View subscription status
- Browse collections

## Usage Examples

### Example 1: Browse Workouts
```
User: "What new workouts are available on Apple Fitness+?"
Claude: I'll check new workouts.
1. Opening Apple Fitness+ via Playwright MCP
2. Navigating to workout library
3. Viewing recent additions
4. Listing new workout types
5. Summarizing available content
```

### Example 2: Find Workout Type
```
User: "Find HIIT workouts on Apple Fitness+"
Claude: I'll search for HIIT.
1. Browsing workout categories
2. Filtering to HIIT
3. Listing available sessions
4. Noting duration options
```

### Example 3: Check Trainers
```
User: "Who are the Apple Fitness+ trainers?"
Claude: I'll list the trainers.
1. Accessing trainer section
2. Listing available trainers
3. Showing their specialties
4. Providing trainer info
```

## Authentication Flow
1. Navigate to fitness.apple.com via Playwright MCP
2. Sign in with Apple ID
3. Enter password
4. Handle 2FA if required (via iMessage)
5. Maintain session for content access

## Error Handling
- **Login Failed**: Retry up to 3 times, notify via iMessage
- **Session Expired**: Re-authenticate automatically
- **Rate Limited**: Implement exponential backoff
- **2FA Required**: Send iMessage notification
- **Content Unavailable**: Check subscription status
- **Region Restricted**: Note geographic limits

## Self-Improvement Instructions
When Apple Fitness+ updates:
1. Document new workout types
2. Update trainer roster
3. Track feature additions
4. Log content organization changes

## Notes
- Requires Apple Fitness+ subscription
- Best with Apple Watch
- Limited web functionality
- Most features on Apple devices
- New workouts added weekly

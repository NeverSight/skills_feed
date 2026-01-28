---
name: oura
description: Track health with Oura Ring - view sleep, readiness, and activity scores
category: health
---

# Oura Skill

## Overview
Enables Claude to use Oura for health tracking including viewing sleep quality, readiness scores, and activity data from the Oura Ring.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/oura/install.sh | bash
```

Or manually:
```bash
cp -r skills/oura ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set OURA_EMAIL "your-email@example.com"
canifi-env set OURA_PASSWORD "your-password"
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
- View readiness score
- Check sleep analysis
- Access activity data
- View HRV trends
- Check body temperature
- Access long-term trends

## Usage Examples

### Example 1: Check Readiness
```
User: "What's my Oura readiness score today?"
Claude: I'll check your readiness.
1. Opening Oura via Playwright MCP
2. Accessing today's data
3. Viewing readiness score
4. Showing contributing factors
5. Interpreting score
```

### Example 2: Analyze Sleep
```
User: "How did I sleep last night according to Oura?"
Claude: I'll analyze your sleep.
1. Accessing sleep section
2. Viewing last night's data
3. Checking sleep stages
4. Reviewing sleep quality metrics
```

### Example 3: View Activity
```
User: "How active have I been today?"
Claude: I'll check your activity.
1. Accessing activity section
2. Viewing today's data
3. Checking movement goals
4. Summarizing activity level
```

## Authentication Flow
1. Navigate to cloud.ouraring.com via Playwright MCP
2. Click "Sign In" and enter email
3. Enter password
4. Handle 2FA if required (via iMessage)
5. Maintain session for data access

## Error Handling
- **Login Failed**: Retry up to 3 times, notify via iMessage
- **Session Expired**: Re-authenticate automatically
- **Rate Limited**: Implement exponential backoff
- **2FA Required**: Send iMessage notification
- **Sync Pending**: Wait for ring sync
- **Data Processing**: Note delay timing

## Self-Improvement Instructions
When Oura updates:
1. Document new health metrics
2. Update score calculation changes
3. Track feature additions
4. Log algorithm improvements

## Notes
- Requires Oura Ring
- Subscription for full features
- Sleep focus tracking
- Temperature deviation monitoring
- Long-term trend analysis

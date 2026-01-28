---
name: cronometer
description: Track detailed nutrition with Cronometer - monitor micronutrients, macros, and dietary intake
category: food
---

# Cronometer Skill

## Overview
Enables Claude to use Cronometer for detailed nutrition tracking including micronutrient analysis, macro monitoring, and comprehensive dietary logging.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/cronometer/install.sh | bash
```

Or manually:
```bash
cp -r skills/cronometer ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set CRONOMETER_EMAIL "your-email@example.com"
canifi-env set CRONOMETER_PASSWORD "your-password"
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
- View detailed nutrition diary
- Check micronutrient intake
- Monitor macro balance
- Access nutrition trends
- View nutrient targets
- Check biometric data

## Usage Examples

### Example 1: Check Micronutrients
```
User: "Am I getting enough vitamins today?"
Claude: I'll check your micronutrients.
1. Opening Cronometer via Playwright MCP
2. Accessing today's diary
3. Viewing vitamin intake
4. Comparing to targets
5. Identifying any gaps
```

### Example 2: View Macro Balance
```
User: "What's my macro ratio for today?"
Claude: I'll calculate your macros.
1. Accessing diary summary
2. Viewing macro totals
3. Calculating percentages
4. Comparing to target ratio
```

### Example 3: Check Nutrition Trends
```
User: "How has my protein intake been this week?"
Claude: I'll analyze your protein trends.
1. Accessing trends section
2. Filtering to protein data
3. Viewing weekly pattern
4. Summarizing average intake
```

## Authentication Flow
1. Navigate to cronometer.com via Playwright MCP
2. Click "Log In" and enter email
3. Enter password
4. Handle 2FA if required (via iMessage)
5. Maintain session for diary access

## Error Handling
- **Login Failed**: Retry up to 3 times, notify via iMessage
- **Session Expired**: Re-authenticate automatically
- **Rate Limited**: Implement exponential backoff
- **2FA Required**: Send iMessage notification
- **Data Unavailable**: Check for logged entries
- **Sync Error**: Refresh and retry

## Self-Improvement Instructions
When Cronometer updates:
1. Document new nutrient tracking
2. Update reporting features
3. Track food database changes
4. Log new biometric options

## Notes
- Most detailed nutrition tracking
- Focus on micronutrients
- Verified food database
- Gold subscription for full features
- Integrates with health devices

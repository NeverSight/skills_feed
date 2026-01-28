---
name: clue
description: Track menstrual cycles with Clue - monitor periods, symptoms, and cycle patterns
category: health
---

# Clue Skill

## Overview
Enables Claude to use Clue for menstrual cycle tracking including viewing cycle predictions, symptom patterns, and reproductive health data.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/clue/install.sh | bash
```

Or manually:
```bash
cp -r skills/clue ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set CLUE_EMAIL "your-email@example.com"
canifi-env set CLUE_PASSWORD "your-password"
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
- View cycle predictions
- Check period history
- Access symptom patterns
- View cycle statistics
- Check tracking history
- Access cycle insights

## Usage Examples

### Example 1: Check Cycle Status
```
User: "Where am I in my cycle?"
Claude: I'll check your cycle status.
1. Opening Clue via Playwright MCP
2. Accessing current cycle view
3. Identifying cycle day
4. Noting phase information
```

### Example 2: View Cycle History
```
User: "How long have my cycles been?"
Claude: I'll analyze your cycle lengths.
1. Accessing cycle history
2. Viewing past cycles
3. Calculating average length
4. Noting any variations
```

### Example 3: Check Symptom Patterns
```
User: "Do I usually get cramps before my period?"
Claude: I'll check your patterns.
1. Accessing symptom data
2. Analyzing cramp logging
3. Identifying timing patterns
4. Summarizing findings
```

## Authentication Flow
1. Navigate to helloclue.com via Playwright MCP
2. Click "Log In" and enter email
3. Enter password
4. Handle 2FA if required (via iMessage)
5. Maintain session for data access

## Error Handling
- **Login Failed**: Retry up to 3 times, notify via iMessage
- **Session Expired**: Re-authenticate automatically
- **Rate Limited**: Implement exponential backoff
- **2FA Required**: Send iMessage notification
- **Data Unavailable**: Check logging history
- **Sync Error**: Refresh and retry

## Self-Improvement Instructions
When Clue updates:
1. Document new tracking categories
2. Update prediction algorithm notes
3. Track feature additions
4. Log privacy changes

## Notes
- Science-based tracking
- Privacy-focused design
- Multiple tracking categories
- Clue Plus for advanced features
- Research collaboration

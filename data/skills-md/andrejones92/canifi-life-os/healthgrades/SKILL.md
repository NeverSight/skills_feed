---
name: healthgrades
description: Find doctors with Healthgrades - search providers, read reviews, and check credentials
category: healthcare
---

# Healthgrades Skill

## Overview
Enables Claude to use Healthgrades for finding and researching healthcare providers including searching doctors, reading patient reviews, and checking credentials.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/healthgrades/install.sh | bash
```

Or manually:
```bash
cp -r skills/healthgrades ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set HEALTHGRADES_EMAIL "your-email@example.com"
canifi-env set HEALTHGRADES_PASSWORD "your-password"
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
- Search for doctors
- Read patient reviews
- Check provider credentials
- View hospital ratings
- Compare providers
- Find specialists

## Usage Examples

### Example 1: Find a Doctor
```
User: "Find a highly rated cardiologist near me"
Claude: I'll search for cardiologists.
1. Opening Healthgrades via Playwright MCP
2. Searching for cardiologists
3. Filtering by location
4. Sorting by patient ratings
5. Listing top-rated options
```

### Example 2: Read Reviews
```
User: "What do patients say about Dr. Johnson?"
Claude: I'll check patient reviews.
1. Finding Dr. Johnson's profile
2. Accessing patient reviews
3. Summarizing feedback themes
4. Noting ratings breakdown
```

### Example 3: Check Credentials
```
User: "Is Dr. Smith board certified?"
Claude: I'll verify credentials.
1. Finding Dr. Smith's profile
2. Viewing credentials section
3. Checking board certifications
4. Noting education and training
```

## Authentication Flow
1. Navigate to healthgrades.com via Playwright MCP
2. Click "Sign in" if needed
3. Enter email and password
4. Handle 2FA if required (via iMessage)
5. Maintain session for account features

## Error Handling
- **Login Failed**: Retry up to 3 times, notify via iMessage
- **Session Expired**: Re-authenticate automatically
- **Rate Limited**: Implement exponential backoff
- **2FA Required**: Send iMessage notification
- **Provider Not Found**: Broaden search criteria
- **Data Unavailable**: Note limited info

## Self-Improvement Instructions
When Healthgrades updates:
1. Document new search filters
2. Update rating criteria changes
3. Track profile information updates
4. Log new comparison features

## Notes
- Free provider search
- Patient review platform
- Hospital quality ratings
- Malpractice history when available
- Insurance filter options

---
name: one-medical
description: Access primary care with One Medical - view appointments, message providers, and access health records
category: healthcare
---

# One Medical Skill

## Overview
Enables Claude to use One Medical for primary care management including viewing appointments, accessing health records, and communicating with care team.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/one-medical/install.sh | bash
```

Or manually:
```bash
cp -r skills/one-medical ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set ONEMEDICAL_EMAIL "your-email@example.com"
canifi-env set ONEMEDICAL_PASSWORD "your-password"
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
- View upcoming appointments
- Access visit history
- View lab results
- Check message inbox
- Access care team info
- View health records

## Usage Examples

### Example 1: Check Appointments
```
User: "Do I have any upcoming One Medical appointments?"
Claude: I'll check your appointments.
1. Opening One Medical via Playwright MCP
2. Accessing appointments section
3. Viewing scheduled visits
4. Listing upcoming appointments
```

### Example 2: View Lab Results
```
User: "Are my lab results in?"
Claude: I'll check for lab results.
1. Accessing health records
2. Viewing lab results section
3. Finding recent results
4. Summarizing available data
```

### Example 3: Check Messages
```
User: "Do I have any messages from my One Medical provider?"
Claude: I'll check your inbox.
1. Accessing message center
2. Viewing recent messages
3. Listing provider communications
4. Summarizing message content
```

## Authentication Flow
1. Navigate to onemedical.com via Playwright MCP
2. Click "Sign in" and enter email
3. Enter password
4. Handle 2FA if required (via iMessage)
5. Maintain session for account access

## Error Handling
- **Login Failed**: Retry up to 3 times, notify via iMessage
- **Session Expired**: Re-authenticate automatically
- **Rate Limited**: Implement exponential backoff
- **2FA Required**: Send iMessage notification
- **Records Unavailable**: Check account status
- **Appointment Error**: Suggest alternatives

## Self-Improvement Instructions
When One Medical updates:
1. Document new care features
2. Update telehealth options
3. Track portal changes
4. Log integration updates

## Notes
- Now part of Amazon
- Membership-based primary care
- Same-day appointments
- Virtual and in-person visits
- 24/7 on-demand care

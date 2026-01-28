---
name: labcorp
description: Access lab results with Labcorp - view test results, check appointments, and manage patient portal
category: healthcare
---

# Labcorp Skill

## Overview
Enables Claude to use Labcorp for lab testing services including viewing test results, checking appointment status, and managing patient portal access.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/labcorp/install.sh | bash
```

Or manually:
```bash
cp -r skills/labcorp ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set LABCORP_EMAIL "your-email@example.com"
canifi-env set LABCORP_PASSWORD "your-password"
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
- View lab test results
- Check appointment status
- Access test history
- Find testing locations
- View order status
- Access patient portal

## Usage Examples

### Example 1: View Lab Results
```
User: "Are my Labcorp results ready?"
Claude: I'll check for your results.
1. Opening Labcorp via Playwright MCP
2. Accessing patient portal
3. Viewing results section
4. Checking for new results
5. Summarizing available results
```

### Example 2: Check Appointments
```
User: "Do I have any scheduled lab appointments?"
Claude: I'll check your appointments.
1. Accessing appointments section
2. Viewing scheduled tests
3. Listing upcoming appointments
4. Providing location details
```

### Example 3: Find Location
```
User: "Where is the nearest Labcorp location?"
Claude: I'll find nearby locations.
1. Accessing location finder
2. Searching nearby facilities
3. Listing addresses and hours
4. Noting available services
```

## Authentication Flow
1. Navigate to labcorp.com via Playwright MCP
2. Click "Sign in" and enter email
3. Enter password
4. Handle 2FA if required (via iMessage)
5. Maintain session for portal access

## Error Handling
- **Login Failed**: Retry up to 3 times, notify via iMessage
- **Session Expired**: Re-authenticate automatically
- **Rate Limited**: Implement exponential backoff
- **2FA Required**: Send iMessage notification
- **Results Pending**: Note processing time
- **Location Unavailable**: Suggest alternatives

## Self-Improvement Instructions
When Labcorp updates:
1. Document new portal features
2. Update result viewing options
3. Track appointment scheduling
4. Log testing service changes

## Notes
- Results released by provider
- Walk-in and scheduled appointments
- Home collection available
- COVID testing services
- Drug testing services

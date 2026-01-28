---
name: teladoc
description: Access telehealth with Teladoc - view visit history, check available services, and manage account
category: healthcare
---

# Teladoc Skill

## Overview
Enables Claude to use Teladoc for telehealth services including viewing visit history, checking available services, and managing account settings.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/teladoc/install.sh | bash
```

Or manually:
```bash
cp -r skills/teladoc ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set TELADOC_EMAIL "your-email@example.com"
canifi-env set TELADOC_PASSWORD "your-password"
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
- View visit history
- Check available services
- Access medical records
- View provider information
- Check prescription status
- Manage account settings

## Usage Examples

### Example 1: View Past Visits
```
User: "Show me my recent Teladoc visits"
Claude: I'll check your visit history.
1. Opening Teladoc via Playwright MCP
2. Accessing visit history
3. Listing recent consultations
4. Summarizing visit details
```

### Example 2: Check Services
```
User: "What telehealth services are available to me?"
Claude: I'll check available services.
1. Accessing services section
2. Viewing available care types
3. Listing coverage options
4. Noting service details
```

### Example 3: Prescription Status
```
User: "Check on my prescription from Teladoc"
Claude: I'll check prescription status.
1. Accessing prescriptions section
2. Finding recent prescriptions
3. Checking pharmacy status
4. Reporting fulfillment info
```

## Authentication Flow
1. Navigate to teladoc.com via Playwright MCP
2. Click "Log in" and enter email
3. Enter password
4. Handle 2FA if required (via iMessage)
5. Maintain session for account access

## Error Handling
- **Login Failed**: Retry up to 3 times, notify via iMessage
- **Session Expired**: Re-authenticate automatically
- **Rate Limited**: Implement exponential backoff
- **2FA Required**: Send iMessage notification
- **Service Unavailable**: Check coverage eligibility
- **Record Not Found**: Verify account details

## Self-Improvement Instructions
When Teladoc updates:
1. Document new service offerings
2. Update specialty care options
3. Track app feature changes
4. Log integration updates

## Notes
- Employer/insurance provided access
- 24/7 availability for some services
- Prescription capability
- Mental health services
- Specialist referrals available

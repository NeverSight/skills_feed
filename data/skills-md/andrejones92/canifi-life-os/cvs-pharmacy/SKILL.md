---
name: cvs-pharmacy
description: Manage prescriptions with CVS - check prescription status, view pharmacy services, and manage refills
category: healthcare
---

# CVS Pharmacy Skill

## Overview
Enables Claude to use CVS Pharmacy for prescription management including checking prescription status, viewing medication history, and managing refills.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/cvs-pharmacy/install.sh | bash
```

Or manually:
```bash
cp -r skills/cvs-pharmacy ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set CVS_EMAIL "your-email@example.com"
canifi-env set CVS_PASSWORD "your-password"
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
- Check prescription status
- View medication list
- Access refill information
- Check pharmacy locations
- View immunization records
- Access ExtraCare rewards

## Usage Examples

### Example 1: Check Prescription Status
```
User: "Is my prescription ready at CVS?"
Claude: I'll check your prescription status.
1. Opening CVS via Playwright MCP
2. Accessing prescriptions section
3. Viewing pending prescriptions
4. Checking ready status
5. Reporting pickup availability
```

### Example 2: View Medications
```
User: "What medications do I have on file at CVS?"
Claude: I'll list your medications.
1. Accessing prescription history
2. Viewing current medications
3. Listing names and dosages
4. Noting refill dates
```

### Example 3: Find Nearby Pharmacy
```
User: "Where is the nearest CVS pharmacy?"
Claude: I'll find nearby locations.
1. Accessing store locator
2. Finding nearest pharmacies
3. Listing addresses and hours
4. Noting services available
```

## Authentication Flow
1. Navigate to cvs.com via Playwright MCP
2. Click "Sign in" and enter email
3. Enter password
4. Handle 2FA if required (via iMessage)
5. Maintain session for account access

## Error Handling
- **Login Failed**: Retry up to 3 times, notify via iMessage
- **Session Expired**: Re-authenticate automatically
- **Rate Limited**: Implement exponential backoff
- **2FA Required**: Send iMessage notification
- **Prescription Not Found**: Verify account details
- **Store Closed**: Show alternative locations

## Self-Improvement Instructions
When CVS updates:
1. Document new pharmacy features
2. Update digital service options
3. Track ExtraCare changes
4. Log MinuteClinic integration

## Notes
- Links to MinuteClinic services
- ExtraCare rewards program
- Photo and retail services
- Drive-thru available
- Immunization services

---
name: care-com
description: Find caregivers for children, seniors, pets, and home care.
category: homeservices
---
# Care.com Skill

Find caregivers for children, seniors, pets, and home care.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/care-com/install.sh | bash
```

Or manually:
```bash
cp -r skills/care-com ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set CARECOM_EMAIL "your_email"
canifi-env set CARECOM_PASSWORD "your_password"
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

1. **Find Caregivers**: Search for all types of care
2. **Post Jobs**: Create caregiver job listings
3. **Background Checks**: Run caregiver checks
4. **Manage Bookings**: Coordinate care schedules
5. **Payment Processing**: Handle caregiver payments

## Usage Examples

### Find Babysitter
```
User: "Find a babysitter for Saturday night"
Assistant: Returns available caregivers
```

### Post Job
```
User: "Post a nanny job listing"
Assistant: Creates job posting
```

### Run Background Check
```
User: "Run a background check on this caregiver"
Assistant: Initiates background screening
```

### Schedule Care
```
User: "Book this caregiver for next week"
Assistant: Creates booking
```

## Authentication Flow

1. Account-based authentication
2. No official API
3. Browser automation required
4. Subscription for full features

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Login Failed | Invalid credentials | Check account |
| No Caregivers | Location/criteria | Expand search |
| Posting Failed | Incomplete info | Complete details |
| Check Failed | Data issue | Verify info |

## Notes

- All care types
- Background check services
- Subscription model
- Care@Work for businesses
- No public API
- Secure messaging

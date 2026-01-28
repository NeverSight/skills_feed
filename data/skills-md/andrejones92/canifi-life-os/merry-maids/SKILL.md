---
name: merry-maids
description: Professional home cleaning services from a trusted national brand.
category: homeservices
---
# Merry Maids Skill

Professional home cleaning services from a trusted national brand.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/merry-maids/install.sh | bash
```

Or manually:
```bash
cp -r skills/merry-maids ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set MERRYMAIDS_EMAIL "your_email"
canifi-env set MERRYMAIDS_PASSWORD "your_password"
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

1. **Book Cleaning**: Schedule house cleaning
2. **Custom Plans**: Create personalized cleaning plans
3. **Get Quote**: Request service estimates
4. **Recurring Service**: Set up regular cleanings
5. **Special Services**: Deep cleaning and move-out

## Usage Examples

### Book Service
```
User: "Book a Merry Maids cleaning"
Assistant: Schedules cleaning appointment
```

### Get Quote
```
User: "Get a quote for deep cleaning"
Assistant: Returns pricing estimate
```

### Set Recurring
```
User: "Set up biweekly cleaning"
Assistant: Creates recurring schedule
```

### Special Clean
```
User: "Book a move-out cleaning"
Assistant: Schedules deep cleaning
```

## Authentication Flow

1. Account-based authentication
2. No official API
3. Browser automation required
4. Local franchise booking

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Login Failed | Invalid credentials | Check account |
| No Service | Location issue | Check coverage |
| Booking Failed | Availability | Try different time |
| Quote Error | Missing details | Complete form |

## Notes

- National brand since 1979
- Bonded and insured
- Custom cleaning plans
- Satisfaction guarantee
- No public API
- Franchise locations

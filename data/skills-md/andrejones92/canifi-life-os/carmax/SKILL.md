---
name: carmax
description: Buy, sell, and trade vehicles at America's largest used car retailer.
category: automotive
---
# CarMax Skill

Buy, sell, and trade vehicles at America's largest used car retailer.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/carmax/install.sh | bash
```

Or manually:
```bash
cp -r skills/carmax ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set CARMAX_EMAIL "your_email"
canifi-env set CARMAX_PASSWORD "your_password"
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

1. **Search Cars**: Browse nationwide inventory
2. **Get Appraisal**: Instant offer for your car
3. **Schedule Test Drive**: Book in-store appointments
4. **Transfer Vehicle**: Request vehicle transfers
5. **Financing Options**: Explore payment options

## Usage Examples

### Search Inventory
```
User: "Find trucks at CarMax near me"
Assistant: Returns available trucks
```

### Get Offer
```
User: "Get a CarMax offer for my car"
Assistant: Starts appraisal process
```

### Schedule Visit
```
User: "Schedule a test drive at CarMax"
Assistant: Books appointment
```

### Transfer Request
```
User: "Transfer this vehicle to my local CarMax"
Assistant: Initiates transfer
```

## Authentication Flow

1. Account-based authentication
2. No official API
3. Browser automation required
4. Store integration

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Login Failed | Invalid credentials | Check account |
| Vehicle Sold | No longer available | Search again |
| Transfer Error | Distance limit | Choose closer store |
| Appointment Error | Availability | Select new time |

## Notes

- Nationwide inventory
- No-haggle pricing
- 30-day money back
- No public API
- In-store appraisals
- Financing available

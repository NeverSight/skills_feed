---
name: getaround
description: Instant car sharing with keyless access for hourly and daily rentals.
category: automotive
---
# Getaround Skill

Instant car sharing with keyless access for hourly and daily rentals.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/getaround/install.sh | bash
```

Or manually:
```bash
cp -r skills/getaround ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set GETAROUND_EMAIL "your_email"
canifi-env set GETAROUND_PASSWORD "your_password"
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

1. **Find Cars**: Search nearby available vehicles
2. **Instant Book**: Reserve with keyless unlock
3. **Share Vehicle**: List your car for sharing
4. **Trip History**: View past and current trips
5. **Earnings Dashboard**: Track hosting income

## Usage Examples

### Find Nearby Car
```
User: "Find a car available right now on Getaround"
Assistant: Returns instantly available vehicles
```

### Start Trip
```
User: "Unlock my Getaround rental"
Assistant: Sends unlock command
```

### View Earnings
```
User: "Show my Getaround hosting earnings"
Assistant: Returns income summary
```

### End Trip
```
User: "End my Getaround trip"
Assistant: Completes rental session
```

## Authentication Flow

1. Account-based authentication
2. No official API
3. Browser automation required
4. Connect hardware for keyless

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Login Failed | Invalid credentials | Check account |
| Unlock Failed | Bluetooth issue | Move closer |
| Booking Error | Car unavailable | Try another |
| Payment Failed | Card issue | Update payment |

## Notes

- Keyless car sharing
- Hourly rentals available
- Getaround Connect hardware
- Insurance included
- No public API
- Instant access

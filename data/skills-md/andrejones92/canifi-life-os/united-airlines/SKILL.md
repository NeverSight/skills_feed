---
name: united-airlines
description: Book flights, manage reservations, check MileagePlus status, and access United Airlines services
category: travel
---

# United Airlines Skill

## Overview
Enables Claude to search and book United flights, manage reservations, track MileagePlus miles, check flight status, and access United's travel services through browser automation.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/united-airlines/install.sh | bash
```

Or manually:
```bash
cp -r skills/united-airlines ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set UNITED_EMAIL "your-email@example.com"
canifi-env set UNITED_MILEAGEPLUS "your-mileageplus-number"
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
- Search and book United flights and partner airlines
- Manage existing reservations and seat assignments
- Check MileagePlus account balance and status
- Track real-time flight status and delays
- Access boarding passes and travel documents
- Upgrade seats using miles or Plus Points

## Usage Examples

### Example 1: Book a Flight
```
User: "Find United flights from Chicago to Denver next Friday"
Claude: I'll search United for those flights.
- Opens united.com via Playwright MCP
- Enters ORD to DEN, next Friday
- Filters by nonstop preference
- Shows options:
  - UA 1234 6:00am: $189, Economy
  - UA 5678 10:30am: $215, Economy
  - UA 9012 3:15pm: $198, Economy Plus available +$79
- Notes MileagePlus earning: 1,400 miles
```

### Example 2: Check MileagePlus Status
```
User: "How many United miles do I have?"
Claude: I'll check your MileagePlus account.
- Logs into United account
- Navigates to MileagePlus dashboard
- Returns: 87,432 miles available
- Premier status: Gold (42,500 PQP earned this year)
- Plus Points: 280 available
- Miles expiring: None in next 18 months
```

### Example 3: Manage Reservation
```
User: "Can I select a window seat for my Denver flight?"
Claude: I'll update your seat assignment.
- Navigates to My Trips
- Locates Denver reservation
- Opens seat map
- Shows available window seats: 12A, 18A, 23F
- Selects 12A (preferred forward location)
- Confirms seat change: Now assigned to 12A
```

## Authentication Flow
1. Navigate to united.com via Playwright MCP
2. Click "Sign in" and enter MileagePlus number or email
3. Enter password from secure storage
4. Handle 2FA via email or SMS
5. Verify Premier status loaded
6. Maintain session for booking operations

## Error Handling
- Login Failed: Retry with email, try password reset
- Flight Sold Out: Show alternative times, waitlist options
- Seat Unavailable: Suggest alternative seats, check upgrade
- Session Expired: Re-authenticate with stored credentials
- Rate Limited: Wait 60 seconds, retry
- 2FA Required: Retrieve code from email/SMS

## Self-Improvement Instructions
After each interaction:
- Track award availability patterns
- Note upgrade clearing times
- Log Premier benefit usage
- Document UI changes

Suggest updates when:
- United updates booking interface
- MileagePlus program changes
- New fare classes introduced
- App features added

## Notes
- Premier members get free seat selection
- Basic Economy has significant restrictions
- Award flights can be booked with miles
- Plus Points upgrade chances vary by route
- United Club access available for Premier 1K
- Polaris business class on international routes

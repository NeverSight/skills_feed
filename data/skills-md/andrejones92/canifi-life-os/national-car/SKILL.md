---
name: national-car
description: Rent cars with Emerald Club benefits, choose your own vehicle, and manage reservations with National Car Rental
category: travel
---

# National Car Rental Skill

## Overview
Enables Claude to search and book rental cars, leverage Emerald Club benefits including Choose Your Own Car, and manage reservations through National's premium car rental network.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/national-car/install.sh | bash
```

Or manually:
```bash
cp -r skills/national-car ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set NATIONAL_EMAIL "your-email@example.com"
canifi-env set NATIONAL_EMERALD "your-emerald-club-number"
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
- Search and book rental cars at National locations
- Access Emerald Club member benefits
- Use Choose Your Own Car feature at Emerald Aisle
- Manage existing reservations
- Book Executive and luxury vehicles
- Arrange one-way rentals between locations

## Usage Examples

### Example 1: Book with Emerald Club
```
User: "Book a National car at O'Hare for my business trip next week"
Claude: I'll search National at O'Hare.
- Opens nationalcar.com via Playwright MCP
- Enters ORD airport, next week dates
- Shows Emerald Club options:
  - Midsize (guaranteed): $68/day
  - Choose Your Own at Aisle: Same price, pick premium
- Notes: Emerald Executive can choose from Executive Aisle
- Total estimate: $476 for 7 days
```

### Example 2: Check Emerald Status
```
User: "What's my National Emerald Club status?"
Claude: I'll check your Emerald Club account.
- Logs into National account
- Returns: Emerald Executive Elite status
- Benefits: Choose any car on Executive Aisle
- Free upgrades, one free rental day/7 rentals
- Bypass counter at all locations
- Rental credits: 2 earned, 1 redeemed
```

### Example 3: Reserve Executive Car
```
User: "I need a luxury car from National in Vegas"
Claude: I'll search Executive Elite options.
- Searches Las Vegas locations
- Shows Executive Aisle vehicles typically available:
  - Lincoln Navigator
  - Cadillac Escalade
  - BMW 5 Series
  - Infiniti QX80
- Notes: With Elite status, any of these at midsize price
- Walk to Executive Aisle and choose
```

## Authentication Flow
1. Navigate to nationalcar.com via Playwright MCP
2. Click "Sign In" and enter Emerald Club number
3. Enter password
4. Handle security verification if prompted
5. Verify Emerald tier displayed
6. Maintain session for reservations

## Error Handling
- Login Failed: Retry with email, check credentials
- Location Unavailable: Suggest nearby National locations
- No Vehicles: Show Enterprise partner availability
- Session Expired: Re-authenticate automatically
- Rate Limited: Wait 45 seconds, retry
- Emerald Aisle Empty: Reserve guaranteed class instead

## Self-Improvement Instructions
After each interaction:
- Track Emerald Aisle availability patterns
- Note pricing by location and day
- Log Executive Elite upgrade frequency
- Document UI changes

Suggest updates when:
- National updates booking interface
- Emerald Club program changes
- New vehicle types added
- Partnership with Enterprise changes

## Notes
- National is part of Enterprise Holdings
- Emerald Aisle: Walk to car, drive away
- Executive Elite is highest Emerald tier
- One Free Day per 7 completed rentals
- Choose Your Own Car only at airports
- Young renter fee applies under 25
- Corporate accounts may have negotiated rates

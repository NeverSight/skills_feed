---
name: amtrak
description: Book train tickets, check schedules, manage reservations, and access Amtrak Guest Rewards
category: travel
---

# Amtrak Skill

## Overview
Enables Claude to search and book Amtrak train tickets, check schedules and status, manage reservations, and access Amtrak Guest Rewards benefits across the national rail network.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/amtrak/install.sh | bash
```

Or manually:
```bash
cp -r skills/amtrak ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set AMTRAK_EMAIL "your-email@example.com"
canifi-env set AMTRAK_GUEST_REWARDS "your-guest-rewards-number"
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
- Search train routes and schedules
- Book tickets in various service classes
- Manage existing reservations
- Check real-time train status and delays
- Access Amtrak Guest Rewards benefits
- Book sleeper accommodations for long routes

## Usage Examples

### Example 1: Book Train Tickets
```
User: "Find Amtrak from NYC to Washington DC tomorrow morning"
Claude: I'll search Amtrak for Northeast Corridor trains.
- Opens amtrak.com via Playwright MCP
- Enters NYP to WAS, tomorrow
- Shows morning departures:
  - Acela 2151 6:00am: $89 Business, $189 First
  - Regional 171 6:30am: $49 Coach, $99 Business
  - Acela 2153 7:00am: $99 Business, $199 First
- Notes: Acela is fastest (2h 45m vs 3h 30m)
```

### Example 2: Check Train Status
```
User: "Is my train to Chicago on time?"
Claude: I'll check your train status.
- Finds reservation for Capitol Limited
- Checks real-time status:
  - Train #29 currently 45 minutes late
  - Current location: Pittsburgh
  - Revised arrival: 9:45am instead of 9:00am
- Notes: Delays common on this route
```

### Example 3: Book Sleeper Room
```
User: "Book a roomette on the California Zephyr from Chicago to San Francisco"
Claude: I'll search sleeper accommodations.
- Searches CHI to EMY (Emeryville/SF)
- Shows California Zephyr options:
  - Coach: $189 one way
  - Roomette: $589 (includes meals)
  - Bedroom: $1,089 (includes meals, private bath)
- Trip duration: 51 hours, stunning scenery
- Roomette fits 2, converts to beds at night
```

## Authentication Flow
1. Navigate to amtrak.com via Playwright MCP
2. Click "Sign In" and enter email
3. Enter password
4. Handle security verification if prompted
5. Verify Guest Rewards status displayed
6. Maintain session for bookings

## Error Handling
- Login Failed: Retry with Guest Rewards number
- Train Sold Out: Check adjacent dates, upgrade class
- Route Unavailable: Suggest connecting services
- Session Expired: Re-authenticate automatically
- Rate Limited: Wait 60 seconds, retry
- Delay Information Unavailable: Check again later

## Self-Improvement Instructions
After each interaction:
- Track on-time performance by route
- Note pricing patterns and sales
- Log Guest Rewards earning rates
- Document UI changes

Suggest updates when:
- Amtrak updates booking interface
- Guest Rewards program changes
- New routes or services added
- Pricing structure changes

## Notes
- Acela fastest on Northeast Corridor
- Long-distance trains include dining car
- Sleeper accommodations include all meals
- USA Rail Pass available for multi-trip travel
- Guest Rewards points don't expire with activity
- Bikes allowed on many routes (reservation required)
- Station access times vary (30min-2hr before departure)

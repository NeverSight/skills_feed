---
name: southwest
description: Book flights, manage Rapid Rewards, check-in, and access Southwest Airlines services
category: travel
---

# Southwest Airlines Skill

## Overview
Enables Claude to search and book Southwest flights, manage Rapid Rewards account, perform online check-in, track Companion Pass progress, and access Southwest's unique travel features.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/southwest/install.sh | bash
```

Or manually:
```bash
cp -r skills/southwest ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set SOUTHWEST_EMAIL "your-email@example.com"
canifi-env set SOUTHWEST_RAPID_REWARDS "your-rr-number"
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
- Search and book Southwest flights (not on aggregators)
- Manage Rapid Rewards points and A-List status
- Perform online check-in at exactly 24 hours
- Track Companion Pass qualification progress
- Change or cancel flights with no fees
- Access EarlyBird check-in and upgraded boarding

## Usage Examples

### Example 1: Book a Wanna Get Away Flight
```
User: "Find cheap Southwest flights from Dallas to Vegas next month"
Claude: I'll search Southwest for the best fares.
- Opens southwest.com via Playwright MCP
- Enters DAL/DFW to LAS, next month dates
- Shows fare calendar with lowest prices:
  - Wed departures: $79 Wanna Get Away
  - Weekend: $149 Wanna Get Away
  - Anytime fare: $289 (fully refundable)
- Recommends: Book Wed-Wed for $158 roundtrip
- Notes: Earns 1,200 Rapid Rewards points
```

### Example 2: Check-in for Flight
```
User: "Check me in for my Southwest flight tomorrow"
Claude: I'll perform your check-in at exactly 24 hours.
- Notes: Flight departs 2:30pm tomorrow
- Schedules check-in for 2:30pm today
- At check-in time:
  - Navigates to check-in page
  - Enters confirmation and name
  - Submits immediately at 24-hour mark
  - Obtains boarding position: A24
- Saves boarding pass to device
```

### Example 3: Track Companion Pass
```
User: "How close am I to Southwest Companion Pass?"
Claude: I'll check your Companion Pass progress.
- Logs into Rapid Rewards account
- Navigates to tier status
- Returns: 87,450 of 135,000 qualifying points
- Or: 72 of 100 qualifying flights
- Current status: A-List Preferred
- Projected: On track for Companion Pass by October
- Tip: Credit card spending also counts
```

## Authentication Flow
1. Navigate to southwest.com via Playwright MCP
2. Click "Log in" and enter Rapid Rewards number
3. Enter password
4. Handle security questions if prompted
5. Verify A-List status displayed
6. Maintain session for bookings and check-in

## Error Handling
- Login Failed: Answer security questions, retry
- Fare Sold Out: Show alternative dates, set alert
- Check-in Failed: Retry immediately, alert user
- Session Expired: Re-authenticate for check-in
- Rate Limited: Wait and retry (critical for check-in)
- 2FA Required: Complete security verification

## Self-Improvement Instructions
After each interaction:
- Track fare patterns by day/time
- Note check-in timing precision
- Log Companion Pass earning rates
- Document UI selector changes

Suggest updates when:
- Southwest changes booking flow
- Rapid Rewards program updates
- Check-in process changes
- New fare types introduced

## Notes
- Southwest not on Google Flights or Kayak - must search directly
- No change or cancellation fees (credit for future travel)
- Wanna Get Away fares are non-refundable but transferable as credit
- Companion Pass allows free companion on all flights
- Bags fly free: 2 checked bags included
- Check-in timing crucial for boarding position
- EarlyBird costs extra but guarantees early boarding

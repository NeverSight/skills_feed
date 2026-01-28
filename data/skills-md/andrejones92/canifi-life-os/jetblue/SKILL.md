---
name: jetblue
description: Book flights, manage TrueBlue points, check Mosaic status, and access JetBlue services
category: travel
---

# JetBlue Skill

## Overview
Enables Claude to search and book JetBlue flights, manage TrueBlue account, track Mosaic status benefits, and access JetBlue's distinctive travel services including Mint class.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/jetblue/install.sh | bash
```

Or manually:
```bash
cp -r skills/jetblue ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set JETBLUE_EMAIL "your-email@example.com"
canifi-env set JETBLUE_TRUEBLUE "your-trueblue-number"
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
- Search and book JetBlue flights with fare comparison
- Manage TrueBlue points and Mosaic status
- Access Mint (business class) availability
- Select seats with extra legroom (Even More Space)
- Track real-time flight status
- Manage travel bank credits

## Usage Examples

### Example 1: Book a Flight
```
User: "Find JetBlue flights from Boston to Fort Lauderdale next week"
Claude: I'll search JetBlue for those flights.
- Opens jetblue.com via Playwright MCP
- Enters BOS to FLL, next week dates
- Shows fare options:
  - Blue Basic: $79 (no carry-on included)
  - Blue: $119 (carry-on, seat selection)
  - Blue Plus: $159 (checked bag, more points)
  - Mint: $399 (lie-flat seat on select flights)
- Even More Space seats: +$45
```

### Example 2: Check Mosaic Benefits
```
User: "What are my JetBlue Mosaic benefits?"
Claude: I'll check your TrueBlue account.
- Logs into TrueBlue account
- Navigates to Mosaic status
- Returns: Mosaic 3 status
- Benefits: Free checked bags (2), Even More Space, priority boarding
- 3x points earning on JetBlue purchases
- Mosaic member pools for family
- Points balance: 45,670 available
```

### Example 3: Book Mint Class
```
User: "Is Mint available on JetBlue to LA?"
Claude: I'll check Mint availability.
- Searches BOS to LAX
- Checks Mint-equipped flights:
  - JB 323 8:00am: Mint available $599
  - JB 687 1:30pm: Mint available $649
  - JB 891 6:45pm: Mint sold out
- Mint includes: Lie-flat seat, meal, amenity kit
- Award price: 40,000 points + $70
```

## Authentication Flow
1. Navigate to jetblue.com via Playwright MCP
2. Click "Log in" and enter TrueBlue number or email
3. Enter password
4. Complete security verification if prompted
5. Verify Mosaic badge displayed
6. Maintain session for bookings

## Error Handling
- Login Failed: Retry with email option, check credentials
- Fare Sold Out: Show alternative flights, fare alerts
- Mint Unavailable: Suggest Even More Space upgrade
- Session Expired: Re-authenticate automatically
- Rate Limited: Wait 45 seconds, retry
- 2FA Required: Complete email verification

## Self-Improvement Instructions
After each interaction:
- Track Mint availability patterns
- Note seasonal pricing trends
- Log Mosaic earning rates
- Document UI changes

Suggest updates when:
- JetBlue updates booking flow
- TrueBlue program changes
- New routes or aircraft added
- Fare structure changes

## Notes
- Blue Basic is cheapest but very restrictive
- Mint only on transcontinental and Caribbean routes
- TrueBlue points don't expire
- Mosaic 4 highest tier with best benefits
- Even More Space worth it on 3+ hour flights
- JetBlue partners with American for connections

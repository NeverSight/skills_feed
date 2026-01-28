---
name: hotels-com
description: Search and book hotels, earn One Key rewards, and manage reservations on Hotels.com
category: travel
---

# Hotels.com Skill

## Overview
Enables Claude to search and book hotels worldwide, earn and redeem One Key rewards, manage reservations, and access member pricing through Hotels.com's platform.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/hotels-com/install.sh | bash
```

Or manually:
```bash
cp -r skills/hotels-com ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set HOTELS_EMAIL "your-email@example.com"
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
- Search hotels by location, dates, and preferences
- Compare prices and read verified reviews
- Earn One Key rewards on bookings
- Access member prices and secret deals
- Manage existing reservations
- Filter by amenities, ratings, and property type

## Usage Examples

### Example 1: Search Hotels
```
User: "Find hotels in San Francisco near Union Square under $200"
Claude: I'll search Hotels.com for SF accommodations.
- Opens hotels.com via Playwright MCP
- Enters Union Square, San Francisco
- Filters: Under $200/night
- Shows results:
  - Hotel Nikko: $179, 4.2 stars, free cancellation
  - Handlery Union Square: $165, 4.0 stars
  - The Marker: $195, 4.5 stars, member price
- Highlights One Key earning: 2% back
```

### Example 2: Check One Key Status
```
User: "How many Hotels.com rewards do I have?"
Claude: I'll check your One Key account.
- Logs into Hotels.com account
- Navigates to rewards section
- Returns: Gold tier status
- One Key Cash: $125.50 available
- Nights booked this year: 12
- Next tier (Platinum): 8 more nights
- Benefits: Member prices, free breakfast at select hotels
```

### Example 3: Find Secret Deals
```
User: "Show me Hotels.com secret deals in Miami"
Claude: I'll find secret deals for Miami.
- Navigates to Secret Prices section
- Searches Miami area
- Shows exclusive deals:
  - "4-star South Beach hotel": $159 (was $245)
  - "Brickell luxury suite": $189 (was $320)
- Notes: Must be logged in to see property names
- Secret Prices save average 15-20%
```

## Authentication Flow
1. Navigate to hotels.com via Playwright MCP
2. Click "Sign in" and enter email
3. Complete password verification
4. Handle email confirmation if required
5. Verify One Key status displayed
6. Maintain session for bookings

## Error Handling
- Login Failed: Try password reset, notify user
- Hotel Sold Out: Suggest similar properties nearby
- Price Changed: Alert user to new price
- Session Expired: Re-authenticate automatically
- Rate Limited: Wait 60 seconds, retry
- 2FA Required: Complete email verification

## Self-Improvement Instructions
After each interaction:
- Track One Key earning patterns
- Note secret deal availability
- Log price comparison accuracy
- Document UI changes

Suggest updates when:
- Hotels.com updates interface
- One Key program changes
- New deal types available
- Search filters modified

## Notes
- One Key rewards work across Expedia, Hotels.com, and Vrbo
- Member prices require being logged in
- Free cancellation policies vary by property
- Secret Prices hide hotel name until booking
- Price Match Guarantee available
- Reviews are from verified guests only

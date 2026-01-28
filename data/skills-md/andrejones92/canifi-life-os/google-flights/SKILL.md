---
name: google-flights
description: Search flights, track prices, explore destinations, and find the best travel deals using Google Flights
category: google
---

# Google Flights Skill

## Overview
Enables Claude to search and compare flights, track price changes, explore destination options, and leverage Google's powerful flight search tools for optimal travel planning.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/google-flights/install.sh | bash
```

Or manually:
```bash
cp -r skills/google-flights ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set GOOGLE_EMAIL "your-email@example.com"
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
- Search flights with flexible date options
- Track prices and receive drop notifications
- Explore destinations by budget and interests
- View price graphs and best times to fly
- Filter by airline alliances, stops, and times
- Check carbon emissions for flight comparison

## Usage Examples

### Example 1: Search Flights with Date Flexibility
```
User: "Find flights from NYC to Tokyo, cheapest time in April"
Claude: I'll search Google Flights for the best April dates.
- Opens Google Flights via Playwright MCP
- Enters JFK/EWR/LGA to NRT/HND
- Selects April date grid view
- Shows price calendar:
  - Cheapest: Apr 8-22, $687 on ANA
  - Average price: $890
  - Peak: Apr 1-7 (cherry blossom), $1,200+
- Recommends: Book Apr 8 departure, returns still cheap
```

### Example 2: Track Flight Price
```
User: "Track prices for SFO to Barcelona in June"
Claude: I'll set up price tracking for that route.
- Opens Google Flights
- Searches SFO to BCN, June dates
- Enables price tracking toggle
- Confirms: Tracking enabled
- Current price: $845 roundtrip
- Typical price range: $750-$1,100
- Notifications will go to your Google account
```

### Example 3: Explore by Budget
```
User: "Where can I fly from Denver for a weekend trip under $400?"
Claude: I'll explore weekend destinations from Denver.
- Uses Google Flights Explore
- Sets origin: Denver
- Filters: Weekend trips, under $400
- Maps shows options:
  - Las Vegas: $98 roundtrip
  - Phoenix: $147 roundtrip
  - San Diego: $198 roundtrip
  - Nashville: $287 roundtrip
- Can filter by interests: beaches, cities, outdoors
```

## Authentication Flow
1. Navigate to google.com/flights via Playwright MCP
2. Sign in with Google account (uses shared Google auth)
3. Credentials: ember@emberbru.com from canifi-env
4. Handle 2FA via authenticator or iMessage
5. Price tracking syncs to Google account
6. Session maintained across Google services

## Error Handling
- Login Failed: Retry Google OAuth, check 2FA
- Search Failed: Simplify query, reduce filters
- No Results: Expand airports, check date range
- Session Expired: Re-authenticate via Google
- Rate Limited: Wait 60 seconds, retry
- 2FA Required: Handle via iMessage or authenticator

## Self-Improvement Instructions
After each interaction:
- Log price tracking accuracy
- Note seasonal patterns discovered
- Track alliance and route coverage
- Document feature updates

Suggest updates when:
- Google Flights adds new features
- Explore function expands
- Price tracking changes
- UI elements update

## Notes
- Google Flights shows carbon emissions per flight
- Tracked prices send notifications via Google
- Some budget airlines may not appear (Spirit, Frontier limited)
- Price insights show if current price is low/high/typical
- Baggage fees shown separately for accurate comparison
- Multi-city trips supported for complex itineraries

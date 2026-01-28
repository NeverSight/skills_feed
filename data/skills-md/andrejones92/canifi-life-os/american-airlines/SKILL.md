---
name: american-airlines
description: Book flights, manage AAdvantage miles, check flight status, and access American Airlines services
category: travel
---

# American Airlines Skill

## Overview
Enables Claude to search and book American Airlines flights, manage AAdvantage account, track Loyalty Points status, access oneworld partner benefits, and handle travel arrangements.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/american-airlines/install.sh | bash
```

Or manually:
```bash
cp -r skills/american-airlines ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set AA_EMAIL "your-email@example.com"
canifi-env set AA_AADVANTAGE "your-aadvantage-number"
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
- Search and book American and oneworld partner flights
- Manage AAdvantage miles and Loyalty Points status
- Select seats and request upgrades
- Check real-time flight status and rebooking
- Access Admiral's Club and Flagship Lounge info
- Book award travel using miles

## Usage Examples

### Example 1: Search Flights
```
User: "Find American flights from Miami to New York tomorrow morning"
Claude: I'll search American for morning flights.
- Opens aa.com via Playwright MCP
- Enters MIA to JFK/LGA/EWR, tomorrow
- Filters: Departure before noon
- Shows options:
  - AA 1234 6:15am MIA-JFK: $189 Main
  - AA 5678 8:00am MIA-LGA: $215 Main Extra
  - AA 9012 10:30am MIA-JFK: $245 First available
- Notes: Earning 1,200 Loyalty Points
```

### Example 2: Check Status Progress
```
User: "What's my AAdvantage status and how close am I to the next level?"
Claude: I'll check your AAdvantage account.
- Logs into AAdvantage account
- Navigates to status dashboard
- Returns: Gold status
- Loyalty Points: 42,500 of 75,000 for Platinum
- Loyalty Choice Rewards: 1 remaining
- Miles balance: 89,432 available
- Status valid through: January 2026
```

### Example 3: Book Award Flight
```
User: "Can I book a flight to London with my American miles?"
Claude: I'll search for award availability.
- Searches award calendar MIA-LHR
- Shows saver awards available:
  - March 15: 30,000 miles + $45 taxes (Economy)
  - March 15: 57,500 miles (Business on BA)
- Anytime awards: 65,000 miles Economy
- Notes: oneworld partners may have better availability
- Recommends booking saver if dates flexible
```

## Authentication Flow
1. Navigate to aa.com via Playwright MCP
2. Click "Log in" and enter AAdvantage number
3. Enter password
4. Handle security verification if prompted
5. Verify status badge displayed
6. Maintain session for bookings

## Error Handling
- Login Failed: Retry, check for account security holds
- Award Not Available: Search alternate dates/partners
- Upgrade Waitlisted: Monitor and alert when clears
- Session Expired: Re-authenticate automatically
- Rate Limited: Wait 60 seconds, retry
- 2FA Required: Complete verification flow

## Self-Improvement Instructions
After each interaction:
- Track award availability patterns
- Note upgrade clearing rates
- Log status qualification rates
- Document selector changes

Suggest updates when:
- American updates booking interface
- AAdvantage program changes
- Award chart modifications
- Partner availability changes

## Notes
- AAdvantage status now based on Loyalty Points (not miles)
- Systemwide Upgrades for Executive Platinum
- Basic Economy cannot select seats or earn full miles
- oneworld partners: BA, Qantas, Cathay, JAL, etc.
- Flagship First/Business on premium international routes
- Admiral's Club access varies by status and fare

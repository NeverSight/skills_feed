---
name: airbnb
description: Search and book accommodations, manage reservations, communicate with hosts, and track upcoming trips on Airbnb
category: travel
---

# Airbnb Skill

## Overview
Enables Claude to search for accommodations, manage bookings, communicate with hosts, and handle trip planning through Airbnb's platform via browser automation.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/airbnb/install.sh | bash
```

Or manually:
```bash
cp -r skills/airbnb ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set AIRBNB_EMAIL "your-email@example.com"
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
- Search listings by location, dates, guests, and amenities
- View listing details, photos, reviews, and availability
- Manage existing reservations and check-in instructions
- Communicate with hosts through Airbnb messaging
- Access saved listings and wishlists
- Check upcoming trips and past booking history

## Usage Examples

### Example 1: Search for Accommodations
```
User: "Find me an Airbnb in Austin for next weekend, 2 guests, under $200/night"
Claude: I'll search Airbnb for Austin accommodations.
- Opens Airbnb via Playwright MCP
- Enters Austin, TX as location
- Sets dates for next weekend
- Filters: 2 guests, max $200/night
- Returns top 5 options with ratings, amenities, and total cost
- Offers to show more details or save to wishlist
```

### Example 2: Check Reservation Details
```
User: "What are the check-in instructions for my Miami trip?"
Claude: I'll find your Miami reservation details.
- Navigates to Trips section
- Locates Miami booking
- Retrieves: Check-in 3pm, lockbox code 4521
- Address: 1234 Ocean Drive, Unit 5B
- Host contact: Maria (Superhost)
- Offers to add to LifeOS Trips database
```

### Example 3: Message Host
```
User: "Ask my Airbnb host if early check-in is possible"
Claude: I'll send that message to your host.
- Opens conversation with upcoming trip host
- Composes message: "Hi! I wanted to check if early check-in might be available for my upcoming stay. Please let me know if there's any flexibility. Thank you!"
- Sends message
- Reports: Message sent to Maria, typically responds within 1 hour
```

## Authentication Flow
1. Navigate to airbnb.com via Playwright MCP
2. Click "Log in" and select email login
3. Enter email from canifi-env
4. Handle email verification code or password
5. Complete 2FA if enabled
6. Maintain session for subsequent requests

## Error Handling
- Login Failed: Try Google OAuth fallback, notify via iMessage
- Listing Unavailable: Suggest similar alternatives
- Booking Failed: Check payment method, alert user
- Session Expired: Re-authenticate automatically
- Rate Limited: Wait 2 minutes, retry
- 2FA Required: Request code via preferred method

## Self-Improvement Instructions
After each interaction:
- Document effective search filter combinations
- Track listing availability patterns
- Note host response time patterns
- Log UI changes for selector updates

Suggest updates when:
- Airbnb changes search interface
- New filter options become available
- Booking flow is modified
- Messaging system updates

## Notes
- Superhost listings tend to have better reliability
- Instant Book listings can be reserved immediately
- Long-term stays (28+ nights) often have discounts
- Always verify check-in instructions before travel
- Never complete payment transactions - user must confirm
- Guest reviews are only visible after completing a stay

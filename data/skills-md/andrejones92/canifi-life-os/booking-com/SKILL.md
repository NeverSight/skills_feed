---
name: booking-com
description: Search and book hotels, apartments, and accommodations worldwide via Booking.com
category: travel
---

# Booking.com Skill

## Overview
Enables Claude to search for hotels and accommodations, compare prices, manage reservations, and access Genius loyalty benefits through Booking.com's platform.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/booking-com/install.sh | bash
```

Or manually:
```bash
cp -r skills/booking-com ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set BOOKING_EMAIL "your-email@example.com"
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
- Search hotels by location, dates, guests, and preferences
- Filter by amenities, rating, price, and property type
- View detailed property information and guest reviews
- Manage existing bookings and cancellations
- Access Genius member discounts and benefits
- Compare prices across room types and rate plans

## Usage Examples

### Example 1: Search Hotels
```
User: "Find hotels in Paris near the Eiffel Tower for December 20-23"
Claude: I'll search Booking.com for Paris hotels.
- Opens Booking.com via Playwright MCP
- Enters Eiffel Tower area, Paris
- Sets dates Dec 20-23, 2 adults
- Applies Genius filter for member discounts
- Returns top 5 hotels: ratings, prices, amenities
- Notes free cancellation options
```

### Example 2: Check Booking Details
```
User: "What's the confirmation number for my London hotel?"
Claude: I'll retrieve your London booking.
- Navigates to My Bookings
- Locates London reservation
- Returns: Confirmation #4829571634
- Hotel: The Strand Palace
- Check-in: Dec 15 at 3pm
- Room: Superior Double, breakfast included
```

### Example 3: Compare Room Options
```
User: "Show me room options at the Marriott in Chicago for next week"
Claude: I'll check available rooms at that property.
- Searches for Marriott Chicago
- Opens property page
- Lists room options:
  - Standard King: $189/night, city view
  - Deluxe Queen: $219/night, lake view
  - Suite: $359/night, separate living area
- Notes Genius Level 2 discount: 15% off
```

## Authentication Flow
1. Navigate to booking.com via Playwright MCP
2. Click "Sign in" and enter email
3. Complete email or password verification
4. Handle 2FA if enabled on account
5. Verify Genius status after login
6. Maintain session cookies

## Error Handling
- Login Failed: Retry with password flow, alert via iMessage
- Property Sold Out: Suggest similar properties nearby
- Booking Failed: Verify payment, suggest alternate dates
- Session Expired: Re-authenticate automatically
- Rate Limited: Wait 60 seconds, retry
- 2FA Required: Retrieve code from email via Playwright

## Self-Improvement Instructions
After each interaction:
- Track effective search filters
- Log price patterns by day/season
- Note Genius discount availability
- Document selector changes

Suggest updates when:
- Booking.com UI changes
- New filter options added
- Genius program terms change
- Property type categories update

## Notes
- Genius Level 2+ gets 10-15% discounts on select properties
- Free cancellation policies vary by property and rate
- Mobile rates sometimes differ from desktop
- Some properties require credit card guarantee
- Price includes taxes unless otherwise noted
- Reviews are verified from actual guests

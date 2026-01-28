---
name: tripadvisor
description: Research destinations, read reviews, find restaurants and attractions, and plan trips with Tripadvisor
category: travel
---

# Tripadvisor Skill

## Overview
Enables Claude to research travel destinations, read authentic reviews, discover restaurants and attractions, compare prices, and create comprehensive trip plans using Tripadvisor's extensive travel database.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/tripadvisor/install.sh | bash
```

Or manually:
```bash
cp -r skills/tripadvisor ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set TRIPADVISOR_EMAIL "your-email@example.com"
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
- Research destinations with comprehensive guides
- Read verified reviews for hotels, restaurants, attractions
- Find and compare restaurants by cuisine and rating
- Discover tours, activities, and experiences
- Create and manage trip itineraries
- Compare hotel prices across booking sites

## Usage Examples

### Example 1: Research Destination
```
User: "What are the top things to do in Barcelona?"
Claude: I'll research Barcelona attractions on Tripadvisor.
- Opens tripadvisor.com via Playwright MCP
- Searches Barcelona attractions
- Returns top rated:
  1. Sagrada Familia: 4.8 stars, 145K reviews
  2. Park Guell: 4.6 stars, 98K reviews
  3. Gothic Quarter: 4.7 stars, 52K reviews
  4. La Boqueria Market: 4.5 stars, 38K reviews
- Notes: Book Sagrada Familia tickets in advance
```

### Example 2: Find Restaurants
```
User: "Find top-rated Italian restaurants in Chicago"
Claude: I'll search for Italian restaurants in Chicago.
- Navigates to Chicago restaurants
- Filters: Italian cuisine, 4+ stars
- Shows top results:
  - Spiaggia: 4.5 stars, $$$$ , 2,100 reviews
  - RPM Italian: 4.5 stars, $$$ , 3,400 reviews
  - Monteverde: 4.7 stars, $$$ , 1,800 reviews
- Includes reservation availability
```

### Example 3: Compare Hotel Prices
```
User: "Compare prices for the Four Seasons Paris"
Claude: I'll compare prices across booking sites.
- Searches Four Seasons Paris
- Clicks price comparison
- Shows prices from multiple sites:
  - Booking.com: $1,245/night
  - Hotels.com: $1,280/night
  - Expedia: $1,260/night
  - Direct: $1,295/night (includes breakfast)
- Notes cancellation policies differ
```

## Authentication Flow
1. Navigate to tripadvisor.com via Playwright MCP
2. Click "Sign In" and enter email
3. Complete password verification
4. Handle email confirmation if required
5. Verify saved trips accessible
6. Maintain session for trip planning

## Error Handling
- Login Failed: Try Google/Facebook OAuth
- Search No Results: Broaden search criteria
- Review Loading Slow: Wait and retry
- Session Expired: Re-authenticate automatically
- Rate Limited: Wait 90 seconds (strict limits)
- Location Not Found: Suggest alternatives

## Self-Improvement Instructions
After each interaction:
- Track review patterns and reliability
- Note price comparison accuracy
- Log popular destination trends
- Document UI changes

Suggest updates when:
- Tripadvisor updates interface
- New booking integrations added
- Review system changes
- Trip planning features updated

## Notes
- Reviews are from verified travelers
- Traveler rankings updated regularly
- Price comparison doesn't include all sites
- Experiences/tours can be booked directly
- Trip planning saves to account
- Some reviews may be translated

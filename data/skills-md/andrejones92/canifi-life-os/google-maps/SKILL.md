---
name: google-maps
description: Enables Claude to search locations, get directions, and explore places in Google Maps via Playwright MCP
category: google
---

# Google Maps Skill

## Overview
Claude can use Google Maps to search for locations, get directions, find businesses, check traffic, and explore places. Useful for trip planning, finding nearby services, and navigation assistance.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/google-maps/install.sh | bash
```

Or manually:
```bash
cp -r skills/google-maps ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set GOOGLE_EMAIL "your-email@gmail.com"
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
- Search for addresses and places
- Get driving, walking, transit, and cycling directions
- Find nearby restaurants, gas stations, and services
- Check real-time traffic conditions
- View business hours and reviews
- Save places to lists
- Measure distances
- Explore street view
- Share locations
- Get estimated travel times
- View satellite imagery
- Find parking information

## Usage Examples

### Example 1: Get Directions
```
User: "How do I get from my house to the airport?"
Claude: Searches route, gets directions.
        Reports: "25.3 miles via I-95, approximately 32 minutes with current traffic.
        Fastest route: Take Main St to I-95 North..."
```

### Example 2: Find Nearby Places
```
User: "Find coffee shops near downtown"
Claude: Searches for coffee shops in downtown area.
        Reports: "Found 12 coffee shops:
        1. Blue Bottle Coffee (0.2 mi) - 4.5 stars, open until 6pm
        2. Starbucks (0.3 mi) - 4.0 stars, open 24 hours..."
```

### Example 3: Check Business Info
```
User: "What are the hours for Whole Foods on Main Street?"
Claude: Finds specific Whole Foods location, reads hours.
        Reports: "Open today 8am-10pm. Phone: (555) 123-4567"
```

### Example 4: Compare Routes
```
User: "What's the fastest way to work right now?"
Claude: Checks traffic on multiple routes.
        Reports: "Route 1 via highway: 28 min (normal traffic)
        Route 2 via surface streets: 35 min (some congestion)
        Recommend Route 1"
```

## Authentication Flow
1. Claude navigates to maps.google.com via Playwright MCP
2. Authenticates with GOOGLE_EMAIL if needed (for saved places)
3. Handles 2FA if prompted (notifies user via iMessage)
4. Maintains session for personalized features

## Selectors Reference
```javascript
// Search box
'#searchboxinput'

// Search button
'#searchbox-searchbutton'

// Directions button
'[aria-label="Directions"]'

// From/To inputs
'input[aria-label="Choose starting point"]'
'input[aria-label="Choose destination"]'

// Travel mode buttons
'[aria-label="Driving"]'
'[aria-label="Transit"]'
'[aria-label="Walking"]'
'[aria-label="Cycling"]'

// Route options
'.section-directions-trip'

// Place details panel
'.section-hero-header-title'

// Hours
'[aria-label*="Hours"]'

// Reviews
'.section-star-display'

// Save button
'[aria-label="Save"]'

// Share button
'[aria-label="Share"]'

// Traffic layer
'[aria-label="Traffic"]'
```

## Error Handling
- **Login Failed**: Retry 3 times, notify user via iMessage
- **Session Expired**: Re-authenticate automatically
- **Location Not Found**: Suggest alternatives, ask for clarification
- **Directions Failed**: Check start/end points, try different modes
- **No Results**: Broaden search area, try different keywords
- **Traffic Data Unavailable**: Report estimated time without traffic

## Self-Improvement Instructions
When you learn a better way to accomplish a task with Google Maps:
1. Document the improvement in your response
2. Suggest updating this skill file with the new approach
3. Include specific search strategies for better results
4. Note any new features or navigation improvements

## Notes
- Real-time traffic updates every few minutes
- Transit schedules may vary; confirm with transit authority
- Street View coverage varies by location
- Saved places sync across devices
- Offline maps can be downloaded for areas
- Business info from Google Business Profile
- Reviews aggregated from Google users
- Estimated times vary based on traffic conditions
- Wheelchair accessible routes available
- Toll roads can be avoided in directions settings

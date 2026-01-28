---
name: ebay
description: Enables Claude to browse eBay listings, manage watchlist, and track bids (no purchases)
version: 1.0.0
author: Canifi
category: ecommerce
---

# eBay Skill

## Overview
Automates eBay operations including searching listings, managing watchlist, tracking bids, and monitoring auctions through browser automation. Note: Actual purchases and bids are not automated for security.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/ebay/install.sh | bash
```

Or manually:
```bash
cp -r skills/ebay ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set EBAY_EMAIL "your-email@example.com"
canifi-env set EBAY_PASSWORD "your-password"
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
- Search and filter listings
- Add items to watchlist
- Track auction status
- View purchase history
- Compare sellers and prices
- Read seller feedback
- Monitor saved searches
- Check ending soon auctions

## Usage Examples

### Example 1: Search Listings
```
User: "Find vintage cameras on eBay"
Claude: I'll search for vintage cameras.
- Navigate to ebay.com
- Search "vintage cameras"
- Apply relevant filters
- Sort by best match or price
- Present top listings
```

### Example 2: Add to Watchlist
```
User: "Add this item to my eBay watchlist"
Claude: I'll add that to your watchlist.
- Navigate to listing
- Click "Add to Watchlist"
- Confirm added
- Note auction end time
```

### Example 3: Check Watched Items
```
User: "Show me my eBay watchlist with ending soon items"
Claude: I'll check your watchlist.
- Navigate to Watchlist
- Sort by ending soonest
- List items with current bids
- Highlight ending within 24 hours
```

### Example 4: Research Seller
```
User: "Check the feedback for this eBay seller"
Claude: I'll review their feedback.
- Navigate to seller's profile
- Gather feedback percentage
- Review recent comments
- Summarize seller reputation
```

## Authentication Flow
1. Navigate to ebay.com via Playwright MCP
2. Click Sign In
3. Enter email/username from canifi-env
4. Enter password
5. Handle 2FA if enabled (notify user via iMessage)
6. Complete CAPTCHA if shown (notify user)
7. Verify account access
8. Maintain session cookies

## Error Handling
- **Login Failed**: Clear cookies, verify credentials
- **Session Expired**: Re-authenticate automatically
- **2FA Required**: iMessage for verification code
- **CAPTCHA Required**: Notify user to complete
- **Listing Ended**: Note auction results
- **Item Unavailable**: Check similar listings
- **Seller Not Found**: Verify seller ID
- **Watchlist Full**: Notify of limit

## Self-Improvement Instructions
When encountering new eBay features:
1. Document new UI elements
2. Add support for new listing types
3. Log successful search patterns
4. Update for eBay changes

## Notes
- Bidding not automated for security
- Auction times in Pacific time
- Buy It Now vs auction listings
- Best Offer allows negotiation
- Seller feedback indicates reliability
- Return policies vary by seller
- Combined shipping available

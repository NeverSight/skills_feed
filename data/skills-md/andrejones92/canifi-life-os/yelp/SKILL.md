---
name: yelp
description: Find and review local businesses, restaurants, and services.
category: food
---
# Yelp Skill

Find and review local businesses, restaurants, and services.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/yelp/install.sh | bash
```

Or manually:
```bash
cp -r skills/yelp ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set YELP_EMAIL "your_email"
canifi-env set YELP_PASSWORD "your_password"
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

1. **Search Business**: Find local businesses
2. **Read Reviews**: Access user reviews
3. **Write Reviews**: Share your experiences
4. **Request Quotes**: Get service estimates
5. **Make Reservations**: Book tables at restaurants

## Usage Examples

### Find Restaurant
```
User: "Find Italian restaurants near me"
Assistant: Returns top-rated options
```

### Read Reviews
```
User: "Show reviews for this business"
Assistant: Returns user reviews
```

### Get Quote
```
User: "Request a quote from this plumber"
Assistant: Sends quote request
```

### Book Table
```
User: "Make a reservation for 4 at 7pm"
Assistant: Books table via Yelp Reservations
```

## Authentication Flow

1. Account-based authentication
2. Yelp Fusion API available
3. Browser automation for some features
4. OAuth2 for API access

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Login Failed | Invalid credentials | Check account |
| Search Error | Location issue | Enable location |
| Review Failed | Guidelines violation | Review content |
| Booking Failed | No availability | Try different time |

## Notes

- Local business reviews
- Restaurant reservations
- Service marketplace
- Yelp Fusion API available
- Mobile check-in
- Photo sharing

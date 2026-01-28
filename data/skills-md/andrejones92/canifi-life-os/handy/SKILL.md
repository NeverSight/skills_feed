---
name: handy
description: Book vetted professionals for home cleaning and handyman services.
category: homeservices
---
# Handy Skill

Book vetted professionals for home cleaning and handyman services.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/handy/install.sh | bash
```

Or manually:
```bash
cp -r skills/handy ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set HANDY_EMAIL "your_email"
canifi-env set HANDY_PASSWORD "your_password"
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

1. **Book Cleaning**: Schedule home cleaning
2. **Handyman Services**: Book repairs and tasks
3. **Recurring Bookings**: Set up regular service
4. **Manage Pros**: Rate and prefer professionals
5. **Gift Cards**: Purchase cleaning gift cards

## Usage Examples

### Book Cleaning
```
User: "Book a house cleaning for Saturday"
Assistant: Schedules cleaning service
```

### Book Handyman
```
User: "Book a handyman for TV mounting"
Assistant: Schedules handyman service
```

### Set Recurring
```
User: "Set up weekly cleaning"
Assistant: Creates recurring booking
```

### Rate Pro
```
User: "Rate my last cleaning"
Assistant: Opens rating interface
```

## Authentication Flow

1. Account-based authentication
2. No official API
3. Browser automation required
4. Background-checked pros

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Login Failed | Invalid credentials | Check account |
| No Availability | Time/location issue | Try different slot |
| Booking Failed | Payment issue | Update card |
| Service Error | Pro unavailable | Reschedule |

## Notes

- Background-checked pros
- Flat-rate pricing
- Happiness guarantee
- Recurring options
- No public API
- Same-day available

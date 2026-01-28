---
name: rover
description: Find trusted pet sitters and dog walkers in your neighborhood.
category: homeservices
---
# Rover Skill

Find trusted pet sitters and dog walkers in your neighborhood.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/rover/install.sh | bash
```

Or manually:
```bash
cp -r skills/rover ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set ROVER_EMAIL "your_email"
canifi-env set ROVER_PASSWORD "your_password"
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

1. **Find Sitters**: Search local pet sitters
2. **Book Services**: Schedule pet care
3. **Dog Walking**: Book daily walks
4. **House Sitting**: Arrange in-home stays
5. **Pet Updates**: Receive care updates

## Usage Examples

### Find Sitter
```
User: "Find a dog sitter for next weekend"
Assistant: Returns nearby sitters
```

### Book Walker
```
User: "Book a daily dog walker"
Assistant: Schedules walking service
```

### Request Boarding
```
User: "Find overnight pet boarding"
Assistant: Returns boarding options
```

### Check Updates
```
User: "Any updates from my pet sitter?"
Assistant: Returns Rover cards and photos
```

## Authentication Flow

1. Account-based authentication
2. No official API
3. Browser automation required
4. Background-checked sitters

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Login Failed | Invalid credentials | Check account |
| No Sitters | Location/dates | Expand search |
| Booking Failed | Sitter unavailable | Try another |
| Payment Failed | Card issue | Update payment |

## Notes

- Background-checked sitters
- Premium insurance
- GPS tracking available
- Rover Guarantee
- No public API
- Photo and video updates

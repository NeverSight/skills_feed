---
name: yourmechanic
description: Book mobile mechanics who come to you for car repairs and maintenance.
category: automotive
---
# YourMechanic Skill

Book mobile mechanics who come to you for car repairs and maintenance.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/yourmechanic/install.sh | bash
```

Or manually:
```bash
cp -r skills/yourmechanic ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set YOURMECHANIC_EMAIL "your_email"
canifi-env set YOURMECHANIC_PASSWORD "your_password"
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

1. **Get Quote**: Instant repair price estimates
2. **Book Service**: Schedule mobile mechanic visits
3. **Service History**: View past repairs
4. **Diagnostic Help**: Identify car problems
5. **Mechanic Selection**: Choose your technician

## Usage Examples

### Get Quote
```
User: "Get a quote for brake pad replacement"
Assistant: Returns pricing and availability
```

### Book Mechanic
```
User: "Book an oil change at my home"
Assistant: Schedules mobile service
```

### Check History
```
User: "Show my service history"
Assistant: Returns past repairs
```

### Diagnose Issue
```
User: "My check engine light is on"
Assistant: Returns possible causes and repair options
```

## Authentication Flow

1. Account-based authentication
2. No official API
3. Browser automation required
4. Location-based service

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Login Failed | Invalid credentials | Check account |
| Service Unavailable | Location issue | Check service area |
| Booking Failed | No mechanics available | Try different time |
| Quote Error | Vehicle not supported | Contact support |

## Notes

- Mobile mechanics
- Upfront pricing
- Service at your location
- Parts included
- No public API
- Fair price guarantee

---
name: angi
description: Connect with verified home service professionals (formerly Angie's List).
category: homeservices
---
# Angi Skill

Connect with verified home service professionals (formerly Angie's List).

## Quick Install

```bash
curl -sSL https://canifi.com/skills/angi/install.sh | bash
```

Or manually:
```bash
cp -r skills/angi ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set ANGI_EMAIL "your_email"
canifi-env set ANGI_PASSWORD "your_password"
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

1. **Find Pros**: Search verified contractors
2. **Read Reviews**: Access honest reviews
3. **Get Quotes**: Request project estimates
4. **Book Services**: Schedule appointments
5. **Project Planning**: Plan home improvements

## Usage Examples

### Find Contractor
```
User: "Find a roofer on Angi"
Assistant: Returns verified contractors
```

### Read Reviews
```
User: "Show reviews for this contractor"
Assistant: Returns customer feedback
```

### Get Estimate
```
User: "Get quotes for bathroom remodel"
Assistant: Requests estimates from pros
```

### Book Pro
```
User: "Book this HVAC technician"
Assistant: Schedules service
```

## Authentication Flow

1. Account-based authentication
2. No official API
3. Browser automation required
4. Verification system

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Login Failed | Invalid credentials | Check account |
| No Pros | Location issue | Expand search |
| Quote Error | Request failed | Retry |
| Booking Failed | Availability | Try different time |

## Notes

- Formerly Angie's List
- Verified reviews
- Background checks
- Cost guides available
- No public API
- Pro certification

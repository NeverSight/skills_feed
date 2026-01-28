---
name: urbansitter
description: Find trusted babysitters recommended by your social network.
category: homeservices
---
# UrbanSitter Skill

Find trusted babysitters recommended by your social network.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/urbansitter/install.sh | bash
```

Or manually:
```bash
cp -r skills/urbansitter ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set URBANSITTER_EMAIL "your_email"
canifi-env set URBANSITTER_PASSWORD "your_password"
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

1. **Find Sitters**: Search recommended babysitters
2. **Network Matching**: See friends' recommendations
3. **Book Sitter**: Schedule babysitting
4. **Pay Sitter**: Process payments
5. **Review History**: Access booking history

## Usage Examples

### Find Sitter
```
User: "Find a babysitter for tonight"
Assistant: Returns available sitters with recommendations
```

### Check Recommendations
```
User: "Which sitters do my friends use?"
Assistant: Shows network-recommended sitters
```

### Book Sitter
```
User: "Book this sitter for Saturday"
Assistant: Creates booking
```

### Pay Sitter
```
User: "Pay my sitter for last night"
Assistant: Processes payment
```

## Authentication Flow

1. Account-based authentication
2. No official API
3. Browser automation required
4. Social network integration

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Login Failed | Invalid credentials | Check account |
| No Sitters | Location/time issue | Expand search |
| Booking Failed | Sitter unavailable | Try another |
| Payment Failed | Card issue | Update payment |

## Notes

- Social recommendations
- Vetted sitters
- In-app booking
- Integrated payments
- No public API
- Corporate programs

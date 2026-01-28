---
name: homeadvisor
description: Find screened and approved home service professionals.
category: homeservices
---
# HomeAdvisor Skill

Find screened and approved home service professionals.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/homeadvisor/install.sh | bash
```

Or manually:
```bash
cp -r skills/homeadvisor ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set HOMEADVISOR_EMAIL "your_email"
canifi-env set HOMEADVISOR_PASSWORD "your_password"
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

1. **Find Pros**: Search approved contractors
2. **True Cost Guide**: View project cost estimates
3. **Get Matched**: Instant pro matching
4. **Read Reviews**: Access customer reviews
5. **Project Tracking**: Monitor job progress

## Usage Examples

### Find Pro
```
User: "Find a landscaper on HomeAdvisor"
Assistant: Returns matched professionals
```

### Check Cost
```
User: "How much does a kitchen remodel cost?"
Assistant: Returns True Cost Guide data
```

### Get Matched
```
User: "Match me with fence installers"
Assistant: Connects with available pros
```

### Track Project
```
User: "Show my project status"
Assistant: Returns job progress
```

## Authentication Flow

1. Account-based authentication
2. No official API
3. Browser automation required
4. Pro screening process

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Login Failed | Invalid credentials | Check account |
| No Matches | Location/service | Expand search |
| Contact Failed | Pro unavailable | Try another |
| Project Error | Data issue | Contact support |

## Notes

- Pre-screened professionals
- True Cost Guide
- Project management tools
- Angi network member
- No public API
- Instant matching

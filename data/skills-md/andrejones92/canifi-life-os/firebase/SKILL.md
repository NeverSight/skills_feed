---
name: firebase
description: Check hosting, monitor analytics, view Firestore, and manage Firebase projects
category: devops
---

# Firebase Skill

## Overview
Enables Claude to access Firebase Console to check hosting deployments, monitor Analytics, view Firestore data, manage Authentication, and oversee Firebase project resources.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/firebase/install.sh | bash
```

Or manually:
```bash
cp -r skills/firebase ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set FIREBASE_EMAIL "your-email@example.com"
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
- View hosting deployment status
- Monitor Analytics and Crashlytics
- Check Firestore usage and data
- View Authentication users
- Monitor Cloud Functions
- Check project usage and billing

## Usage Examples

### Example 1: Check Hosting
```
User: "What's the Firebase hosting status?"
Claude: I'll check your Firebase hosting.
- Opens console.firebase.google.com via Playwright MCP
- Logs into Google account
- Hosting status:
  - Production: my-app.web.app (live)
  - Last deploy: 2 hours ago
  - Release version: v45
  - CDN: All regions cached
- Preview channels: 2 active
```

### Example 2: View Analytics
```
User: "Show Firebase Analytics"
Claude: I'll check your app analytics.
- Views Analytics dashboard
- Last 7 days:
  - Active users: 12,345
  - Sessions: 34,567
  - Screen views: 89,012
- Top events: login, purchase, share
- User retention: 35% day 7
- Crashes: 12 (0.01%)
```

### Example 3: Check Firestore
```
User: "How's my Firestore usage?"
Claude: I'll check Firestore metrics.
- Views Firestore usage
- Current usage:
  - Reads: 45,678 today
  - Writes: 12,345 today
  - Deletes: 234 today
  - Storage: 2.3GB
- Daily quota: 50k reads (91% used)
- No billing alerts
```

## Authentication Flow
1. Navigate to console.firebase.google.com via Playwright MCP
2. Sign in with Google account
3. Use credentials from canifi-env
4. Handle 2FA if required
5. Select project if multiple
6. Maintain Google session

## Error Handling
- Login Failed: Re-authenticate Google
- Project Not Found: Check project access
- Quota Exceeded: Check billing settings
- Session Expired: Re-authenticate
- Function Error: Check function logs
- Rate Limited: Wait and retry

## Self-Improvement Instructions
After each interaction:
- Track common monitoring patterns
- Note analytics preferences
- Log quota monitoring
- Document console changes

Suggest updates when:
- Firebase console updates
- New features added
- Pricing changes
- Integration expands

## Notes
- Part of Google Cloud
- Hosting is CDN-backed
- Functions are serverless
- Firestore is NoSQL
- Auth has many providers
- Crashlytics for mobile
- Performance monitoring available

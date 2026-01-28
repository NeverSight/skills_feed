---
name: supabase
description: Monitor database, check auth users, view storage, and manage Supabase projects
category: devops
---

# Supabase Skill

## Overview
Enables Claude to access Supabase to monitor PostgreSQL database, check Authentication users, view Storage buckets, and manage backend-as-a-service projects.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/supabase/install.sh | bash
```

Or manually:
```bash
cp -r skills/supabase ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set SUPABASE_EMAIL "your-email@example.com"
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
- View database tables and queries
- Check Auth users and sessions
- Monitor Storage usage
- View Edge Functions
- Check API usage
- View real-time subscriptions

## Usage Examples

### Example 1: Check Database
```
User: "How's my Supabase database?"
Claude: I'll check your Supabase dashboard.
- Opens supabase.com via Playwright MCP
- Logs into account
- Database (my-project):
  - Status: Healthy
  - Tables: 12
  - Size: 234MB
  - Connections: 8/100
- Query performance: Normal
- Last migration: 3 days ago
```

### Example 2: View Auth Users
```
User: "How many users do I have?"
Claude: I'll check Authentication.
- Views Auth section
- Users:
  - Total: 1,234
  - New today: 23
  - Active (24h): 456
  - Providers: Email, Google, GitHub
- Sessions: 890 active
- Auth rate limits: OK
```

### Example 3: Check Storage
```
User: "What's in my Supabase storage?"
Claude: I'll check Storage buckets.
- Views Storage section
- Buckets:
  - avatars: 234 files, 45MB
  - uploads: 567 files, 890MB
  - public: 89 files, 123MB
- Total storage: 1.06GB / 1GB (over)
- Bandwidth: 5.6GB this month
```

## Authentication Flow
1. Navigate to supabase.com via Playwright MCP
2. Sign in with email or GitHub
3. Enter password or OAuth
4. Handle 2FA if enabled
5. Select organization/project
6. Maintain session for dashboard

## Error Handling
- Login Failed: Try GitHub OAuth
- Database Paused: Wake on free tier
- Storage Full: Check limits
- Session Expired: Re-authenticate
- Rate Limited: Check usage
- Function Error: View logs

## Self-Improvement Instructions
After each interaction:
- Track database queries
- Note auth patterns
- Log storage usage
- Document UI changes

Suggest updates when:
- Supabase updates dashboard
- New features added
- Pricing changes
- Database features expand

## Notes
- Open source Firebase alternative
- PostgreSQL database
- Realtime subscriptions
- Row Level Security
- Edge Functions (Deno)
- Local development supported
- Self-hosting option

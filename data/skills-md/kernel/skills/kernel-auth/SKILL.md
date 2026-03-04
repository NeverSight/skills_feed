---
name: kernel-auth
description: Setup and manage Kernel authentication connections for any website (Gmail, GitHub, Outlook, or custom domains). Handles managed auth flows with automatic reauthentication support.
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": ["kernel"] },
      },
  }
---

# Kernel Auth Skill

Setup and manage Kernel managed authentication connections for **any website** with safety checks and reauthentication support.

## Quick Start

```bash
kernel-auth setup gmail
```

Then visit the URL printed to complete login.

> **Works for any website** — See [Using Custom Domains](#using-custom-domains) for any other site.

## Usage

```bash
kernel-auth setup <service> [--profile-name <name>]
```

### Built-in Services

- `gmail` → gmail.com
- `github` → github.com
- `outlook` → outlook.com

### Using Custom Domains

For any other website, use the `--domain` flag:

```bash
kernel-auth setup --domain amazon.com --profile-name amazon-main
kernel-auth setup --domain linkedin.com
kernel-auth setup --domain example.com --profile-name custom-site
```

### Examples

```bash
kernel-auth setup gmail
kernel-auth setup github --profile-name github-work
kernel-auth setup outlook
```

## Authentication Flow

1. **Create auth connection** — Sets up a managed auth profile (domain + profile name)
2. **Initiate login session** — Generates a hosted login URL
3. **You visit URL** — Complete the login flow on your device/browser
4. **Login state stored in profile** — Kernel saves your authenticated session
5. **Use authenticated browser** — Create browser sessions with that profile, automatically logged in

## Key Concepts

### Auth Connections
- Each connection ties a service domain to a profile name
- Connections can be reused for multiple browser sessions
- Status: `AUTHENTICATED` (user completed login, state stored) or `NEEDS_AUTH` (never logged in or login session expired)

### Login Sessions
- Login sessions (the hosted URL) expire after a generous timeframe as cleanup
- If you don't complete login within that window, the session is deleted
- The connection itself stays — just initiate a new login session

Check connection status:
```bash
kernel auth connections list  # Check status
kernel auth connections get <id>  # Get connection details
```

If a connection shows `NEEDS_AUTH`:
```bash
kernel-auth setup <service>  # Re-initiate login session with fresh URL
```

### Why Manual URL Visit?
- **Login sessions are time-bound** — If you don't visit within the window, they expire (cleanup)
- **Prevent auto-opening** — Avoid Telegram/email clients accidentally consuming the link
- **Control is yours** — You visit the URL when you're ready

## Checking Status

```bash
# List all auth connections
kernel auth connections list -o json

# Check specific connection
kernel auth connections get <connection-id> -o json | jq '.status'
```

## Using Authenticated Browsers

Once auth is connected, create browser sessions with that profile:

```bash
# Create browser with Gmail auth already loaded
kernel browser create --profile-name gmail-main --stealth -o json

# Browser will be logged into Gmail automatically
```

## Important Notes

### ⚠️ Profile Deletion = Cascade Delete
Deleting a Kernel profile deletes ALL connections attached to it:
```bash
kernel profile delete gmail-main  # Deletes ALL gmail-main connections
```

Use sparingly. Better to refresh auth than delete and recreate.

### 🔗 Telegram & Link Previews
If you send auth URLs via Telegram, disable link previews in settings:
- Settings → Privacy & Security → Link Preview → Never show

Otherwise Telegram auto-opens the URL and consumes the code.

### 🌐 Network Requirements
Kernel auth requires:
- Outbound HTTPS to Kernel's managed auth service
- Browser with JavaScript enabled
- Cookie/session storage support

## Scripts

- `setup` — Create connection, generate login URL, display instructions
- No background watchers — You control when/if you visit the URL

## Troubleshooting

### "Code already used"
The auth code was consumed. This happens if:
- You visited the URL twice
- Telegram/email client auto-opened it
- Someone else completed the login first

Solution: Run `kernel-auth setup <service>` again to get a fresh code.

### "Code expired"
Codes expire after ~40 minutes. Re-run setup to generate a new one.

### "Connection not found"
The connection may have been deleted. Run setup again to create it.

### Auth Status is NEEDS_AUTH
You didn't complete the login within the session window, or you need to re-authenticate. Re-initiate login:
```bash
kernel-auth setup gmail
```

## Integration with OpenClaw

The auth skill integrates with OpenClaw cron jobs:
1. Cron job checks auth status before running
2. If `AUTHENTICATED`, proceeds with browser automation
3. If not, sends message requesting reauthentication
4. User confirms, system re-runs auth flow

Example from GMAIL_DAILY_WORKFLOW.md:
```bash
# Daily cron checks this before scraping
AUTH_STATUS=$(kernel auth connections list -o json | jq -r ".[] | select(.domain == \"gmail.com\") | .status")
if [ "$AUTH_STATUS" != "AUTHENTICATED" ]; then
  echo "Reauthentication needed"
  exit 1
fi
```

## Advanced

### Programmatic Auth Check
```bash
# Get auth status
kernel auth connections list -o json | jq '.[] | {id, status, domain}'

# Delete and recreate
kernel profile delete gmail-main --yes
kernel-auth setup gmail
```

### Multiple Accounts
Create separate profiles for each account:
```bash
kernel-auth setup gmail --profile-name gmail-personal
kernel-auth setup gmail --profile-name gmail-work
```

Then use the appropriate profile when creating browsers:
```bash
kernel browser create --profile-name gmail-work --stealth
```

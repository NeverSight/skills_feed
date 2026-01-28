---
name: tdameritrade
description: View investment accounts, check thinkorswim data, and access TD Ameritrade research (now Schwab)
category: finance
---

# TD Ameritrade Skill

## Overview
Enables Claude to access TD Ameritrade (now integrated with Charles Schwab) to view investment accounts, access thinkorswim platform data, and research investments. Note: TD Ameritrade is transitioning to Schwab.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/tdameritrade/install.sh | bash
```

Or manually:
```bash
cp -r skills/tdameritrade ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set TDAMERITRADE_USERNAME "your-username"
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
- View account balances and positions
- Access thinkorswim platform research
- Check portfolio performance
- Monitor options and futures positions
- View trading education resources
- Check Schwab migration status

## Usage Examples

### Example 1: Check Accounts
```
User: "What's in my TD Ameritrade account?"
Claude: I'll check your TD Ameritrade accounts.
- Opens tdameritrade.com via Playwright MCP
- May redirect to Schwab if migrated
- Returns: Total Value: $178,901.23
  - Margin Account: $145,678.90
  - IRA: $33,222.33
- Available to trade: $45,000
- Margin buying power: $290,000
```

### Example 2: Access thinkorswim Data
```
User: "What's my thinkorswim showing?"
Claude: I'll check thinkorswim research.
- Accesses thinkorswim web platform
- Current analysis:
  - Market Maker Move: SPY +/- 1.2%
  - VIX: 14.5 (low volatility)
  - Top movers in watchlist displayed
- Charts and technical data available
```

### Example 3: Check Migration Status
```
User: "Has my TD account moved to Schwab?"
Claude: I'll check your migration status.
- Checks account transition status
- Status: Scheduled for migration
- Migration date: February 2024
- Action required: None, automatic transfer
- Your Schwab account will have same positions
- Notes: thinkorswim remains available
```

## Authentication Flow
1. Navigate to tdameritrade.com via Playwright MCP
2. May redirect to Schwab login if migrated
3. Enter user ID and password
4. Handle 2FA via SMS or authenticator
5. Note migration banners/redirects
6. Maintain session appropriately

## Error Handling
- Login Failed: Check if account migrated to Schwab
- Redirect to Schwab: Update to use Schwab skill
- 2FA Required: Complete verification
- Account Locked: Direct to support
- Session Expired: Re-authenticate
- Platform Down: Check for migration maintenance

## Self-Improvement Instructions
After each interaction:
- Track migration status changes
- Note thinkorswim feature usage
- Log redirect patterns
- Document transition timeline

Suggest updates when:
- Migration complete (deprecate skill)
- thinkorswim changes
- Schwab integration finalized
- Auth requirements change

## Notes
- Claude CANNOT execute trades
- TD Ameritrade merging into Schwab
- thinkorswim platform continues under Schwab
- Accounts automatically transfer
- Check migration status regularly
- Paper trading available for practice
- Education resources transferring to Schwab

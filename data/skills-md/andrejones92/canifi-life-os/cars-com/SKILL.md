---
name: cars-com
description: Research, buy, and sell cars with comprehensive automotive resources.
category: automotive
---
# Cars.com Skill

Research, buy, and sell cars with comprehensive automotive resources.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/cars-com/install.sh | bash
```

Or manually:
```bash
cp -r skills/cars-com ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set CARSCOM_EMAIL "your_email"
canifi-env set CARSCOM_PASSWORD "your_password"
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

1. **Search Inventory**: Find new and used cars
2. **Research Tools**: Reviews, comparisons, and guides
3. **Dealer Ratings**: View dealer reputation
4. **Sell Your Car**: List your vehicle for sale
5. **Service Shops**: Find repair shops

## Usage Examples

### Search Cars
```
User: "Find electric vehicles on Cars.com"
Assistant: Returns EV listings
```

### Read Reviews
```
User: "Show reviews for 2024 Toyota Camry"
Assistant: Returns expert and owner reviews
```

### Check Dealer
```
User: "What's this dealer's rating?"
Assistant: Returns dealer reviews
```

### List Car
```
User: "List my car for sale on Cars.com"
Assistant: Starts listing process
```

## Authentication Flow

1. Account-based authentication
2. No official API
3. Browser automation required
4. Dealer network access

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Login Failed | Invalid credentials | Check account |
| Search Error | No results | Broaden criteria |
| Listing Error | Missing info | Complete details |
| Contact Failed | Dealer issue | Try again |

## Notes

- Comprehensive research
- Expert reviews
- Owner reviews
- Dealer ratings
- No public API
- Mobile apps available

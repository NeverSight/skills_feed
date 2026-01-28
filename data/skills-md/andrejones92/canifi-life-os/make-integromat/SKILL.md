---
name: make-integromat
description: Visual automation platform for complex workflows.
category: utilities
---
# Make (Integromat) Skill

Visual automation platform for complex workflows.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/make-integromat/install.sh | bash
```

Or manually:
```bash
cp -r skills/make-integromat ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set MAKE_API_KEY "your_api_key"
canifi-env set MAKE_TEAM_ID "your_team_id"
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

1. **Create Scenarios**: Build visual automations
2. **Run Scenarios**: Execute workflows
3. **Manage Scenarios**: Toggle and edit
4. **View Executions**: Check run history
5. **Data Stores**: Manage internal databases

## Usage Examples

### Run Scenario
```
User: "Run the data sync scenario"
Assistant: Executes scenario
```

### Check Executions
```
User: "Show recent scenario runs"
Assistant: Returns execution history
```

### Toggle Scenario
```
User: "Pause my backup scenario"
Assistant: Deactivates scenario
```

### View Data Store
```
User: "Show my Make data store"
Assistant: Returns stored data
```

## Authentication Flow

1. API key authentication
2. OAuth for connections
3. Webhook triggers
4. Team-based access

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Auth Failed | Invalid key | Check API key |
| Execution Error | Module failed | Check logs |
| Connection Lost | OAuth expired | Reconnect |
| Operations Limit | Plan exceeded | Upgrade |

## Notes

- Visual builder
- Advanced branching
- Error handling
- Data stores
- Custom functions
- API modules

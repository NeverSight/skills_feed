---
name: pandadoc
description: Create, send, and track documents with PandaDoc's document automation platform.
category: legal
---
# PandaDoc Skill

Create, send, and track documents with PandaDoc's document automation platform.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/pandadoc/install.sh | bash
```

Or manually:
```bash
cp -r skills/pandadoc ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set PANDADOC_API_KEY "your_api_key"
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

1. **Document Creation**: Create documents from templates with content library
2. **E-signatures**: Collect legally binding electronic signatures
3. **Proposals**: Build and send sales proposals with pricing tables
4. **Payments**: Collect payments within documents
5. **Analytics**: Track document views and engagement

## Usage Examples

### Create Document
```
User: "Create a proposal for the enterprise deal"
Assistant: Creates document from template
```

### Send for Signature
```
User: "Send the contract for signing"
Assistant: Sends document with signature fields
```

### Check Analytics
```
User: "Has the client viewed the proposal?"
Assistant: Returns document analytics
```

### Add Payment
```
User: "Add a payment request to the invoice"
Assistant: Adds payment collection to document
```

## Authentication Flow

1. Generate API key in PandaDoc settings
2. Use API key for authentication
3. Bearer token in header
4. Workspace-scoped access

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| 401 Unauthorized | Invalid API key | Verify credentials |
| 403 Forbidden | No access | Check permissions |
| 404 Not Found | Document not found | Verify document ID |
| 429 Rate Limited | Too many requests | Wait and retry |

## Notes

- All-in-one document platform
- Content library for reuse
- CRM integrations
- Payment collection
- Document analytics
- Free tier available

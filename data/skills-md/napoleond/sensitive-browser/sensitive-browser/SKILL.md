---
name: sensitive-browser
description: Execute sensitive browser actions (login, payments, form filling) outside the core agent loop using a dedicated CLI tool. Use when Claude needs to handle credentials, payment information, or other sensitive data in browser automation workflows. Triggers when users ask to log into websites, fill payment forms, or perform authenticated browser actions where sensitive data must be kept secure and separate from the main agent context.
---

# Sensitive Browser

Execute sensitive browser actions securely by delegating credential handling, payments, and form filling to a dedicated subprocess with isolated context.

## When to Use

- User asks to log into a website with credentials
- User needs to fill payment information on a checkout page
- User needs to complete forms with personal/sensitive data
- Browser automation requires authentication handoff

## Prerequisites

The `ATXP_CONNECTION` environment variable must be defined for LLM access. This provides the connection string to the ATXP platform.

If not configured, see the [ATXP CLI](https://github.com/atxp-dev/cli) for setup instructions.

## Workflow

### 1. Prepare Sensitive Data File

Create a JSON file with the user's sensitive data. Ask the user for the values needed:

```json
{
  "credentials": {
    "username": "user@example.com",
    "password": "secret"
  },
  "payment": {
    "cardNumber": "4111111111111111",
    "expiry": "12/28",
    "cvv": "123",
    "billingZip": "94102"
  },
  "personal": {
    "fullName": "Jane Doe",
    "phone": "+1-555-0123",
    "address": "123 Main St"
  }
}
```

Only include the fields needed for the task. Store securely and delete after use.

### 2. Execute the Sensitive Action

```bash
npx sensitive-browser "<task>" \
  --sensitive-data ./creds.json \
  --url <target-url> \
  --state ./session.json \
  --output ./session.json
```

**Options:**
| Option | Description |
|--------|-------------|
| `<task>` | Natural language task (e.g., "log in with credentials") |
| `-d, --sensitive-data <path>` | Path to sensitive data JSON (required) |
| `-u, --url <url>` | Target URL to navigate to |
| `-s, --state <path>` | Playwright storage state to load |
| `-o, --output <path>` | Output path for updated state |

### 3. Integration with agent-browser

When used with agent-browser, hand off session state:

```bash
# Save current session
agent-browser --session myapp state save ./session.json

# Hand off to sensitive-browser for login
npx sensitive-browser "log in with credentials" \
  --state ./session.json \
  --sensitive-data ./creds.json

# Resume agent-browser with authenticated session
agent-browser --session myapp state load ./session.json
```

## Security Notes

- Sensitive data values are never logged or displayed
- The tool shows which fields will be used, not their values
- Delete sensitive data files after use
- Consider environment variables or secret managers for production

## Sensitive Data Schema

Supported field categories:

- `credentials`: username, password, email
- `payment`: cardNumber, expiry, cvv, billingZip, cardholderName
- `personal`: fullName, firstName, lastName, phone, address, city, state, zip, country, dateOfBirth
- Custom fields: Any additional `key: value` pairs as needed

---
name: google-sheets
description: |
  Read Google Sheets spreadsheets - get content, fetch specific ranges, search for spreadsheets, and view metadata.
  Use when user asks to: read a spreadsheet, get data from Google Sheets, find a spreadsheet, check sheet contents,
  export spreadsheet data, or get cell values. Lightweight alternative to full Google Workspace MCP server with
  standalone OAuth authentication. Read-only access.
---

# Google Sheets

Lightweight Google Sheets integration with standalone OAuth authentication. No MCP server required. Read-only access.

> **⚠️ Requires Google Workspace account.** Personal Gmail accounts are not supported.

## First-Time Setup

Authenticate with Google (opens browser):
```bash
python scripts/auth.py login
```

Check authentication status:
```bash
python scripts/auth.py status
```

Logout when needed:
```bash
python scripts/auth.py logout
```

## Commands

All operations via `scripts/sheets.py`. Auto-authenticates on first use if not logged in.

```bash
# Get spreadsheet content as plain text (default)
python scripts/sheets.py get-text SPREADSHEET_ID

# Get spreadsheet content as CSV
python scripts/sheets.py get-text SPREADSHEET_ID --format csv

# Get spreadsheet content as JSON
python scripts/sheets.py get-text SPREADSHEET_ID --format json

# Get values from a specific range (A1 notation)
python scripts/sheets.py get-range SPREADSHEET_ID "Sheet1!A1:D10"
python scripts/sheets.py get-range SPREADSHEET_ID "A1:C5"

# Find spreadsheets by search query
python scripts/sheets.py find "budget 2024"
python scripts/sheets.py find "sales report" --limit 5

# Get spreadsheet metadata (sheets, dimensions, etc.)
python scripts/sheets.py get-metadata SPREADSHEET_ID
```

## Spreadsheet ID

You can use either:
- The spreadsheet ID: `1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms`
- The full URL: `https://docs.google.com/spreadsheets/d/1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms/edit`

The script automatically extracts the ID from URLs.

## Output Formats

### Text (default)
Human-readable format with pipe separators:
```
Spreadsheet Title: Sales Data
Sheet Name: Q1
Name | Revenue | Units
Product A | 10000 | 50
Product B | 15000 | 75
```

### CSV
Standard CSV format, suitable for further processing:
```
Name,Revenue,Units
Product A,10000,50
Product B,15000,75
```

### JSON
Structured data format:
```json
{
  "Q1": [
    ["Name", "Revenue", "Units"],
    ["Product A", "10000", "50"]
  ]
}
```

## A1 Notation Examples

- `Sheet1!A1:B10` - Range A1 to B10 on Sheet1
- `Sheet1!A:A` - All of column A on Sheet1
- `Sheet1!1:1` - All of row 1 on Sheet1
- `A1:C5` - Range on the first sheet

## Token Management

Tokens stored securely using the system keyring:
- **macOS**: Keychain
- **Windows**: Windows Credential Locker
- **Linux**: Secret Service API (GNOME Keyring, KDE Wallet, etc.)

Service name: `google-sheets-skill-oauth`

Tokens automatically refresh when expired using Google's cloud function.

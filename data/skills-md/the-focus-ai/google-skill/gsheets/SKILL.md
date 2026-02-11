---
name: gsheets
description: This skill should be used when the user asks to "read spreadsheet", "write to sheet", "create spreadsheet", "list spreadsheets", "google sheets", "read cells", "write cells", "append rows", "sheet data", or mentions Google Sheets operations. Provides Google Sheets API integration for reading, writing, and managing spreadsheets.
version: 0.1.0
---

# Google Sheets Skill

Create, read, write, and manage Google Sheets spreadsheets.

## First-Time Setup

Run `npx tsx ${CLAUDE_PLUGIN_ROOT}/scripts/gmail.ts auth` to authenticate with Google. This opens a browser for OAuth consent and grants access to all Google services including Sheets.

Tokens are stored per-project in `.claude/google-skill.local.json`.

## Using Your Own Credentials (Optional)

By default, this skill uses embedded OAuth credentials. To use your own Google Cloud project instead, save your credentials to `~/.config/google-skill/credentials.json`.

## Commands

```bash
# List your spreadsheets
npx tsx ${CLAUDE_PLUGIN_ROOT}/scripts/gsheets.ts list
npx tsx ${CLAUDE_PLUGIN_ROOT}/scripts/gsheets.ts list --max=50

# Get spreadsheet metadata (title, sheets, etc.)
npx tsx ${CLAUDE_PLUGIN_ROOT}/scripts/gsheets.ts get <spreadsheetId>

# Read cell values (A1 notation)
npx tsx ${CLAUDE_PLUGIN_ROOT}/scripts/gsheets.ts read <spreadsheetId> "Sheet1!A1:D10"

# Write values to cells
npx tsx ${CLAUDE_PLUGIN_ROOT}/scripts/gsheets.ts write <spreadsheetId> "Sheet1!A1" \
  --values='[["Hello","World"],["Row 2","Data"]]'

# Append rows to end of sheet
npx tsx ${CLAUDE_PLUGIN_ROOT}/scripts/gsheets.ts append <spreadsheetId> "Sheet1!A:D" \
  --values='[["New","Row","Data"]]'

# Clear a range
npx tsx ${CLAUDE_PLUGIN_ROOT}/scripts/gsheets.ts clear <spreadsheetId> "Sheet1!A1:D10"

# Create new spreadsheet
npx tsx ${CLAUDE_PLUGIN_ROOT}/scripts/gsheets.ts create --title="My Spreadsheet"
npx tsx ${CLAUDE_PLUGIN_ROOT}/scripts/gsheets.ts create --title="Project Data" --sheets="Q1,Q2,Q3,Q4"

# Add new sheet/tab to existing spreadsheet
npx tsx ${CLAUDE_PLUGIN_ROOT}/scripts/gsheets.ts add-sheet <spreadsheetId> --title="New Tab"
```

## A1 Notation Reference

| Notation | Meaning |
|----------|---------|
| `Sheet1!A1` | Single cell A1 in Sheet1 |
| `Sheet1!A1:D10` | Range from A1 to D10 |
| `Sheet1!A:D` | Columns A through D (all rows) |
| `Sheet1!1:10` | Rows 1 through 10 (all columns) |
| `A1:D10` | Range in first sheet |

## Values Format

Values are JSON arrays of arrays:
```json
[
  ["Header 1", "Header 2", "Header 3"],
  ["Row 1", 123, true],
  ["Row 2", 456, false]
]
```

Supported value types: strings, numbers, booleans, null (empty cell).

## Output

All commands return JSON with `success` and `data` fields.

## Help

```bash
npx tsx ${CLAUDE_PLUGIN_ROOT}/scripts/gsheets.ts --help
```

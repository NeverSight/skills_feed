---
name: google-sheets
description: Manage Google Sheets spreadsheets. Read/write cell values and ranges, manage sheets, formatting, and formulas. Use when working with Google Sheets spreadsheet management.
metadata:
  author: odyssey4me
  version: "0.1.0"
license: MIT
---

# Google Sheets

Interact with Google Sheets for spreadsheet management, data manipulation, and formula operations.

## Installation

1. **Install Python dependencies**:
   ```bash
   pip install --user google-auth google-auth-oauthlib google-api-python-client keyring pyyaml
   ```

2. **Download the skill** from [Releases](https://github.com/odyssey4me/agent-skills/releases) or use directly from this repository.

## Setup Verification

After installation, verify the skill is properly configured:

```bash
python scripts/google-sheets.py check
```

This will check:
- Python dependencies (google-auth, google-auth-oauthlib, google-api-python-client, keyring, pyyaml)
- Authentication configuration
- Connectivity to Google Sheets API

If anything is missing, the check command will provide setup instructions.

## Authentication

Google Sheets uses OAuth 2.0 for authentication. For complete setup instructions, see:

1. [GCP Project Setup Guide](../../docs/gcp-project-setup.md) - Create project, enable Sheets API
2. [Google OAuth Setup Guide](../../docs/google-oauth-setup.md) - Configure credentials

### Quick Start

1. Create `~/.config/agent-skills/google.yaml`:
   ```yaml
   oauth_client:
     client_id: your-client-id.apps.googleusercontent.com
     client_secret: your-client-secret
   ```

2. Run `python scripts/google-sheets.py check` to trigger OAuth flow and verify setup.

### OAuth Scopes

The skill requests granular scopes for different operations:

| Scope | Permission | Used For |
|-------|-----------|----------|
| `spreadsheets.readonly` | Read spreadsheets | Reading cell values and metadata |
| `spreadsheets` | Full access | Creating and modifying spreadsheets |

### Scope Errors

If you encounter "insufficient scope" errors, revoke your token and re-authenticate:

1. Revoke at https://myaccount.google.com/permissions
2. Clear token: `keyring del agent-skills google-sheets-token-json`
3. Re-run: `python scripts/google-sheets.py check`

## Commands

### check

Verify configuration and connectivity.

```bash
python scripts/google-sheets.py check
```

This validates:
- Python dependencies are installed
- Authentication is configured
- Can connect to Google Sheets API
- Creates a test spreadsheet to verify write access

### auth setup

Store OAuth 2.0 client credentials for custom OAuth flow.

```bash
python scripts/google-sheets.py auth setup \
  --client-id YOUR_CLIENT_ID \
  --client-secret YOUR_CLIENT_SECRET
```

Credentials are saved to `~/.config/agent-skills/google-sheets.yaml`.

**Options:**
- `--client-id` - OAuth 2.0 client ID (required)
- `--client-secret` - OAuth 2.0 client secret (required)

### spreadsheets create

Create a new Google Sheets spreadsheet.

```bash
python scripts/google-sheets.py spreadsheets create --title "My Spreadsheet"
```

**Options:**
- `--title` - Spreadsheet title (required)
- `--sheets` - Comma-separated sheet names (optional)
- `--json` - Output as JSON

**Example:**
```bash
# Create with default Sheet1
python scripts/google-sheets.py spreadsheets create --title "Sales Data"

# Create with custom sheets
python scripts/google-sheets.py spreadsheets create \
  --title "Q1 Report" \
  --sheets "Summary,January,February,March"

# Output:
# ✓ Spreadsheet created successfully
# Title: Q1 Report
# Spreadsheet ID: 1abc...xyz
# Sheets: 4 (Summary, January, February, March)
# URL: https://docs.google.com/spreadsheets/d/1abc...xyz/edit
```

### spreadsheets get

Get spreadsheet metadata and structure.

```bash
python scripts/google-sheets.py spreadsheets get SPREADSHEET_ID
```

**Arguments:**
- `spreadsheet_id` - The Google Sheets spreadsheet ID

**Options:**
- `--json` - Output full spreadsheet structure as JSON

**Example:**
```bash
python scripts/google-sheets.py spreadsheets get 1abc...xyz

# Output:
# Title: Sales Data
# Spreadsheet ID: 1abc...xyz
# Sheets: 2 (Sheet1, Summary)
# URL: https://docs.google.com/spreadsheets/d/1abc...xyz/edit
```

### values read

Read cell values from a range.

```bash
python scripts/google-sheets.py values read SPREADSHEET_ID --range "Sheet1!A1:D5"
```

**Arguments:**
- `spreadsheet_id` - The Google Sheets spreadsheet ID

**Options:**
- `--range` - Range in A1 notation (required, e.g., "Sheet1!A1:D5")
- `--format` - Value format: FORMATTED_VALUE (default), UNFORMATTED_VALUE, or FORMULA
- `--json` - Output as JSON

**Example:**
```bash
# Read a range
python scripts/google-sheets.py values read 1abc...xyz --range "Sheet1!A1:C3"

# Output (formatted as table):
# Name      | Age | City
# Alice     | 30  | NYC
# Bob       | 25  | LA

# Read formulas
python scripts/google-sheets.py values read 1abc...xyz \
  --range "Sheet1!D1:D10" \
  --format FORMULA
```

See [references/range-notation.md](references/range-notation.md) for A1 notation details.

### values write

Write values to a range.

```bash
python scripts/google-sheets.py values write SPREADSHEET_ID \
  --range "Sheet1!A1" \
  --values '[[\"Name\",\"Age\"],[\"Alice\",30]]'
```

**Arguments:**
- `spreadsheet_id` - The Google Sheets spreadsheet ID

**Options:**
- `--range` - Starting range in A1 notation (required)
- `--values` - Values as JSON 2D array (required)
- `--json` - Output API response as JSON

**Example:**
```bash
# Write data starting at A1
python scripts/google-sheets.py values write 1abc...xyz \
  --range "Sheet1!A1" \
  --values '[[\"Product\",\"Price\",\"Quantity\"],[\"Widget\",9.99,100]]'

# Write a single row
python scripts/google-sheets.py values write 1abc...xyz \
  --range "Sheet1!A5" \
  --values '[[\"Total\",999,50]]'

# Output:
# ✓ Values written successfully
#   Updated cells: 6
#   Updated range: Sheet1!A1:C2
```

**Note:** Values are entered as the user would type them. Formulas start with `=`.

### values append

Append rows to the end of a sheet.

```bash
python scripts/google-sheets.py values append SPREADSHEET_ID \
  --range "Sheet1" \
  --values '[[\"New\",\"Row\",\"Data\"]]'
```

**Arguments:**
- `spreadsheet_id` - The Google Sheets spreadsheet ID

**Options:**
- `--range` - Sheet name or range (required)
- `--values` - Values as JSON 2D array (required)
- `--json` - Output API response as JSON

**Example:**
```bash
# Append a single row
python scripts/google-sheets.py values append 1abc...xyz \
  --range "Sheet1" \
  --values '[[\"Charlie\",35,\"Chicago\"]]'

# Append multiple rows
python scripts/google-sheets.py values append 1abc...xyz \
  --range "Sheet1" \
  --values '[[\"David\",28,\"Boston\"],[\"Eve\",32,\"Seattle\"]]'

# Output:
# ✓ Values appended successfully
#   Updated cells: 3
#   Updated range: Sheet1!A4:C4
```

### values clear

Clear values in a range.

```bash
python scripts/google-sheets.py values clear SPREADSHEET_ID --range "Sheet1!A1:D10"
```

**Arguments:**
- `spreadsheet_id` - The Google Sheets spreadsheet ID

**Options:**
- `--range` - Range in A1 notation (required)
- `--json` - Output API response as JSON

**Example:**
```bash
# Clear a range
python scripts/google-sheets.py values clear 1abc...xyz --range "Sheet1!A1:Z100"

# Output:
# ✓ Values cleared successfully
#   Cleared range: Sheet1!A1:Z100
```

**Warning:** This only clears values, not formatting or formulas in protected cells.

### sheets create

Add a new sheet to a spreadsheet.

```bash
python scripts/google-sheets.py sheets create SPREADSHEET_ID --title "New Sheet"
```

**Arguments:**
- `spreadsheet_id` - The Google Sheets spreadsheet ID

**Options:**
- `--title` - Sheet title (required)
- `--json` - Output API response as JSON

**Example:**
```bash
python scripts/google-sheets.py sheets create 1abc...xyz --title "Q2 Data"

# Output:
# ✓ Sheet created successfully
#   Title: Q2 Data
#   Sheet ID: 123456789
```

### sheets delete

Delete a sheet from a spreadsheet.

```bash
python scripts/google-sheets.py sheets delete SPREADSHEET_ID --sheet-id 123456789
```

**Arguments:**
- `spreadsheet_id` - The Google Sheets spreadsheet ID

**Options:**
- `--sheet-id` - Sheet ID (required, not the title!)
- `--json` - Output API response as JSON

**Example:**
```bash
# Get sheet IDs first
python scripts/google-sheets.py spreadsheets get 1abc...xyz --json | jq '.sheets[].properties | {title, sheetId}'

# Delete a sheet
python scripts/google-sheets.py sheets delete 1abc...xyz --sheet-id 123456789

# Output:
# ✓ Sheet deleted successfully
```

**Warning:** Cannot delete the last remaining sheet in a spreadsheet.

## Examples

### Create and populate a spreadsheet

```bash
# Create spreadsheet
SS_ID=$(python scripts/google-sheets.py spreadsheets create \
  --title "Employee Data" --json | jq -r '.spreadsheetId')

# Write headers
python scripts/google-sheets.py values write $SS_ID \
  --range "Sheet1!A1" \
  --values '[["Name","Department","Salary","Start Date"]]'

# Append employee records
python scripts/google-sheets.py values append $SS_ID \
  --range "Sheet1" \
  --values '[["Alice","Engineering",120000,"2023-01-15"],["Bob","Sales",95000,"2023-03-01"]]'

# Add a summary sheet
python scripts/google-sheets.py sheets create $SS_ID --title "Summary"

# Read the data
python scripts/google-sheets.py values read $SS_ID --range "Sheet1!A1:D10"
```

### Work with formulas

```bash
# Write data with formulas
python scripts/google-sheets.py values write $SS_ID \
  --range "Sheet1!A1" \
  --values '[["Item","Price","Qty","Total"],["Widget",10,5,"=B2*C2"],["Gadget",20,3,"=B3*C3"]]'

# Read formulas
python scripts/google-sheets.py values read $SS_ID \
  --range "Sheet1!D2:D3" \
  --format FORMULA

# Read calculated values
python scripts/google-sheets.py values read $SS_ID \
  --range "Sheet1!D2:D3" \
  --format FORMATTED_VALUE
```

### Batch operations

```bash
#!/bin/bash
SS_ID="your-spreadsheet-id"

# Clear old data
python scripts/google-sheets.py values clear $SS_ID --range "Sheet1!A1:Z1000"

# Write new data in batches
python scripts/google-sheets.py values write $SS_ID \
  --range "Sheet1!A1" \
  --values '[["Date","Revenue","Expenses","Profit"]]'

for month in Jan Feb Mar; do
  python scripts/google-sheets.py values append $SS_ID \
    --range "Sheet1" \
    --values "[[\"\$month\",10000,7000,\"=B${ROW}-C${ROW}\"]]"
done
```

## Troubleshooting

### "Insufficient scope" errors

You need to revoke and re-authenticate to grant additional permissions:

1. Go to https://myaccount.google.com/permissions
2. Find "Agent Skills" and remove access
3. Delete stored token: `keyring del agent-skills google-sheets-token-json`
4. Run `python scripts/google-sheets.py check` to re-authenticate

### Cannot find spreadsheet

Make sure you're using the correct spreadsheet ID from the URL:
- URL: `https://docs.google.com/spreadsheets/d/1abc...xyz/edit`
- Spreadsheet ID: `1abc...xyz`

### Invalid range errors

- Use proper A1 notation: `Sheet1!A1:D5`
- Sheet names with spaces need quotes: `'My Sheet'!A1:B2`
- See [references/range-notation.md](references/range-notation.md) for details

### JSON parsing errors for --values

Ensure proper JSON escaping:
```bash
# Correct
--values '[["Hello","World"]]'
--values "[[\"Name\",\"Age\"]]"

# Incorrect
--values [[Hello,World]]  # Missing quotes
```

### Sheet ID vs Sheet Title

Commands use different identifiers:
- `sheets create` - Uses title (string)
- `sheets delete` - Uses sheet ID (number)
- Use `spreadsheets get --json` to find sheet IDs

### Dependencies not found

Install required dependencies:

```bash
pip install --user google-auth google-auth-oauthlib google-api-python-client keyring pyyaml
```

### OAuth flow fails

Ensure your GCP project has:
1. Google Sheets API enabled (`sheets.googleapis.com`)
2. OAuth 2.0 credentials created
3. OAuth consent screen configured
4. Your email added as a test user (if app is in testing mode)

See [docs/gcp-project-setup.md](../../docs/gcp-project-setup.md) for detailed instructions.

## Related Skills

- [Google Drive](../google-drive/SKILL.md) - File management (Drive manages file metadata, Sheets manages content)
- [Google Docs](../google-docs/SKILL.md) - Document creation and editing
- [Google Slides](../google-slides/SKILL.md) - Presentation management

## API Reference

For advanced usage, see:
- [Google Sheets API Documentation](https://developers.google.com/sheets/api)
- [Reading and writing cell values](https://developers.google.com/sheets/api/guides/values)
- [A1 notation reference](references/range-notation.md)
- [Formula examples](references/formulas-guide.md)

---
name: google-sheets
description: Google Sheets API via curl. Use this skill to read, write, and manage spreadsheet data programmatically.
vm0_secrets:
  - GOOGLE_SHEETS_CLIENT_SECRET
  - GOOGLE_SHEETS_REFRESH_TOKEN
vm0_vars:
  - GOOGLE_SHEETS_CLIENT_ID
---

# Google Sheets API

Use the Google Sheets API via direct `curl` calls to **read, write, and manage spreadsheet data**.

> Official docs: `https://developers.google.com/sheets/api`

---

## When to Use

Use this skill when you need to:

- **Read data** from Google Sheets
- **Write or update** cell values
- **Append rows** to existing sheets
- **Create new spreadsheets**
- **Get spreadsheet metadata** (sheet names, properties)
- **Batch update** multiple ranges at once

---

## Prerequisites

### Option 1: OAuth Playground (Recommended for testing)

1. **Create Google Cloud Project**
   - Go to https://console.cloud.google.com
   - Create a new project or select existing
   - Enable Google Sheets API: https://console.cloud.google.com/apis/library/sheets.googleapis.com

2. **Configure OAuth Consent Screen**
   - Go to https://console.cloud.google.com/apis/credentials/consent
   - Select **External** → Create
   - Fill required fields (app name, support email, developer email)
   - Click **Save and Continue** through Scopes (skip adding scopes)
   - In **Audience** section, click **Add Users** and add your Gmail address as test user
   - Save and continue to finish

3. **Create OAuth Client ID**
   - Go to https://console.cloud.google.com/apis/credentials
   - Click **Create Credentials** → **OAuth client ID**
   - Choose **Web application** (not Desktop)
   - Add Authorized redirect URI: `https://developers.google.com/oauthplayground`
   - Click Create and note the **Client ID** and **Client Secret**

4. **Get Refresh Token**
   - Go to https://developers.google.com/oauthplayground/
   - Click **Settings** (gear icon ⚙️) → Check **Use your own OAuth credentials**
   - Enter your Client ID and Client Secret
   - In the left panel, enter scope: `https://www.googleapis.com/auth/spreadsheets`
   - Click **Authorize APIs** → Sign in with your test user account
   - Click **Exchange authorization code for tokens**
   - Copy the **Refresh token**

5. **Set Environment Variables**

```bash
export GOOGLE_SHEETS_CLIENT_ID="your-client-id"
export GOOGLE_SHEETS_CLIENT_SECRET="your-client-secret"
export GOOGLE_SHEETS_REFRESH_TOKEN="your-refresh-token"
```

6. **Get Access Token** (before making API calls)

```bash
bash -c 'curl -s -X POST "https://oauth2.googleapis.com/token" -d "client_id=$GOOGLE_SHEETS_CLIENT_ID" -d "client_secret=$GOOGLE_SHEETS_CLIENT_SECRET" -d "refresh_token=$GOOGLE_SHEETS_REFRESH_TOKEN" -d "grant_type=refresh_token"' | jq -r '.access_token' > /tmp/sheets_token.txt

# Verify token was obtained
head -c 20 /tmp/sheets_token.txt && echo "..."
```

Then use `$(cat /tmp/sheets_token.txt)` inside `bash -c` wrappers for API calls.

### Option 2: Service Account

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a project and enable the Google Sheets API
3. Create a Service Account and download JSON key
4. Share your spreadsheet with the service account email
5. Generate access token:

```bash
gcloud auth activate-service-account --key-file=service-account.json
export GOOGLE_ACCESS_TOKEN=$(gcloud auth print-access-token)
```

### Option 3: API Key (Read-only, Public Sheets)

For publicly accessible sheets, you can use an API key:

```bash
export GOOGLE_API_KEY="your-api-key"
```

---


> **Important:** When using `$VAR` in a command that pipes to another command, wrap the command containing `$VAR` in `bash -c '...'`. Due to a Claude Code bug, environment variables are silently cleared when pipes are used directly.
> ```bash
> bash -c 'curl -s "https://api.example.com" -H "Authorization: Bearer $API_KEY"'
> ```

## How to Use

All examples below use `${GOOGLE_ACCESS_TOKEN}`. Before running, either:
- Set manually: `GOOGLE_ACCESS_TOKEN="ya29.xxx..."`, or
- Replace `${GOOGLE_ACCESS_TOKEN}` with `$(cat /tmp/sheets_token.txt)` in each command

> **Important:** In range notation like `Sheet1!A1:D10`, the `!` must be URL encoded as `%21` in the URL path (e.g., `Sheet1%21A1:D10`). All examples below use this encoding.

Base URL: `https://sheets.googleapis.com/v4/spreadsheets`

**Finding your Spreadsheet ID:**
The spreadsheet ID is in the URL: `https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/edit`

---

### 1. Get Spreadsheet Metadata

Get information about a spreadsheet (sheets, properties). Replace `<your-spreadsheet-id>` with your actual spreadsheet ID:

```bash
bash -c 'curl -s "https://sheets.googleapis.com/v4/spreadsheets/<your-spreadsheet-id>" -H "Authorization: Bearer ${GOOGLE_ACCESS_TOKEN}"' | jq '{title: .properties.title, sheets: [.sheets[].properties | {sheetId, title}]}''
```

---

### 2. Read Cell Values

Read a range of cells. Replace `<your-spreadsheet-id>` with your actual spreadsheet ID:

```bash
bash -c 'curl -s "https://sheets.googleapis.com/v4/spreadsheets/<your-spreadsheet-id>/values/Sheet1%21A1:D10" -H "Authorization: Bearer ${GOOGLE_ACCESS_TOKEN}"' | jq '.values'
```

---

### 3. Read Entire Sheet

Read all data from a sheet. Replace `<your-spreadsheet-id>` with your actual spreadsheet ID:

```bash
bash -c 'curl -s "https://sheets.googleapis.com/v4/spreadsheets/<your-spreadsheet-id>/values/Sheet1" -H "Authorization: Bearer ${GOOGLE_ACCESS_TOKEN}"' | jq '.values'
```

---

### 4. Read with API Key (Public Sheets)

For publicly accessible sheets. Replace `<your-spreadsheet-id>` with your actual spreadsheet ID:

```bash
bash -c 'curl -s "https://sheets.googleapis.com/v4/spreadsheets/<your-spreadsheet-id>/values/Sheet1%21A1:D10?key=${GOOGLE_API_KEY}"' | jq '.values'
```

---

### 5. Write Cell Values

Update a range of cells. Replace `<your-spreadsheet-id>` with your actual spreadsheet ID.

Write to `/tmp/gsheets_request.json`:

```json
{
  "values": [
    ["Name", "Email", "Status"]
  ]
}
```

Then run:

```bash
bash -c 'curl -s -X PUT "https://sheets.googleapis.com/v4/spreadsheets/<your-spreadsheet-id>/values/Sheet1%21A1:C1?valueInputOption=USER_ENTERED" -H "Authorization: Bearer ${GOOGLE_ACCESS_TOKEN}" -H "Content-Type: application/json" -d @/tmp/gsheets_request.json' | jq '.updatedCells'
```

**valueInputOption:**
- `RAW`: Values are stored as-is
- `USER_ENTERED`: Values are parsed as if typed by user (formulas evaluated)

---

### 6. Append Rows

Add new rows to the end of a sheet. Replace `<your-spreadsheet-id>` with your actual spreadsheet ID.

Write to `/tmp/gsheets_request.json`:

```json
{
  "values": [
    ["John Doe", "john@example.com", "Active"]
  ]
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://sheets.googleapis.com/v4/spreadsheets/<your-spreadsheet-id>/values/Sheet1%21A:C:append?valueInputOption=USER_ENTERED&insertDataOption=INSERT_ROWS" -H "Authorization: Bearer ${GOOGLE_ACCESS_TOKEN}" -H "Content-Type: application/json" -d @/tmp/gsheets_request.json' | jq '.updates | {updatedRange, updatedRows}'
```

---

### 7. Batch Read Multiple Ranges

Read multiple ranges in one request. Replace `<your-spreadsheet-id>` with your actual spreadsheet ID:

```bash
bash -c 'curl -s "https://sheets.googleapis.com/v4/spreadsheets/<your-spreadsheet-id>/values:batchGet?ranges=Sheet1%21A1:B5&ranges=Sheet1%21D1:E5" -H "Authorization: Bearer ${GOOGLE_ACCESS_TOKEN}"' | jq '.valueRanges'
```

---

### 8. Batch Update Multiple Ranges

Update multiple ranges in one request. Replace `<your-spreadsheet-id>` with your actual spreadsheet ID.

Write to `/tmp/gsheets_request.json`:

```json
{
  "valueInputOption": "USER_ENTERED",
  "data": [
    {
      "range": "Sheet1!A1",
      "values": [["Header 1"]]
    },
    {
      "range": "Sheet1!B1",
      "values": [["Header 2"]]
    }
  ]
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://sheets.googleapis.com/v4/spreadsheets/<your-spreadsheet-id>/values:batchUpdate" -H "Authorization: Bearer ${GOOGLE_ACCESS_TOKEN}" -H "Content-Type: application/json" -d @/tmp/gsheets_request.json' | jq '.totalUpdatedCells'
```

---

### 9. Clear Cell Values

Clear a range of cells. Replace `<your-spreadsheet-id>` with your actual spreadsheet ID.

Write to `/tmp/gsheets_request.json`:

```json
{}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://sheets.googleapis.com/v4/spreadsheets/<your-spreadsheet-id>/values/Sheet1%21A2:C100:clear" -H "Authorization: Bearer ${GOOGLE_ACCESS_TOKEN}" -H "Content-Type: application/json" -d @/tmp/gsheets_request.json' | jq '.clearedRange'
```

---

### 10. Create New Spreadsheet

Create a new spreadsheet:

Write to `/tmp/gsheets_request.json`:

```json
{
  "properties": {
    "title": "My New Spreadsheet"
  },
  "sheets": [
    {
      "properties": {
        "title": "Data"
      }
    }
  ]
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://sheets.googleapis.com/v4/spreadsheets" -H "Authorization: Bearer ${GOOGLE_ACCESS_TOKEN}" -H "Content-Type: application/json" -d @/tmp/gsheets_request.json' | jq '.spreadsheetId, .spreadsheetUrl'
```

---

### 11. Add New Sheet

Add a new sheet to an existing spreadsheet. Replace `<your-spreadsheet-id>` with your actual spreadsheet ID.

Write to `/tmp/gsheets_request.json`:

```json
{
  "requests": [
    {
      "addSheet": {
        "properties": {
          "title": "New Sheet"
        }
      }
    }
  ]
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://sheets.googleapis.com/v4/spreadsheets/<your-spreadsheet-id>:batchUpdate" -H "Authorization: Bearer ${GOOGLE_ACCESS_TOKEN}" -H "Content-Type: application/json" -d @/tmp/gsheets_request.json' | jq '.replies[0].addSheet.properties'
```

---

### 12. Delete Sheet

Delete a sheet from a spreadsheet (use sheetId from metadata). Replace `<your-spreadsheet-id>` with your actual spreadsheet ID.

Write to `/tmp/gsheets_request.json`:

```json
{
  "requests": [
    {
      "deleteSheet": {
        "sheetId": 123456789
      }
    }
  ]
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://sheets.googleapis.com/v4/spreadsheets/<your-spreadsheet-id>:batchUpdate" -H "Authorization: Bearer ${GOOGLE_ACCESS_TOKEN}" -H "Content-Type: application/json" -d @/tmp/gsheets_request.json'
```

---

### 13. Search for Values

Find cells containing specific text (read all then filter). Replace `<your-spreadsheet-id>` with your actual spreadsheet ID:

```bash
bash -c 'curl -s "https://sheets.googleapis.com/v4/spreadsheets/<your-spreadsheet-id>/values/Sheet1" -H "Authorization: Bearer ${GOOGLE_ACCESS_TOKEN}"' | jq '[.values[] | select(.[0] | ascii_downcase | contains("search_term"))]'
```

---

## A1 Notation Reference

| Notation | Description |
|----------|-------------|
| `Sheet1!A1` | Single cell A1 in Sheet1 |
| `Sheet1!A1:B2` | Range from A1 to B2 |
| `Sheet1!A:A` | Entire column A |
| `Sheet1!1:1` | Entire row 1 |
| `Sheet1!A1:C` | From A1 to end of column C |
| `'Sheet Name'!A1` | Sheet names with spaces need quotes |

---

## Guidelines

1. **Token expiration**: Access tokens expire after ~1 hour; refresh with `gcloud auth print-access-token`
2. **Share with service account**: When using service accounts, share the spreadsheet with the service account email
3. **Rate limits**: Default quota is 300 requests per minute per project
4. **Use batch operations**: Combine multiple reads/writes to reduce API calls
5. **valueInputOption**: Use `USER_ENTERED` for formulas, `RAW` for literal strings
6. **URL encode ranges**: Ranges with special characters need URL encoding (e.g., spaces → `%20`)

---
name: google-sheets
description: Enables Claude to create, edit, analyze, and automate Google Sheets spreadsheets via Playwright MCP
category: google
---

# Google Sheets Skill

## Overview
Claude can work with Google Sheets to create spreadsheets, enter and analyze data, build formulas, create charts, and automate data workflows. This includes reading data, performing calculations, and generating insights from spreadsheet data.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/google-sheets/install.sh | bash
```

Or manually:
```bash
cp -r skills/google-sheets ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set GOOGLE_EMAIL "your-email@gmail.com"
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
- Create new spreadsheets and worksheets
- Read and analyze spreadsheet data
- Enter and edit cell values
- Build and apply formulas and functions
- Create charts and visualizations
- Format cells, rows, and columns
- Sort and filter data
- Create pivot tables
- Import and export data (CSV, XLSX)
- Apply conditional formatting
- Protect sheets and ranges
- Share and collaborate with permissions

## Usage Examples

### Example 1: Create Budget Spreadsheet
```
User: "Create a monthly budget spreadsheet"
Claude: Creates new sheet with columns for Category, Budgeted, Actual, Difference.
        Adds SUM formulas for totals, conditional formatting for over-budget items.
        Returns: "Created budget spreadsheet: [link]"
```

### Example 2: Analyze Data
```
User: "What were my top 5 expenses last month?"
Claude: Opens expense sheet, sorts by amount descending, reads top 5 entries.
        Reports: "Top 5 expenses: 1. Rent $1500, 2. Car Payment $450..."
```

### Example 3: Add Formula
```
User: "Add a formula to calculate the running total in column D"
Claude: Navigates to column D, enters formula =SUM($C$2:C2) in first data row,
        copies formula down to all rows. Confirms: "Running total formula applied"
```

### Example 4: Create Chart
```
User: "Create a pie chart of spending by category"
Claude: Selects category and amount columns, inserts pie chart,
        applies labels and formatting. Reports: "Pie chart created"
```

## Authentication Flow
1. Claude navigates to sheets.google.com via Playwright MCP
2. Authenticates with GOOGLE_EMAIL if needed
3. Handles 2FA if prompted (notifies user via iMessage)
4. Maintains session for subsequent spreadsheet operations

## Selectors Reference
```javascript
// New spreadsheet button
'#newButton' or '[aria-label="New"]'

// Spreadsheet title
'.docs-title-input'

// Cell reference box
'#t-name-box'

// Formula bar
'#t-formula-bar-input'

// Active cell
'.cell-input'

// Sheet tabs
'.docs-sheet-tab'

// Add sheet button
'#sheet-add-button'

// Menu bar
'.menu-button'

// Insert menu
'#docs-insert-menu'

// Format menu
'#docs-format-menu'

// Chart dialog
'.charts-dialog'

// Filter button
'[aria-label="Create a filter"]'
```

## Common Formulas Reference
```
=SUM(A1:A10)           // Sum range
=AVERAGE(A1:A10)       // Average
=VLOOKUP(key,range,col,false)  // Vertical lookup
=IF(condition,true,false)       // Conditional
=COUNTIF(range,criteria)        // Count matching
=SUMIF(range,criteria,sum_range) // Sum matching
=CONCATENATE(A1," ",B1)         // Join text
=TODAY()               // Current date
=GOOGLEFINANCE("GOOG") // Stock price
```

## Error Handling
- **Login Failed**: Retry 3 times, notify user via iMessage
- **Session Expired**: Re-authenticate automatically
- **Spreadsheet Not Found**: Search Drive for similar names, ask user to clarify
- **Formula Error**: Identify error type (#REF!, #VALUE!, etc.), suggest fix
- **Permission Denied**: Notify user, offer to request access
- **Rate Limited**: Wait and retry with exponential backoff

## Self-Improvement Instructions
When you learn a better way to accomplish a task with Google Sheets:
1. Document the improvement in your response
2. Suggest updating this skill file with the new approach
3. Include specific formulas or techniques that worked better
4. Note keyboard shortcuts for efficiency

## Notes
- Google Sheets auto-saves changes
- Large datasets may require pagination or filtering for performance
- Some functions have usage limits (IMPORTDATA, GOOGLEFINANCE)
- Keyboard shortcuts: Ctrl+C/V for copy/paste, Ctrl+Z for undo
- Maximum cell limit: 10 million cells per spreadsheet
- For heavy data processing, consider Apps Script automation

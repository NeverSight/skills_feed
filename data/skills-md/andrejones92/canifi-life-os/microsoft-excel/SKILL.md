---
name: microsoft-excel
description: Enables Claude to create, edit, and analyze spreadsheets in Microsoft Excel Online via Playwright MCP
category: microsoft
---

# Microsoft Excel Skill

## Overview
Claude can work with Microsoft Excel Online to create spreadsheets, analyze data, build formulas, create charts, and automate calculations. Includes support for pivot tables, conditional formatting, and data analysis tools.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/microsoft-excel/install.sh | bash
```

Or manually:
```bash
cp -r skills/microsoft-excel ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set MICROSOFT_EMAIL "your-email@outlook.com"
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
- Create and edit spreadsheets
- Enter and format data
- Build formulas and functions
- Create charts and visualizations
- Apply conditional formatting
- Create pivot tables
- Sort and filter data
- Use data validation
- Import and export data
- Create named ranges
- Protect sheets and workbooks
- Collaborate in real-time

## Usage Examples

### Example 1: Create Spreadsheet
```
User: "Create an expense tracker in Excel"
Claude: Creates new workbook "Expense Tracker", adds columns for
        Date, Category, Description, Amount. Adds SUM formula for total.
        Returns: "Created expense tracker: [link]"
```

### Example 2: Analyze Data
```
User: "Create a pivot table from my sales data"
Claude: Selects data range, inserts pivot table,
        configures rows, columns, and values.
        Confirms: "Pivot table created showing sales by region and product"
```

### Example 3: Create Chart
```
User: "Make a line chart showing revenue trends"
Claude: Selects revenue data, inserts line chart,
        adds titles and labels. Confirms: "Revenue trend chart created"
```

### Example 4: Apply Formulas
```
User: "Add a formula to calculate profit margin in column E"
Claude: Enters formula =(D2-C2)/D2 for margin calculation,
        applies to all rows. Confirms: "Profit margin formula applied"
```

## Authentication Flow
1. Claude navigates to excel.office.com via Playwright MCP
2. Authenticates with MICROSOFT_EMAIL if needed
3. Handles 2FA if prompted (notifies user via iMessage)
4. Maintains session for spreadsheet operations

## Selectors Reference
```javascript
// New workbook
'[aria-label="New blank workbook"]'

// Workbook name
'[aria-label="Workbook name"]'

// Cell input
'.formulabar-input' or 'input[name="Cell"]'

// Active cell
'[aria-selected="true"]'

// Ribbon tabs
'[role="tablist"]'

// Insert tab
'[aria-label="Insert"]'

// Formulas tab
'[aria-label="Formulas"]'

// Data tab
'[aria-label="Data"]'

// Chart button
'[aria-label="Insert chart"]'

// Sort button
'[aria-label="Sort"]'

// Filter button
'[aria-label="Filter"]'
```

## Common Formulas
```
=SUM(A1:A10)              // Sum range
=AVERAGE(A1:A10)          // Average
=VLOOKUP(key,range,col,0) // Vertical lookup
=IF(condition,true,false) // Conditional
=COUNTIF(range,criteria)  // Count matching
=SUMIF(range,crit,sum)    // Sum matching
=TEXT(A1,"format")        // Format text
=TODAY()                  // Current date
=CONCATENATE(A1,B1)       // Join text
```

## Error Handling
- **Login Failed**: Retry 3 times, notify user via iMessage
- **Session Expired**: Re-authenticate automatically
- **Workbook Not Found**: Search OneDrive, ask for clarification
- **Formula Error**: Identify error type, suggest fix
- **Chart Create Failed**: Verify data selection, retry
- **Save Failed**: Enable AutoSave, retry

## Self-Improvement Instructions
When you learn a better way to accomplish a task with Excel Online:
1. Document the improvement in your response
2. Suggest updating this skill file with the new approach
3. Include specific formulas or techniques that work better
4. Note differences from desktop Excel

## Notes
- Excel Online auto-saves to OneDrive
- Some advanced features only in desktop version
- Co-authoring shows other users' selections
- Maximum rows: 1,048,576 per sheet
- Keyboard shortcuts: Ctrl+C/V, Ctrl+Z for undo
- Power Query limited in online version
- Macros not supported in online version
- Can open and edit .xlsx, .xlsm files

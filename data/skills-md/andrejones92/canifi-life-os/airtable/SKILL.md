---
name: airtable
description: Enables Claude to create, manage, and query databases in Airtable via Playwright MCP
category: productivity
---

# Airtable Skill

## Overview
Claude can manage your Airtable bases to create databases, add records, build views, and create automations. A flexible database platform that combines spreadsheet simplicity with database power.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/airtable/install.sh | bash
```

Or manually:
```bash
cp -r skills/airtable ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set AIRTABLE_EMAIL "your-email@example.com"
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
- Create and manage bases
- Add and edit records
- Create tables with custom fields
- Build filtered views
- Create forms for data entry
- Set up automations
- Link between tables
- Create interfaces
- Generate reports
- Use extensions
- Import/export data
- Build apps on data

## Usage Examples

### Example 1: Add Record
```
User: "Add a new contact to the CRM base: John Smith, john@example.com"
Claude: Opens CRM base, adds record with name and email.
        Confirms: "Contact added: John Smith"
```

### Example 2: Query Data
```
User: "Show me all high-priority tasks in Airtable"
Claude: Opens Tasks table, filters by priority.
        Reports: "5 high-priority tasks: Design review, API update..."
```

### Example 3: Create View
```
User: "Create a view showing only overdue items"
Claude: Creates filtered view with due date < today.
        Confirms: "Created 'Overdue Items' view"
```

### Example 4: Update Record
```
User: "Mark the Johnson deal as closed-won"
Claude: Finds record, updates status field.
        Confirms: "Johnson deal status updated to Closed-Won"
```

## Authentication Flow
1. Claude navigates to airtable.com via Playwright MCP
2. Enters AIRTABLE_EMAIL for authentication
3. Handles 2FA if required (notifies user via iMessage)
4. Maintains session for database operations

## Selectors Reference
```javascript
// Base list
'.bases-list'

// Table tabs
'.tableTabList'

// Record rows
'.dataRow'

// Cell content
'.cellContainer'

// Add record button
'[aria-label="Add record"]'

// Field input
'.cellInput'

// View menu
'.viewMenuButton'

// Create view
'.addViewButton'

// Filter button
'[aria-label="Filter"]'

// Sort button
'[aria-label="Sort"]'
```

## Field Types
```
Text            // Single line or long text
Number          // Integer or decimal
Select          // Single or multi-select
Date            // Date with optional time
Checkbox        // Boolean true/false
Link            // Link to another record
Attachment      // Files and images
Formula         // Calculated fields
Rollup          // Aggregate linked records
Lookup          // Pull fields from linked records
```

## Error Handling
- **Login Failed**: Retry 3 times, notify user via iMessage
- **Session Expired**: Re-authenticate automatically
- **Base Not Found**: List available bases, ask user
- **Record Create Failed**: Retry, check required fields
- **Formula Error**: Identify syntax issue, suggest fix
- **Permission Denied**: Notify user of access issue

## Self-Improvement Instructions
When you learn a better way to accomplish a task with Airtable:
1. Document the improvement in your response
2. Suggest updating this skill file with the new approach
3. Include specific base organization patterns
4. Note useful formula techniques

## Notes
- Relational database with spreadsheet interface
- Forms for external data collection
- Automations for workflows
- Extensions for added functionality
- Interfaces for custom apps
- Sync for external data sources
- API for advanced integrations
- Templates for common use cases

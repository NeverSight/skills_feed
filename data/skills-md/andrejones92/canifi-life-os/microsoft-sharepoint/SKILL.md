---
name: microsoft-sharepoint
description: Enables Claude to access, organize, and collaborate on Microsoft SharePoint sites and document libraries via Playwright MCP
category: microsoft
---

# Microsoft SharePoint Skill

## Overview
Claude can interact with Microsoft SharePoint to access team sites, manage document libraries, create pages, and collaborate on organizational content. Ideal for enterprise content management and team collaboration.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/microsoft-sharepoint/install.sh | bash
```

Or manually:
```bash
cp -r skills/microsoft-sharepoint ~/.canifi/skills/
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
- Navigate team and communication sites
- Access document libraries
- Upload and download files
- Create and edit pages
- Search site content
- Manage lists and libraries
- View and edit metadata
- Share documents and folders
- Create news posts
- Access shared files
- Manage site permissions (view only)
- Navigate site hierarchy

## Usage Examples

### Example 1: Find Document
```
User: "Find the HR policies document on SharePoint"
Claude: Searches SharePoint for "HR policies".
        Reports: "Found in HR Team Site > Documents:
        HR Policies 2024.pdf (updated last week)"
```

### Example 2: Access Library
```
User: "Show me what's in the Marketing team's document library"
Claude: Navigates to Marketing site, opens Documents library.
        Reports: "Marketing Documents contains 47 items:
        Folders: Campaigns, Brand Assets, Reports..."
```

### Example 3: Download Report
```
User: "Download the quarterly sales report from SharePoint"
Claude: Locates report in Sales site, downloads file.
        Confirms: "Downloaded Q4 Sales Report.xlsx"
```

### Example 4: Search Content
```
User: "Search SharePoint for project proposals from last month"
Claude: Searches with date filter for "project proposal".
        Reports: "Found 5 proposals:
        1. Website Redesign Proposal (Marketing)..."
```

## Authentication Flow
1. Claude navigates to [tenant].sharepoint.com via Playwright MCP
2. Authenticates with MICROSOFT_EMAIL if needed
3. Handles 2FA if prompted (notifies user via iMessage)
4. Maintains session for SharePoint operations

## Selectors Reference
```javascript
// Site navigation
'[aria-label="Site navigation"]'

// Document library
'[data-automationid="FieldRenderer-name"]'

// File list
'[role="grid"]'

// Search box
'[aria-label="Search"]'

// Upload button
'[aria-label="Upload"]'

// New button
'[aria-label="New"]'

// Download
'[aria-label="Download"]'

// Share button
'[aria-label="Share"]'

// Quick launch
'.ms-Nav-navItems'

// Breadcrumb
'.breadcrumb'
```

## Error Handling
- **Login Failed**: Retry 3 times, notify user via iMessage
- **Session Expired**: Re-authenticate automatically
- **Site Not Found**: List accessible sites, ask for clarification
- **Access Denied**: Notify user of permission requirement
- **File Not Found**: Search variations, check recycle bin
- **Download Failed**: Retry, check permissions

## Self-Improvement Instructions
When you learn a better way to accomplish a task with SharePoint:
1. Document the improvement in your response
2. Suggest updating this skill file with the new approach
3. Include specific navigation patterns
4. Note tenant-specific configurations

## Notes
- SharePoint URL varies by organization tenant
- Permissions managed by site owners/admins
- Document libraries integrate with OneDrive sync
- Metadata enables advanced organization
- Lists for structured data management
- Modern vs classic sites have different UIs
- Search indexes all site content
- News posts for organizational communication

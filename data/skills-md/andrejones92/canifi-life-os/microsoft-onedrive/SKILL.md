---
name: microsoft-onedrive
description: Enables Claude to upload, organize, and manage files in Microsoft OneDrive via Playwright MCP
category: microsoft
---

# Microsoft OneDrive Skill

## Overview
Claude can manage your Microsoft OneDrive to upload files, organize folders, search content, share files, and maintain your cloud storage. Integrates with Microsoft 365 apps for seamless file management.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/microsoft-onedrive/install.sh | bash
```

Or manually:
```bash
cp -r skills/microsoft-onedrive ~/.canifi/skills/
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
- Upload and download files
- Create and organize folders
- Search files by name or content
- Share files and folders with permissions
- Move and copy files
- View file versions
- Manage storage quota
- Create shortcuts
- Access shared files
- Sync status monitoring
- Recover deleted files
- Generate sharing links

## Usage Examples

### Example 1: Find File
```
User: "Find my quarterly report in OneDrive"
Claude: Searches OneDrive for "quarterly report".
        Reports: "Found 3 files:
        1. Q4 Report 2024.docx (modified yesterday)
        2. Q3 Report 2024.xlsx (2 months ago)..."
```

### Example 2: Organize Files
```
User: "Create a folder for client documents and move relevant files"
Claude: Creates "Client Documents" folder, identifies and moves files.
        Confirms: "Created folder, moved 15 files"
```

### Example 3: Share File
```
User: "Share the proposal with sarah@company.com with edit access"
Claude: Locates proposal, shares with Sarah as editor.
        Confirms: "Shared with sarah@company.com (can edit)"
```

### Example 4: Check Storage
```
User: "How much OneDrive storage am I using?"
Claude: Checks storage quota.
        Reports: "Using 45.2 GB of 1 TB (4.5%). Largest items:
        Videos folder (30 GB)..."
```

## Authentication Flow
1. Claude navigates to onedrive.live.com via Playwright MCP
2. Authenticates with MICROSOFT_EMAIL if needed
3. Handles 2FA if prompted (notifies user via iMessage)
4. Maintains session for OneDrive operations

## Selectors Reference
```javascript
// New button
'[aria-label="New"]'

// Upload button
'[aria-label="Upload"]'

// File list
'[role="grid"]'

// File item
'[role="row"]'

// Search box
'[aria-label="Search"]'

// Folder navigation
'.breadcrumb'

// Share button
'[aria-label="Share"]'

// Download button
'[aria-label="Download"]'

// Move to button
'[aria-label="Move to"]'

// Delete button
'[aria-label="Delete"]'

// Storage info
'.storage-info'
```

## Error Handling
- **Login Failed**: Retry 3 times, notify user via iMessage
- **Session Expired**: Re-authenticate automatically
- **File Not Found**: Search with variations, ask for clarification
- **Upload Failed**: Check file size, retry in chunks
- **Share Failed**: Verify email, check sharing restrictions
- **Storage Full**: Notify user, suggest cleanup

## Self-Improvement Instructions
When you learn a better way to accomplish a task with OneDrive:
1. Document the improvement in your response
2. Suggest updating this skill file with the new approach
3. Include specific search or organization tips
4. Note any sync behavior improvements

## Notes
- Free tier: 5 GB storage
- Microsoft 365 subscription: 1 TB+ storage
- Files on demand allows cloud-only storage
- Personal Vault for sensitive files
- Recycle bin retains files for 30 days
- Version history for document recovery
- Integrates with Windows File Explorer
- Mobile apps available for iOS/Android

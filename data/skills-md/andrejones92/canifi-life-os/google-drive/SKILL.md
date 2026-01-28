---
name: google-drive
description: Enables Claude to upload, organize, search, and manage files in Google Drive via Playwright MCP
category: google
---

# Google Drive Skill

## Overview
Claude can manage your Google Drive to upload files, organize folders, search content, share files, and maintain your cloud storage. This includes managing permissions, syncing across devices, and integrating with other Google Workspace apps.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/google-drive/install.sh | bash
```

Or manually:
```bash
cp -r skills/google-drive ~/.canifi/skills/
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
- Upload and download files
- Create and organize folders
- Search files by name, type, or content
- Share files and folders with permissions
- Move and copy files between folders
- View and restore file versions
- Empty trash and manage storage
- Create shortcuts to files
- Star and organize important files
- View storage usage and quota
- Access shared drives and team folders
- Preview documents, images, and videos

## Usage Examples

### Example 1: Find a File
```
User: "Find my resume document"
Claude: Searches Drive for "resume", returns results:
        "Found 3 files: Resume_2024.docx (modified yesterday),
        Resume_old.pdf (3 months ago)..."
```

### Example 2: Organize Files
```
User: "Create a folder for Q4 reports and move all Q4 files there"
Claude: Creates "Q4 Reports" folder, searches for Q4-related files,
        moves them to new folder. Reports: "Created folder, moved 12 files"
```

### Example 3: Share File
```
User: "Share the project proposal with john@example.com as editor"
Claude: Locates file, opens sharing dialog, adds john@example.com with edit
        permissions. Confirms: "Shared with john@example.com (Editor access)"
```

### Example 4: Check Storage
```
User: "How much Drive storage am I using?"
Claude: Opens storage view, reads usage. Reports:
        "Using 8.2 GB of 15 GB (54%). Largest files: video.mp4 (2.1GB)..."
```

## Authentication Flow
1. Claude navigates to drive.google.com via Playwright MCP
2. Authenticates with GOOGLE_EMAIL if needed
3. Handles 2FA if prompted (notifies user via iMessage)
4. Maintains session for subsequent Drive operations

## Selectors Reference
```javascript
// New button
'[aria-label="New"]'

// Search box
'input[aria-label="Search in Drive"]'

// File list
'.Q5txwe' // File rows

// File name
'.KL4NAf'

// Folder navigation
'.a-fc-Uc' // Breadcrumb

// Context menu
'[role="menu"]'

// Share button
'[aria-label="Share"]'

// Download button
'[aria-label="Download"]'

// Move to button
'[aria-label="Move to"]'

// Trash button
'[aria-label="Move to trash"]'

// Storage indicator
'.a-Ja-we'

// Upload file
'[aria-label="File upload"]'

// Create folder
'[aria-label="Folder"]'
```

## Error Handling
- **Login Failed**: Retry 3 times, notify user via iMessage
- **Session Expired**: Re-authenticate automatically
- **File Not Found**: Search with variations, ask user to clarify
- **Upload Failed**: Retry with smaller chunks, check file size limits
- **Share Failed**: Verify email address, check sharing restrictions
- **Storage Full**: Notify user, suggest cleanup options
- **Permission Denied**: Notify user, explain access requirements

## Self-Improvement Instructions
When you learn a better way to accomplish a task with Google Drive:
1. Document the improvement in your response
2. Suggest updating this skill file with the new approach
3. Include specific search operators or navigation tips
4. Note any organizational best practices

## Notes
- Free storage: 15 GB shared across Drive, Gmail, Photos
- Maximum file size: 5 TB
- Search operators: type:pdf, owner:me, before:2024-01-01
- Shared drives for team collaboration
- Offline access available for specific files
- Version history retained for 30 days (or 100 versions)
- Trash auto-deletes after 30 days
- Keyboard shortcuts: N for new, / for search

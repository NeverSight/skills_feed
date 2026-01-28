---
name: microsoft-word
description: Enables Claude to create, edit, and format documents in Microsoft Word Online via Playwright MCP
category: microsoft
---

# Microsoft Word Skill

## Overview
Claude can work with Microsoft Word Online to create, edit, and format documents. This includes writing content, applying styles, inserting media, collaborating with comments, and exporting documents.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/microsoft-word/install.sh | bash
```

Or manually:
```bash
cp -r skills/microsoft-word ~/.canifi/skills/
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
- Create new documents from scratch or templates
- Read and edit existing documents
- Apply formatting and styles
- Insert images, tables, and charts
- Add headers, footers, and page numbers
- Track changes and add comments
- Create table of contents
- Export as PDF, DOCX, or other formats
- Collaborate in real-time
- Use dictation and voice typing
- Apply templates and themes

## Usage Examples

### Example 1: Create Document
```
User: "Create a Word document for my project report"
Claude: Creates new document "Project Report", adds title,
        sections for Introduction, Methodology, Results, Conclusion.
        Returns: "Created document: [link]"
```

### Example 2: Format Document
```
User: "Apply professional formatting to my resume"
Claude: Opens resume, applies consistent heading styles,
        adjusts margins, adds section dividers.
        Confirms: "Professional formatting applied"
```

### Example 3: Add Table
```
User: "Insert a comparison table in my document"
Claude: Inserts table with appropriate columns and rows,
        formats with alternating colors.
        Confirms: "Comparison table inserted"
```

### Example 4: Export PDF
```
User: "Export my proposal as a PDF"
Claude: Opens document, navigates to File > Export > PDF,
        downloads file. Reports: "Proposal exported as PDF"
```

## Authentication Flow
1. Claude navigates to word.office.com via Playwright MCP
2. Authenticates with MICROSOFT_EMAIL if needed
3. Handles 2FA if prompted (notifies user via iMessage)
4. Maintains session for document operations

## Selectors Reference
```javascript
// New document
'[aria-label="New blank document"]'

// Document title
'[aria-label="Document name"]'

// Editing area
'[contenteditable="true"]' or '.WACEditing'

// Ribbon tabs
'[role="tablist"]'

// Home tab
'[aria-label="Home"]'

// Insert tab
'[aria-label="Insert"]'

// Bold button
'[aria-label="Bold"]'

// Font selector
'[aria-label="Font"]'

// Style gallery
'[aria-label="Styles"]'

// Save button
'[aria-label="Save"]'

// Share button
'[aria-label="Share"]'
```

## Error Handling
- **Login Failed**: Retry 3 times, notify user via iMessage
- **Session Expired**: Re-authenticate automatically
- **Document Not Found**: Search OneDrive, ask for clarification
- **Save Failed**: Enable AutoSave, retry, copy as backup
- **Format Apply Failed**: Retry, try alternative method
- **Export Failed**: Try alternative format, notify user

## Self-Improvement Instructions
When you learn a better way to accomplish a task with Word Online:
1. Document the improvement in your response
2. Suggest updating this skill file with the new approach
3. Include specific keyboard shortcuts or ribbon paths
4. Note differences from desktop Word

## Notes
- Word Online auto-saves to OneDrive
- Some features only available in desktop version
- Real-time collaboration shows other users' cursors
- Templates available from Start screen
- Track changes for revision management
- Comments for collaboration feedback
- Editor pane for writing suggestions
- Dictation available with microphone

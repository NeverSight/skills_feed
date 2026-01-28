---
name: google-docs
description: Enables Claude to create, edit, read, and collaborate on Google Docs documents via Playwright MCP
category: google
---

# Google Docs Skill

## Overview
Claude can work with Google Docs to create, edit, and manage documents. This includes writing content, formatting text, inserting images, collaborating with comments, and exporting documents in various formats.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/google-docs/install.sh | bash
```

Or manually:
```bash
cp -r skills/google-docs ~/.canifi/skills/
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
- Create new documents from scratch or templates
- Read and summarize existing documents
- Edit text content and apply formatting
- Insert images, tables, and charts
- Add and respond to comments
- Share documents and manage permissions
- Export documents as PDF, DOCX, or plain text
- Track and review document history
- Use voice typing transcription
- Apply heading styles and create table of contents
- Find and replace text across documents

## Usage Examples

### Example 1: Create a Document
```
User: "Create a meeting notes document for today's standup"
Claude: Creates new Google Doc titled "Standup Notes - [Date]",
        adds template with Attendees, Discussion Points, Action Items sections.
        Returns: "Created document: [link]"
```

### Example 2: Edit Existing Document
```
User: "Add a conclusion section to my project proposal doc"
Claude: Opens the specified document, scrolls to end, adds "Conclusion"
        heading with appropriate content based on document context.
```

### Example 3: Summarize Document
```
User: "Summarize the Q4 report document"
Claude: Opens document, reads all content, provides concise summary
        of key points, metrics, and conclusions.
```

### Example 4: Export Document
```
User: "Export my resume as a PDF"
Claude: Opens resume document, navigates to File > Download > PDF,
        confirms download. Reports: "Resume exported as PDF"
```

## Authentication Flow
1. Claude navigates to docs.google.com via Playwright MCP
2. Authenticates with GOOGLE_EMAIL if needed
3. Handles 2FA if prompted (notifies user via iMessage)
4. Maintains session for subsequent document operations

## Selectors Reference
```javascript
// New document button
'#docs-new-button' or '[aria-label="New"]'

// Document title
'.docs-title-input'

// Main editing area
'.kix-appview-editor'

// Document content
'.kix-paragraphrenderer'

// Menu bar items
'.menu-button'

// File menu
'#docs-file-menu'

// Insert menu
'#docs-insert-menu'

// Format menu
'#docs-format-menu'

// Share button
'.docs-titlebar-share-client-button'

// Comments panel
'.docos-anchoreddocoview'

// Find and replace
'Ctrl+H' keyboard shortcut
```

## Error Handling
- **Login Failed**: Retry 3 times, notify user via iMessage
- **Session Expired**: Re-authenticate automatically
- **Document Not Found**: Search Drive for similar names, ask user to clarify
- **Permission Denied**: Notify user they lack access, offer to request access
- **Save Failed**: Retry save, if persistent, copy content to clipboard as backup
- **Rate Limited**: Wait and retry with exponential backoff

## Self-Improvement Instructions
When you learn a better way to accomplish a task with Google Docs:
1. Document the improvement in your response
2. Suggest updating this skill file with the new approach
3. Include specific keyboard shortcuts or menu paths that work better
4. Note any UI changes affecting selectors

## Notes
- Google Docs auto-saves; explicit save is rarely needed
- Large documents may require scrolling to access all content
- Collaborative editing may show other users' cursors
- Some formatting options require the Format menu
- Voice typing requires microphone permissions
- Export formats: PDF, DOCX, ODT, RTF, TXT, HTML, EPUB

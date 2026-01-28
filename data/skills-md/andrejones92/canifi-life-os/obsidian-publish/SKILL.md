---
name: obsidian-publish
description: Enables Claude to publish and manage content on Obsidian Publish sites via Playwright MCP
category: productivity
---

# Obsidian Publish Skill

## Overview
Claude can manage your Obsidian Publish site to publish notes, manage site settings, and create a public knowledge base. Publish transforms your markdown notes into a beautiful website.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/obsidian-publish/install.sh | bash
```

Or manually:
```bash
cp -r skills/obsidian-publish ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set OBSIDIAN_PUBLISH_EMAIL "your-email@example.com"
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
- Publish notes to the web
- Unpublish content
- Manage site settings
- Update site navigation
- Configure custom domains
- Set up site appearance
- Manage page links
- Update published content
- View site analytics
- Configure search
- Set page aliases
- Manage access control

## Usage Examples

### Example 1: Publish Note
```
User: "Publish my 'Getting Started' note to Obsidian Publish"
Claude: Navigates to publish settings, selects note, publishes.
        Confirms: "Published: yoursite.publish.obsidian.md/getting-started"
```

### Example 2: Update Site
```
User: "Sync all changed notes to my publish site"
Claude: Checks for changes, publishes updated notes.
        Reports: "Published 5 updated notes, 2 new notes"
```

### Example 3: Manage Navigation
```
User: "Add 'Resources' to the site navigation"
Claude: Opens site settings, adds Resources to nav.
        Confirms: "Added Resources to site navigation"
```

### Example 4: Unpublish Content
```
User: "Remove the draft article from the published site"
Claude: Finds note, unpublishes it.
        Confirms: "Unpublished 'Draft Article'"
```

## Authentication Flow
1. Claude navigates to publish.obsidian.md via Playwright MCP
2. Enters OBSIDIAN_PUBLISH_EMAIL for authentication
3. Handles 2FA if required (notifies user via iMessage)
4. Maintains session for publish operations

## Selectors Reference
```javascript
// Site selector
'.site-selector'

// File tree
'.file-tree'

// Publish button
'.publish-button'

// Unpublish button
'.unpublish-button'

// Settings
'.site-settings'

// Navigation editor
'.nav-editor'

// Appearance settings
'.appearance-settings'

// Search config
'.search-settings'

// Custom domain
'.domain-settings'

// File checkbox
'.file-checkbox'
```

## Error Handling
- **Login Failed**: Retry 3 times, notify user via iMessage
- **Session Expired**: Re-authenticate automatically
- **Publish Failed**: Check file validity, retry
- **Site Not Found**: List available sites, ask user
- **Sync Failed**: Check for conflicts, retry
- **Domain Error**: Verify DNS settings

## Self-Improvement Instructions
When you learn a better way to accomplish a task with Obsidian Publish:
1. Document the improvement in your response
2. Suggest updating this skill file with the new approach
3. Include specific publishing workflows
4. Note site configuration best practices

## Notes
- Publish subscription required
- Selective publishing of notes
- Links between published notes work
- Custom CSS supported
- Password protection available
- Custom domain support
- Search functionality built-in
- Mobile-responsive design
- Google indexing supported

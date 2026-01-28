---
name: google-sites
description: Enables Claude to create and edit websites using Google Sites via Playwright MCP
category: google
---

# Google Sites Skill

## Overview
Claude can create and manage Google Sites to build simple websites, team portals, and project pages. This includes adding content, embedding media, and publishing sites.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/google-sites/install.sh | bash
```

Or manually:
```bash
cp -r skills/google-sites ~/.canifi/skills/
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
- Create new sites from scratch or templates
- Add and edit pages
- Insert text, images, and videos
- Embed Google Drive files
- Add navigation and menus
- Apply themes and customize design
- Publish and unpublish sites
- Share editing permissions
- Create internal links
- Embed forms and calendars
- Set custom domains
- Manage site structure

## Usage Examples

### Example 1: Create Site
```
User: "Create a site for our team project"
Claude: Creates new site titled "Team Project", adds home page
        with project overview section. Returns: "Site created: [preview link]"
```

### Example 2: Add Page
```
User: "Add a 'Resources' page to the team site"
Claude: Opens site, adds new page "Resources" to navigation.
        Confirms: "Added Resources page to site"
```

### Example 3: Embed Content
```
User: "Embed our project timeline spreadsheet on the home page"
Claude: Inserts Google Sheets embed with timeline.
        Confirms: "Timeline spreadsheet embedded on home page"
```

### Example 4: Publish Site
```
User: "Make the team site public"
Claude: Opens publishing settings, configures visibility.
        Reports: "Site published at: sites.google.com/view/team-project"
```

## Authentication Flow
1. Claude navigates to sites.google.com via Playwright MCP
2. Authenticates with GOOGLE_EMAIL if needed
3. Handles 2FA if prompted (notifies user via iMessage)
4. Maintains session for subsequent Sites operations

## Selectors Reference
```javascript
// Create site
'[aria-label="Create new site"]'

// Site title
'.docs-title-input'

// Insert menu
'[aria-label="Insert"]'

// Pages panel
'[aria-label="Pages"]'

// Add page
'[aria-label="Add page"]'

// Text box
'[aria-label="Text box"]'

// Image button
'[aria-label="Images"]'

// Embed button
'[aria-label="Embed"]'

// Drive embed
'[aria-label="Google Drive"]'

// Theme button
'[aria-label="Themes"]'

// Preview button
'[aria-label="Preview"]'

// Publish button
'[aria-label="Publish"]'

// Share button
'[aria-label="Share with others"]'
```

## Embeddable Content
```
Google Docs
Google Sheets
Google Slides
Google Forms
Google Calendar
Google Maps
YouTube videos
Google Drive files
External URLs (via iframe)
```

## Error Handling
- **Login Failed**: Retry 3 times, notify user via iMessage
- **Session Expired**: Re-authenticate automatically
- **Site Creation Failed**: Check storage quota, retry
- **Embed Failed**: Verify file permissions, try alternative embed
- **Publish Failed**: Check domain settings, verify permissions
- **Theme Apply Failed**: Retry, suggest alternative themes

## Self-Improvement Instructions
When you learn a better way to accomplish a task with Google Sites:
1. Document the improvement in your response
2. Suggest updating this skill file with the new approach
3. Include specific design tips for better sites
4. Note any new embed options or features

## Notes
- Sites auto-save all changes
- Custom domains require verification
- Sites are responsive by default
- Maximum pages: no hard limit, but navigation may be affected
- Files embedded from Drive inherit sharing settings
- Published sites indexed by Google Search
- Version history available
- Multiple editors can collaborate simultaneously
- Banner images recommended: 1600 x 400 pixels
- Sites integrate with Google Analytics

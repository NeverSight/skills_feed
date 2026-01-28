---
name: adobe-illustrator-web
description: Create vector graphics with Illustrator on the web - design logos, icons, and illustrations with AI-powered tools
category: design
---

# Adobe Illustrator Web Skill

## Overview
Enables Claude to use Adobe Illustrator's web version for vector graphic creation including AI-powered features, basic illustration tools, and vector editing capabilities.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/adobe-illustrator-web/install.sh | bash
```

Or manually:
```bash
cp -r skills/adobe-illustrator-web ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set ADOBE_EMAIL "your-email@example.com"
canifi-env set ADOBE_PASSWORD "your-password"
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
- Create and edit vector graphics
- Use AI-powered design tools
- Create simple logos and icons
- Export in vector formats (SVG, AI)
- Apply colors and gradients
- Sync with Creative Cloud

## Usage Examples

### Example 1: Create Simple Logo
```
User: "Create a simple geometric logo for my brand"
Claude: I'll create a logo design.
1. Opening Illustrator web via Playwright MCP
2. Creating new artboard
3. Using shape tools for geometry
4. Adding brand colors
5. Exporting as SVG
```

### Example 2: Edit Vector File
```
User: "Change the colors in my logo to match new brand guidelines"
Claude: I'll update your logo colors.
1. Opening the logo file
2. Selecting color elements
3. Applying new brand colors
4. Saving updated version
5. Exporting in required formats
```

### Example 3: Create Icons
```
User: "Make a set of simple navigation icons"
Claude: I'll create navigation icons.
1. Setting up icon artboards
2. Creating home, menu, search icons
3. Ensuring consistent style
4. Exporting as SVG set
```

## Authentication Flow
1. Navigate to illustrator.adobe.com via Playwright MCP
2. Sign in with Adobe ID
3. Enter email and password
4. Handle 2FA if enabled (via iMessage)
5. Wait for web app to load

## Error Handling
- **Login Failed**: Retry up to 3 times, notify via iMessage
- **Session Expired**: Re-authenticate with Adobe ID
- **Rate Limited**: Implement backoff strategy
- **2FA Required**: Send iMessage notification
- **Save Failed**: Retry or export locally
- **Complex File**: Suggest desktop version

## Self-Improvement Instructions
When Illustrator web updates:
1. Document new vector tools
2. Update AI feature capabilities
3. Track export format changes
4. Log new template options

## Notes
- Requires Creative Cloud subscription
- Web version has limited features
- Complex vectors may need desktop app
- AI tools may have usage limits
- Files sync with Creative Cloud

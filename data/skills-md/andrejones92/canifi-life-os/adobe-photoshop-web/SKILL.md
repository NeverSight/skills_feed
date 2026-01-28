---
name: adobe-photoshop-web
description: Edit images with Photoshop on the web - perform advanced photo editing, apply AI features, and manage creative projects
category: design
---

# Adobe Photoshop Web Skill

## Overview
Enables Claude to use Adobe Photoshop's web version for image editing tasks including AI-powered features like Generative Fill, background removal, and standard photo editing operations.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/adobe-photoshop-web/install.sh | bash
```

Or manually:
```bash
cp -r skills/adobe-photoshop-web ~/.canifi/skills/
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
- Open and edit images in browser
- Use Generative Fill AI features
- Remove and replace backgrounds
- Apply filters and adjustments
- Export in various formats
- Sync with Creative Cloud

## Usage Examples

### Example 1: Remove Background
```
User: "Remove the background from my product photo"
Claude: I'll remove the background.
1. Opening Photoshop web via Playwright MCP
2. Uploading your product image
3. Using AI background removal
4. Refining edges if needed
5. Exporting as transparent PNG
```

### Example 2: Generative Fill
```
User: "Extend my landscape photo to make it wider"
Claude: I'll extend your image.
1. Opening the landscape in Photoshop web
2. Expanding canvas to desired width
3. Using Generative Fill on new areas
4. Prompting for matching landscape
5. Blending results naturally
```

### Example 3: Apply Adjustments
```
User: "Enhance the colors and lighting in my portrait"
Claude: I'll enhance your portrait.
1. Opening the portrait image
2. Applying auto-enhance adjustments
3. Fine-tuning exposure and color
4. Saving enhanced version
```

## Authentication Flow
1. Navigate to photoshop.adobe.com via Playwright MCP
2. Sign in with Adobe ID
3. Enter email and password
4. Handle 2FA if enabled (via iMessage)
5. Wait for web app to fully load

## Error Handling
- **Login Failed**: Retry up to 3 times, notify via iMessage
- **Session Expired**: Re-authenticate with Adobe ID
- **Rate Limited**: Implement backoff strategy
- **2FA Required**: Send iMessage notification
- **Processing Failed**: Retry operation or simplify
- **File Too Large**: Suggest resize or compression

## Self-Improvement Instructions
When Photoshop web updates:
1. Document new AI features and tools
2. Update workflow for new capabilities
3. Track interface changes
4. Log performance improvements

## Notes
- Requires Creative Cloud subscription
- Web version has fewer features than desktop
- Large files may be slower to process
- Generative AI features use credits
- Syncs with Creative Cloud storage

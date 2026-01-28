---
name: adobe-express
description: Create quick graphics and content with Adobe Express - design social media posts, flyers, logos, and short videos
category: design
---

# Adobe Express Skill

## Overview
Enables Claude to use Adobe Express (formerly Adobe Spark) for quick content creation including social media graphics, web pages, short videos, and marketing materials with Adobe's design tools and stock assets.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/adobe-express/install.sh | bash
```

Or manually:
```bash
cp -r skills/adobe-express ~/.canifi/skills/
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
- Create graphics from templates
- Design social media posts and stories
- Create short videos and animations
- Remove image backgrounds
- Resize designs for multiple platforms
- Access Adobe Stock images and assets

## Usage Examples

### Example 1: Create Quick Social Graphic
```
User: "Make a quick LinkedIn post graphic about our new feature"
Claude: I'll create a LinkedIn graphic for you.
1. Opening Adobe Express via Playwright MCP
2. Selecting LinkedIn post template
3. Adding feature announcement text
4. Applying brand elements
5. Exporting in optimal format
```

### Example 2: Remove Background
```
User: "Remove the background from my product photo"
Claude: I'll remove the background from your image.
1. Accessing Adobe Express background remover
2. Uploading your product photo
3. Processing automatic background removal
4. Downloading the transparent PNG
```

### Example 3: Create Video Story
```
User: "Create a 15-second Instagram story video for our sale"
Claude: I'll create an animated story for the sale.
1. Opening video creation in Adobe Express
2. Selecting Instagram Story format
3. Adding sale announcement with animations
4. Exporting as MP4 for Instagram
```

## Authentication Flow
1. Navigate to express.adobe.com via Playwright MCP
2. Click sign in with Adobe ID
3. Enter email and password
4. Handle 2FA if enabled (via iMessage)
5. Maintain Adobe session cookies

## Error Handling
- **Login Failed**: Retry up to 3 times, notify via iMessage
- **Session Expired**: Re-authenticate with stored credentials
- **Rate Limited**: Implement backoff strategy
- **2FA Required**: Send iMessage notification for code
- **Asset Not Found**: Search Adobe Stock alternatives
- **Export Failed**: Retry or suggest alternative format

## Self-Improvement Instructions
When Adobe Express updates its interface:
1. Document new features and navigation paths
2. Update selector references as needed
3. Log UI changes to improvement tracking
4. Test common workflows after updates

## Notes
- Premium features require Adobe Creative Cloud subscription
- Adobe Stock assets may have licensing restrictions
- Video processing times vary by length and complexity
- Some features sync with other Adobe apps
- Mobile-created content accessible on web

---
name: unsplash
description: Access free high-quality stock photos on Unsplash - search, download, and manage photo collections for projects
category: design
---

# Unsplash Skill

## Overview
Enables Claude to use Unsplash for finding and downloading high-quality, royalty-free images for design projects, presentations, and content creation.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/unsplash/install.sh | bash
```

Or manually:
```bash
cp -r skills/unsplash ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set UNSPLASH_EMAIL "your-email@example.com"
canifi-env set UNSPLASH_PASSWORD "your-password"
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
- Search photos by keyword and filters
- Download images in various resolutions
- Create and manage photo collections
- View photographer profiles
- Track download history
- Access curated editorial collections

## Usage Examples

### Example 1: Find Project Images
```
User: "Find high-quality nature photos for my website header"
Claude: I'll search for nature header images.
1. Opening Unsplash via Playwright MCP
2. Searching "nature landscape header"
3. Filtering by orientation (landscape)
4. Previewing top results
5. Downloading selected images in high resolution
```

### Example 2: Create Collection
```
User: "Save team photos to a new collection called 'About Page'"
Claude: I'll organize photos into a new collection.
1. Creating new collection "About Page"
2. Searching for professional team photos
3. Adding selected images to collection
4. Confirming collection is ready for use
```

### Example 3: Download for Social Media
```
User: "Get some abstract gradient backgrounds for Instagram"
Claude: I'll find abstract backgrounds.
1. Searching "abstract gradient background"
2. Filtering by color palette
3. Downloading in Instagram-optimized resolution
4. Saving to your designated folder
```

## Authentication Flow
1. Navigate to unsplash.com via Playwright MCP
2. Click "Login" and enter credentials
3. Handle Google/SSO if configured
4. Maintain session for collections access
5. Track download attribution requirements

## Error Handling
- **Login Failed**: Retry up to 3 times, notify via iMessage
- **Session Expired**: Re-authenticate automatically
- **Rate Limited**: Implement exponential backoff
- **Download Failed**: Retry with different resolution
- **Search No Results**: Suggest alternative keywords
- **Collection Full**: Prompt to organize or upgrade

## Self-Improvement Instructions
When Unsplash updates features:
1. Document new search filters and options
2. Update download resolution options
3. Track collection management changes
4. Log API or rate limit adjustments

## Notes
- Unsplash images are free but require attribution
- High-resolution downloads may take longer
- Some photos have usage restrictions
- API limits apply even for logged-in users
- Collections help organize project assets

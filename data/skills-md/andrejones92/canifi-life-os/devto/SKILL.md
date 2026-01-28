---
name: devto
description: Enables Claude to manage DEV.to articles, comments, and developer community engagement
version: 1.0.0
author: Canifi
category: productivity
---

# DEV.to Skill

## Overview
Automates DEV.to operations including publishing articles, engaging with content, managing profile, and participating in the developer community through browser automation.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/devto/install.sh | bash
```

Or manually:
```bash
cp -r skills/devto ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set DEVTO_EMAIL "your-email@example.com"
canifi-env set DEVTO_PASSWORD "your-password"
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
- Write and publish articles
- React to posts (likes, unicorns, etc.)
- Comment on articles
- Follow users and tags
- Search content
- Manage drafts
- Access reading list
- View analytics

## Usage Examples

### Example 1: Publish Article
```
User: "Publish this article to DEV.to"
Claude: I'll publish that article.
- Navigate to dev.to/new
- Enter title and content
- Add tags and cover image
- Publish article
- Confirm live
```

### Example 2: React to Post
```
User: "Give that helpful article a heart and unicorn"
Claude: I'll add those reactions.
- Navigate to article
- Click heart reaction
- Click unicorn reaction
- Confirm reactions added
```

### Example 3: Follow Tag
```
User: "Follow the #javascript tag on DEV"
Claude: I'll follow that tag.
- Navigate to tag page
- Click Follow button
- Confirm following
- Tag added to feed
```

### Example 4: Save to Reading List
```
User: "Save this article to my DEV reading list"
Claude: I'll save that article.
- Navigate to article
- Click save/bookmark button
- Confirm added to reading list
```

## Authentication Flow
1. Navigate to dev.to via Playwright MCP
2. Click login and enter email
3. Enter password from canifi-env
4. Handle OAuth if using GitHub/Twitter
5. Verify feed access
6. Maintain session cookies

## Error Handling
- **Login Failed**: Try OAuth options, verify credentials
- **Session Expired**: Re-authenticate automatically
- **Article Failed**: Check markdown format
- **Rate Limited**: Wait before posting
- **Tag Not Found**: Check tag spelling
- **Draft Lost**: Check autosave status
- **Image Upload Failed**: Check format and size
- **Comment Failed**: Check community guidelines

## Self-Improvement Instructions
When encountering new DEV.to features:
1. Document new editor elements
2. Add support for new content features
3. Log successful publishing patterns
4. Update for platform changes

## Notes
- DEV.to uses Markdown for articles
- Cover images improve visibility
- Tags help discoverability
- Series group related articles
- Community guidelines are friendly
- Reading time calculated automatically
- Forem platform powers DEV

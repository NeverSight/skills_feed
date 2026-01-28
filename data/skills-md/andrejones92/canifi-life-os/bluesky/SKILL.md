---
name: bluesky
description: Enables Claude to manage Bluesky posts and engagement through browser automation
version: 1.0.0
author: Canifi
category: social
---

# Bluesky Skill

## Overview
Automates Bluesky Social operations including creating posts, reposting, managing follows, and engaging with the decentralized social network through browser automation.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/bluesky/install.sh | bash
```

Or manually:
```bash
cp -r skills/bluesky ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set BLUESKY_HANDLE "your-handle.bsky.social"
canifi-env set BLUESKY_PASSWORD "your-app-password"
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
- Create and publish posts
- Repost and quote posts
- Like content
- Follow/unfollow accounts
- Search users and content
- Manage custom feeds
- View notifications
- Handle threads

## Usage Examples

### Example 1: Create a Post
```
User: "Post on Bluesky about decentralized social media"
Claude: I'll create that Bluesky post.
- Navigate to bsky.app
- Click compose
- Write post about decentralization
- Add image if provided
- Publish post
```

### Example 2: Quote Post
```
User: "Quote that post with my perspective"
Claude: I'll create a quote post.
- Find original post
- Click quote option
- Add your commentary
- Publish quote post
```

### Example 3: Explore Custom Feeds
```
User: "Show me what's on the 'Science' custom feed"
Claude: I'll check that feed.
- Navigate to Feeds section
- Find Science feed
- Browse posts
- Summarize interesting content
```

### Example 4: Search Content
```
User: "Find posts about AI safety on Bluesky"
Claude: I'll search for that topic.
- Use search function
- Search "AI safety"
- Browse results
- Present relevant posts
```

## Authentication Flow
1. Navigate to bsky.app via Playwright MCP
2. Enter handle and app password from canifi-env
3. Verify home feed access
4. Maintain session cookies

## Error Handling
- **Login Failed**: Verify handle and app password
- **Session Expired**: Re-authenticate automatically
- **App Password Invalid**: Notify user to generate new one
- **Rate Limited**: Implement backoff
- **Post Failed**: Check character limit (300)
- **User Not Found**: Verify handle format
- **Feed Not Found**: Search available feeds
- **Image Upload Failed**: Check format and size

## Self-Improvement Instructions
When encountering new Bluesky features:
1. Document new UI elements
2. Add support for new post types
3. Log successful patterns
4. Update for AT Protocol changes

## Notes
- Uses AT Protocol (decentralized)
- App passwords recommended over main password
- Custom feeds are algorithmic views
- Character limit is 300
- Threading supported
- Image alt text encouraged
- No DMs currently
- Moderation via labelers

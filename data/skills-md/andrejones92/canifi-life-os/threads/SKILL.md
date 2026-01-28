---
name: threads
description: Enables Claude to manage Threads posts and engagement through browser automation
version: 1.0.0
author: Canifi
category: social
---

# Threads Skill

## Overview
Automates Threads (by Meta/Instagram) operations including creating posts, engaging with content, and managing profile through browser automation.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/threads/install.sh | bash
```

Or manually:
```bash
cp -r skills/threads ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set INSTAGRAM_USERNAME "your-instagram-username"
canifi-env set INSTAGRAM_PASSWORD "your-instagram-password"
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
- Create and publish threads
- Reply to posts
- Like and repost content
- Follow/unfollow accounts
- Search users and topics
- View notifications
- Quote posts
- Manage profile settings

## Usage Examples

### Example 1: Create a Post
```
User: "Post on Threads about the product update"
Claude: I'll create that Threads post.
- Navigate to threads.net
- Click create post
- Write product update content
- Publish thread
- Confirm posted
```

### Example 2: Engage with Content
```
User: "Like and reply to posts from tech accounts"
Claude: I'll engage with that content.
- Navigate to feed
- Find tech-related posts
- Like interesting content
- Add thoughtful replies
- Confirm engagement
```

### Example 3: Quote Post
```
User: "Quote that post with my take"
Claude: I'll create a quote post.
- Find original post
- Click quote option
- Add your commentary
- Post quote thread
- Confirm published
```

### Example 4: Search Topics
```
User: "Find posts about AI on Threads"
Claude: I'll search for AI content.
- Use search function
- Search "AI" or related terms
- Browse results
- Present relevant posts
```

## Authentication Flow
1. Navigate to threads.net via Playwright MCP
2. Click login and use Instagram credentials
3. Enter username and password from canifi-env
4. Handle 2FA if enabled (notify user via iMessage)
5. Verify feed access
6. Maintain session cookies

## Error Handling
- **Login Failed**: Clear cookies, verify Instagram credentials
- **Session Expired**: Re-authenticate via Instagram
- **2FA Required**: iMessage for verification code
- **Post Failed**: Check content guidelines
- **Rate Limited**: Implement backoff
- **Account Restricted**: Check Instagram account status
- **User Not Found**: Verify username
- **Feature Unavailable**: May need app for some features

## Self-Improvement Instructions
When encountering new Threads features:
1. Document new UI elements
2. Add support for new post types
3. Log successful posting patterns
4. Update for platform changes

## Notes
- Threads uses Instagram login
- Character limit is 500
- Images supported in posts
- Fediverse integration coming
- Some features app-only
- Linked with Instagram account
- Algorithm shows For You content

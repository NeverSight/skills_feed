---
name: instagram
description: Enables Claude to manage Instagram posts, stories, reels, and engagement through browser automation
version: 1.0.0
author: Canifi
category: social
---

# Instagram Skill

## Overview
Automates Instagram operations including posting content, managing stories, engaging with followers, and analyzing insights through the web interface.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/instagram/install.sh | bash
```

Or manually:
```bash
cp -r skills/instagram ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set INSTAGRAM_USERNAME "your-username"
canifi-env set INSTAGRAM_PASSWORD "your-password"
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
- Upload and manage stories
- Like and comment on posts
- Follow/unfollow accounts
- Search users and hashtags
- View and respond to DMs (see instagram-dms)
- Access insights and analytics
- Save posts to collections

## Usage Examples

### Example 1: Create a Post
```
User: "Post this photo to Instagram with a caption about the sunset"
Claude: I'll create that Instagram post.
- Navigate to instagram.com
- Click create post
- Upload photo
- Write sunset caption with hashtags
- Publish post
- Confirm posted successfully
```

### Example 2: Engage with Content
```
User: "Like the last 5 posts from @naturephotography"
Claude: I'll engage with those posts.
- Navigate to @naturephotography profile
- View recent posts
- Like last 5 posts
- Confirm engagement complete
```

### Example 3: Check Insights
```
User: "Show me my Instagram insights for this week"
Claude: I'll pull your insights.
- Navigate to Insights section
- Gather this week's metrics
- Compile reach, engagement, followers
- Present analytics summary
```

### Example 4: Search Hashtag
```
User: "Find top posts for #travelgram"
Claude: I'll search that hashtag.
- Navigate to hashtag search
- Search #travelgram
- Display top and recent posts
- Summarize engagement levels
```

## Authentication Flow
1. Navigate to instagram.com via Playwright MCP
2. Enter username and password from canifi-env
3. Handle suspicious login verification (notify user)
4. Complete 2FA if enabled (notify user via iMessage)
5. Handle "Save Login Info" prompt
6. Verify feed access
7. Maintain session cookies

## Error Handling
- **Login Failed**: Clear cookies, verify credentials
- **Session Expired**: Re-authenticate automatically
- **2FA Required**: iMessage for verification code
- **Suspicious Login**: Notify user to verify via app
- **Rate Limited**: Wait and implement backoff
- **Content Blocked**: Check community guidelines
- **Account Restricted**: Notify user of temporary block
- **Upload Failed**: Check file format and size

## Self-Improvement Instructions
When encountering new Instagram features:
1. Document new UI elements and flows
2. Add support for new content types
3. Log successful posting patterns
4. Update for reels and stories changes

## Notes
- Instagram frequently updates UI
- Creator/Business accounts have more features
- Insights require Professional account
- Some features only available in mobile app
- Posting times affect engagement
- Hashtag limits: 30 per post
- Story content expires in 24 hours

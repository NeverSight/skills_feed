---
name: tumblr
description: Enables Claude to manage Tumblr posts, reblogs, and blog operations
version: 1.0.0
author: Canifi
category: social
---

# Tumblr Skill

## Overview
Automates Tumblr operations including creating posts, reblogging, managing blogs, and engaging with content through browser automation.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/tumblr/install.sh | bash
```

Or manually:
```bash
cp -r skills/tumblr ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set TUMBLR_EMAIL "your-email@example.com"
canifi-env set TUMBLR_PASSWORD "your-password"
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
- Create various post types (text, photo, quote, link, chat, audio, video)
- Reblog posts with commentary
- Like posts
- Follow and unfollow blogs
- Search tags and content
- Manage blog settings
- Queue and schedule posts
- Edit blog theme

## Usage Examples

### Example 1: Create a Post
```
User: "Post this photo to Tumblr with aesthetic tags"
Claude: I'll create that Tumblr post.
- Navigate to tumblr.com
- Click create post
- Select photo post
- Upload image
- Add caption and tags
- Publish post
```

### Example 2: Reblog with Commentary
```
User: "Reblog that post with my thoughts added"
Claude: I'll reblog with your commentary.
- Find original post
- Click reblog
- Add commentary
- Include tags
- Post reblog
```

### Example 3: Search Tags
```
User: "Find posts tagged #photography"
Claude: I'll search that tag.
- Navigate to tag search
- Search #photography
- Browse recent and top posts
- Present interesting finds
```

### Example 4: Queue Posts
```
User: "Add this to my Tumblr queue"
Claude: I'll queue that post.
- Create new post
- Instead of Publish, select Queue
- Confirm added to queue
- Verify in queue list
```

## Authentication Flow
1. Navigate to tumblr.com/login via Playwright MCP
2. Enter email and password from canifi-env
3. Handle 2FA if enabled (notify user via iMessage)
4. Verify dashboard access
5. Maintain session cookies

## Error Handling
- **Login Failed**: Clear cookies, verify credentials
- **Session Expired**: Re-authenticate automatically
- **2FA Required**: iMessage for verification code
- **Post Failed**: Check content guidelines
- **Media Upload Error**: Verify file format and size
- **Rate Limited**: Wait before continuing
- **Blog Not Found**: Verify blog name
- **Tag Blocked**: Some tags restricted

## Self-Improvement Instructions
When encountering new Tumblr features:
1. Document new post editor elements
2. Add support for new post types
3. Log successful posting patterns
4. Update for Tumblr changes

## Notes
- Multiple blogs per account possible
- Tumblr has unique reblog culture
- Tags are important for discovery
- Queue maintains posting schedule
- Ask feature for anonymous questions
- Community labels for mature content
- Blaze for promoted posts

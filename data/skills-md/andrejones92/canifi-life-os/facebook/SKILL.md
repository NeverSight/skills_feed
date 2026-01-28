---
name: facebook
description: Enables Claude to manage Facebook posts, pages, groups, and engagement through browser automation
version: 1.0.0
author: Canifi
category: social
---

# Facebook Skill

## Overview
Automates Facebook operations including posting content, managing pages, participating in groups, and engaging with the social network through browser automation.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/facebook/install.sh | bash
```

Or manually:
```bash
cp -r skills/facebook ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set FACEBOOK_EMAIL "your-email@example.com"
canifi-env set FACEBOOK_PASSWORD "your-password"
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
- Create posts on profile and pages
- Manage Facebook Pages
- Participate in groups
- Like, comment, and share content
- Search people and content
- Access notifications
- View and manage events
- Check insights for pages

## Usage Examples

### Example 1: Create a Post
```
User: "Post an update to Facebook about the product launch"
Claude: I'll create that Facebook post.
- Navigate to facebook.com
- Click create post
- Write product launch announcement
- Add any media if provided
- Publish post
- Confirm posted
```

### Example 2: Post to Page
```
User: "Post to my business page about the sale"
Claude: I'll post to your page.
- Navigate to Facebook Page
- Click create post
- Write sale announcement
- Schedule or publish immediately
- Confirm posted
```

### Example 3: Engage in Group
```
User: "Post in the Marketing Professionals group"
Claude: I'll post in that group.
- Navigate to Marketing Professionals group
- Create new post
- Write content
- Submit for approval if required
- Confirm posted or pending
```

### Example 4: Check Page Insights
```
User: "Show me my Facebook Page insights"
Claude: I'll pull those insights.
- Navigate to Page Insights
- Gather reach and engagement data
- Compile follower growth
- Present analytics summary
```

## Authentication Flow
1. Navigate to facebook.com via Playwright MCP
2. Enter email and password from canifi-env
3. Handle 2FA if enabled (notify user via iMessage)
4. Handle device recognition prompt
5. Verify news feed access
6. Maintain session cookies

## Error Handling
- **Login Failed**: Clear cookies, verify credentials
- **Session Expired**: Re-authenticate automatically
- **2FA Required**: iMessage for verification code
- **Account Checkpoint**: Handle security verification
- **Rate Limited**: Implement backoff
- **Content Blocked**: Check community standards
- **Page Access Denied**: Verify page admin role
- **Group Approval**: Notify of pending status

## Self-Improvement Instructions
When encountering new Facebook features:
1. Document new UI elements
2. Add support for new post types
3. Log successful page patterns
4. Update for Meta platform changes

## Notes
- Facebook frequently updates interface
- Pages have different features than profiles
- Group posts may need approval
- Meta Business Suite for page management
- Some features require admin access
- API changes affect automation
- Privacy settings affect visibility

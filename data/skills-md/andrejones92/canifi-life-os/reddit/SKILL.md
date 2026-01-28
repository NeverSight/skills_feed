---
name: reddit
description: Enables Claude to manage Reddit posts, comments, and community engagement
version: 1.0.0
author: Canifi
category: social
---

# Reddit Skill

## Overview
Automates Reddit operations including posting, commenting, voting, and community participation through browser automation.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/reddit/install.sh | bash
```

Or manually:
```bash
cp -r skills/reddit ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set REDDIT_USERNAME "your-username"
canifi-env set REDDIT_PASSWORD "your-password"
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
- Create posts (text, link, image)
- Comment on posts
- Upvote and downvote content
- Join and leave subreddits
- Search reddit content
- Manage saved posts
- View user profile
- Sort and filter content

## Usage Examples

### Example 1: Create a Post
```
User: "Post to r/technology about the new AI tool"
Claude: I'll create that Reddit post.
- Navigate to reddit.com
- Go to r/technology
- Click Create Post
- Select post type
- Write title and content
- Submit post
- Confirm posted
```

### Example 2: Comment on Post
```
User: "Reply to the top post on r/programming"
Claude: I'll add a comment.
- Navigate to r/programming
- Find top post
- Click comment
- Write thoughtful reply
- Submit comment
```

### Example 3: Search Reddit
```
User: "Find posts about Python tutorials"
Claude: I'll search for that content.
- Use Reddit search
- Search "Python tutorials"
- Filter by relevance or date
- Present top results
```

### Example 4: Join Subreddit
```
User: "Join r/MachineLearning"
Claude: I'll join that subreddit.
- Navigate to r/MachineLearning
- Click Join button
- Confirm subscription
- Verify in subscriptions
```

## Authentication Flow
1. Navigate to reddit.com/login via Playwright MCP
2. Enter username and password from canifi-env
3. Handle 2FA if enabled (notify user via iMessage)
4. Verify home feed access
5. Handle any CAPTCHA (notify user)
6. Maintain session cookies

## Error Handling
- **Login Failed**: Clear cookies, verify credentials
- **Session Expired**: Re-authenticate automatically
- **2FA Required**: iMessage for verification code
- **CAPTCHA Required**: Notify user to complete
- **Rate Limited**: Wait before posting again
- **Subreddit Restricted**: Check posting rules
- **Shadowbanned**: Notify user of potential issue
- **Post Removed**: Check subreddit rules

## Self-Improvement Instructions
When encountering new Reddit features:
1. Document new UI elements
2. Add support for new post types
3. Log successful posting patterns
4. Update for Reddit changes

## Notes
- Reddit has old and new design
- Subreddits have different rules
- Karma affects posting ability
- Some subreddits require flair
- Automod may filter posts
- Rate limits vary by karma
- Premium features available
